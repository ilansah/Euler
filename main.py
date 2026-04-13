import math
import matplotlib.pyplot as plt
from typing import Callable

# Question 1
g = 9.8
l = 1.0

# Question 2
def subdiv_reg(a, b, n):
    h = (b - a) / n
    return [a + i * h for i in range(n + 1)]


# Question 3
def int_rectangle(f, subdiv):
    somme = 0.0
    for i in range(len(subdiv) - 1):
        h = subdiv[i+1] - subdiv[i]
        somme += f(subdiv[i]) * h
    return somme

# Question 4
def int_trapeze(f, subdiv):
    somme = 0.0
    for i in range(len(subdiv) - 1):
        h = subdiv[i+1] - subdiv[i]
        somme += (f(subdiv[i]) + f(subdiv[i+1])) / 2 * h
    return somme


# Question 5
def f_q5(x):
    return math.sqrt(1 - x**2)

print("Question 5 :")
I_exact = math.pi / 4
for n in [100, 1000, 10000]:
    sub = subdiv_reg(0, 1, n)
    err_rect = abs(int_rectangle(f_q5, sub) - I_exact)
    err_trap = abs(int_trapeze(f_q5, sub) - I_exact)
    print(f"n={n} | Err Rectangle: {err_rect:.6f} | Err Trapèze: {err_trap:.6f}")


# Question 6
def periode(theta_max):
    def f_periode(theta):
        return 1.0 / math.sqrt(math.cos(theta) - math.cos(theta_max))
    
    # On s'arrête un peu avant theta_max pour éviter la division par zéro à la borne
    sub = subdiv_reg(0, theta_max - 1e-5, 5000)
    
    # La méthode des trapèzes est déconseillée car elle nous forcerait 
    # à calculer f(theta_max) ce qui déclencherait une division par zéro.
    return 2 * math.sqrt(2 * l / g) * int_rectangle(f_periode, sub)


# Question 7
def trace_periode():
    thetas = subdiv_reg(0.1, 3.14, 500)
    T = [periode(t) for t in thetas]
    
    plt.plot(thetas, T)
    plt.xlabel("Theta max (rad)")
    plt.ylabel("Période T (s)")
    plt.title("Évolution de la période en fonction de l'angle initial")
    plt.show()

# trace_periode()


# Question 8
def methode_Euler(x0: float, y0: float, xN: float, N: int, g: Callable[[float, float], float]) -> list:
    h = (xN - x0) / N
    x = x0
    y = y0
    y_vals = [y0]
    
    for _ in range(N):
        y = y + h * g(x, y)
        x = x + h
        y_vals.append(y)
        
    return y_vals


# Question 9
def f_exp(x, y):
    return y

x_vals_exp = subdiv_reg(0, 5, 100)
y_vals_exp = methode_Euler(0, 1, 5, 100, f_exp)

# plt.plot(x_vals_exp, y_vals_exp)
# plt.title("Graphe de la fonction exponentielle (Euler)")
# plt.show()


# Question 10
# L'approche d'Euler d'ordre 1 ne marche pas directement pour la position de la masse
# car l'équation du pendule est une équation différentielle d'ordre 2.


# Question 11
def methode_Euler_2(x0: float, y0: float, yp0: float, xN: float, N: int, g: Callable[[float, float, float], float]) -> list:
    h = (xN - x0) / N
    x = x0
    y = y0
    yp = yp0
    y_vals = [y0]
    
    for _ in range(N):
        yp_new = yp + h * g(x, y, yp)
        y_new = y + h * yp
        y = y_new
        yp = yp_new
        x = x + h
        y_vals.append(y)
        
    return y_vals


# Question 12
def f_pendule(x, y, yp):
    return -(g / l) * math.sin(y)

t_vals = subdiv_reg(0, 10, 1000)
theta_vals = methode_Euler_2(0, 1.0, 0, 10, 1000, f_pendule)

# plt.plot(t_vals, theta_vals)
# plt.title("Mouvement du pendule simple (Euler ordre 2)")
# plt.xlabel("Temps (s)")
# plt.ylabel("Theta (rad)")
# plt.show()
