# webster delay model
def delay_webster(y_r,s,L,sigma,is_stochastic=False):
    q_r = s*y_r
    Q = q_r.sum()
    Y = y_r.sum()
    d = L/(2*Q*sigma*(sigma-Y))*(q_r/(1-y_r)*(sigma-y_r)**2).sum()
    if is_stochastic and sigma<1.0:
        d += 4*sigma**2/(2*Q*(1-sigma))
    return d