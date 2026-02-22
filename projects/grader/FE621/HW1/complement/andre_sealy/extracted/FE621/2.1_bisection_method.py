import re
from datetime import datetime

import pandas as pd
from pandas.core.base import SelectionMixin

from bisection import implied_vol

risk_free_rate = 0.0362


def select_option_type(x: str) -> str:
    """
    Accepts: 'c', 'p', 'C', 'P', 'call', 'put'
    Returns: 'c' or 'p'
    """
    if x is None:
        return None
    s = str(x).strip().lower()
    if s in ("c", "call", "calls"):
        return "c"
    if s in ("p", "put", "puts"):
        return "p"
    raise ValueError("option_type must be one of: c, p, call, put")


def calculate_implied_vol(
    csv_file="data1.csv",
    ticker=None,
    option_type=None,
    stock_price=None,
    risk_free_rate=risk_free_rate,
):
    df = pd.read_csv(csv_file)

    # --- ticker filter (regex against contractSymbol) ---
    if ticker:
        t = str(ticker).strip().upper()
        # Options contractSymbol typically starts with the ticker, e.g. SPY260220C...
        # If you truly want "anywhere in the string", remove the leading '^'.
        pattern = rf"^{re.escape(t)}"
        df = df[df["contractSymbol"].str.contains(pattern, regex=True, na=False)]

    # --- option_type normalization + filter (uses column option_type in CSV) ---
    opt = select_option_type(option_type) if option_type else None

    if "option_type" not in df.columns:
        raise KeyError("CSV is missing required column: option_type")

    # Normalize CSV values like 'C'/'P' -> 'c'/'p'
    df["option_type"] = (
        df["contractSymbol"]
        .astype(str)
        .str.extract(r"^[A-Z]+\d{6}([CP])", expand=False)
        .str.lower()
    )

    df = df[df["option_type"].isin(["c", "p"])]

    if opt:
        df = df[df["option_type"] == opt]

    # --- dates / maturity ---
    df["lastTradeDate"] = pd.to_datetime(df["lastTradeDate"], utc=True, errors="coerce")
    df["expirationDate"] = pd.to_datetime(
        df["expirationDate"], utc=True, errors="coerce"
    )
    df["T"] = (df["expirationDate"] - df["lastTradeDate"]).dt.total_seconds() / (
        365.25 * 24 * 3600
    )

    # --- stock price input ---
    if stock_price is None:
        raise ValueError("stock_price is required")
    df["S"] = float(stock_price)

    # --- implied vol calc ---
    calculated_vols = []
    for _, row in df.iterrows():
        try:
            vol = implied_vol(
                option_type=row["option_type"],  # expects 'c' or 'p'
                bid=float(row["bid"]),
                ask=float(row["ask"]),
                S=float(row["S"]),
                K=float(row["strike"]),
                r=float(risk_free_rate),
                T=float(row["T"]),
            )
            calculated_vols.append(vol)
        except Exception:
            calculated_vols.append(None)

    df["cal_implied_vol"] = calculated_vols

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

    results_df = calculate_implied_vol(
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
    print("Implied Volatility Calculated")
    print("=" * 50)
    print(f"\nTicker: {ticker.upper()}")
    print(f"Option type: {select_option_type(option_type)}")
    print(f"Stock Price (S): {stock_price}")
    print(f"Risk-Free Rate (r): {risk_free_rate}")
    print(f"Total options processed (after filters): {len(results_df)}")

    if "impliedVolatility" in results_df.columns:
        print("\nComparison with market implied volatility:")
        print(f"Mean absolute difference: {results_df['vol_abs_difference'].mean()}")

    display_cols = ["contractSymbol", "strike", "option_type", "T", "S"]
    if "impliedVolatility" in results_df.columns:
        display_cols.extend(["impliedVolatility", "cal_implied_vol", "vol_difference"])
    else:
        display_cols.append("cal_implied_vol")

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

    results_df.to_csv(f"data/{ticker}_{option_type}_bisection.csv", index=False)
