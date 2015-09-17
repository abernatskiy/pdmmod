#!/usr/bin/python
import sys
import os
sys.path.append('../../')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import subprocess

import hpClasses
from result import *
from clusteredHP import *

def plotSpecific(cr,names):
    arrays=[cr.means[name] for name in names]
    for (name,data) in zip (names,arrays):
        if not 'f' in name:
            plt.plot(cr.times,data,label=name,color='0.85',linewidth=3)
        else:
            plt.plot(cr.times,data,label=name,linewidth=3)
    plt.legend()
    plt.title('Time evolutions of selected sequences',fontsize=30)
    plt.ylabel('Population',fontsize=22,linewidth=3)
    plt.xlabel('Time',fontsize=22)
    plt.xlim((0,100))
    plt.show()
    return None


modelNum = 12
natData = hpClasses.readNativeList(25)
minLength=4
maxLength=25
noR=1

for simNum in range(117,126):
    try:
        os.mkdir('012_output'+str(simNum)+'/figures/')
    except:
        print('folder exists')
    save = True
    try:
        cr = ClusteredResults(
            modelNum,simNum,minLength,maxLength,nonSteadyPercent=0.5
            )
        cr.plotHPstats(natData,None,saveFig=save,nonSteadyPercent=0.5)
        cr.plot2DClustLen(4,7,saveFig=save)
        cr.plot2DClustLen(8,13,saveFig=save)
        cr.plot2DClustLen(14,19,saveFig=save)
        cr.plot2DClustLen(20,25,saveFig=save)
    except:
        print(str(simNum)+' not finished')
        #subprocess.call(['touch','012_output'+str(simNum)+'/not_done'])
        #r = Result(modelNum,simNum,reorganize=True,numOfRuns=3,traj=True)
        #cr = ClusteredResults(
            #modelNum,simNum,minLength,maxLength,nonSteadyPercent=0.5
            #)
        #cr.plotHPstats(natData,None,saveFig=save,nonSteadyPercent=0.5)
        #cr.plot2DClustLen(4,7,saveFig=save)
        #cr.plot2DClustLen(8,13,saveFig=save)
        #cr.plot2DClustLen(14,19,saveFig=save)
        #cr.plot2DClustLen(20,25,saveFig=save)
    else:
        print(str(simNum)+' done')