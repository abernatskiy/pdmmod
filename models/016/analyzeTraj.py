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
import scipy.stats

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

def kurtosisAsTime(result,trajNum,minLength,maxLength):
    kurtDict = {}
    seqDict = {}
    with open(r.outputDir+'traj'+str(trajNum)) as infile:
        for line in infile:
            if not line[0]=='#':
                dlist=line.split(',')[0:-1]
                time = float(dlist[0])
                kurtDict[time]=[0]*(maxLength-minLength+1)
                seqDict[time]=pd = [[] for _ in range(25)]
                for couple in dlist[1:]:
                    pair = couple.split(' ')
                    if 'f' in pair[0]:
                        (seqDict[time][(len(pair[0])-2)]).append(float(pair[1]))
                    else:
                        (seqDict[time][(len(pair[0])-1)]).append(float(pair[1]))
    #for (time, data) in seqDict.items():
        #kurtDict[time] = [
            #scipy.stats.kurtosis(lData,axis=0,fisher=True,bias=False) 
            #for lData in data
            #]
    
    return seqDict, kurtDict

def seqDict(result,trajNum,minTime):
    seqDict = {}
    with open(r.outputDir+'traj'+str(trajNum)) as infile:
        for line in infile:
            if not line[0]=='#':
                dlist=line.split(',')[0:-1]
                time = float(dlist[0])
                if time >= minTime:
                    for couple in dlist[1:]:
                        pair = couple.split(' ')
                        if pair[0] in seqDict.keys():
                            seqDict[pair[0]].append(int(pair[1]))
                        else:
                            seqDict[pair[0]]=[int(pair[1])]
    return seqDict

def getFreqs(seqSumDict,maxLength):
    freqs = dict([(i,{}) for i in  range(1,maxLength+1)])
    for (seq, pop) in seqSumDict.items():
        if 'f' in seq:
            l = len(seq)-1
        else:
            l = len(seq)
        if pop in freqs[l].keys():
            (freqs[l])[pop]+=1
        else:
            (freqs[l])[pop]=1
    for (l, fr) in freqs.items():
        freqs[l]=OrderedDict(sorted(fr.items(), key=lambda t: t[0], reverse=False))
    intFr = {}
    for (l, fr) in freqs.items():
        intFr[l]={}
        for (freq,count) in fr.items():
            counts = list(fr.values())
            freqs = list(fr.keys())
            i = freqs.index(freq)
            intFr[l][freq]=sum(counts[i:])
    
    return freqs,intFr

modelNum = 16
simNum = 6
minLength = 8
maxLength = 25
r = Result(modelNum, simNum, reorganize=False, numOfRuns=3, traj=True)
sd = seqDict(r,0,100)

sds = {}
for seq in sd.keys():
    sds[seq]=sum(sd[seq])/((200-100)*100+1)

p, fr = getFreqs(sds,maxLength)



#sd, kt = kurtosisAsTime(r,0,1,25)
##tpl = totalPopTime(r,0)
##fpl = foldPopTime(r,0)

##plt.plot(fpl[0],tpl[1])
##plt.plot(fpl[0],fpl[1])
##plt.show()

#tail =  []
#theRange =[x/10 for x in range(1990,2001)]
#for i in range(len(theRange)):
    #key = theRange[i]
    #tail.append(np.array(sd[key]))


#distrDict = lenDistrAsTime(r,0,1,25)
#pickle.dump(distrDict,open('distrDict83.p','wb'))
#distrDict = pickle.load(open('distrDict6.p','rb'))
#sortedDistrDict = OrderedDict(sorted(distrDict.items(), key=lambda t: t[0], reverse=False))
#X = np.array([list(range(minLength,maxLength+1))]*301)

#yl = []
#zl = []
#count = 0
#for (time, distr) in sortedDistrDict.items():
    #yl.append([time]*(maxLength-minLength+1))
    #distr = [item for item in distr]
    #zl.append(distr)
    #count+=1

#Y = np.array(yl)
#Z = np.array(zl)

nc = 3
fig, axes = plt.subplots(
    nrows=int((maxLength-minLength+1)/nc), ncols=nc, figsize=(8, 16)
    )
for (length,freqs) in fr.items():
    if length>=minLength and length<=maxLength:
        #print('length',length)
        #print((length-minLength)  )
        #print( int((length-minLength)/nc),(length-minLength)%(nc) )
        axes[int((length-minLength)/nc),(length-minLength)%(nc)].plot(list(freqs.keys()),list(freqs.values()),'o')
        axes[int((length-minLength)/nc),(length-minLength)%(nc)].set_yscale('log')
        axes[int((length-minLength)/nc),(length-minLength)%(nc)].set_xscale('log')
        axes[int((length-minLength)/nc),(length-minLength)%(nc)].set_title(str(length))

plt.show()


#ax = fig.gca(projection='3d')
#ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.9)

##ax.set_zscale('log')

#plt.show()

