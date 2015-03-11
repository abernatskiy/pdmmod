#!/usr/bin/python
'''Library for a script which runs simulations 
'''
from os import system as system
import subprocess

class Simulation(object):
    def __init__(self,modelName,howLong,

def runSeveralSeries(modelName,,howMany,traj=False):
    '''runs several simulations sequentially, store average, st.deviation and optionally trajectories
    '''
    command = 
    system('mkdir '+modelName)
    for i in range(howMany):
        subprocess.call(command)
    
    return None

def runSeveralParallelPC():
    '''
    '''
    
    return None

