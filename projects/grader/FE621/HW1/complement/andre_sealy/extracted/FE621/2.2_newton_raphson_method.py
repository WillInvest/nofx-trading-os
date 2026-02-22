import re
from math import exp

import pandas as pd

from black_scholes import bs_call, bs_put
from newton_raphson import newton

risk_free_rate = 0.0362


def select_option_type(x: str):
    if x is None:
        return None
    s = str(x).strip().lower()
    if s in ("c", "call", "calls"):
        return "c"
    if s in ("p", "put", "puts"):
        return "p"
    raise ValueError("option_type must be one of: c, p, call, put")


def implied_vol_newton(
    option_type, bid, ask, S, K, r, T, x0=0.3, tol=1e-6, max_iter=50
):
    option_price = (bid + ask) / 2.0
    if option_price <= 0 or T <= 0 or S <= 0 or K <= 0:
        return None

    discK = K * exp(-r * T)

    # No-arbitrage bounds
    if option_type == "c":
        lower = max(S - discK, 0.0)
        upper = S
    else:
        lower = max(discK - S, 0.0)
        upper = discK

    if option_price < lower - 1e-12 or option_price > upper + 1e-12:
        return None

    def f(sigma):
        sigma = max(float(sigma), 1e-6)
        if option_type == "c":
            return bs_call(S, K, T, r, sigma) - option_price
        return bs_put(S, K, T, r, sigma) - option_price

    sigma = newton(f, x0=x0, tol=tol, max_iter=max_iter)

    if sigma is None:
        return None
    if sigma <= 0:
        return None
    if sigma > 10.0:
        return None
    return sigma


def calculate_implied_vol_newton(
    csv_file="data1.csv",
    ticker=None,
    option_type=None,
    stock_price=None,
    risk_free_rate=risk_free_rate,
):
    df = pd.read_csv(csv_file)

    if ticker:
        t = str(ticker).strip().upper()
        df = df[
            df["contractSymbol"]
            .astype(str)
            .str.contains(rf"^{re.escape(t)}", regex=True, na=False)
        ]
    df["option_type"] = (
        df["contractSymbol"]
        .astype(str)
        .str.extract(r"^[A-Z]+\d{6}([CP])", expand=False)
        .str.lower()
    )

    df = df[df["option_type"].isin(["c", "p"])]
    opt = select_option_type(option_type) if option_type else None

    if opt:
        df = df[df["option_type"] == opt]

    df["lastTradeDate"] = pd.to_datetime(df["lastTradeDate"], utc=True, errors="coerce")
    df["expirationDate"] = pd.to_datetime(
        df["expirationDate"], utc=True, errors="coerce"
    )
    df["T"] = (df["expirationDate"] - df["lastTradeDate"]).dt.total_seconds() / (
        365.25 * 24 * 3600
    )

    if stock_price is None:
        raise ValueError("stock_price is required")
    df["S"] = float(stock_price)

    vols = []
    for _, row in df.iterrows():
        vols.append(
            implied_vol_newton(
                option_type=row["option_type"],
                bid=row["bid"],
                ask=row["ask"],
                S=row["S"],
                K=row["strike"],
                r=float(risk_free_rate),
                T=row["T"],
                x0=0.3,
                tol=1e-6,
                max_iter=50,
            )
        )

    df["cal_implied_vol"] = vols

    # compare with market implied volatility
    if "impliedVolatility" in df.columns:
        df["vol_difference"] = df["cal_implied_vol"] - df["impliedVolatility"]
        df["vol_abs_difference"] = df["vol_difference"].abs()

    return df


if __name__ == "__main__":
    ticker = input("Ticker (e.g. SPY): ").strip()
    option_type = input("Option type (c/p or call/put): ").strip()
    stock_price = float(input("Stock price (S): ").strip())

    r_in = input(f"Risk-free rate r (press Enter for {risk_free_rate}): ").strip()
    risk_free_rate = float(r_in) if r_in else risk_free_rate

    results_df = calculate_implied_vol_newton(
        csv_file="data1.csv",
        ticker=ticker,
        option_type=option_type,
        stock_price=stock_price,
        risk_free_rate=risk_free_rate,
    )

    results_df.drop(
        columns=[
            "change",
            "percentChange",
            "openInterest",
            "contractSize",
            "currency",
            "volume",
        ],
        inplace=True,
    )

    print("=" * 50)
    print("Implied Volatility (Newton-Raphson Calculator)")
    print("=" * 50)
    print(f"\nTicker: {ticker.upper()}")
    print(f"Stock Price (S): {stock_price}")
    print(f"Risk-Free Rate (r): {risk_free_rate}")
    print(f"Total options processed (after filters): {len(results_df)}")

    if "impliedVolatility" in results_df.columns and len(results_df) > 0:
        print("\nComparison with market implied volatility:")
        print(f"Mean absolute difference: {results_df['vol_abs_difference'].mean()}")

    display_cols = [
        "contractSymbol",
        "strike",
        "bid",
        "ask",
        "option_type",
        "T",
        "S",
        "cal_implied_vol",
    ]
    if "impliedVolatility" in results_df.columns:
        display_cols.extend(["impliedVolatility", "vol_difference"])

    print("\n" + "=" * 50)
    print("Results")
    print(results_df[display_cols].to_string(index=False))

    results_df = results_df[
        [
            "contractSymbol",
            "lastTradeDate",
            "expirationDate",
            "option_type",
            "lastPrice",
            "S",
            "strike",
            "T",
            "impliedVolatility",
            "cal_implied_vol",
            "vol_difference",
            "vol_abs_difference",
            "inTheMoney",
        ]
    ]

    results_df = results_df.dropna()

    results_df.to_csv(f"data/{ticker}_{option_type}_newton.csv", index=False)
