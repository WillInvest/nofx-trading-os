# Q12 - Reprice options using DATA2 spot price + DATA1 implied vols
# Also adjusts T by one trading day (1/252)

import numpy as np
import pandas as pd
from tabulate import tabulate

import config
from black_scholes import bs_call_price, bs_put_price


def reprice_with_data2(iv_df, spots, r):
    rows = []
    for ticker in iv_df["Ticker"].unique():
        S_data1 = spots[ticker]
        S_data2 = spots[ticker]
        if S_data1 is None:
            continue

        subset = iv_df[(iv_df["Ticker"] == ticker)].dropna(subset=["IV_Bisection"])
        for _, row in subset.iterrows():
            K = row["Strike"]
            T_orig = row["T"]
            sigma = row["IV_Bisection"]
            otype = row["Type"]

            # one trading day has passed
            T_new = max(T_orig - 1.0 / 252.0, 1e-6)

            bs_fn = bs_call_price if otype == "call" else bs_put_price
            predicted_price = bs_fn(S_data2, K, T_new, r, sigma)

            rows.append({
                "Ticker": ticker,
                "Type": otype,
                "Strike": K,
                "Expiry": row["Expiry"],
                "S_DATA1": S_data1,
                "S_DATA2": S_data2,
                "IV_DATA1": sigma,
                "T_DATA1": T_orig,
                "T_DATA2": T_new,
                "Market_MidPrice": row["MidPrice"],
                "Predicted_Price": predicted_price,
                "Diff": predicted_price - row["MidPrice"],
            })

    return pd.DataFrame(rows)


def run_data2_pricing(iv_df, data):
    print("=" * 78)
    print("Q12 - DATA2 REPRICING")
    print("=" * 78)

    df = reprice_with_data2(iv_df, data["spots"], data["risk_free_rate"])
    if df.empty:
        print("  No DATA2 repricing results.")
        return df

    df.to_csv(f"{config.OUTPUT_DIR}/data2_repricing.csv", index=False)
    print(f"  Saved {len(df)} rows to {config.OUTPUT_DIR}/data2_repricing.csv")

    show = df.head(30)[[
        "Ticker", "Type", "Strike", "S_DATA1", "S_DATA2",
        "Market_MidPrice", "Predicted_Price", "Diff"
    ]]
    print(tabulate(show, headers="keys", tablefmt="grid",
                   floatfmt=".4f", showindex=False))

    print(f"\n  Mean |diff|:  {df['Diff'].abs().mean():.4f}")
    print(f"  Max  |diff|:  {df['Diff'].abs().max():.4f}\n")
    return df


if __name__ == "__main__":
    print("Run via main.py (needs IV data).")
