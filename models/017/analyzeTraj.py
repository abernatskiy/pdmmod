#!/usr/bin/python
import sys
sys.path.append('../../')
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import subprocess
import pickle
import numpy as np
from collections import OrderedDict
import math
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm


import hpClasses
from result import *
from clusteredHP import *


def totalPopTime(result,trajNum):
    totalPopList = []
    times = []
    with open(r.outputDir+'traj'+str(trajNum)) as infile:
        for line in infile:
            if not line[0]=='#':
                dlist=line.split(',')[0:-1]
                times.append(float(dlist[0]))
                totalPopList.append(
                    sum([int((item.split(' '))[1]) for item in dlist[1:]])
                    )

    return times, totalPopList

def lenDistrAsTime(result,trajNum,minLength,maxLength):
    distrDict ={}
    with open(r.outputDir+'traj'+str(trajNum)) as infile:
        for line in infile:
            if not line[0]=='#':
                dlist=line.split(',')[0:-1]
                time = float(dlist[0])
                distrDict[time]=[0]*(maxLength-minLength+1)
                for couple in dlist[1:]:
                    pair = couple.split(' ')
                    if 'f' in pair[0]:
                        distrDict[time][(len(pair[0])-2)]+=int(pair[1])
                    else:
                        distrDict[time][(len(pair[0])-1)]+=int(pair[1])
    return distrDict


def foldPopTime(result,trajNum):
    totalPopList = []
    times = []
    with open(r.outputDir+'traj'+str(trajNum)) as infile:
        for line in infile:
            if not line[0]=='#':
                dlist=line.split(',')[0:-1]
                times.append(float(dlist[0]))
                totalPopList.append(0)
                for pair in dlist[1:]:
                    pair = pair.split(' ')
                    if 'f' in pair[0]:
                        totalPopList[-1]+=int(pair[1])

    return times, totalPopList


modelNum = 17
simNum = 22
minLength = 1
maxLength = 25
r = Result(modelNum, simNum, reorganize=False, numOfRuns=3, traj=True)
tpl = totalPopTime(r,0)
fpl = foldPopTime(r,0)

plt.plot(fpl[0],tpl[1])
plt.plot(fpl[0],fpl[1])
plt.show()

#distrDict = lenDistrAsTime(r,0,1,25)
#pickle.dump(distrDict,open('distrDict75.p','wb'))
#distrDict = pickle.load(open('distrDict6.p','rb'))
#sortedDistrDict = OrderedDict(sorted(distrDict.items(), key=lambda t: t[0], reverse=False))
#X = np.array([list(range(minLength,maxLength+1))]*501)

#yl = []
#zl = []
#count = 0
#for (time, distr) in sortedDistrDict.items():
    #if (time*10)%1 ==0.0:
        #yl.append([time]*(maxLength-minLength+1))
        #distr = [item for item in distr]
        #zl.append(distr)
        #count+=1

#Y = np.array(yl)
#Z = np.array(zl)

#fig = plt.figure()
#ax = fig.gca(projection='3d')
#ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.9)

###ax.set_zscale('log')

#plt.show()

