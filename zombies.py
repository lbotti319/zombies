from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt

def d_zombie(t, y, alpha, b, m, z, r, k):
    """
    Population Variables:
        S: susceptible population
        Z: zombie population
        U: undead population
        D: dead population
    Model Parameters:
	    alpha: infection probability in an encounter
        b: natural birth rate per individual per year
        m: probability of death per year
        z: zombification probability
        r: recovery probability
        k: probability that a zombie is killed by a human
    """
    S, Z, U, D = y
    result = [
        (b - m - alpha*Z)*S + r*U, #dS
        z*U - k*S*Z,    #dZ
        alpha*S*Z - z*U - r*U,  #dU
        (k*Z+m)*S   #dD
    ]
    return result


def plot_it(solution):
    plt.plot(solution.t, solution.y.T[:,:3])
    plt.xlabel('t')
    plt.legend(['Susceptibles', 'Zombies', 'Undead'], shadow=True, loc='upper right')
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
    

def zombie_human_behavior(t, y, *args):
    """
    t: time
    y: Population values
        S: susceptible population
        Z: zombie population
        E: exposed population
        Q: quarantined population
        D: dead population
        x_S: proportion of susceptibles who support murder when q_max is reached
        x_E: proportion of exposed who are willing to reveal they are bitten
        L: accumulated socio-economic losses due to murder 
    args: model parameters
        alpha: infection probability in encounter
        b: natural birth rate per individual per year
        m: natural probability of death per individual per year
        z: zombification probability once exposed
        r: recovery probability
        k: probability that a zombie is killed by a human
        q_max: maximum quarentine capacity 
        C_0: Proportion of exposed that are found to be exposed by the rest of the population
        eps_S: sensitivity to socioeconomic losses
        eps_E: sensitivity to societal pressure revealing exposure
        mu: decay rate for socio-economic losses
        l_S: murder impact rate on socio-psych-economic health
        k_S: Learning rate of the susceptible population
        k_E: Learning rate of the exposed population
    """

    S, Z, E, Q, D, x_S, x_E, L = y
    alpha, b, m, z, r, k, q_max, C_0, eps_S, eps_E, mu, l_S, k_S, k_E = args
    
    
    if Q >= q_max and x_S >= 0.5: 
        C = C_0
    else: 
        C = 0
    

   

    if Q < q_max:   # if there is enough room for exposed in quarentine
        dE = alpha*S*Z - z*E - r*E - E*(C_0 + x_E) - C*E
        dQ = E*(C_0 + x_E) - r*Q - z*Q
        
    else:
        dE = alpha*S*Z - z*E - r*E - C*E
        dQ = -r*Q - z*Q

    dS = b*S - m*S - alpha*S*Z + r*(Q+E)
    dZ = z*E - k*S*Z
    dD = k*S*Z + m*S + z*Q + C*E
    dx_S = k_S*x_S * (1 - x_S) * (Z + Q - eps_S*L)
    # The feelings towards self quarantine don't change even if it is unavailable
    dx_E = k_E*x_E*(1 - x_E) * ((z - r)*(E + Q) - eps_E)
    dL = l_S*C - mu*L 

    return [dS, dZ, dE, dQ, dD, dx_S, dx_E, dL]
