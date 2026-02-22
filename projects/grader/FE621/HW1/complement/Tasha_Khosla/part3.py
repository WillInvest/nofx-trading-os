from math import sqrt, log, exp, pi
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Given parameters
x_t = 1000.0
y_t = 1000.0
P_t = y_t / x_t
k = x_t * y_t
S_t = 1.0
dt = 1.0 / 365.0


# lognormal density S_(t+1)
def f_S_next(s, sigma):  #
    if s <= 0:
        return 0.0
    mu = log(S_t) + (-0.5 * sigma**2) * dt
    v = sigma**2 * dt
    return (1.0 / (s * sqrt(2.0 * pi * v))) * exp(-((log(s) - mu) ** 2) / (2.0 * v))


def delta_y_case1(s, gamma):
    return (1.0 / (1.0 - gamma)) * (sqrt(k * s * (1.0 - gamma)) - y_t)


def delta_x_case2(s, gamma):
    if s <= 0:
        return 0.0
    return (1.0 / (1.0 - gamma)) * (sqrt(k * (1.0 - gamma) / s) - x_t)


# Trapezoidal rule
def trapezoid_integral(g, a, b, n):
    h = (b - a) / n
    s_prev = a
    total = 0.0
    for i in range(1, n + 1):
        s_i = a + i * h
        total += h * (g(s_prev) + g(s_i)) / 2.0
        s_prev = s_i
    return total


def expected_fee_revenue(sigma=0.2, gamma=0.003, n=1000000, M=2.0, eps=1e-12):
    # use 10^-12 for lower bound of integral because ln(0) does not exist
    # M is an upper bound (200% price level)
    upper = P_t / (1.0 - gamma)  # P_t/(1-gamma)
    lower = P_t * (1.0 - gamma)  # P_t(1-gamma)

    # First integral
    def g1(s):
        return gamma * delta_y_case1(s, gamma) * f_S_next(s, sigma)

    # Second integral
    def g2(s):
        return gamma * delta_x_case2(s, gamma) * s * f_S_next(s, sigma)

    I1 = trapezoid_integral(g1, upper, M, n)
    I2 = trapezoid_integral(g2, eps, lower, n)
    return I1 + I2


if __name__ == "__main__":
    val = expected_fee_revenue(n=1000000, M=5.0)
    print("E[R(S_{t+1})] =", val)

# Part c

sigmas_discrete = [0.2, 0.6, 1.0]
gammas = [0.001, 0.003, 0.01]

n_trapezoidal = 100000
M_limit = 5.0  # to approximate infinity
epsilons = 1e-12  # to fix the 0 problem

# E[R] table
rows = []
for sigma in sigmas_discrete:
    for gamma in gammas:
        ER = expected_fee_revenue(
            sigma=sigma, gamma=gamma, n=n_trapezoidal, M=M_limit, eps=epsilons
        )
        rows.append({"sigma": sigma, "gamma": gamma, "E[R]": ER})

df_ER = pd.DataFrame(rows)

# pivot so each row is sigma and columns are gamma
df_pivot = df_ER.pivot(index="sigma", columns="gamma", values="E[R]")

# argmax over the 3 fee rates
gamma_star = df_pivot.idxmax(axis=1)  # gamma that maximizes E[R] for each sigma
ER_star = df_pivot.max(axis=1)  # max E[R] value

df_summary = df_pivot.copy()
df_summary["gamma_star"] = gamma_star
df_summary["E[R]_max"] = ER_star

print("\nTable: E[R] for each (sigma, gamma) and gamma*(sigma)")
print(df_summary)

# Grid for optimal gamma

sigma_grid = np.round(np.arange(0.10, 1.00 + 0.01, 0.01), 2)

gamma_star_grid = []
ER_star_grid = []

for sigma in sigma_grid:
    ER_vals = []
    for gamma in gammas:
        ER_vals.append(
            expected_fee_revenue(
                sigma=sigma, gamma=gamma, n=n_trapezoidal, M=M_limit, eps=epsilons
            )
        )
    ER_vals = np.array(ER_vals)

    j = int(np.argmax(ER_vals))
    gamma_star_grid.append(gammas[j])
    ER_star_grid.append(float(ER_vals[j]))

df_grid = pd.DataFrame(
    {"sigma": sigma_grid, "gamma_star": gamma_star_grid, "E[R]_max": ER_star_grid}
)

print("\nFirst few rows of sigma-grid results")
print(df_grid.head(10))

# Plot sigma vs gamma star

plt.figure()
plt.plot(df_grid["sigma"], df_grid["gamma_star"], marker="o", linestyle="-")
plt.xlabel("sigma")
plt.ylabel("gamma*(sigma)")
plt.title("Optimal fee rate gamma* vs volatility sigma")
plt.show()
