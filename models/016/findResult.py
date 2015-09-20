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

def plotStandardFirstTime(
    startSim,endSim,modelNum,minLength=4,maxLength=25,nonSteadyPercent=0.5
    ):
    for simNum in range(0,7):
        try:
            os.mkdir(str("%03d" %modelNum)+'_output'+str(simNum)+'/figures/')
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
            subprocess.call(['touch',str("%03d" %modelNum)+'_output'+str(simNum)+'/not_done'])
            r = Result(modelNum,simNum,reorganize=True,numOfRuns=3,traj=True)
            cr = ClusteredResults(
                modelNum,simNum,minLength,maxLength,nonSteadyPercent=0.5
                )
            cr.plotHPstats(natData,None,saveFig=save,nonSteadyPercent=0.5)
            cr.plot2DClustLen(4,7,saveFig=save)
            cr.plot2DClustLen(8,13,saveFig=save)
            cr.plot2DClustLen(14,19,saveFig=save)
            cr.plot2DClustLen(20,25,saveFig=save)
        else:
            print(str(simNum)+' done')
            
def plotStandardReplot(
    startSim,endSim,modelNum,minLength=4,maxLength=25,nonSteadyPercent=0.5
    ):
    save = True
    redone=[]
    new=[]
    for simNum in range(startSim,endSim):
        commonPath =  str("%03d" %modelNum)+'_output'+str(simNum)+'/'
        if os.path.isfile(commonPath+'figures/000.png'):
            if os.path.isfile(commonPath+'not_done'):
                r = Result(modelNum,simNum,reorganize=True,numOfRuns=3,traj=True)
                cr = ClusteredResults(
                    modelNum,simNum,minLength,maxLength,nonSteadyPercent=0.5
                    )
                cr.plotHPstats(natData,None,saveFig=save,nonSteadyPercent=0.5)
                cr.plot2DClustLen(4,7,saveFig=save)
                cr.plot2DClustLen(8,13,saveFig=save)
                cr.plot2DClustLen(14,19,saveFig=save)
                cr.plot2DClustLen(20,25,saveFig=save)
                subprocess.call(['rm','-r',commonPath+'not_done'])
                redone.append(simNum)
            else:
                print(str(simNum)+' already has been done')
                continue
        else:
            new.append(simNum)
            plotStandardFirstTime(
                simNum,simNum+1,
                modelNum,minLength=4,maxLength=25,nonSteadyPercent=0.5
                )
    print('redone',redone)
    print('new',new)

###EDIT HERE###

modelNum = 16
natData = hpClasses.readNativeList(25)
minLength=4
maxLength=25
noR=1
startSim = 0
endSim = 78
plotStandardReplot(startSim,endSim,
                   modelNum,minLength=4,maxLength=25,nonSteadyPercent=0.5)

