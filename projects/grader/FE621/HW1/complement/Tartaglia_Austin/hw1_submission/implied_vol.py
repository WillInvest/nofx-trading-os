# Implied volatility computation (Q6, Q7, Q8)
# Uses bisection, Newton, and secant to invert BS for sigma
# Also compares with VIX and analyzes convergence speed

import numpy as np
import pandas as pd
from tabulate import tabulate

import config
from black_scholes import bs_call_price, bs_put_price, bs_vega
from root_finding import bisection, newton, secant


def _iv_objective(sigma, S, K, T, r, market_price, opt_type):
    # f(sigma) = BS(sigma) - market_price; root is the implied vol
    bs_fn = bs_call_price if opt_type == "call" else bs_put_price
    return bs_fn(S, K, T, r, sigma) - market_price


def _iv_vega(sigma, S, K, T, r):
    return bs_vega(S, K, T, r, sigma)


def compute_iv_bisection(S, K, T, r, market_price, opt_type):
    f = lambda sig: _iv_objective(sig, S, K, T, r, market_price, opt_type)
    try:
        fa = f(config.IV_LOWER)
        fb = f(config.IV_UPPER)
        if fa * fb > 0:
            return None, 0, 0.0
        return bisection(f, config.IV_LOWER, config.IV_UPPER,
                         tol=config.TOLERANCE, max_iter=config.MAX_ITER)
    except Exception:
        return None, 0, 0.0


def compute_iv_newton(S, K, T, r, market_price, opt_type):
    # Newton uses vega as the derivative of BS w.r.t. sigma
    f = lambda sig: _iv_objective(sig, S, K, T, r, market_price, opt_type)
    fp = lambda sig: _iv_vega(sig, S, K, T, r)
    try:
        iv, iters, t = newton(f, fp, 0.3,
                              tol=config.TOLERANCE, max_iter=config.MAX_ITER)
        if iv <= 0 or iv > config.IV_UPPER:
            return None, iters, t
        return iv, iters, t
    except Exception:
        return None, 0, 0.0


def compute_iv_secant(S, K, T, r, market_price, opt_type):
    f = lambda sig: _iv_objective(sig, S, K, T, r, market_price, opt_type)
    try:
        iv, iters, t = secant(f, 0.1, 0.5,
                              tol=config.TOLERANCE, max_iter=config.MAX_ITER)
        if iv <= 0 or iv > config.IV_UPPER:
            return None, iters, t
        return iv, iters, t
    except Exception:
        return None, 0, 0.0


def compute_all_ivs(all_chains, spots, r):
    # loop over every option, compute IV with all three methods
    rows = []
    for ticker, by_exp in all_chains.items():
        S = spots[ticker]
        if S is None:
            continue
        for exp, (calls_df, puts_df) in by_exp.items():
            for label, df in [("call", calls_df), ("put", puts_df)]:
                if df is None or df.empty:
                    continue
                T_val = df["T"].iloc[0]
                for _, row in df.iterrows():
                    K = row["strike"]
                    bid = row.get("bid", 0) or 0
                    ask = row.get("ask", 0) or 0
                    vol = row.get("volume", 0) or 0

                    # skip options with no valid quotes or zero volume
                    if bid <= 0 and ask <= 0:
                        continue
                    if vol <= 0:
                        continue

                    mid = (bid + ask) / 2.0
                    if mid <= 0:
                        continue

                    moneyness = K / S

                    iv_b, it_b, t_b = compute_iv_bisection(
                        S, K, T_val, r, mid, label)
                    iv_n, it_n, t_n = compute_iv_newton(
                        S, K, T_val, r, mid, label)
                    iv_s, it_s, t_s = compute_iv_secant(
                        S, K, T_val, r, mid, label)

                    rows.append({
                        "Ticker": ticker,
                        "Expiry": exp,
                        "Type": label,
                        "Strike": K,
                        "MidPrice": mid,
                        "Moneyness": moneyness,
                        "IV_Bisection": iv_b,
                        "IV_Newton": iv_n,
                        "IV_Secant": iv_s,
                        "Iters_Bisection": it_b,
                        "Iters_Newton": it_n,
                        "Iters_Secant": it_s,
                        "Time_Bisection": t_b,
                        "Time_Newton": t_n,
                        "Time_Secant": t_s,
                        "T": T_val,
                        "SpotPrice": S,
                    })

    return pd.DataFrame(rows)


def atm_summary(iv_df):
    # Q6: report ATM IV and average IV within the moneyness band
    band_lo = config.MONEYNESS_LOWER
    band_hi = config.MONEYNESS_UPPER
    summary_rows = []

    for (ticker, exp, otype), grp in iv_df.groupby(["Ticker", "Expiry", "Type"]):
        valid = grp.dropna(subset=["IV_Bisection"])
        if valid.empty:
            continue

        # ATM = strike closest to spot
        atm_idx = (valid["Moneyness"] - 1.0).abs().idxmin()
        atm_iv = valid.loc[atm_idx, "IV_Bisection"]
        atm_strike = valid.loc[atm_idx, "Strike"]

        # average IV for options in the moneyness band
        band = valid[(valid["Moneyness"] >= band_lo) &
                     (valid["Moneyness"] <= band_hi)]
        avg_iv = band["IV_Bisection"].mean() if not band.empty else None

        summary_rows.append({
            "Ticker": ticker,
            "Expiry": exp,
            "Type": otype,
            "ATM_Strike": atm_strike,
            "ATM_IV": atm_iv,
            f"Avg_IV_{band_lo}-{band_hi}": avg_iv,
            "N_in_band": len(band),
        })

    return pd.DataFrame(summary_rows)


def vix_comparison(iv_df, current_vix):
    # Q8: compare implied vols with current VIX value
    print("\n  Q8: IMPLIED VOL vs VIX COMPARISON")
    if current_vix:
        print(f"  Current ^VIX value: {current_vix:.2f}%")
        vix_decimal = current_vix / 100.0
    else:
        print("  Current ^VIX value: N/A")
        vix_decimal = None

    spy = iv_df[iv_df["Ticker"] == "SPY"].dropna(subset=["IV_Bisection"])
    if spy.empty:
        print("  No SPY IV data for comparison.")
        return

    comp_rows = []
    for (exp, otype), grp in spy.groupby(["Expiry", "Type"]):
        atm = grp.loc[(grp["Moneyness"] - 1.0).abs().idxmin()]
        comp_rows.append({
            "Expiry": exp,
            "Type": otype,
            "T": atm["T"],
            "ATM_IV": atm["IV_Bisection"],
            "VIX_decimal": vix_decimal,
            "Diff": atm["IV_Bisection"] - vix_decimal if vix_decimal else None,
        })
    comp_df = pd.DataFrame(comp_rows)
    print(tabulate(comp_df, headers="keys", tablefmt="grid",
                   floatfmt=".4f", showindex=False))

    print("\n  Commentary:")
    print("  VIX measures 30-day expected vol for S&P 500 options (ATM-weighted).")
    print("  As maturity increases, ATM implied vol may rise or fall relative to")
    print("  VIX depending on the term structure of volatility.")
    print("  ITM/OTM options typically exhibit higher IV than ATM (volatility smile/")
    print("  skew), which diverges from the VIX's ATM-focused measure.")
    print()


def convergence_summary(iv_df):
    # Q7: compare convergence speed of the three root-finding methods
    print("\n  Q7: CONVERGENCE COMPARISON")
    valid = iv_df.dropna(subset=["IV_Bisection", "IV_Newton"])
    if valid.empty:
        print("  No data for comparison.")
        return
    summary = {
        "Method": ["Bisection", "Newton", "Secant"],
        "Avg_Iters": [
            valid["Iters_Bisection"].mean(),
            valid["Iters_Newton"].mean(),
            valid["Iters_Secant"].mean(),
        ],
        "Avg_Time_ms": [
            valid["Time_Bisection"].mean() * 1000,
            valid["Time_Newton"].mean() * 1000,
            valid["Time_Secant"].mean() * 1000,
        ],
    }
    print(tabulate(pd.DataFrame(summary), headers="keys", tablefmt="grid",
                   floatfmt=".4f", showindex=False))
    print("  Newton converges quadratically and is typically fastest.")
    print("  Bisection is robust but converges linearly (more iterations).")
    print()


def run_implied_vol(data):
    print("=" * 78)
    print("PART 2 - IMPLIED VOLATILITY (Q6-Q8)")
    print("=" * 78)

    iv_df = compute_all_ivs(
        data["all_chains"], data["spots"], data["risk_free_rate"]
    )

    if iv_df.empty:
        print("  No implied vols computed (no valid option data).")
        return iv_df

    iv_df.to_csv(f"{config.OUTPUT_DIR}/implied_vols.csv", index=False)
    print(f"  Saved {len(iv_df)} IV rows to {config.OUTPUT_DIR}/implied_vols.csv")

    atm = atm_summary(iv_df)
    print("\n  Q6: ATM IMPLIED VOLATILITY SUMMARY")
    print(tabulate(atm, headers="keys", tablefmt="grid",
                   floatfmt=".4f", showindex=False))

    convergence_summary(iv_df)

    # Robustly get VIX
    current_iv_vix = data.get("current_vix")
    if current_iv_vix is None and "vix" in data and not data["vix"].empty:
         try:
             current_iv_vix = data["vix"]["Close"].iloc[-1]
         except:
             current_iv_vix = None

    vix_comparison(iv_df, current_iv_vix)

    # Q8: compare TSLA vs SPY IV levels
    print("  TSLA vs SPY COMMENTARY")
    for ticker in ["TSLA", "SPY"]:
        subset = iv_df[(iv_df["Ticker"] == ticker)].dropna(subset=["IV_Bisection"])
        if not subset.empty:
            avg = subset["IV_Bisection"].mean()
            print(f"  {ticker} average IV: {avg:.4f}")
    print("  TSLA options typically have significantly higher implied")
    print("  volatility than SPY, reflecting its higher idiosyncratic risk")
    print("  and speculative activity relative to the diversified S&P 500.\n")

    return iv_df


if __name__ == "__main__":
    print("Run via main.py (needs data_gathering output).")
