# Put-Call Parity verification (Q9)
# For each strike, compute the theoretical call/put from the other side
# using C - P = S - K*exp(-rT), then compare with market bid/ask

import numpy as np
import pandas as pd
from tabulate import tabulate

import config


def verify_parity(all_chains, spots, r):
    rows = []
    for ticker, by_exp in all_chains.items():
        S = spots[ticker]
        if S is None:
            continue
        for exp, (calls_df, puts_df) in by_exp.items():
            if calls_df is None or puts_df is None:
                continue
            if calls_df.empty or puts_df.empty:
                continue

            T = calls_df["T"].iloc[0]
            discount = np.exp(-r * T)

            # merge calls and puts on strike
            calls = calls_df[["strike", "bid", "ask"]].copy()
            calls.columns = ["strike", "call_bid", "call_ask"]
            puts = puts_df[["strike", "bid", "ask"]].copy()
            puts.columns = ["strike", "put_bid", "put_ask"]

            merged = pd.merge(calls, puts, on="strike", how="inner")
            merged.drop_duplicates(subset=["strike"], inplace=True)

            for _, row in merged.iterrows():
                K = row["strike"]
                c_bid = row["call_bid"] or 0
                c_ask = row["call_ask"] or 0
                p_bid = row["put_bid"] or 0
                p_ask = row["put_ask"] or 0
                c_mid = (c_bid + c_ask) / 2 if (c_bid + c_ask) > 0 else None
                p_mid = (p_bid + p_ask) / 2 if (p_bid + p_ask) > 0 else None

                if c_mid is None or p_mid is None:
                    continue

                # from put-call parity: C - P = S - K*e^(-rT)
                p_parity = c_mid - S + K * discount   # theoretical put from call
                c_parity = p_mid + S - K * discount   # theoretical call from put
                parity_diff = (c_mid - p_mid) - (S - K * discount)

                rows.append({
                    "Ticker": ticker,
                    "Expiry": exp,
                    "Strike": K,
                    "Market_Call_Bid": c_bid,
                    "Market_Call_Ask": c_ask,
                    "Market_Call_Mid": c_mid,
                    "Market_Put_Bid": p_bid,
                    "Market_Put_Ask": p_ask,
                    "Market_Put_Mid": p_mid,
                    "Parity_Call": c_parity,
                    "Parity_Put": p_parity,
                    "Parity_Error": parity_diff,
                })

    return pd.DataFrame(rows)


def run_put_call_parity(data):
    print("=" * 78)
    print("Q9 - PUT-CALL PARITY VERIFICATION")
    print("=" * 78)

    df = verify_parity(
        data["all_chains"], data["spots"], data["risk_free_rate"]
    )
    if df.empty:
        print("  No matching call-put pairs found.")
        return df

    df.to_csv(f"{config.OUTPUT_DIR}/put_call_parity.csv", index=False)
    print(f"  Saved {len(df)} rows to {config.OUTPUT_DIR}/put_call_parity.csv")

    for (ticker, exp), grp in df.groupby(["Ticker", "Expiry"]):
        print(f"\n  {ticker}  {exp}  ({len(grp)} strikes)")
        show = grp.head(20)[[
            "Strike", "Market_Call_Mid", "Market_Put_Mid",
            "Parity_Call", "Parity_Put",
            "Market_Call_Bid", "Market_Call_Ask",
            "Market_Put_Bid", "Market_Put_Ask",
            "Parity_Error"
        ]]
        print(tabulate(show, headers="keys", tablefmt="grid",
                       floatfmt=".4f", showindex=False))

    abs_err = df["Parity_Error"].abs()
    print(f"\n  Mean |parity error|:   {abs_err.mean():.4f}")
    print(f"  Max  |parity error|:   {abs_err.max():.4f}")
    print("  Small deviations are expected due to bid-ask spread,")
    print("  dividends, and American-exercise premium.\n")

    return df


if __name__ == "__main__":
    print("Run via main.py (needs data_gathering output).")
