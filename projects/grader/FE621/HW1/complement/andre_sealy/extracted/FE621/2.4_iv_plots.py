import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def norm_option_type(x: str) -> str:
    s = str(x).strip().lower()
    if s in ("c", "call"):
        return "c"
    if s in ("p", "put"):
        return "p"
    raise ValueError("option_type must be c/p (or call/put)")


def data_path(data_dir: str, ticker: str, option_type: str, method: str) -> str:
    t = str(ticker).strip().upper()
    ot = norm_option_type(option_type)
    m = str(method).strip().lower()
    path = os.path.join(data_dir, f"{t}_{ot}_{m}.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Expected: {path}")
    return path


def load_iv_data(
    ticker: str,
    option_type: str,
    method: str,
    data_dir: str = "data",
    iv_col: str = "cal_implied_vol",
) -> pd.DataFrame:
    path = data_path(data_dir, ticker, option_type, method)
    df = pd.read_csv(path)
    if iv_col not in df.columns:
        raise KeyError(f"IV column {iv_col!r} not in {path}")
    df["expirationDate"] = pd.to_datetime(
        df["expirationDate"], utc=True, errors="coerce"
    )
    df = df.dropna(subset=["strike", "T", iv_col, "expirationDate"])
    return df


def plot_iv_by_expiration(
    df: pd.DataFrame,
    iv_col: str = "cal_implied_vol",
    n_expirations: int = 3,
    title: str = "IV vs Strike by Expiration Date",
):
    exp_dates = df.groupby("expirationDate")["T"].first().nsmallest(n_expirations).index

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]

    for i, exp_date in enumerate(exp_dates):
        sub = df[df["expirationDate"] == exp_date].sort_values("strike")
        ax.plot(
            sub["strike"],
            sub[iv_col],
            label=exp_date.strftime("%Y-%m-%d"),
            color=colors[i % len(colors)],
            marker="o",
            markersize=4,
        )

    ax.set_xlabel("Strike K")
    ax.set_ylabel("Implied Volatility σ")
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    ticker = input("Ticker (SPY/TSLA/VIX): ").strip().upper()
    option_type = input("Option type (c/p): ").strip()
    method = input("Method (bisection/newton): ").strip()

    df = load_iv_data(ticker, option_type, method)
    plot_iv_by_expiration(
        df,
        iv_col="cal_implied_vol",
        title=f"IV vs Strike by Expiration Date — {ticker} {option_type} {method}",
    )
