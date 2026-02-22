# Part 4 (Bonus) - Double integration using the composite trapezoidal rule
# from Rouah (2013), pp. 118-119
#
# The formula for each sub-rectangle [xi, xi+1] x [yj, yj+1] is:
#   (dx*dy/16) * [ corners + 2*edge_midpoints + 4*center ]

import numpy as np
from tabulate import tabulate


def double_trapezoidal(f, x_lo, x_hi, y_lo, y_hi, dx, dy):
    # number of panels in each direction
    nx = round((x_hi - x_lo) / dx)
    ny = round((y_hi - y_lo) / dy)
    dx = (x_hi - x_lo) / nx
    dy = (y_hi - y_lo) / ny

    xs = np.array([x_lo + i * dx for i in range(nx + 1)])
    ys = np.array([y_lo + j * dy for j in range(ny + 1)])

    total = 0.0
    for i in range(nx):
        for j in range(ny):
            xi = xs[i]
            xi1 = xs[i + 1]
            yj = ys[j]
            yj1 = ys[j + 1]
            xm = (xi + xi1) / 2.0   # midpoint in x
            ym = (yj + yj1) / 2.0   # midpoint in y

            corners = f(xi, yj) + f(xi, yj1) + f(xi1, yj) + f(xi1, yj1)
            edges = 2.0 * (f(xm, yj) + f(xm, yj1) + f(xi, ym) + f(xi1, ym))
            center = 4.0 * f(xm, ym)

            total += (dx * dy / 16.0) * (corners + edges + center)

    return total


def run_bonus():
    print("=" * 78)
    print("PART 4 - BONUS: DOUBLE INTEGRATION")
    print("=" * 78)

    x_lo, x_hi = 0.0, 1.0
    y_lo, y_hi = 0.0, 3.0

    f1 = lambda x, y: x * y
    exact1 = 9.0 / 4.0          # = 2.25

    f2 = lambda x, y: np.exp(x + y)
    exact2 = (np.e - 1) * (np.e**3 - 1)   # ~ 32.7943

    # four (dx, dy) pairs as required by the assignment
    dx_dy_pairs = [
        (0.5, 1.5),
        (0.2, 0.5),
        (0.05, 0.15),
        (0.01, 0.03),
    ]

    rows = []
    for dx, dy in dx_dy_pairs:
        num1 = double_trapezoidal(f1, x_lo, x_hi, y_lo, y_hi, dx, dy)
        num2 = double_trapezoidal(f2, x_lo, x_hi, y_lo, y_hi, dx, dy)
        rows.append({
            "dx": dx,
            "dy": dy,
            "Num_f1": num1,
            "Exact_f1": exact1,
            "Error_f1": abs(num1 - exact1),
            "Num_f2": num2,
            "Exact_f2": exact2,
            "Error_f2": abs(num2 - exact2),
        })

    print(f"\n  Domain: x in [{x_lo}, {x_hi}],  y in [{y_lo}, {y_hi}]")
    print(f"  f1(x,y) = x*y          exact = {exact1}")
    print(f"  f2(x,y) = e^(x+y)      exact = {exact2:.6f}\n")
    print(tabulate(rows, headers="keys", tablefmt="grid", floatfmt=".10f"))

    print(f"\n  With finest grid (dx={dx_dy_pairs[-1][0]}, dy={dx_dy_pairs[-1][1]}):")
    print(f"    f1 error = {rows[-1]['Error_f1']:.2e}")
    print(f"    f2 error = {rows[-1]['Error_f2']:.2e}")
    print()


if __name__ == "__main__":
    run_bonus()
