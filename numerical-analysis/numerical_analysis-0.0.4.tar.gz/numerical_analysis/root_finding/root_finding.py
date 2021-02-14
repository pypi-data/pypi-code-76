def bisection(f, x0, x1, error=1e-15):
    if f(x0) * f(x1) > 0:
        print("No root found.")
    else:
        while True:
            mid = 0.5 * (x0 + x1)
            if abs(f(mid)) < error:
                return mid
            elif f(x0) * f(mid) > 0:
                x0 = mid
            else:
                x1 = mid

def secant(f, x0, x1, error=1e-15):
    fx0 = f(x0)
    fx1 = f(x1)
    while abs(fx1) > error:
        x2 = (x0 * fx1 - x1 * fx0) / (fx1 - fx0)
        x0, x1 = x1, x2
        fx0, fx1 = fx1, f(x2)
    return x1

def newton_raphson(f, df_dx, x0, error=1e-15):
    while abs(f(x0)) > error:
        x0 -= f(x0) / df_dx(x0)
    return x0

def newton_raphson_multiple_roots(f, df_dx, n, error=1e-15):

    def sigma(x):
        nonlocal roots
        s = 0
        for root in roots:
            s += 1 / (x - root)
        return s

    def nr_step(xold):
        nonlocal xk_old
        return xold - f(xold) / (df_dx(xold) - f(xold) * sigma(xold))

    roots = []

    for i in range(n):

        xk_old = 2
        xk_new = nr_step(xk_old)
        ek = xk_new - xk_old
        xk_old = xk_new

        while abs(ek) > error:
            xk_new = nr_step(xk_old)
            ek = xk_new - xk_old
            xk_old = xk_new

        roots.append(xk_new)

    return sorted(roots)
