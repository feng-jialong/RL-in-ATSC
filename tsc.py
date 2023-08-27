import numpy as np
from itertools import cycle

from utils import delay_webster

# traffic controller factory
def tsc_factory(name):
    if name == 'pretimed':
        return PretimedTSC
    elif name == 'webster':
        return WebsterTSC
    elif name == 'mpc':
        return MPCTSC

class TrafficSignalController():
    def __init__(self,config):
        self.config = config
        self.y = config['yellow']
        self.r = config['red']
        self.tl = config['timeloss']
        self.L = config['L']
        self.phase_scheme = np.array(config['phase_scheme'])
    
    def run(self):
        pass
    
    def update(self):
        pass

class PretimedTSC(TrafficSignalController):
    def __init__(self,config):
        super(PretimedTSC,self).__init__(config)
        self.g_time = config['g_time']
        
        # fixed-time controller
        if isinstance(self.g_time,float):
            self.g_time = self.g_time*np.ones(4).astype(int)  # 绿灯时间
        elif isinstance(self.g_time,np.ndarray):
            self.g_time = self.g_time.astype(int)

        phase_time = np.stack([self.g_time+self.y-self.tl,(self.tl+self.r)*np.ones(4)],axis=0)
        phase_time = phase_time.swapaxes(0,1).reshape(-1).astype(int)  # 相位时间
        
        phase = np.stack([self.phase_scheme,-np.ones((4,2))],axis=0)
        phase = phase.swapaxes(0,1).reshape(-1,2).astype(int)

        phase_sequence = np.repeat(phase,phase_time,axis=0)
        phase_sequence = cycle([phase_sequence[i] for i in range(len(phase_sequence))])
        
        self.phase_sequence = phase_sequence
    
    def next(self):
        return next(self.phase_sequence)

class WebsterTSC(TrafficSignalController):
    def __init__(self,config):
        super(WebsterTSC,self).__init__(config)
        self.mode = config['webster_mode']
        assert self.mode in ['approximate','exact']
        
        # initialize
        self.cycle_time = None
        self.update(240*np.ones((4,2)))
    
    def next(self):
        return next(self.phase_sequence)
    
    def update(self,arrival):
        self.webster_timing(arrival)
    
    def webster_timing(self,arrival,mode=None):
        # webster's (approximation)
        y_r = (arrival/self.config['sfr']).max(axis=-1)  # 对应于单口放行的流量比计算
        Y = y_r.sum()
        L = self.L
        if Y > 0.8:
            y_r = y_r/Y*0.8
            Y = 0.8

        if mode is None:
            mode = self.mode

        if mode=='approximate':
            C = (1.5*L+5.0)/(1-Y)

        elif mode=='exact':
            C_min = np.ceil(L/(1-Y)).astype(int)
            C_range = [C_min,1.5*C_min]
            C_arr = np.arange(*C_range,0.1)[1:]
            num_C = len(C_arr)
            sigma_arr = C_arr*Y/(C_arr-L)
            delay_arr = np.zeros(num_C)
            for i,sigma in enumerate(sigma_arr):
                delay_arr[i] = delay_webster(y_r,sigma,self.config)
            C = C_arr[np.argmin(delay_arr)]
        
        # C = np.ceil(C).astype(int)
        g = np.ceil((C-L)*y_r/Y).astype(int)  # 有效绿灯时间
        g = (g+self.tl-self.y).astype(int)  # 绿灯时间
        phase_time = np.stack([g,(self.tl+self.r)*np.ones(4)],axis=0)
        phase_time = phase_time.swapaxes(0,1).reshape(-1).astype(int)  # 相位时间

        phase = np.stack([self.phase_scheme,-np.ones((4,2))],axis=0)
        phase = phase.swapaxes(0,1).reshape(-1,2).astype(int)

        self.cycle_time = phase_time.sum()
        
        phase_sequence = np.repeat(phase,phase_time,axis=0)
        phase_sequence = cycle([phase_sequence[i] for i in range(len(phase_sequence))])
        
        self.phase_sequence = phase_sequence

class MPCTSC():
    def __init__(self):
        pass
  
    def mpc_controller(config):
        pass        

def q_learning_controller(config):
    # Q-learning
    q_value = np.zeros((2*120,2))  # (state,action)