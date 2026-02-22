import os
import re
from math import exp, log, sqrt

import numpy as np
import pandas as pd
from scipy.stats import norm

DAY_2_SPOT = {"TSLA": 410.45, "SPY": 687.47, "VIX": 18.03}
DAYS_IN_YEAR = 365.25
VALUATION_DATE2 = pd.Timestamp("2026-02-06", tz="UTC")


def norm_ot(x):
    s = str(x).strip().lower()
    if s in ("c", "call"):
        return "c"
    if s in ("p", "put"):
        return "p"
    raise ValueError("option_type must be c/p (or call/put)")


def bs_price(option_type, S, K, T, r, sigma):
    S = float(S)
    K = float(K)
    T = float(T)
    r = float(r)
    sigma = float(sigma)

    if S <= 0 or K <= 0 or T <= 0 or sigma <= 0:
        return np.nan

    d1 = (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))

    d2 = d1 - sigma * sqrt(T)

    if option_type == "c":
        return S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
    else:
        return K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


def data_path(data_dir: str, ticker: str, option_type: str, method: str):
    """
    Expected format similiar data/SPY_p_bisection.csv
    """
    t = str(ticker).strip().upper()
    ot = norm_ot(option_type)
    m = str(method).strip().lower()

    candidates = [
        os.path.join(data_dir, f"{t}_{ot}_{m}.csv"),
        os.path.join(data_dir, f"{t}_{ot}_{m}_method.csv"),
        os.path.join(data_dir, f"{t}_{ot}.csv"),
    ]

    for p in candidates:
        if os.path.exists(p):
            return p

    raise FileNotFoundError(
        f"Could not find a file for ticker={t}, option_type={ot}, method={m} in {data_dir}. "
        f"Tried: {candidates}"
    )


def price_day2(
    ticker: str,
    option_type: str,
    method: str,
    r: float,
    data_dir: str = "data",
    iv_col: str = "cal_implied_vol",
    day2_spot: dict | None = None,
    valuation_date2: pd.Timestamp = VALUATION_DATE2,
    data2_csv: str = "data2.csv",
):

    t = str(ticker).strip().upper()
    ot = norm_ot(option_type)

    if day2_spot is None:
        day2_spot = DAY_2_SPOT

    if t not in day2_spot:
        raise KeyError(f"No day-2 spot configured for ticker {t}. Add it to DAY2_SPOT.")

    path = data_path(data_dir=data_dir, ticker=t, option_type=ot, method=method)
    df = pd.read_csv(path)

    if iv_col not in df.columns:
        raise KeyError(f"Missing required IV column {iv_col!r} in {path}")

    # Use option_type from the file if present, but enforce requested ot filter.
    if "option_type" in df.columns:
        df["ot"] = df["option_type"].astype(str).str.strip().str.lower().str[0]
    else:
        # Derive from contractSymbol if needed
        df["ot"] = (
            df["contractSymbol"]
            .astype(str)
            .str.extract(r"^[A-Z]+\d{6}([CP])", expand=False)
            .str.lower()
        )

    df = df[df["ot"] == ot].copy()

    # Parse dates
    df["expirationDate"] = pd.to_datetime(
        df["expirationDate"], utc=True, errors="coerce"
    )
    df["valuationDate"] = valuation_date2
    df["T"] = (df["expirationDate"] - df["valuationDate"]).dt.total_seconds() / (
        DAYS_IN_YEAR * 24 * 3600
    )

    S_2 = float(day2_spot[t])
    df["S_2"] = S_2

    prices_2 = []
    for _, row in df.iterrows():
        try:
            K = float(row["strike"])
            sigma = float(row[iv_col])
            T = float(row["T"])

            if pd.isna(K) or pd.isna(sigma) or pd.isna(T) or T <= 0 or sigma <= 0:
                prices_2.append(np.nan)
                continue

            prices_2.append(bs_price(ot, S_2, K, T, r, sigma))

        except Exception:
            prices_2.append(np.nan)

    df['bs_price'] = prices_2

    df2 = pd.read_csv(data2_csv)

    keep_cols = ["contractSymbol", "lastPrice"]
    df2 = df2[keep_cols].copy()
    df2 = df2.rename(columns={"lastPrice": "optionPrice"})
    # Merge (left join keeps all rows from your model file)
    df = df.merge(df2, on="contractSymbol", how="left", suffixes=("", "_mkt2"))

    df["price_dff_day2"] = df["bs_price"] - df["optionPrice"]

    return df, path


if __name__ == "__main__":
    ticker = input("Ticker (SPY/TSLA/VIX): ").strip().upper()
    option_type = input("Option type (c/p): ").strip()
    method = input("Method (bisection/newton/...): ").strip()
    r = float(input("Risk-free rate r: "))

    out_df, in_path = price_day2(
        ticker=ticker,
        option_type=option_type,
        method=method,
        r=r,
        data_dir="data",
        iv_col="cal_implied_vol",
        day2_spot=DAY_2_SPOT,
        valuation_date2=VALUATION_DATE2,
        data2_csv="data2.csv",
    )

    print(f"\nLoaded: {in_path}")
    print(f"Valuation date: {VALUATION_DATE2}")
    print(f"Rows after option_type filter: {len(out_df)}")

    cols = [
        "contractSymbol",
        "ot",
        "strike",
        # "expirationDate",
        # "valuationDate",
        "T",
        "S_2",
        "cal_implied_vol",
        "bs_price",
        "optionPrice",
        "price_dff_day2",
    ]

    print(out_df[cols].head(50).to_string(index=False))
