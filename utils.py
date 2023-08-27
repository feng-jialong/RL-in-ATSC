import os
import argparse
import yaml

# webster delay model
def delay_webster(y_r,sigma,config):
    is_stochastic = config['is_stochastic']
    sfr = config['sfr']  # sfr: 饱和流率
    L = config['L']  # L: 总损失时间
    # sigma: saturation degree
    q_r = sfr*y_r
    Q,Y = q_r.sum(),y_r.sum()
    
    d = L/(2*Q*sigma*(sigma-Y))*(q_r/(1-y_r)*(sigma-y_r)**2).sum()
    if is_stochastic and sigma<1.0:
        d += len(config['phase_scheme'])*sigma**2/(2*Q*(1-sigma))  # 4相位
    return d

# configuration优先级: cmd > hardcode > default

def parse_config(default_config_dir):
    # 1. load default configs
    with open(default_config_dir, "r+") as f:
        config = yaml.safe_load(f)
    
    # 2. update hardcode configs
    # config['key'] = value

    # 3. cmd arguments
    parser = argparse.ArgumentParser("parse cmd arguments")
    # parse_known_args返回两个元素，第一个为所求的NameSpace，第二个是unknown args的列表
    args = vars(parser.parse_known_args()[0])
    config.update(args)
    
    # 4. construct derived configs
    config['L'] = len(config['phase_scheme'])*(config['red']+config['timeloss'])

    return config


