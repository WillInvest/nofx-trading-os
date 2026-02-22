import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

x_t = 1000.0
y_t = 1000.0
k = x_t * y_t
P_t = y_t / x_t

S_t = 1.0
dt = 1.0 / 365.0

EPS = 1e-12
M_SIGMA = 7.0
N_LOW = 30000
N_HIGH = 30000

GAMMAS = [0.001, 0.003, 0.01]


def lognormal_pdf(s, mu, nu):
    return (1 / (s * nu * np.sqrt(2 * np.pi))) * np.exp(
        -((np.log(s) - mu) ** 2) / (2 * nu**2)
    )


def trapz_uniform(fvals, h):
    return h * (0.5 * fvals[0] + np.sum(fvals[1:-1]) + 0.5 * fvals[-1])


def expected_fee_one_step(sigma, gamma):
    mu = np.log(S_t) - 0.5 * sigma**2 * dt
    nu = sigma * np.sqrt(dt)

    s_L = P_t * (1 - gamma)
    s_U = P_t / (1 - gamma)
    s_max = np.exp(mu + M_SIGMA * nu)

    s_grid_low = np.linspace(EPS, s_L, N_LOW + 1)
    h2 = s_grid_low[1] - s_grid_low[0]

    Delta_x = (1 / (1 - gamma)) * (np.sqrt(k * (1 - gamma) / s_grid_low) - x_t)
    g2 = gamma * Delta_x * s_grid_low * lognormal_pdf(s_grid_low, mu, nu)
    I2 = trapz_uniform(g2, h2)

    s_grid_high = np.linspace(s_U, s_max, N_HIGH + 1)
    h1 = s_grid_high[1] - s_grid_high[0]

    Delta_y = (1 / (1 - gamma)) * (np.sqrt(k * (1 - gamma) * s_grid_high) - y_t)
    g1 = gamma * Delta_y * lognormal_pdf(s_grid_high, mu, nu)
    I1 = trapz_uniform(g1, h1)

    return I1 + I2


sigmas_discrete = [0.2, 0.6, 1.0]

rows = []
for sig in sigmas_discrete:
    for gam in GAMMAS:
        er = expected_fee_one_step(sig, gam)
        rows.append({"sigma": sig, "gamma": gam, "E[R]": er})

df = pd.DataFrame(rows)

pivot = df.pivot(index="sigma", columns="gamma", values="E[R]").reset_index()
pivot.columns.name = None

print("\nE[R] table (rows=sigma, cols=gamma):")
print(pivot.to_string(index=False))

sigma_grid = np.arange(0.1, 1.01, 0.01)
gamma_star_list = []

for sig in sigma_grid:
    ERs = [expected_fee_one_step(sig, gam) for gam in GAMMAS]
    gamma_star_list.append(GAMMAS[np.argmax(ERs)])

# Plot σ vs γ*(σ)
plt.figure(figsize=(6, 4))
plt.plot(sigma_grid, gamma_star_list, marker="o", linestyle="None")
plt.xlabel(r"$\sigma$")
plt.ylabel(r"$\gamma^*(\sigma)$")
plt.title("Optimal fee rate vs volatility")
plt.grid(True)
plt.show()
