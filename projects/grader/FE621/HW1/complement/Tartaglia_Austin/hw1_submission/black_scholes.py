# Black-Scholes pricing formulas (Q5)
# Implemented from scratch -- only using scipy for the normal CDF

import numpy as np
from scipy.stats import norm


def _validate(S, K, T, r, sigma):
    if S <= 0:
        raise ValueError(f"S must be > 0, got {S}")
    if K <= 0:
        raise ValueError(f"K must be > 0, got {K}")
    if T <= 0:
        raise ValueError(f"T must be > 0, got {T}")
    if sigma <= 0:
        raise ValueError(f"sigma must be > 0, got {sigma}")


def bs_d1(S, K, T, r, sigma):
    _validate(S, K, T, r, sigma)
    return (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))


def bs_d2(S, K, T, r, sigma):
    return bs_d1(S, K, T, r, sigma) - sigma * np.sqrt(T)


def bs_call_price(S, K, T, r, sigma):
    # C = S*N(d1) - K*exp(-rT)*N(d2)
    _validate(S, K, T, r, sigma)
    d1 = bs_d1(S, K, T, r, sigma)
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)


def bs_put_price(S, K, T, r, sigma):
    # P = K*exp(-rT)*N(-d2) - S*N(-d1)
    _validate(S, K, T, r, sigma)
    d1 = bs_d1(S, K, T, r, sigma)
    d2 = d1 - sigma * np.sqrt(T)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


def bs_vega(S, K, T, r, sigma):
    # dC/dsigma = S*sqrt(T)*phi(d1) -- needed for Newton's method (Q7)
    _validate(S, K, T, r, sigma)
    d1 = bs_d1(S, K, T, r, sigma)
    return S * np.sqrt(T) * norm.pdf(d1)


if __name__ == "__main__":
    # quick sanity check against textbook values
    c = bs_call_price(100, 100, 1.0, 0.05, 0.2)
    p = bs_put_price(100, 100, 1.0, 0.05, 0.2)
    print(f"BS Call = {c:.4f}  (expect ~10.4506)")
    print(f"BS Put  = {p:.4f}  (expect ~ 5.5735)")
    print(f"Vega    = {bs_vega(100, 100, 1.0, 0.05, 0.2):.4f}")
