import pandas as pd
import numpy as np
from scipy.stats import norm
from datetime import datetime
import time
import matplotlib.pyplot as plt

#========================== Key Functions =========================
# black_scholes function / ##Problem 5 requirement##
def black_scholes(S, K, T, r, sigma, option_type):

    if T <= 0:
        return max(S-K,0) if option_type=="call" else max(K-S,0)

    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    if option_type == "call":
        return S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    else:
        return K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)

# time to maturity calculation
def time_to_maturity(expiration, current_time):

    exp = datetime.strptime(expiration, "%Y-%m-%d")
    delta = exp - current_time
    return max(delta.days/365, 1e-8)

# Mid-price function
def mid_price(row):
    return (row["bid"] + row["ask"]) / 2

# implied vol calculation function
def implied_vol_bisection(S, K, T, r, market_price, option_type):
    tol = 1e-6
    max_iter = 100
    lower = 1e-6
    upper = 5.0
    for i in range(max_iter):
        mid = (lower + upper) / 2
        price = black_scholes(S, K, T, r, mid, option_type)
        diff = price - market_price
        if abs(diff) < tol:
            return mid
        price_low = black_scholes(S, K, T, r, lower, option_type)
        if (price_low - market_price) * diff < 0:
            upper = mid
        else:
            lower = mid
    return mid

def compute_iv_for_dataframe(df, S, r, current_time):
    iv_list = []
    for _, row in df.iterrows():
        K = row["strike"]
        option_type = row["type"]
        market_price = mid_price(row)
        T = time_to_maturity(row["expiration"], current_time)

        iv = implied_vol_bisection(S, K, T, r, market_price, option_type)
        iv_list.append(iv)
    df["implied_vol"] = iv_list
    return df

# Vega calculation
def vega(S, K, T, r, sigma):
    if T <= 0:
        return 0
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return S * np.sqrt(T) * norm.pdf(d1)

# Newton Methodi
def implied_vol_newton(S, K, T, r, market_price, option_type):
    tol = 1e-6
    max_iter = 100
    sigma = 0.3  # initial guess
    for i in range(max_iter):
        price = black_scholes(S, K, T, r, sigma, option_type)
        diff = price - market_price
        if abs(diff) < tol:
            return sigma
        v = vega(S, K, T, r, sigma)
        if abs(v) < 1e-8:
            break
        sigma = sigma - diff / v
        if sigma <= 0:
            sigma = 1e-6
    return sigma

# Put call parity function for data frame
def check_put_call_parity(df, S, r, current_time):
    results = []
    # separating put/calls and remerging to have both data in one row
    calls = df[df["type"] == "call"]
    puts  = df[df["type"] == "put"]
    merged = pd.merge(calls, puts, on=["strike", "expiration"], suffixes=("_call", "_put"))

    for _, row in merged.iterrows():
        K = row["strike"]
        T = time_to_maturity(row["expiration"], current_time)
        C = (row["bid_call"] + row["ask_call"]) / 2
        P = (row["bid_put"] + row["ask_put"]) / 2

        # Parity equation
        lhs = C - P
        rhs = S - K * np.exp(-r*T)
        diff = lhs - rhs

        results.append({"strike": K,"expiration": row["expiration"],"parity_diff": diff})
    return pd.DataFrame(results)

# gamma calculation function
def greeks_call(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    delta = norm.cdf(d1)
    gamma = norm.pdf(d1) / (S*sigma*np.sqrt(T))
    vega  = S*np.sqrt(T)*norm.pdf(d1)
    return delta, gamma, vega
def delta_fd_call(S, K, T, r, sigma, h=1e-4):
    return (black_scholes(S+h, K, T, r, sigma, "call") - black_scholes(S-h, K, T, r, sigma, "call")) / (2*h)
def gamma_fd_call(S, K, T, r, sigma, h=1e-4):
    return (black_scholes(S+h, K, T, r, sigma, "call") - 2*black_scholes(S, K, T, r, sigma, "call") + black_scholes(S-h, K, T, r, sigma, "call")) / (h**2)
def vega_fd_call(S, K, T, r, sigma, h=1e-4):
    return (black_scholes(S, K, T, r, sigma+h, "call") - black_scholes(S, K, T, r, sigma-h, "call")) / (2*h)
def compare_greeks_call(S, K, T, r, sigma):
    delta_a, gamma_a, vega_a = greeks_call(S, K, T, r, sigma)

    delta_n = delta_fd_call(S, K, T, r, sigma)
    gamma_n = gamma_fd_call(S, K, T, r, sigma)
    vega_n  = vega_fd_call(S, K, T, r, sigma)

    return pd.DataFrame({"Greek": ["Delta","Gamma","Vega"],"Analytic": [delta_a, gamma_a, vega_a],"Finite_Diff": [delta_n, gamma_n, vega_n]})


#========================== Calculations ===========================
# Importing data 1
tsla = pd.read_csv("TSLA_DATA1_options.csv")
spy = pd.read_csv("SPY_DATA1_options.csv")
meta = pd.read_csv("metadata_DATA1.csv")

r = meta["Interest_Rate"].iloc[0]
S_tsla = meta["TSLA_price"].iloc[0]
S_spy = meta["SPY_price"].iloc[0]

# Calculating IV for data1 on the data frame. ##Problem 6 requirement##
current_time = datetime.strptime(meta["Download_Time_ET"].iloc[0].split()[0],"%Y-%m-%d")

tsla_iv = compute_iv_for_dataframe(tsla, S_tsla, r, current_time)
spy_iv = compute_iv_for_dataframe(spy, S_spy, r, current_time)
tsla_iv["moneyness"] = S_tsla / tsla_iv["strike"]
spy_iv["moneyness"] = S_spy / spy_iv["strike"]
tsla_atm_avg = tsla_iv[(tsla_iv["moneyness"] >= 0.95) & (tsla_iv["moneyness"] <= 1.05)]["implied_vol"].mean()
spy_atm_avg = spy_iv[(spy_iv["moneyness"] >= 0.95) & (spy_iv["moneyness"] <= 1.05)]["implied_vol"].mean()

print("TSLA ATM Avg IV:", tsla_atm_avg)
print("SPY ATM Avg IV:", spy_atm_avg)

# comparing processing time for bisection and newton methods. ##Problem 7 requirement##
atm_row = tsla_iv.iloc[(tsla_iv["strike"] - S_tsla).abs().argsort()[:1]]
row = atm_row.iloc[0]
K = row["strike"]
option_type = row["type"]
market_price = mid_price(row)
T = time_to_maturity(row["expiration"], current_time)

# Bisection
start = time.time()
iv_bis = implied_vol_bisection(S_tsla, K, T, r, market_price, option_type)
end = time.time()
bis_time = end - start
# Newton
start = time.time()
iv_new = implied_vol_newton(S_tsla, K, T, r, market_price, option_type)
end = time.time()
new_time = end - start

print("Bisection IV:", iv_bis)
print("Newton IV:", iv_new)
print("Bisection time:", bis_time)
print("Newton time:", new_time)

# Problem 8 requirement, finding average IV grouped by expiration and option types.
tsla_summary = tsla_iv.groupby("expiration")["implied_vol"].mean().reset_index()
spy_summary  = spy_iv.groupby("expiration")["implied_vol"].mean().reset_index()

print("TSLA Maturity IV:")
print(tsla_summary)
print("\nSPY Maturity IV:")
print(spy_summary)

tsla_cp = tsla_iv.groupby(["expiration","type"])["implied_vol"].mean().reset_index()
spy_cp  = spy_iv.groupby(["expiration","type"])["implied_vol"].mean().reset_index()

print("\nTSLA Call vs Put:")
print(tsla_cp)
print("\nSPY Call vs Put:")
print(spy_cp)

VIX = meta["VIX_price"].iloc[0]
print("\nVIX level:", VIX)

#Problem 9 requirement, put call parity
tsla_parity = check_put_call_parity(tsla, S_tsla, r, current_time)
spy_parity  = check_put_call_parity(spy, S_spy, r, current_time)
print("\nTSLA Parity Mean Diff:", tsla_parity["parity_diff"].mean())
print("SPY Parity Mean Diff:", spy_parity["parity_diff"].mean())

#Problem 10 requirement, IV smile plot
plt.figure(figsize=(8,6))
for exp in tsla_iv["expiration"].unique():
    subset = tsla_iv[tsla_iv["expiration"] == exp]
    plt.scatter(subset["strike"],subset["implied_vol"],label=exp,s=10)

plt.xlabel("Strike")
plt.ylabel("Implied Volatility")
plt.title("TSLA IV Smile")
plt.legend()
plt.show()

plt.figure(figsize=(8,6))
for exp in spy_iv["expiration"].unique():
    subset = spy_iv[spy_iv["expiration"] == exp]
    plt.scatter(subset["strike"],subset["implied_vol"],label=exp, s=15)

plt.xlabel("Strike")
plt.ylabel("Implied Volatility")
plt.title("SPY IV Smile")
plt.legend()
plt.show()

#Problem 11 requirement, Greeks
atm_call = tsla_iv[(tsla_iv["type"]=="call")].iloc[(tsla_iv["strike"] - S_tsla).abs().argsort()[:1]].iloc[0]
K = atm_call["strike"]
sigma = atm_call["implied_vol"]
T = time_to_maturity(atm_call["expiration"], current_time)
comparison_table = compare_greeks_call(S_tsla, K, T, r, sigma)
print("\n", comparison_table)

#Problem 12, calculation with data2
tsla2 = pd.read_csv("TSLA_DATA2_options.csv")
spy2  = pd.read_csv("SPY_DATA2_options.csv")
meta2 = pd.read_csv("metadata_DATA2.csv")
S_tsla_2 = meta2["TSLA_price"].iloc[0]
S_spy_2  = meta2["SPY_price"].iloc[0]
current_time_2 = datetime.strptime(meta2["Download_Time_ET"].iloc[0].split()[0],"%Y-%m-%d")

r2 = meta2["Interest_Rate"].iloc[0]
merged = pd.merge(tsla_iv[["strike", "expiration", "type", "implied_vol"]],tsla2,on=["strike", "expiration", "type"],suffixes=("_data1", "_data2"))
theoretical_prices = []
market_prices = []

for _, row in merged.iterrows():
    K = row["strike"]
    sigma = row["implied_vol"]
    option_type = row["type"]
    T = time_to_maturity(row["expiration"], current_time_2)
    price = black_scholes(S_tsla_2, K, T, r2, sigma, option_type)
    theoretical_prices.append(price)
merged["theoretical_price"] = theoretical_prices
merged["market_price"] = (merged["bid"] + merged["ask"]) / 2
merged["pricing_error"] = merged["theoretical_price"] - merged["market_price"]

print("\n",merged[["strike","expiration","type","theoretical_price","market_price","pricing_error"]].head())