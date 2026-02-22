from math import exp, log, sqrt

from scipy.stats import norm


def d1(S, K, T, r, sigma):
    return (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))


def d2(S, K, T, r, sigma):
    return d1(S, K, T, r, sigma) - sigma * sqrt(T)


def bs_call(S, K, T, r, sigma):
    return S * norm.cdf(d1(S, K, T, r, sigma)) - K * exp(-r * T) * norm.cdf(
        d2(S, K, T, r, sigma)
    )


def bs_put(S, K, T, r, sigma):
    d1v = d1(S, K, T, r, sigma)
    d2v = d2(S, K, T, r, sigma)
    return K * exp(-r * T) * norm.cdf(-d2v) - S * norm.cdf(-d1v)
