import numpy as np
from scipy.stats import poisson

# factory function
def arrival_generator_factory(name):
    if name == 'constant':
        return ConstantGenerator
    elif name == 'autoregressive':
        return AutoregressiveGenerator

class ArrivalGenerator():
    def __init__(self,config):
        pass
    
    def next(self):
        # 返回下一时间步的交通到达
        pass

class ConstantGenerator(ArrivalGenerator):
    def __init__(self,config):
        super(ConstantGenerator,self).__init__(config)
        self.is_stochastic = config['is_stochastic']
        
        self.arrival = 240.0*np.ones((4,2))  # 到达率用vph表示, array of (4,2)
        
    def next(self,arrival=None):
        if arrival is not  None:
            self.arrival = arrival
        
        if self.is_stochastic:
            return poisson(self.arrival/3600).rvs()
        else:
            return self.arrival/3600
    
class AutoregressiveGenerator(ArrivalGenerator):
    def __init__(self,config):
        super(AutoregressiveGenerator,self).__init__(config)
        pass
    
    def next(self):
        pass