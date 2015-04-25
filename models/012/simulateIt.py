#!/usr/bin/python
import sys
sys.path.append('../../')

from libSimulate import *
try:
    from parameters import correspond
except:
    correspond = {}

#TESTING
modelNum = 12
termCond = ('simulateTime',50,0.5)
numOfRuns = 3
traj = False
rewrite = False
log_level = 'INFO'
#s = Simulation(modelNum,termCond,rewrite,None,numOfRuns,traj,log_level)
#s.runSeveralSeries()
##s.runSeveralParallelCluster(kernels=3, onNode=0)
#s.reorganizeOutput()
ss = SimulationsSet(modelNum,termCond,correspond,numOfRuns,traj,log_level)
#ss.runSimsOnCluster(3)
#ss.runSimsOnPC()