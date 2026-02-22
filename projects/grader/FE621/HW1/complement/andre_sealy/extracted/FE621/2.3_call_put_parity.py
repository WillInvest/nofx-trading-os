import re
from math import exp

import numpy as np
import pandas as pd

risk_free_rate = 0.0362
days_in_year = 365.25

spot_by_ticker = {
    "SPY": 679.52,
    "TSLA": 399.63,
    "VIX": 20.52,
}


def parity_price(option_type, last_price, S, K, r, T):
    if (
        option_type is None
        or pd.isna(option_type)
        or pd.isna(last_price)
        or pd.isna(S)
        or pd.isna(K)
        or pd.isna(T)
    ):
        return np.nan

    ot = str(option_type).strip().upper()
    last_price = float(last_price)
    S = float(S)
    K = float(K)
    T = float(T)
    r = float(r)

    discK = K * exp(-r * T)

    if ot == "C":
        return last_price - S + discK
    elif ot == "P":
        return last_price + S - discK
    else:
        return np.nan


if __name__ == "__main__":
    df = pd.read_csv("data1.csv")
    df["ticker"] = (
        df["contractSymbol"].astype(str).str.extract(r"^([A-Z]+)", expand=False)
    )

    df["S"] = df["ticker"].map(spot_by_ticker)

    df = df[df["S"].notna().copy()]

    df["expirationDate"] = pd.to_datetime(
        df["expirationDate"], utc=True, errors="coerce"
    )
    collection_dt = pd.Timestamp("2026-02-05", tz="UTC")
    df["T"] = (df["expirationDate"] - collection_dt).dt.total_seconds() / (
        days_in_year * 24 * 3600
    )
    df["mid_price"] = (df["bid"] + df["ask"]) / 2

    df["parity_price"] = df.apply(
        lambda row: parity_price(
            option_type=row.get("option_type"),
            last_price=row.get("mid_price"),
            S=row.get("S"),
            K=row.get("strike"),
            r=risk_free_rate,
            T=row.get("T"),
        ),
        axis=1,
    )

    df["parity_price_type"] = (
        df["option_type"].astype(str).str.strip().str.upper().map({"C": "P", "P": "C"})
    )


    df = df.sort_values(by=["ticker", "expirationDate", "strike", "option_type"])
    df.to_csv("data/call_put_parity.csv", index=False)

    cols = [
        "ticker",
        "contractSymbol",
        "option_type",
        "strike",
        "mid_price",
        "S",
        "T",
        "parity_price_type",
        "parity_price",
    ]
    print(df[cols].head(20).to_string(index=False))