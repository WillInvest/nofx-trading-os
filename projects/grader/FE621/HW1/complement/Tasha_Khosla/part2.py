import time
from collections.abc import Callable
from pathlib import Path

import pandas as pd
import scipy
import math

from matplotlib import pyplot as plt

DATA_DIR = Path("fe621_hw1_part1_output")


def black_scholes(
    spot: float, strike: float, r: float, sigma: float, t: float
) -> tuple[float, float, float, float]:
    d1 = (math.log(spot / strike) + (r + (sigma**2) / 2) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)
    call = scipy.stats.norm.cdf(d1) * spot - scipy.stats.norm.cdf(
        d2
    ) * strike * math.exp(-r * t)
    put = scipy.stats.norm.cdf(-d2) * strike * math.exp(
        -r * t
    ) - spot * scipy.stats.norm.cdf(-d1)
    return d1, d2, call, put


def vega(spot: float, strike: float, r: float, sigma: float, t: float) -> float:
    d1 = (math.log(spot / strike) + (r + (sigma**2) / 2) * t) / (sigma * math.sqrt(t))
    return spot * scipy.stats.norm.pdf(d1) * math.sqrt(t)


def get_bs_call_or_put_fn(
    option_type: str, spot: float, strike: float, r: float, t: float, mid_price: float
) -> Callable[float]:
    if option_type == "call":

        def f(s: float):
            return black_scholes(spot, strike, r, s, t)[2] - mid_price
    elif option_type == "put":

        def f(s: float):
            return black_scholes(spot, strike, r, s, t)[3] - mid_price
    else:
        raise ValueError(f'Invalid option type "{option_type}"')
    return f


def bisection_method(
    spot: float,
    strike: float,
    r: float,
    t: float,
    mid_price: float,
    option_type: str,
    tolerance: float = 1e-6,
    lower_bound: float = 1e-6,  # Textbook suggests 0, but then you divide by 0...
    upper_bound: float = 5.0,  # These options are just... super volatile?
) -> float:
    a = lower_bound
    b = upper_bound
    midpoint = (a + b) / 2

    f = get_bs_call_or_put_fn(option_type, spot, strike, r, t, mid_price)

    while abs(b - a) >= tolerance:
        midpoint = (a + b) / 2
        f_midpoint = f(midpoint)
        if f(a) * f_midpoint < 0:
            b = midpoint
        else:
            a = midpoint
    return midpoint


def newtons_method(
    spot: float,
    strike: float,
    r: float,
    t: float,
    mid_price: float,
    option_type: str,
    tolerance: float = 1e-6,
    max_iterations: int = 10,
    initial_vol: float = 0.2,
) -> float:
    vol = initial_vol
    f = get_bs_call_or_put_fn(option_type, spot, strike, r, t, mid_price)
    for _ in range(max_iterations):
        numerator = f(vol)
        if numerator < tolerance:
            return vol
        denominator = vega(spot, strike, r, vol, t)
        vol = vol - (numerator / denominator)
    return vol


def put_call_parity(
    option_value: float,
    strike: float,
    r: float,
    t: float,
    mid_price: float,
    option_type: str,
) -> float:
    if option_type == "put":
        return option_value - strike * math.exp(-r * t) + mid_price
    if option_type == "call":
        return option_value + strike * math.exp(-r * t) - mid_price
    raise ValueError(f'Invalid option type "{option_type}"')


def bs_greeks(
    spot: float, strike: float, r: float, sigma: float, t: float
) -> tuple[float, float, float]:
    d1 = (math.log(spot / strike) + (r + 0.5 * sigma**2) * t) / (sigma * math.sqrt(t))
    delta = scipy.stats.norm.cdf(d1)
    vega = spot * math.sqrt(t) * scipy.stats.norm.pdf(d1)
    gamma = scipy.stats.norm.pdf(d1) / (spot * sigma * math.sqrt(t))
    return delta, vega, gamma


def bs_greeks_finite_difference(
    spot: float,
    strike: float,
    r: float,
    sigma: float,
    t: float,
    h_s: float | None = None,
    h_sigma=1e-4,
):
    if h_s is None:
        h_s = 0.01 * spot

    c0 = black_scholes(spot, strike, r, sigma, t)[2]
    c_up = black_scholes(spot + h_s, strike, r, sigma, t)[2]
    c_dn = black_scholes(spot - h_s, strike, r, sigma, t)[2]

    delta = (c_up - c_dn) / (2 * h_s)
    gamma = (c_up - 2 * c0 + c_dn) / (h_s**2)

    c_sigma_up = black_scholes(spot, strike, r, sigma + h_sigma, t)[2]
    c_sigma_dn = black_scholes(spot, strike, r, sigma - h_sigma, t)[2]
    vega = (c_sigma_up - c_sigma_dn) / (2 * h_sigma)

    return delta, vega, gamma


def main():
    pd.set_option("display.width", 200)
    pd.set_option("display.max_columns", 12)
    day1 = pd.read_csv(DATA_DIR / "DATA1_20260209_113004_options.csv")
    stocks = ["TSLA", "SPY"]

    day1["mid"] = (day1["bid"] + day1["ask"]) / 2.0
    day1 = day1[day1["volume"] > 0]

    day1["expiration"] = pd.to_datetime(day1["expiration"])
    day1["download_time_local"] = pd.to_datetime(day1["download_time_local"])

    day1["days_to_expiry"] = (day1["expiration"] - day1["download_time_local"]).apply(
        lambda d: d.days
    )
    day1["T"] = day1["days_to_expiry"] / 365.0

    implied_vols = []

    print("Calculating implied volatilities using bisection...")
    start = time.time()
    for _, option in day1.iterrows():
        implied_vols.append(
            bisection_method(
                option["underlying_spot_at_download"],
                option["strike"],
                option["risk_free_rate_decimal"],
                option["T"],
                option["mid"],
                option["option_type"],
            )
        )
    end = time.time()
    print(f"Took {end - start:.2f} seconds")

    day1["implied_volatility"] = implied_vols

    implied_vols.clear()

    print("Calculating implied volatilities using Newton's method...")
    start = time.time()
    for _, option in day1.iterrows():
        implied_vols.append(
            newtons_method(
                option["underlying_spot_at_download"],
                option["strike"],
                option["risk_free_rate_decimal"],
                option["T"],
                option["mid"],
                option["option_type"],
            )
        )
    end = time.time()
    print(f"Took {end - start:.2f} seconds")
    day1["implied_volatility_newtons"] = implied_vols

    day1["moneyness"] = abs(day1["strike"] - day1["underlying_spot_at_download"])
    day1["moneyness_ratio"] = day1["underlying_spot_at_download"] / day1["strike"]
    for stock in stocks:
        day1_stock = day1[day1["underlying_symbol"] == stock]
        day1_stock_atm = day1_stock[
            day1_stock["moneyness"] == day1_stock["moneyness"].min()
        ]
        day1_stock_between = day1_stock[
            day1_stock["moneyness_ratio"].between(0.9, 1.1, inclusive="both")
        ]
        avg_iv = day1_stock_between["implied_volatility"].mean()
        print(
            f"At the money for {stock}:\n{day1_stock_atm[['moneyness', 'implied_volatility', 'implied_volatility_newtons']]}\nAverage IV for between ITM and OOTM: {avg_iv}"
        )

    part8_table = day1[
        [
            "underlying_symbol",
            "expiration",
            "days_to_expiry",
            "option_type",
            "strike",
            "moneyness_ratio",
            "implied_volatility",
        ]
    ].sort_values(["underlying_symbol", "expiration", "strike"])

    print(part8_table)
    part8_table.to_csv("part8.csv")

    pcp = []
    for _, option in day1.iterrows():
        pcp.append(
            put_call_parity(
                option["underlying_spot_at_download"],
                option["strike"],
                option["risk_free_rate_decimal"],
                option["T"],
                option["mid"],
                option["option_type"],
            )
        )

    day1["put_call_parity"] = pcp
    print(day1[["option_type", "mid", "put_call_parity", "bid", "ask"]])

    # 2d plot
    maturities = sorted(day1["T"].unique())  # should have 3 unique maturities

    plt.figure(figsize=(8, 6))
    for t in maturities:
        subset = day1[day1["T"] == t]
        plt.scatter(
            subset["strike"], subset["implied_volatility"], label=f"T={round(t, 3)}"
        )

    plt.xlabel("Strike (K)")
    plt.ylabel("Implied Volatility")
    plt.title("Implied Volatility Smile")
    plt.legend()
    plt.grid(True)
    plt.savefig("part10_2d.svg")
    plt.show()

    # 3d plot

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    ax.scatter(day1["strike"], day1["T"], day1["implied_volatility"])

    ax.set_xlabel("Strike")
    ax.set_ylabel("Maturity (T)")
    ax.set_zlabel("Implied Volatility")

    plt.title("Implied Volatility Surface")
    plt.savefig("part10_3d.svg")
    plt.show()

    # greek time!

    greeks = []
    for _, row in day1[day1["option_type"] == "call"].iterrows():
        spot = float(row["underlying_spot_at_download"])
        strike = float(row["strike"])
        t = float(row["T"])
        r = float(row["risk_free_rate_decimal"])
        sigma = float(row["implied_volatility"])

        delta, vega, gamma = bs_greeks(spot, strike, r, sigma, t)
        delta_fd, vega_fd, gamma_fd = bs_greeks_finite_difference(
            spot, strike, r, sigma, t
        )

        greeks.append(
            {
                "underlying_symbol": row["underlying_symbol"],
                "expiration": row["expiration"],
                "strike": strike,
                "T": t,
                "sigma": sigma,
                "delta_bs": delta,
                "delta_fd": delta_fd,
                "vega_bs": vega,
                "vega_fd": vega_fd,
                "gamma_bs": gamma,
                "gamma_fd": gamma_fd,
            }
        )

    greeks = pd.DataFrame(greeks)

    print(greeks)
    greeks.to_csv("greeks.csv")

    # Part 12
    day2 = pd.read_csv(DATA_DIR / "DATA2_20260210_103345_options.csv")
    # quick and dirty, same format as day 1
    day2["mid"] = (day2["bid"] + day2["ask"]) / 2.0
    day2 = day2[day2["volume"] > 0]
    day2["expiration"] = pd.to_datetime(day2["expiration"])
    day2["download_time_local"] = pd.to_datetime(day2["download_time_local"])
    day2["days_to_expiry"] = (day2["expiration"] - day2["download_time_local"]).apply(
        lambda d: d.days
    )
    day2["T"] = day2["days_to_expiry"] / 365.0

    day1 = (
        day1[
            [
                "underlying_symbol",
                "expiration",
                "strike",
                "option_type",
                "implied_volatility",
            ]
        ]
        .dropna()
        .drop_duplicates()
    )

    day2 = day2.merge(
        day1,
        on=["underlying_symbol", "expiration", "strike", "option_type"],
        how="left",
    )

    prices = []
    for _, row in day2.iterrows():
        bs = black_scholes(
            row["underlying_spot_at_download"],
            row["strike"],
            row["risk_free_rate_decimal"],
            row["implied_volatility"],
            row["T"],
        )
        option_type = row["option_type"]
        if option_type == "call":
            prices.append(bs[2])
        elif option_type == "put":
            prices.append(bs[3])
        else:
            raise ValueError(f'Invalid option type "{option_type}"')

    day2["price_using_day1"] = prices
    print(day2)
    day2.to_csv("part12.csv")


if __name__ == "__main__":
    main()
