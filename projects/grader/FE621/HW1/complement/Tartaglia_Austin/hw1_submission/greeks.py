# Greeks computation (Q11)
# Analytical formulas vs numerical (central finite difference) approximations

import numpy as np
import pandas as pd
from scipy.stats import norm
from tabulate import tabulate

import config
from black_scholes import bs_d1, bs_call_price, bs_put_price, bs_vega


# --- Analytical Greeks ---

def delta_call(S, K, T, r, sigma):
    return norm.cdf(bs_d1(S, K, T, r, sigma))


def delta_put(S, K, T, r, sigma):
    return delta_call(S, K, T, r, sigma) - 1.0


def gamma(S, K, T, r, sigma):
    d1 = bs_d1(S, K, T, r, sigma)
    return norm.pdf(d1) / (S * sigma * np.sqrt(T))


def vega_analytical(S, K, T, r, sigma):
    return bs_vega(S, K, T, r, sigma)


# --- Numerical Greeks (central finite differences) ---

def delta_num(S, K, T, r, sigma, opt_type="call"):
    h = 0.01 * S
    bs_fn = bs_call_price if opt_type == "call" else bs_put_price
    return (bs_fn(S + h, K, T, r, sigma) -
            bs_fn(S - h, K, T, r, sigma)) / (2 * h)


def gamma_num(S, K, T, r, sigma, opt_type="call"):
    h = 0.01 * S
    bs_fn = bs_call_price if opt_type == "call" else bs_put_price
    return (bs_fn(S + h, K, T, r, sigma) -
            2 * bs_fn(S, K, T, r, sigma) +
            bs_fn(S - h, K, T, r, sigma)) / (h ** 2)


def vega_num(S, K, T, r, sigma, opt_type="call"):
    h = 0.001
    bs_fn = bs_call_price if opt_type == "call" else bs_put_price
    sig_lo = max(sigma - h, 1e-6)
    return (bs_fn(S, K, T, r, sigma + h) -
            bs_fn(S, K, T, r, sig_lo)) / (2 * h)


def greeks_comparison(iv_df, r, n_sample=20):
    # pick the ~20 most ATM options for each ticker and compare
    rows = []
    for ticker in iv_df["Ticker"].unique():
        subset = iv_df[(iv_df["Ticker"] == ticker)].dropna(subset=["IV_Bisection"])
        if subset.empty:
            continue
        subset = subset.copy()
        subset["abs_m"] = (subset["Moneyness"] - 1.0).abs()
        sample = subset.nsmallest(n_sample, "abs_m")

        for _, row in sample.iterrows():
            S = row["SpotPrice"]
            K = row["Strike"]
            T = row["T"]
            sigma = row["IV_Bisection"]
            otype = row["Type"]

            if sigma is None or sigma <= 0 or T <= 0:
                continue

            if otype == "call":
                a_delta = delta_call(S, K, T, r, sigma)
            else:
                a_delta = delta_put(S, K, T, r, sigma)
            a_gamma = gamma(S, K, T, r, sigma)
            a_vega = vega_analytical(S, K, T, r, sigma)

            n_delta = delta_num(S, K, T, r, sigma, otype)
            n_gamma = gamma_num(S, K, T, r, sigma, otype)
            n_vega = vega_num(S, K, T, r, sigma, otype)

            rows.append({
                "Ticker": ticker,
                "Type": otype,
                "Strike": K,
                "Expiry": row["Expiry"],
                "Ana_Delta": a_delta,
                "Num_Delta": n_delta,
                "Ana_Gamma": a_gamma,
                "Num_Gamma": n_gamma,
                "Ana_Vega": a_vega,
                "Num_Vega": n_vega,
            })

    return pd.DataFrame(rows)


def run_greeks(iv_df, r):
    print("=" * 78)
    print("Q11 - GREEKS: ANALYTICAL vs NUMERICAL")
    print("=" * 78)

    df = greeks_comparison(iv_df, r)
    if df.empty:
        print("  No data for Greeks comparison.")
        return df

    df.to_csv(f"{config.OUTPUT_DIR}/greeks_comparison.csv", index=False)
    print(f"  Saved {len(df)} rows to {config.OUTPUT_DIR}/greeks_comparison.csv")

    show_cols = ["Ticker", "Type", "Strike",
                 "Ana_Delta", "Num_Delta",
                 "Ana_Gamma", "Num_Gamma",
                 "Ana_Vega", "Num_Vega"]
    print(tabulate(df[show_cols].head(30), headers="keys", tablefmt="grid",
                   floatfmt=".6f", showindex=False))
    print()
    return df


if __name__ == "__main__":
    print("Run via main.py (needs IV data).")
