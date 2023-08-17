import numpy as np
from itertools import cycle

from utils import default_config

def fixed_time_controller(g_time=20.0,config=default_config):
    # fixed-time controller
    if isinstance(g_time,float):
        g = g_time*np.ones(4).astype(int)  # 绿灯时间
    elif isinstance(g_time,np.ndarray):
        g = g_time.astype(int)

    phase_time = np.stack([g+config['yellow']-config['timeloss'],(config['timeloss']+config['red'])*np.ones(4)],axis=0)
    phase_time = phase_time.swapaxes(0,1).reshape(-1).astype(int)  # 相位时间

    phase_sequence = np.repeat(config['phase'],phase_time,axis=0)
    phase_sequence = cycle([phase_sequence[i] for i in range(len(phase_sequence))])
    return phase_sequence

def webster_controller(mode='approximate',config=default_config):
    assert mode in ['approximate','exact']
    
    # webster's (approximation)
    y_r = (q/s).max(axis=-1)  # 对应于单口放行的流量比计算
    Y = y_r.sum()
    L = 4*(t+r)
    if Y > 0.8:
        y_r = y_r/Y*0.8
        Y = 0.8
    
    if mode=='approximate':
        C = (1.5*L+5.0)/(1-Y)
    elif mode=='exact':
        C_max = 50
        C_min = np.ceil(L/(1-Y)).astype(int)
        C_arr = np.arange(C_min,C_max,0.2)
        num_C = len(C_arr)
        sigma_arr = C_arr*Y/(C_arr-L)
        delay_arr = np.zeros(num_C)
        for i,sigma in enumerate(sigma_arr):
            delay_arr[i] = delay_webster(y_r,s,L,sigma,is_stochastic=False)
        C = C_arr[np.argmin(delay_arr)]
    
    g = (C-L)*y_r/Y  # 有效绿灯时间
    g = (g+t-a).astype(int)  # 绿灯时间
    print(g)
    phase_time = np.stack([g+a-t,(t+r)*np.ones(4)],axis=0).swapaxes(0,1).reshape(-1).astype(int)  # 相位时间

    phase_sequence = np.repeat(phase,phase_time,axis=0)
    phase_sequence = cycle([phase_sequence[i] for i in range(len(phase_sequence))])
    
def mpc_controller(config=default_config):
    pass        

def q_learning_controller(config=default_config):
    # Q-learning
    q_value = np.zeros((2*120,2))  # (state,action)