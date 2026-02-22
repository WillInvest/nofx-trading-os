def derivative(f, x, dx=1e-5):
    return (f(x + dx) - f(x - dx)) / (2.0 * dx)


def newton_step(f, x, dx=1e-5):
    dfx = derivative(f, x, dx=dx)
    if dfx == 0 or dfx != dfx:
        return None
    return x - f(x) / dfx


def newton(f, x0, tol=1e-6, max_iter=50, dx=1e-5):
    x = float(x0)
    for _ in range(max_iter):
        fx = f(x)
        if abs(fx) < tol:
            return x

        x_next = newton_step(f, x, dx=dx)
        if x_next is None or x_next != x_next:
            return None

        if abs(x_next - x) < tol:
            return x_next

        x = x_next

    return None
