import numpy as np
from scipy.stats import poisson

class ArrivalGenerator():
    def __init__(self):
        pass
    
    def next(self):
        # 返回下一时间步的交通到达
        pass

class ConstantGenerator(ArrivalGenerator):
    def __init__(self,arrival,is_stochastic):
        self.is_stochastic = is_stochastic
        self.arrival = arrival  # 到达率用vph表示, array of (4,2)
        
    def next(self):
        if self.is_stochastic:
            return poisson(self.arrival/3600).rvs()
        else:
            return self.arrival/3600
    
class AutoregressionGenerator(ArrivalGenerator):
    def __init__(self):
        pass
    
    def next(self):
        pass