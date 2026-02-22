# Root-finding methods for implied volatility (Q6, Q7)
# Each method returns (root, iterations, elapsed_time)

import time


def bisection(f, a, b, tol=1e-6, max_iter=1000):
    # standard bisection -- needs f(a) and f(b) to have opposite signs
    start = time.time()
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError(
            f"f(a)={fa:.6g} and f(b)={fb:.6g} have same sign; "
            "bisection needs a sign change on [a, b]."
        )
    for i in range(1, max_iter + 1):
        mid = (a + b) / 2.0
        fm = f(mid)
        if abs(fm) < tol or (b - a) / 2.0 < tol:
            return mid, i, time.time() - start
        if fa * fm < 0:
            b = mid
            fb = fm
        else:
            a = mid
            fa = fm
    return (a + b) / 2.0, max_iter, time.time() - start


def newton(f, f_prime, x0, tol=1e-6, max_iter=1000):
    # Newton's method -- requires derivative f_prime (vega for IV)
    start = time.time()
    x = x0
    for i in range(1, max_iter + 1):
        fx = f(x)
        fpx = f_prime(x)
        if abs(fpx) < 1e-14:
            return x, i, time.time() - start
        x_new = x - fx / fpx
        if abs(x_new - x) < tol:
            return x_new, i, time.time() - start
        x = x_new
    return x, max_iter, time.time() - start


def secant(f, x0, x1, tol=1e-6, max_iter=1000):
    # secant method -- like Newton but approximates derivative from two points
    start = time.time()
    f0 = f(x0)
    for i in range(1, max_iter + 1):
        f1 = f(x1)
        if abs(f1 - f0) < 1e-14:
            return x1, i, time.time() - start
        x_new = x1 - f1 * (x1 - x0) / (f1 - f0)
        if abs(x_new - x1) < tol:
            return x_new, i, time.time() - start
        x0, f0 = x1, f1
        x1 = x_new
    return x1, max_iter, time.time() - start


if __name__ == "__main__":
    # test with f(x) = x^2 - 4, root should be 2
    root_b, iters_b, t_b = bisection(lambda x: x**2 - 4, 0, 5)
    root_n, iters_n, t_n = newton(lambda x: x**2 - 4, lambda x: 2*x, 3.0)
    root_s, iters_s, t_s = secant(lambda x: x**2 - 4, 0, 5)
    print(f"Bisection: root={root_b:.8f}, iters={iters_b}, time={t_b:.6f}s")
    print(f"Newton:    root={root_n:.8f}, iters={iters_n}, time={t_n:.6f}s")
    print(f"Secant:    root={root_s:.8f}, iters={iters_s}, time={t_s:.6f}s")
