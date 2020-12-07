from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt

def d_zombie(t, y, b, m, alpha, z, k):
    """
    Population Variables:
        S: susceptible population
        Z: zombie population
        U: undead population
        D: dead population
    Model Parameters:
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


def corona_basic(t, y, *args):
    """
    t: time
    y: Population values
        S: Susceptible
        E: Exposed
        A: Asymptomatic infected
        I: Symptomatic infected
        Q: Quarantined
        H: Hospitalized
        R: Removed (Dead/Recovered)
    args: model parameters
        beta: Infection Rate
        eta_A, eta_Q, eta_H: Asymptomatic, Quarantined, Hospitalized infection rates
        sigma: Disease progression rate from exposed to infections
        q: Proportion of exposed developing asymptomatic infections
        g_A, g_I, g_Q, g_H: Recover rates of symptomatic, asympotmatic, quarantined, and hospitalized people
        w_Q, w_H: Quarantine and Hospitalization rates
        v_Q: Quarantine violation rate
        v_H: Hospitalization discharge rate
        d_I, d_A, d_Q, d_H: Death rates of symptomatic, asymptomatic, quarantined, and hospitalized individuals
        
    """
    S, E, A, I, Q, H, R = y
    beta, eta_A, eta_Q, eta_H, sigma, q, g_A, g_I, g_Q, g_H, w_Q, w_H, v_Q, v_H, d_I, d_A, d_Q, d_H = args
    infection_force = beta* (I + eta_A*A + eta_Q*Q + eta_H*H)
    dS = -1*infection_force*S
    dE = infection_force*S - sigma*E
    dA = q*sigma*E - (g_A + d_A)*A
    dI = (1 - q)*sigma*E + v_Q*Q + v_H*H - (w_Q + w_H + g_I + d_I)*I
    dQ = w_Q*I - (v_Q + g_Q + d_Q)*Q
    dH = w_H*I - (v_H + g_H + d_H)*H
    dR = (g_A + d_A)*A + (g_I + d_I)*I + (g_Q + d_Q)*Q + (g_H + d_H)*H
    return [dS, dE, dA, dI, dQ, dH, dR]


    

def corona_expanded(t, y, *args):
    """
    t: time
    y: Tuple of population values
        S: susceptible
        E: Exposed
        A: Asymptomatic infected
        I: Symptomatic infected
        Q: Quarantined
        H: Hospitalized
        R: Removed (Dead/Recovered)
        x_s: Proportion of susceptible individuals who support closure
        x_I: Proportion of symptomatically infected individuals who self-isolate
        L_s: Accumulated socio-economic losses due to closures
    args: model parameters
        
        
    """
    
    S, E, A, I, Q, H, R, x_s, x_I, L_s= y
