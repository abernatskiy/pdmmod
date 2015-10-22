#!/usr/bin/python
import sys
import os
sys.path.append('../../')
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import subprocess

import hpClasses
from result import *
from clusteredHP import *




            

    

###EDIT HERE###

modelNum = 16
natData = hpClasses.readNativeList(25)
minLength=1
maxLength=25
noR=1
nonSteadyPercent = 0.5
simNum = 12
cr = ClusteredResults(modelNum,simNum,minLength,maxLength,nonSteadyPercent)
cr.plotOutstanders(natData)
#for simNum in range(0,9):
    #print('simNum is',simNum)
    #r = Result(modelNum,simNum)
    #jointData = r.makeDictOfLengths(maxLength, nonSteadyPercent)
    #lengthsDistr = r.getLengthDistribution(natData,jointData,nonSteadyPercent)
    #plt.plot(list(range(1,maxLength+1)), lengthsDistr, linewidth=4,label='sim. '+str(simNum))
#plt.yscale('log')
#plt.xscale('log')
#plt.legend()
#plt.show()
#startSim = 0
#endSim = 78
#plotStandardReplot(startSim,endSim,
                   #modelNum,minLength=4,maxLength=25,nonSteadyPercent=0.5)

