import os
from datetime import datetime, date

import pandas as pd
import yfinance as yf

##### Fill these out when downloading

# DATA2 on the second day
DATA_TAG = "DATA2"
# https://www.federalreserve.gov/releases/h15/
RISK_FREE_RATE_DECIMAL: float = 0.0364  # federal funds rate from site

#####

OUT_DIR = "fe621_hw1_part1_output"

EQUITY_TICKERS = ["TSLA", "SPY", "^VIX"]
OPTION_TICKERS = ["TSLA", "SPY"]


def time_to_strings(time: datetime) -> tuple[str, str]:
    iso = time.isoformat(timespec="seconds")
    iso_filename_safe = time.strftime("%Y%m%d_%H%M%S")
    return iso, iso_filename_safe


def get_asset_price(ticker: yf.Ticker) -> float:
    # Get the asset price at the time of this download
    # Use getattr as otherwise an exception is thrown if column doesn't exist
    fast_info = getattr(ticker, "fast_info", None)
    if fast_info:
        last_price = fast_info.get("last_price", None)
        if last_price is not None:
            return float(last_price)

    # Use these as a fallback
    info = ticker.info
    for k in ["regularMarketPrice", "previousClose"]:
        if k in info and info[k] is not None:
            return float(info[k])

    # No current asset price :(
    raise RuntimeError(f"Could not determine spot price for {ticker.ticker}")


def is_third_friday(d: date) -> bool:
    # weekday 4 is a Friday
    return d.weekday() == 4 and 14 < d.day <= 21


def next_three_monthly_expirations(ticker: yf.Ticker) -> list[str]:
    # Take the 3 next third Friday expirations
    today = date.today()
    expirations = []
    for expiration in ticker.options:
        expiration_date = date.fromisoformat(expiration)
        if expiration_date >= today and is_third_friday(expiration_date):
            expirations.append(expiration)

    expirations.sort()
    if len(expirations) < 3:
        print(
            f"WARNING: {ticker.ticker} has only {len(expirations)} monthly expirations"
        )

    return expirations[:3]


def dedup_and_datetime(df: pd.DataFrame) -> pd.DataFrame:
    # don't modify the passed in df
    df = df.copy()

    df = df.drop_duplicates()
    if "lastTradeDate" in df.columns:
        df["lastTradeDate"] = pd.to_datetime(df["lastTradeDate"], errors="coerce")

    return df


def download_part1_dataset(
    data_tag: str, out_dir: str, risk_free_rate_decimal: float
) -> tuple[pd.DataFrame, pd.DataFrame]:
    os.makedirs(out_dir, exist_ok=True)
    time_iso, time_fs_name = time_to_strings(datetime.now())

    # ----- Spot snapshot -----
    spot_rows = []
    for sym in EQUITY_TICKERS:
        t = yf.Ticker(sym)
        spot = get_asset_price(t)
        spot_rows.append(
            {
                "data_tag": data_tag,
                "download_time_local": time_iso,
                "symbol": sym,
                "spot_price": spot,
                "risk_free_rate_decimal": risk_free_rate_decimal,
            }
        )
    spot_snapshot = pd.DataFrame(spot_rows)

    # ----- Options -----
    all_option_rows = []

    for sym in OPTION_TICKERS:
        t = yf.Ticker(sym)
        underlying_spot = float(
            spot_snapshot.loc[spot_snapshot["symbol"] == sym, "spot_price"].iloc[0]
        )

        expirations = next_three_monthly_expirations(t)

        for exp in expirations:
            chain = t.option_chain(exp)

            calls = dedup_and_datetime(chain.calls)
            puts = dedup_and_datetime(chain.puts)

            calls["option_type"] = "call"
            puts["option_type"] = "put"

            for df in (calls, puts):
                df["data_tag"] = data_tag
                df["download_time_local"] = time_iso
                df["underlying_symbol"] = sym
                df["underlying_spot_at_download"] = underlying_spot
                df["expiration"] = exp
                df["risk_free_rate_decimal"] = risk_free_rate_decimal

            all_option_rows.append(calls)
            all_option_rows.append(puts)

    options_long = (
        pd.concat(all_option_rows, ignore_index=True)
        if all_option_rows
        else pd.DataFrame()
    )

    # Final cleanup: make column order a bit nicer (optional)
    preferred_front = [
        "data_tag",
        "download_time_local",
        "underlying_symbol",
        "underlying_spot_at_download",
        "expiration",
        "option_type",
        "contractSymbol",
        "strike",
        "bid",
        "ask",
        "lastPrice",
        "volume",
        "openInterest",
        "impliedVolatility",
        "inTheMoney",
        "lastTradeDate",
        "risk_free_rate_decimal",
    ]
    cols = [c for c in preferred_front if c in options_long.columns] + [
        c for c in options_long.columns if c not in preferred_front
    ]
    options_long = options_long[cols].drop_duplicates()

    spot_path = os.path.join(out_dir, f"{data_tag}_{time_fs_name}_spot.csv")
    opt_path = os.path.join(out_dir, f"{data_tag}_{time_fs_name}_options.csv")

    spot_snapshot.to_csv(spot_path, index=False)
    options_long.to_csv(opt_path, index=False)

    print(f"\nSaved spot snapshot to: {spot_path}")
    print(f"Saved option chains to: {opt_path}")

    return spot_snapshot, options_long


if __name__ == "__main__":
    spot_snapshot, options_long = download_part1_dataset(
        data_tag=DATA_TAG,
        out_dir=OUT_DIR,
        risk_free_rate_decimal=RISK_FREE_RATE_DECIMAL,
    )

    print(f"Spot snapshot:\n{spot_snapshot}")
    print(f"\nOptions rows: {len(options_long)}")
    if len(options_long) > 0:
        print(
            options_long[["underlying_symbol", "expiration", "option_type"]]
            .value_counts()
            .head(10)
        )
