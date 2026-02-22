import numpy as np

sigma = 0.2
gamma = 0.003
dt = 1 / 365
x_t = 1000.0
y_t = 1000.0
S_t = 1.0

k = x_t * y_t
P_t = y_t / x_t

# Lognormal parameters
mu = np.log(S_t) - 0.5 * sigma**2 * dt
nu = sigma * np.sqrt(dt)

# No-arbitrage boundaries
s_L = P_t * (1 - gamma)
s_U = P_t / (1 - gamma)

# Truncation limits
s_min = 1e-12
s_max = np.exp(mu + 7 * nu)

# Grid sizes
N_low = 30000
N_high = 30000


# Lognormal PDF
def lognormal_pdf(s):
    return (1 / (s * nu * np.sqrt(2 * np.pi))) * np.exp(
        -((np.log(s) - mu) ** 2) / (2 * nu**2)
    )


def Delta_y_case1(s):
    return (1 / (1 - gamma)) * (np.sqrt(k * (1 - gamma) * s) - y_t)


def Delta_x_case2(s):
    return (1 / (1 - gamma)) * (np.sqrt(k * (1 - gamma) / s) - x_t)


def trapz_uniform(fvals, h):
    return h * (0.5 * fvals[0] + np.sum(fvals[1:-1]) + 0.5 * fvals[-1])


s_grid_low = np.linspace(s_min, s_L, N_low + 1)
h2 = s_grid_low[1] - s_grid_low[0]

g2 = gamma * Delta_x_case2(s_grid_low) * s_grid_low * lognormal_pdf(s_grid_low)
I2 = trapz_uniform(g2, h2)


s_grid_high = np.linspace(s_U, s_max, N_high + 1)
h1 = s_grid_high[1] - s_grid_high[0]

g1 = gamma * Delta_y_case1(s_grid_high) * lognormal_pdf(s_grid_high)
I1 = trapz_uniform(g1, h1)


expected_fee = I1 + I2

print("Expected one-day fee revenue ≈", expected_fee)
