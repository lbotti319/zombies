def zombie_human_behavior(t, y, *args):
    """
    t: time
    y: Population values
        S: susceptible population
        Z: zombie population
        E: exposed population
        Q: quarantined population
        D: dead population
        L: accumulated socio-economic losses due to murder 
        x_S: proportion of susceptibles who support killing when q_max is reached
        x_E: proportion of exposed who are willing to reveal they are bitten
    args: model parameters
        alpha: infection probability in encounter
        b: natural birth rate per individual per year
        m: natural probability of death per individual per year
        z: zombification probability once exposed
        r: recovery probability
        k: probability that a zombie is killed by a human
        q_max: maximum quarentine capacity 
        x_S: proportion of susceptibles who support killing when q_max is reached
        x_E: proportion of exposed who are willing to reveal they are bitten
        C: proportion of exposed willing to reveal depending on q_max and x_S
        eps_S: sensitivity to socioeconomic losses
        eps_E: sensitivity to societal pressure revealing exposure
        mu: decay rate for socio-economic losses  
    """

    S, Z, E, Q, D, x_S, x_E, L = y
    alpha, b, m, z, r, k, q_max, C, eps_S, eps_E, mu = args
    
    
    if Q >= q_max and x_S >= 0.5: 
        C = C
    else: 
        C = 0
    
   
    if Q < q_max:   # if there is enough room for exposed in quarentine
        dE = alpha*S*Z - z*E - r*E - E*(C + x_E) - C*E
        dQ = E*(C + x_E) - r*Q - z*Q
        dx_E = k*x_E*(1 - x_E) * ((z - r)*(E + Q) - eps_E)
    elif Q >= q_max:
        dE = alpha*S*Z - z*E - r*E - C*E
        dQ = r*Q - z*Q
        dx_E = 0

    dS = b*S - m*S - alpha*S*Z + r*(Q+E)
    dZ = z*E - k*S*Z
    dD = k*S*Z + m*S + z*Q + C*E
    dx_S = k*x_S * (1 - x_S) * (Z + Q - eps_S*L)
    dL = alpha*C - mu*L 

    return [dS, dZ, dE, dQ, dD, dx_S, dx_E, dL]
