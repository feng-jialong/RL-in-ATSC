#%%
import numpy as np
import scipy
from scipy.stats import poisson
from tsc import tsc_factory
from arrival_generator import arrival_generator_factory

# point queue model
def point_queue_model(id,config):
    sim_length = config['sim_length']
    
    generator = arrival_generator_factory(config['generator'])(config)
    controller = tsc_factory(config['controller'])(config)
    
    # sim_length: simulation duration in seconds
    step_length = 1.0  # 步长调整未实现,因此固定1秒为步长
    step_num = np.ceil(sim_length/step_length).astype(int)
    q_record = np.zeros((step_num,4,2))  # 交叉口当前排队
    q_state = np.zeros((4,2))
    
    for i in range(step_num):
        # arrival
        q_state += generator.next()
        
        # departure
        flag = np.zeros(8)
        p = controller.next()  # 给出下一秒的相位
        if p[0]>=0 and p[1]>=0:
            flag[p] = 1.0
        
        q_state -= config['sfr']/3600*flag.reshape((4,2))
        np.place(q_state,q_state<0,0)
        q_record[i] = q_state[:]
    
    np.save(f'./results/{id}.npy',q_record)