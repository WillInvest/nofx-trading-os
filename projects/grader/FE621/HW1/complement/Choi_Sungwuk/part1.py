import yfinance as yf
import pandas as pd
from datetime import datetime
from fredapi import Fred
import pytz

SYMBOLS = ["TSLA", "SPY", "^VIX"]
OUTPUT_PREFIX = "DATA2"
TIMEZONE = pytz.timezone("US/Eastern")

# Verifying time of data import.
now = datetime.now(TIMEZONE)
print("Download Time (ET):", now)

# Using FRED to import interest rate data from H15
FRED_API_KEY = "0fa4f50d7dcb9b1075c13c9e3a24c732 "
fred = Fred(api_key=FRED_API_KEY)
rate_series = fred.get_series_latest_release("DFF")
interest_rate = rate_series.iloc[-1] / 100
print("Interest Rate (decimal):", interest_rate)

# Equity and option data generating functions.
def download_equity(symbol):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1d", interval="1m")
    current_price = hist.iloc[-1]["Close"]
    return current_price, hist

def get_monthly_expirations(ticker):
     expirations = ticker.options
     monthly = []

     for exp in expirations:
         date_obj = datetime.strptime(exp, "%Y-%m-%d")
         if date_obj.weekday() == 4 and 15 <= date_obj.day <= 21:
             monthly.append(exp)
     return monthly[:3]

def download_option_chain(symbol):
    ticker = yf.Ticker(symbol)
    expirations = get_monthly_expirations(ticker)
    all_options = []

    for exp in expirations:
        chain = ticker.option_chain(exp)

        calls = chain.calls.copy()
        puts = chain.puts.copy()
        calls["type"] = "call"
        puts["type"] = "put"
        calls["expiration"] = exp
        puts["expiration"] = exp

        all_options.append(calls)
        all_options.append(puts)

    df = pd.concat(all_options, ignore_index=True)

    # cleaning data
    df = df.drop_duplicates()
    df = df[(df["volume"] > 0)]
    df = df[(df["bid"] > 0) & (df["ask"] > 0)]
    df = df.reset_index(drop=True)

    return df

# generating prices for given symbols above.
equity_prices = {}

for sym in SYMBOLS:
    price, hist = download_equity(sym)
    equity_prices[sym] = price
    hist.to_csv(f"{sym}_{OUTPUT_PREFIX}_equity.csv")
    print(f"{sym} price:", price)

# generating option chains for next 3 expiry
for sym in ["TSLA", "SPY"]:
    options_df = download_option_chain(sym)
    options_df.to_csv(f"{sym}_{OUTPUT_PREFIX}_options.csv", index=False)
    print(f"{sym} options saved.")

# Saving data in csv file format
meta = pd.DataFrame({
    "Download_Time_ET": [now],
    "Interest_Rate": [interest_rate],
    "TSLA_price": [equity_prices["TSLA"]],
    "SPY_price": [equity_prices["SPY"]],
    "VIX_price": [equity_prices["^VIX"]]
})

meta.to_csv(f"metadata_{OUTPUT_PREFIX}.csv", index=False)
