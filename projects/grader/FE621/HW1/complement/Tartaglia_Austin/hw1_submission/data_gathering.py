# Data gathering module (Q1, Q2, Q4)
# Downloads equity prices, VIX, and option chains from Yahoo Finance DIRECTLY using requests
# (Bypassing yfinance library due to curl_cffi/cookie issues)
# Records spot prices, computes time-to-maturity, saves everything to CSV

import os
import datetime
import time
import numpy as np
import pandas as pd
import requests
import json
import random

import config

# -- Yahoo Finance Direct Scraper Implementation --

class YahooScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.crumb = None
        
        # Initialize cookie/crumb on start
        self._get_yahoo_cookie_and_crumb()

    def _get_yahoo_cookie_and_crumb(self):
        """ Fetch cookie from fc.yahoo.com and crumb from query1 """
        print("  Initializing Yahoo Finance session (fetching cookie/crumb)...")
        try:
            # 1. Get Cookie
            # 'https://fc.yahoo.com' often redirects to 'https://www.yahoo.com/?...' setting cookies
            r = self.session.get("https://fc.yahoo.com", timeout=10, allow_redirects=True)
            # We don't need to read response, just let session handle cookies
            
            # 2. Get Crumb
            # Try query1 first
            r2 = self.session.get("https://query1.finance.yahoo.com/v1/test/getcrumb", timeout=10)
            if r2.status_code == 200:
                self.crumb = r2.text
                print(f"    Got crumb: {self.crumb[:5]}...")
                return

            # Try query2 fallback
            r3 = self.session.get("https://query2.finance.yahoo.com/v1/test/getcrumb", timeout=10)
            if r3.status_code == 200:
                self.crumb = r3.text
                print(f"    Got crumb: {self.crumb[:5]}...")
                return
                
            print("    Warning: Failed to fetch crumb. API calls might fail if authentication is enforced.")
            
        except Exception as eobj:
            print(f"    Warning: Failed to initialize cookie/crumb: {eobj}")

    def _get_json(self, url, params=None):
        """ Fetch JSON with retry and error handling """
        if params is None:
            params = {}
        if self.crumb:
            params['crumb'] = self.crumb

        for attempt in range(3):
            try:
                r = self.session.get(url, params=params, timeout=10)
                r.raise_for_status()
                return r.json()
            except requests.exceptions.RequestException as e:
                # If 401/403, maybe try refreshing crumb?
                if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code in (401, 403):
                     print(f"      Attempt {attempt+1} failed (Auth/Forbidden). Refreshing crumb...")
                     self._get_yahoo_cookie_and_crumb()
                     if self.crumb:
                         params['crumb'] = self.crumb
                
                # Backoff
                time.sleep(1 + attempt) 
                
        print(f"    Failed to fetch {url} after 3 attempts.")
        return None

    def get_history(self, ticker, period="5d"):
        """ 
        Fetch historical data from query2.finance.yahoo.com/v8/finance/chart
        period: "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"
        """
        url = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}"
        params = {
            "range": period,
            "interval": "1d",
            "includePrePost": "false",
            "events": "div,splits"
        }
        
        data = self._get_json(url, params)
        if not data or "chart" not in data or "result" not in data["chart"] or not data["chart"]["result"]:
            print(f"    No chart data found for {ticker}")
            return pd.DataFrame()

        result = data["chart"]["result"][0]
        timestamp = result.get("timestamp", [])
        
        quotes = result.get("indicators", {}).get("quote", [{}])[0]
        adjclose = result.get("indicators", {}).get("adjclose", [{}])[0].get("adjclose", [])
        
        opens = quotes.get("open", [])
        highs = quotes.get("high", [])
        lows = quotes.get("low", [])
        closes = quotes.get("close", [])
        volumes = quotes.get("volume", [])

        # Construct DataFrame
        df_dict = {
            "Date": pd.to_datetime(timestamp, unit="s").tz_localize("UTC").tz_convert("America/New_York").tz_localize(None), # Convert to consistent timezone if needed, here mimicking yfinance's naive/local behavior
            "Open": opens,
            "High": highs,
            "Low": lows,
            "Close": closes,
            "Volume": volumes,
            "Adj Close": adjclose if adjclose else closes # Fallback if adjclose missing
        }
        
        # Handle differing lengths (rare but possible with nulls)
        max_len = len(timestamp)
        for k in df_dict:
            if len(df_dict[k]) < max_len:
                 df_dict[k] = df_dict[k] + [None]*(max_len - len(df_dict[k]))
            elif len(df_dict[k]) > max_len:
                 df_dict[k] = df_dict[k][:max_len]

        df = pd.DataFrame(df_dict)
        if not df.empty:
            df.set_index("Date", inplace=True)
        return df

    def get_option_expiries(self, ticker):
        """ Fetch available expiry dates (timestamps) """
        url = f"https://query2.finance.yahoo.com/v7/finance/options/{ticker}"
        data = self._get_json(url)
        if not data or "optionChain" not in data or "result" not in data["optionChain"] or not data["optionChain"]["result"]:
             return []
        
        return data["optionChain"]["result"][0].get("expirationDates", [])

    def get_option_chain(self, ticker, date_timestamp):
        """ Fetch option chain for a specific expiration timestamp """
        url = f"https://query2.finance.yahoo.com/v7/finance/options/{ticker}"
        params = {"date": date_timestamp}
        data = self._get_json(url, params)
        
        if not data or "optionChain" not in data or "result" not in data["optionChain"] or not data["optionChain"]["result"]:
             return [], []
        
        chain = data["optionChain"]["result"][0].get("options", [{}])[0]
        calls_data = chain.get("calls", [])
        puts_data = chain.get("puts", [])
        
        # Convert to DataFrame-friendly list of dicts
        calls = []
        for c in calls_data:
            calls.append(self._parse_option(c, "call"))
            
        puts = []
        for p in puts_data:
            puts.append(self._parse_option(p, "put"))
            
        return calls, puts

    def _parse_option(self, raw, type_):
        return {
            "contractSymbol": raw.get("contractSymbol"),
            "strike": raw.get("strike"),
            "lastPrice": raw.get("lastPrice"),
            "bid": raw.get("bid"),
            "ask": raw.get("ask"),
            "change": raw.get("change"),
            "percentChange": raw.get("percentChange"),
            "volume": raw.get("volume"),
            "openInterest": raw.get("openInterest"),
            "impliedVolatility": raw.get("impliedVolatility"),
            "inTheMoney": raw.get("inTheMoney"),
            "contractSize": raw.get("contractSize"),
            "currency": raw.get("currency"),
            "type": type_
        }

# Global instance
scraper = YahooScraper()

# -- Logic adapted to match old data_gathering.py interface --

def _select_monthly_expiries(ticker_symbol, n=3):
    # pick the next n monthly expiry dates
    timestamps = scraper.get_option_expiries(ticker_symbol)
    if not timestamps:
        raise RuntimeError(f"No option expiry dates found for {ticker_symbol}")

    stored_dates = []
    
    # Identify 3rd Fridays
    import calendar
    today = datetime.date.today()
    valid_dates = []
    ts_map = {}
    
    for ts in timestamps:
        dt = datetime.date.fromtimestamp(ts)
        if dt <= today:
            continue
            
        # Check if it is a Friday
        if dt.weekday() == 4: # Friday
            # Check if it is the 3rd Friday of the month
            c = calendar.monthcalendar(dt.year, dt.month)
            fridays = [week[calendar.FRIDAY] for week in c if week[calendar.FRIDAY] != 0]
            
            # 3rd Friday is index 2?
            if len(fridays) >= 3 and dt.day == fridays[2]:
                valid_dates.append(ts)
                ts_map[ts] = dt.strftime("%Y-%m-%d")
    
    valid_dates.sort()
    
    # Fallback
    if len(valid_dates) < n:
        print(f"Warning: Could not find {n} strict monthly (3rd Friday) expiries. Falling back to next available expiries including weeklies.")
        valid_dates = [ts for ts in sorted(timestamps) if datetime.date.fromtimestamp(ts) > today]

    # Return top n
    chosen_ts = valid_dates[:n]
    return [datetime.date.fromtimestamp(ts).strftime("%Y-%m-%d") for ts in chosen_ts]


def download_equity(tickers, period="5d"):
    result = {}
    for t in tickers:
        print(f"  Downloading equity history for {t} ...")
        df = scraper.get_history(t, period=period)
        if df.empty:
            print(f"    Warning: No data for {t}")
        result[t] = df
    return result


def download_vix():
    print("  Downloading VIX data ...")
    vix_df = scraper.get_history("^VIX", period="5d")
    if vix_df.empty:
        # Retry with just VIX or another symbol if needed, but ^VIX is standard
        # Sometimes yahoo uses VIX instead of ^VIX? No, ^VIX is correct.
        print("    Warning: Could not download VIX data")
        
    # Get most recent Close
    if not vix_df.empty:
        current_vix = vix_df["Close"].iloc[-1]
    else:
        current_vix = 20.0 # Fallback sane default
        
    return current_vix, vix_df


def download_option_chains(ticker_symbol, expiries, spot_price, ref_date=None):
    print(f"  Fetching expiry map for {ticker_symbol}...")
    all_ts = scraper.get_option_expiries(ticker_symbol)
    
    # Create mapping: "YYYY-MM-DD" -> timestamp
    date_to_ts = {}
    for ts in all_ts:
        d_str = datetime.date.fromtimestamp(ts).strftime("%Y-%m-%d")
        date_to_ts[d_str] = ts
        
    chains = {}
    
    for exp_str in expiries:
        print(f"  Downloading {ticker_symbol} options for {exp_str} ...")
        if exp_str not in date_to_ts:
            print(f"    Warning: Expiry {exp_str} not found in current chain list. Skipping.")
            continue
            
        ts = date_to_ts[exp_str]
        calls_list, puts_list = scraper.get_option_chain(ticker_symbol, ts)
        
        calls_df = pd.DataFrame(calls_list)
        puts_df = pd.DataFrame(puts_list)
        
        chains[exp_str] = (calls_df, puts_df)
        
    return chains


def gather_all():
    print("Starting data gathering (Direct Yahoo Scraping)...")
    
    # 1. Download Equity History (Spot Prices)
    equity_data = download_equity(config.TICKERS_EQUITY)
    
    spot_prices = {}
    for t, df in equity_data.items():
        if not df.empty:
            spot_prices[t] = df["Close"].iloc[-1]
            print(f"  {t} Spot Price: {spot_prices[t]:.2f}")
    
    # 2. Download VIX
    current_vix, vix_df = download_vix()
    print(f"  Current VIX: {current_vix:.2f}")

    # 3. Select Expiries & 4. Chains
    # import config (removed redundant import)
    tickers = config.TICKERS_EQUITY 
    chains_data = {}
    
    for t in tickers:
        print(f"  Selecting expiries for {t} ...")
        try:
            exps = _select_monthly_expiries(t, n=3)
            print(f"    Selected: {exps}")
            
            chains = download_option_chains(t, exps, spot_prices.get(t), ref_date=None)
            chains_data[t] = chains
            
        except Exception as e:
            print(f"    Error processing {t}: {e}")

    # 5. Process and Save to CSV
    print("  Processing and saving data...")
    if not os.path.exists(config.OUTPUT_DIR):
        os.makedirs(config.OUTPUT_DIR)
        
    # Save Equity History
    for t, df in equity_data.items():
        path = os.path.join(config.OUTPUT_DIR, f"history_{t}.csv")
        df.to_csv(path)
        print(f"    Saved {path}")

    # Save VIX
    if not vix_df.empty:
        vix_df.to_csv(os.path.join(config.OUTPUT_DIR, "history_VIX.csv"))
        print(f"    Saved VIX history")

    # Save Options
    today = datetime.date.today()
    
    for t, chain_dict in chains_data.items():
        all_opts = []
        spot = spot_prices.get(t, 0.0)
        
        for exp_date, (calls, puts) in chain_dict.items():
            exp_dt = datetime.datetime.strptime(exp_date, "%Y-%m-%d").date()
            ttm = (exp_dt - today).days / 365.0
            
            def process_df(df, type_):
                if df.empty: return df
                df["Type"] = type_
                df["Expiry"] = exp_date 
                df["T"] = ttm
                df["Underlying"] = t
                df["Underlying_Price"] = spot
                return df

            if not calls.empty:
                all_opts.append(process_df(calls, "Call"))
            if not puts.empty:
                all_opts.append(process_df(puts, "Put"))
                
        if all_opts:
            full_chain_df = pd.concat(all_opts, ignore_index=True)
            col_order = ["contractSymbol", "Type", "Expiry", "T", "strike", "lastPrice", "bid", "ask", "impliedVolatility", "volume", "openInterest", "Underlying", "Underlying_Price"]
            existing = [c for c in col_order if c in full_chain_df.columns]
            full_chain_df = full_chain_df[existing]
            
            out_path = os.path.join(config.OUTPUT_DIR, f"options_{t}.csv")
            full_chain_df.to_csv(out_path, index=False)
            print(f"    Saved {out_path} ({len(full_chain_df)} rows)")
        else:
            print(f"    Warning: No option data gathered for {t}")

    print("Data gathering complete.")
    
    # Return structure matching what main.py and implied_vol.py expect
    return {
        "all_chains": chains_data,  # Contains {ticker: {expiry: (calls, puts)}}
        "spots": spot_prices,
        "risk_free_rate": config.RISK_FREE_RATE,
        "equity": equity_data,
        "vix": vix_df,
        "chains": chains_data, # Redundant alias if needed legacy
        "current_vix": current_vix
    }

if __name__ == "__main__":
    gather_all()
