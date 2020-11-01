from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt

def d_zombie(t, y, b, m, alpha, z, k):
    """
    S: susceptible population
    Z: zombie population
    U: undead population
    D: dead population
    b: babies per individual per year
    m: probability of death per year
    alpha: infection probability in an encounter
    z: zombification probability
    k: probability that a zombie is killed by a human
    """
    S, Z, U, D = y
    result = [
        (b - m - alpha*Z)*S,
        z*U - k*S*Z,
        alpha*S*Z - z*U,
        (k*Z+m)*S
    ]
    return result


def plot_it(solution):
	plt.plot(solution.t, solution.y.T)
	plt.xlabel('t')
	plt.legend(['Susceptibles', 'Zombies', 'Undead','Dead'], shadow=True, loc='upper right')
	plt.title('Population Changes Over Time')
	plt.show()