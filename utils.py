import numpy as np
import scipy
from scipy.stats import poisson

default_config = {}

# webster delay model
def delay_webster(y_r,s,L,sigma,is_stochastic=False):
    # is_stochastic: 是否包括随机项
    q_r = s*y_r
    Q = q_r.sum()
    Y = y_r.sum()
    d = L/(2*Q*sigma*(sigma-Y))*(q_r/(1-y_r)*(sigma-y_r)**2).sum()
    if is_stochastic and sigma<1.0:
        d += 4*sigma**2/(2*Q*(1-sigma))
    return d

# point queue model
def point_queue_model(id,phase_sequence,q,sim_length=1800,is_stochastic=False,config=default_config):
    # sim_length: simulation duration in seconds
    step_length = 1.0  # 步长调整未实现
    step_num = np.ceil(sim_length/step_length).astype(int)
    q_record = np.zeros((step_num,4,2))  # 交叉口当前排队
    q_state = np.zeros((4,2))
    for i in range(step_num):
        flag = np.zeros(8)
        p = next(phase_sequence)
        if p[0]>=0 and p[1]>=0:
            flag[p] = 1.0
        # arrival
        if is_stochastic:
            q_state += poisson.rvs(q/3600)
        else:
            q_state += q/3600
        # departure
        q_state -= config['sfr']/3600*flag.reshape((4,2))
        np.place(q_state,q_state<0,0)
        q_record[i] = q_state[:]
    np.save(f'./exp1/{id}.npy',q_record)