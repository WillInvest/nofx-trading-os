# Part 3 - AMM Fee Revenue for a CPMM (BTC/USDC pool)
# Derives swap amounts under arbitrage, computes expected fee revenue
# via trapezoidal integration over lognormal density, and finds optimal gamma

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import lognorm
from tabulate import tabulate

import config


def fee_revenue(S_next, x_t, y_t, gamma_fee):
    # one-step fee revenue R(S_{t+1}) given pool state and fee rate
    k = x_t * y_t
    P_t = y_t / x_t
    upper = P_t / (1 - gamma_fee)   # top of no-arb band
    lower = P_t * (1 - gamma_fee)   # bottom of no-arb band

    if S_next > upper:
        # Case 1: BTC cheaper in pool, arbers swap USDC -> BTC
        x_new = np.sqrt(k / (S_next * (1 - gamma_fee)))
        y_new = np.sqrt(k * S_next * (1 - gamma_fee))
        delta_y = (y_new - y_t) / (1 - gamma_fee)
        return gamma_fee * delta_y

    elif S_next < lower:
        # Case 2: BTC cheaper outside, arbers swap BTC -> USDC
        x_new = np.sqrt(k * (1 - gamma_fee) / S_next)
        delta_x = (x_new - x_t) / (1 - gamma_fee)
        return gamma_fee * delta_x * S_next

    else:
        # inside no-arb band, no trade happens
        return 0.0


def fee_revenue_vectorized(S_arr, x_t, y_t, gamma_fee):
    # vectorized version for integration over a grid of S values
    k = x_t * y_t
    P_t = y_t / x_t
    upper = P_t / (1 - gamma_fee)
    lower = P_t * (1 - gamma_fee)

    R = np.zeros_like(S_arr, dtype=float)

    # Case 1
    mask1 = S_arr > upper
    S1 = S_arr[mask1]
    x_new1 = np.sqrt(k / (S1 * (1 - gamma_fee)))
    y_new1 = np.sqrt(k * S1 * (1 - gamma_fee))
    delta_y1 = (y_new1 - y_t) / (1 - gamma_fee)
    R[mask1] = gamma_fee * delta_y1

    # Case 2
    mask2 = S_arr < lower
    S2 = S_arr[mask2]
    x_new2 = np.sqrt(k * (1 - gamma_fee) / S2)
    delta_x2 = (x_new2 - x_t) / (1 - gamma_fee)
    R[mask2] = gamma_fee * delta_x2 * S2

    return R


def trapezoidal(f, a, b, n):
    # composite trapezoidal rule for 1D integration
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    return h * (0.5 * y[0] + np.sum(y[1:-1]) + 0.5 * y[-1])


def lognormal_pdf(s, S_t, sigma, dt):
    # density of S_{t+1} under GBM: S_{t+1} = S_t * exp(-0.5*sigma^2*dt + sigma*sqrt(dt)*Z)
    mu_ln = np.log(S_t) - 0.5 * sigma**2 * dt
    sigma_ln = sigma * np.sqrt(dt)
    return lognorm.pdf(s, s=sigma_ln, scale=np.exp(mu_ln))


def expected_fee_revenue(x_t, y_t, gamma_fee, sigma, dt=1/365,
                         n_grid=20000):
    # E[R] = integral of R(s) * f(s) ds using trapezoidal rule
    S_t = y_t / x_t

    sigma_ln = sigma * np.sqrt(dt)
    mu_ln = np.log(S_t) - 0.5 * sigma**2 * dt
    lower_bound = max(1e-10, np.exp(mu_ln - 6 * sigma_ln))
    upper_bound = np.exp(mu_ln + 6 * sigma_ln)

    def integrand(s):
        R = fee_revenue_vectorized(s, x_t, y_t, gamma_fee)
        f = lognormal_pdf(s, S_t, sigma, dt)
        return R * f

    return trapezoidal(integrand, lower_bound, upper_bound, n_grid)


def compute_fee_table(sigmas, gammas, x_t=1000, y_t=1000, dt=1/365):
    # build the sigma x gamma table of E[R] values
    data = {}
    for g in gammas:
        col = []
        for s in sigmas:
            er = expected_fee_revenue(x_t, y_t, g, s, dt)
            col.append(er)
        data[f"gamma={g}"] = col
    df = pd.DataFrame(data, index=[f"sigma={s}" for s in sigmas])
    return df


def optimal_gamma(sigma_grid, gamma_candidates, x_t=1000, y_t=1000,
                   dt=1/365):
    # for each sigma, find the gamma that maximizes E[R]
    gamma_star = []
    for s in sigma_grid:
        best_g, best_er = None, -np.inf
        for g in gamma_candidates:
            er = expected_fee_revenue(x_t, y_t, g, s, dt)
            if er > best_er:
                best_er = er
                best_g = g
        gamma_star.append(best_g)
    return np.array(gamma_star)


def run_amm(output_dir=config.OUTPUT_DIR):
    print("=" * 78)
    print("PART 3 - AMM FEE REVENUE (CPMM)")
    print("=" * 78)

    os.makedirs(output_dir, exist_ok=True)

    x_t, y_t = 1000, 1000
    P = y_t / x_t
    gamma_fee = 0.003

    # Part (a): show fee revenue for a few example prices
    print(f"\n  (a) Fee revenue examples:")
    print(f"      Pool: x_t={x_t}, y_t={y_t}, P_t={P}, gamma={gamma_fee}")
    for S_next in [1.05, 1.02, 1.00, 0.98, 0.95]:
        R = fee_revenue(S_next, x_t, y_t, gamma_fee)
        print(f"      S_next={S_next:.2f}  ->  R = {R:.6f} USDC")

    # Part (b): expected fee revenue
    print(f"\n  (b) Expected fee revenue (sigma=0.2, gamma=0.003):")
    er = expected_fee_revenue(x_t, y_t, 0.003, 0.2)
    print(f"      E[R] = {er:.8f} USDC")

    # Part (c): table and optimal gamma
    sigmas_coarse = [0.2, 0.6, 1.0]
    gammas_coarse = [0.001, 0.003, 0.01]

    print(f"\n  (c) E[R] table (3 x 3):")
    table = compute_fee_table(sigmas_coarse, gammas_coarse)
    print(tabulate(table, headers="keys", tablefmt="grid", floatfmt=".8f"))
    table.to_csv(os.path.join(output_dir, "amm_fee_table.csv"))

    for s in sigmas_coarse:
        row = table.loc[f"sigma={s}"]
        best_col = row.idxmax()
        print(f"      sigma={s}: gamma* = {best_col}  (E[R] = {row[best_col]:.8f})")

    # fine grid: gamma*(sigma) for sigma in [0.1, 1.0]
    print(f"\n  Plotting gamma*(sigma) over sigma in [0.1, 1.0] ...")
    sigma_fine = np.arange(0.1, 1.01, 0.01)
    gamma_candidates = np.arange(0.001, 0.051, 0.001)
    g_star = optimal_gamma(sigma_fine, gamma_candidates)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(sigma_fine, g_star, "o-", markersize=3)
    ax.set_xlabel("sigma (Volatility)")
    ax.set_ylabel("gamma* (Optimal Fee Rate)")
    ax.set_title("Optimal Fee Rate gamma*(sigma) for CPMM")
    ax.grid(True, alpha=0.3)
    path = os.path.join(output_dir, "amm_optimal_gamma.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  -> {path}\n")


if __name__ == "__main__":
    run_amm()
