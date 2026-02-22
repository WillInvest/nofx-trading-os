import numpy as np
import pandas as pd
from scipy.stats import norm


def _ot_norm(option_type: str) -> str:
    ot = str(option_type).strip().lower()
    if ot in ("c", "call"):
        return "c"
    if ot in ("p", "put"):
        return "p"
    raise ValueError("option_type must be 'c'/'call' or 'p'/'put'")


def black_scholes(option_type, S, K, T, r, sigma, q=0.0):
    ot = _ot_norm(option_type)

    S = float(S)
    K = float(K)
    T = float(T)
    r = float(r)
    sigma = float(sigma)
    q = float(q)
    if S <= 0 or K <= 0 or T <= 0 or sigma <= 0:
        raise ValueError("S, K, T, sigma must be > 0")

    sqrtT = np.sqrt(T)
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * sqrtT)
    d2 = d1 - sigma * sqrtT

    df_r = np.exp(-r * T)
    df_q = np.exp(-q * T)

    if ot == "c":
        return S * df_q * norm.cdf(d1) - K * df_r * norm.cdf(d2)
    else:
        return K * df_r * norm.cdf(-d2) - S * df_q * norm.cdf(-d1)


def delta_bs(option_type, S, K, T, r, sigma, q=0.0):
    ot = _ot_norm(option_type)

    S = float(S)
    K = float(K)
    T = float(T)
    r = float(r)
    sigma = float(sigma)
    q = float(q)
    sqrtT = np.sqrt(T)
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * sqrtT)

    if ot == "c":
        return np.exp(-q * T) * norm.cdf(d1)
    else:
        return np.exp(-q * T) * (norm.cdf(d1) - 1.0)


def gamma_bs(S, K, T, r, sigma, q=0.0):
    S = float(S)
    K = float(K)
    T = float(T)
    r = float(r)
    sigma = float(sigma)
    q = float(q)
    sqrtT = np.sqrt(T)
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * sqrtT)

    # NOTE: pdf (not cdf)
    return (np.exp(-q * T) * norm.pdf(d1)) / (S * sigma * sqrtT)


def vega_bs(S, K, T, r, sigma, q=0.0):
    S = float(S)
    K = float(K)
    T = float(T)
    r = float(r)
    sigma = float(sigma)
    q = float(q)
    sqrtT = np.sqrt(T)
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * sqrtT)

    return S * np.exp(-q * T) * norm.pdf(d1) * sqrtT


def delta_fdm(option_type, S, K, T, r, sigma, q=0.0, ds=1e-3, method="central"):
    ot = _ot_norm(option_type)
    method = str(method).strip().lower()

    if method == "central":
        return (
            black_scholes(ot, S + ds, K, T, r, sigma, q=q)
            - black_scholes(ot, S - ds, K, T, r, sigma, q=q)
        ) / (2 * ds)
    if method == "forward":
        return (
            black_scholes(ot, S + ds, K, T, r, sigma, q=q)
            - black_scholes(ot, S, K, T, r, sigma, q=q)
        ) / ds
    if method == "backward":
        return (
            black_scholes(ot, S, K, T, r, sigma, q=q)
            - black_scholes(ot, S - ds, K, T, r, sigma, q=q)
        ) / ds

    raise ValueError("method must be 'central', 'forward', or 'backward'")


def gamma_fdm(option_type, S, K, T, r, sigma, q=0.0, ds=1e-2, method="central"):
    ot = _ot_norm(option_type)
    method = str(method).strip().lower()
    if method != "central":
        raise ValueError("gamma_fdm supports method='central' only")

    return (
        black_scholes(ot, S + ds, K, T, r, sigma, q=q)
        - 2.0 * black_scholes(ot, S, K, T, r, sigma, q=q)
        + black_scholes(ot, S - ds, K, T, r, sigma, q=q)
    ) / (ds**2)


def vega_fdm(option_type, S, K, T, r, sigma, q=0.0, dv=1e-4, method="central"):
    ot = _ot_norm(option_type)
    method = str(method).strip().lower()

    if method == "central":
        return (
            black_scholes(ot, S, K, T, r, sigma + dv, q=q)
            - black_scholes(ot, S, K, T, r, sigma - dv, q=q)
        ) / (2 * dv)
    if method == "forward":
        return (
            black_scholes(ot, S, K, T, r, sigma + dv, q=q)
            - black_scholes(ot, S, K, T, r, sigma, q=q)
        ) / dv
    if method == "backward":
        return (
            black_scholes(ot, S, K, T, r, sigma, q=q)
            - black_scholes(ot, S, K, T, r, sigma - dv, q=q)
        ) / dv

    raise ValueError("method must be 'central', 'forward', or 'backward'")


if __name__ == "__main__":
    import os

    import numpy as np
    import pandas as pd

    r = float(input("Risk-free rate r: ").strip())
    q = 0.0  # dividend yield (set if needed)

    spot_by_ticker = {"SPY": 679.52, "TSLA": 399.63, "VIX": 20.52}

    df = pd.read_csv("data1.csv")

    # ticker -> S
    df["ticker"] = (
        df["contractSymbol"].astype(str).str.extract(r"^([A-Z]+)", expand=False)
    )
    df["S"] = df["ticker"].map(spot_by_ticker)

    # dates -> T (years)
    df["lastTradeDate"] = pd.to_datetime(df["lastTradeDate"], utc=True, errors="coerce")
    df["expirationDate"] = pd.to_datetime(
        df["expirationDate"], utc=True, errors="coerce"
    )
    df["T"] = (df["expirationDate"] - df["lastTradeDate"]).dt.total_seconds() / (
        365.25 * 24 * 3600
    )

    # derive option type from contractSymbol (robust)
    df["ot"] = (
        df["contractSymbol"]
        .astype(str)
        .str.extract(r"^[A-Z]+\d{6}([CP])", expand=False)
        .str.lower()
    )

    sigma_col = "impliedVolatility"  # or your computed IV column

    # Pre-create output columns (NaN by default)
    out_cols = [
        "bs_price",
        "delta_bs",
        "gamma_bs",
        "vega_bs",
        "delta_fdm",
        "gamma_fdm",
        "vega_fdm",
    ]
    for c in out_cols:
        df[c] = np.nan

    # Compute row-by-row, write directly into df (no list length mismatch possible)
    for idx, row in df.iterrows():
        try:
            ot = row["ot"]
            S = row["S"]
            K = row["strike"]
            T = row["T"]
            sigma = row[sigma_col]

            if pd.isna(ot) or pd.isna(S) or pd.isna(K) or pd.isna(T) or pd.isna(sigma):
                continue

            S = float(S)
            K = float(K)
            T = float(T)
            sigma = float(sigma)
            if ot not in ("c", "p") or S <= 0 or K <= 0 or T <= 0 or sigma <= 0:
                continue

            df.at[idx, "bs_price"] = black_scholes(ot, S, K, T, r, sigma, q=q)

            # analytic greeks
            df.at[idx, "delta_bs"] = delta_bs(ot, S, K, T, r, sigma, q=q)
            df.at[idx, "gamma_bs"] = gamma_bs(S, K, T, r, sigma, q=q)
            df.at[idx, "vega_bs"] = vega_bs(S, K, T, r, sigma, q=q)

            # finite-difference greeks
            df.at[idx, "delta_fdm"] = delta_fdm(
                ot, S, K, T, r, sigma, q=q, ds=1e-3, method="central"
            )
            df.at[idx, "gamma_fdm"] = gamma_fdm(
                ot, S, K, T, r, sigma, q=q, ds=1e-2, method="central"
            )
            df.at[idx, "vega_fdm"] = vega_fdm(
                ot, S, K, T, r, sigma, q=q, dv=1e-4, method="central"
            )

        except Exception as e:
            # Uncomment to debug a specific bad row:
            # print("row failed:", row.get("contractSymbol"), "error:", e)
            continue

    print(
        df[["contractSymbol", "ticker", "ot", "strike", "S", "T", sigma_col] + out_cols]
        .head(20)
        .to_string(index=False)
    )

    os.makedirs("data", exist_ok=True)
    df.to_csv(
        "data/greeks.csv", index=False
    )  # --- Replace your __main__ block with this (computes BOTH analytic and FDM greeks for calls+puts) ---
