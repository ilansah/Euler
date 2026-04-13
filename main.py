import math
import matplotlib.pyplot as plt

g = 9.81
l = 1.0


# Q2
def subdiv_reg(a, b, n):
    return [a + i * (b - a) / n for i in range(n + 1)]


# Q3
def int_rectangle(f, subdiv):
    somme = 0
    for i in range(len(subdiv) - 1):
        h = subdiv[i+1] - subdiv[i]
        somme += f(subdiv[i]) * h
    return somme


# Q4
def int_trapeze(f, subdiv):
    somme = 0
    for i in range(len(subdiv) - 1):
        h = subdiv[i+1] - subdiv[i]
        somme += (f(subdiv[i]) + f(subdiv[i+1])) / 2 * h
    return somme


# Q5
def verif_methodes():
    f = lambda x: math.sqrt(1 - x**2)
    val = math.pi / 4
    print(f"{'n':>7} | {'Err Rectangle':>15} | {'Err Trapeze':>15}")
    print("-" * 45)
    for n in [100, 1000, 10000]:
        sub = subdiv_reg(0, 1, n)
        er = abs(int_rectangle(f, sub) - val)
        et = abs(int_trapeze(f, sub) - val)
        print(f"{n:7d} | {er:15.8e} | {et:15.8e}")


# Q6
def periode(theta_max):
    def integrand(theta):
        d = math.cos(theta) - math.cos(theta_max)
        if d <= 0:
            return 0
        return 1 / math.sqrt(d)
    sub = subdiv_reg(0, theta_max - 1e-7, 10000)
    return 2 * math.sqrt(2 * l / g) * int_rectangle(integrand, sub)


# Q7
def trace_periode():
    thetas = subdiv_reg(0.1, 3.14, 500)
    T0 = 2 * math.pi * math.sqrt(l / g)
    plt.figure()
    plt.plot(thetas, [periode(t) for t in thetas], label="T(theta_max)")
    plt.axhline(y=T0, color='r', linestyle='--', label="T0")
    plt.xlabel("theta_max (rad)")
    plt.ylabel("Periode T (s)")
    plt.title("Periode du pendule en fonction de l'amplitude")
    plt.legend()
    plt.grid(True)
    plt.show()


# Q8
def methode_Euler(x0, y0, xN, N, f):
    h = (xN - x0) / N
    xs = [x0]
    ys = [y0]
    for _ in range(N):
        ys.append(ys[-1] + h * f(xs[-1], ys[-1]))
        xs.append(xs[-1] + h)
    return xs, ys


# Q9
def trace_exp():
    xs, ys = methode_Euler(0, 1, 2, 100, lambda x, y: y)
    xs_ex = subdiv_reg(0, 2, 200)
    plt.figure()
    plt.plot(xs, ys, label="Euler")
    plt.plot(xs_ex, [math.exp(x) for x in xs_ex], '--', label="exp(x)")
    plt.title("y' = y, y(0) = 1")
    plt.legend()
    plt.grid(True)
    plt.show()


# Q10
# Euler ordre 1 n'est pas adapté au pendule : l'énergie dérive à chaque pas,
# l'amplitude augmente artificiellement. Il faut Euler ordre 2.


# Q11
def methode_Euler_2(x0, y0, yp0, xN, N, f):
    h = (xN - x0) / N
    xs = [x0]
    ys = [y0]
    yps = [yp0]
    for _ in range(N):
        y_new = ys[-1] + h * yps[-1]
        yp_new = yps[-1] + h * f(xs[-1], ys[-1], yps[-1])
        xs.append(xs[-1] + h)
        ys.append(y_new)
        yps.append(yp_new)
    return xs, ys, yps


# Q12
def simulation_pendule():
    theta_max = math.pi / 4
    f = lambda t, th, thp: -(g / l) * math.sin(th)
    T = periode(theta_max)
    xs, ys, _ = methode_Euler_2(0, theta_max, 0, 3 * T, 3000, f)
    plt.figure()
    plt.plot(xs, ys)
    plt.title(f"Pendule - theta_max = {theta_max:.2f} rad, T = {T:.4f} s")
    plt.xlabel("t (s)")
    plt.ylabel("theta (rad)")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    verif_methodes()
    trace_periode()
    trace_exp()
    simulation_pendule()