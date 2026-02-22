import numpy as np
from scipy import integrate
import pandas as pd
import matplotlib.pyplot as plt

# expected fee calculation using trapezoidal rule
def expected_fee_trap(S0, x0, y0, gamma, sigma=0.2, dt=1/365, n=2000):
    k = x0 * y0
    m = -0.5*sigma**2*dt
    sd = sigma*np.sqrt(dt)

    z = np.linspace(-4, 4, n)

    phi = (1/np.sqrt(2*np.pi))*np.exp(-0.5*z**2)
    S = S0 * np.exp(m + sd*z)
    R_vals = []

    for s in S:
        x1 = np.sqrt(k / ((1-gamma)*s))
        dx = x1 - x0
        R = gamma * abs(dx)
        R_vals.append(R)

    integrand = np.array(R_vals) * phi
    expected = integrate.trapezoid(integrand, z)

    return expected

# running example with expected fee
S0 = 1
x0 = 1000
y0 = 1000
gamma = 0.003

val = expected_fee_trap(S0, x0, y0, gamma)
print("Expected fee:", val)

# (c) requirement
sigmas = [0.2, 0.6, 1.0]
gammas = [0.001, 0.003, 0.01]
results = []

for s in sigmas:
    best_gamma = None
    best_val = -1
    for g in gammas:
        val = expected_fee_trap(S0, x0, y0, g, sigma=s)
        results.append((s, g, val))
        if val > best_val:
            best_val = val
            best_gamma = g
    print(f"Sigma {s}: best gamma = {best_gamma}")

df_results = pd.DataFrame(results, columns=["sigma", "gamma", "E_R"])
print(df_results)

sigma_grid = np.linspace(0.1, 1.0, 20)
gamma_star = []

for s in sigma_grid:
    vals = [expected_fee_trap(S0, x0, y0, g, sigma=s) for g in gammas]
    gamma_star.append(gammas[np.argmax(vals)])

plt.plot(sigma_grid, gamma_star)
plt.xlabel("sigma")
plt.ylabel("gamma")
plt.show()