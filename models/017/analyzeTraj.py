#!/usr/bin/python
import sys
sys.path.append('../../')
import matplotlib
matplotlib.use('Agg')
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
plt.gcf().subplots_adjust(bottom=0.15)
plt.gcf().subplots_adjust(left=0.15)

def totalPopTime(result,filename):
    totalPopList = []
    times = []
    with open(r.outputDir+filename) as infile:
        for line in infile:
            if not line[0]=='#':
                dlist=line.split(',')[0:-1]
                times.append(float(dlist[0]))
                totalPopList.append(
                    sum([int((item.split(' '))[1]) for item in dlist[1:]])
                    )

    return times, totalPopList

def lenDistrAsTime(result,filename,minLength,maxLength):
    distrDict ={}
    with open(r.outputDir+filename) as infile:
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

def seqDict(result,filename,minTime):
    seqDict = {}
    times = []
    with open(r.outputDir+filename) as infile:
        for line in infile:
            if not line[0]=='#':
                dlist=line.split(',')[0:-1]
                time = float(dlist[0])
                if time >= minTime:
                    times.append(time)
                    for couple in dlist[1:]:
                        pair = couple.split(' ')
                        if pair[0] in seqDict.keys():
                            seqDict[pair[0]].append(int(pair[1]))
                        else:
                            seqDict[pair[0]]=[int(pair[1])]
                            
    print(len(times))
    #print(times)
    return seqDict, len(times)

def seqDictToData(seqDict,timeSteps):
    sequences = [[] for i in range(25)]
    for (seq, pops) in seqDict.items():
        if 'f' in seq:
            length = len(seq)-1
        else:
            length = len(seq)
        sequences[length-1].append(float(sum(pops))/float(timeSteps))
    return sequences

def normalize(plotData,denominator):
    normal = [[] for i in range(25)]
    for i in range(25):
        for item in plotData[i]:
            normal[i].append(item/denominator)
        if normal[i]==[]:
            normal[i]=10**(-15)
    return normal

def boxplotThem(dataToPlot,title):
    means = [np.mean(item) for item in dataToPlot]
    fig = plt.figure(1, figsize=(9,6))
    ax = fig.add_subplot(111)

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    for i in range(25):
        print('length ',str(i+1))
        for item in dataToPlot[i]:
            ax.scatter(i+1,item)

    ax.plot(list(range(1,26)),means,linewidth=4,color='r')

    ax.set_xticks([1,5,10,15,20,25])
    ax.set_xticklabels([r"$1",r"$5$",r"$10$",r"$15$",r"$20$",r"$25$"],fontsize = 25)

    ax.set_yscale('log')
    ax.set_yticks([0.00000001,0.000001,0.0001,0.01,1])
    ax.xaxis.set_tick_params(width=1.5)
    ax.yaxis.set_tick_params(width=1.5)
    ax.set_yticklabels([r"$10^{-8}$",r"$10^{-6}$",r"$10^{-4}$",r"$10^{-2}$",r"$1$"],fontsize = 25)
    ax.get_yaxis().get_major_formatter().labelOnlyBase = False
    ax.set_ylabel('relative population',fontsize = 30)
    ax.set_xlabel(r'length',fontsize = 30)
    ax.set_xlim(0,26)
    ax.set_ylim(0.00000005)
    plt.suptitle(title,fontsize=30)
    plt.savefig(r.outputDir+'distr.png')

def outToIn(result,filename):
    popsFIle = open('populations.txt','a')
    with open(r.outputDir+filename) as infile:
        for line in infile:
            if not line[0]=='#':
                dlist=line.split(',')[0:-1]
                time = float(dlist[0])
                for couple in dlist[1:]:
                    popsFIle.write(couple+'\n')
    popsFIle.close()

def bugPlot(r,filename,title):
    t, tpt = totalPopTime(r,filename)
    plt.plot(t,tpt,label='totalpop')
    plt.legend()
    plt.title(title,fontsize=25)
    plt.savefig(r.outputDir+'tpt.png')
    dd = lenDistrAsTime(r,filename,1,25)
    odd = OrderedDict(sorted(dd.items(), key=lambda t: t[0], reverse=False))
    lenDistr = [[] for i in range(25)]
    for (time,distr) in odd.items():
        for i in range(25):
            lenDistr[i].append(distr[i])

    idx=1
    plt.clf()
    for l in lenDistr:
        plt.plot(t,l,label = str(idx))
        plt.legend()
        plt.title(title,fontsize=25)
        plt.savefig(r.outputDir+'len'+str(idx)+'.png')
        idx+=1
        plt.clf()

#sd = seqDict(r,0,100)

#sds = {}
#for seq in sd.keys():
    #sds[seq]=sum(sd[seq])/((200-100)*100+1)

#p, fr = getFreqs(sds,maxLength)

def fitInLen(freqs):
    fits = {}
    for (length, values) in freqs.items():
        xx = []
        yy = []
        for (pop,freq) in values.items():
            xx.append(math.log10(pop))
            yy.append(math.log10(freq))
            x = np.array(xx)
            y = np.array(yy)
            A = np.vstack([x, np.ones(len(x))]).T
            fits[length] = np.linalg.lstsq(A, y)[0]
    return fits

def plotInLen(r,freqs,fits,title):
    nc = 3
    minLength=8
    maxLength=25
    fig, axes = plt.subplots(
        nrows=int((maxLength-minLength+1)/2/nc), ncols=nc, figsize=(12, 12)
        )
    index = 0
    for (length,freqs) in freqs.items():
        if length>=minLength and length<=maxLength and length%2==1:
            sortedFreqs = OrderedDict(sorted(freqs.items(),key=lambda t: t[0], reverse=False))
            axes[int((index)/nc),(index)%(nc)].plot(
                list(sortedFreqs.keys()),list(sortedFreqs.values()),'o'
                )
            m, c = fits[length-1]
            axes[int((index)/nc),(index)%(nc)].plot(
                list(sortedFreqs.keys()),
                [(10**(c)*xi**(m)) for xi in sortedFreqs.keys()],
                linewidth = 3,
                label = 'y = '+str("%.2f" %(10**c))+'x^'+str("%.2f" %m)
                )
            axes[int((index)/nc),(index)%(nc)].set_yscale('log')
            axes[int((index)/nc),(index)%(nc)].set_xscale('log')
            #axes[int((index)/nc),(index)%(nc)].legend()
            axes[int((index)/nc),(index)%(nc)].set_title(str(length)+'-mers')
            index+=1
    
    plt.suptitle(title,fontsize=25)
    plt.savefig(r.outputDir+'inlen.png')


def readParams(result,filename):
    seqDict = {}
    times = []
    with open(r.outputDir+filename) as infile:
        for line in infile:
            if line[0]=='#':
                data = line.split(' ')
                if not data[1] == 'Parameters:':
                    continue
                else:
                    parameters = data[2:]
            else:
                return parameters

plt.clf()
modelNum = 17
simNum = 1
minLength = 1
maxLength = 25
r = Result(modelNum, simNum, reorganize=False, numOfRuns=1, traj=True)
filename = 'traj0'


title=''
parameters = readParams(r,filename)
for par in parameters:
    if 'hydrolysis' in par or 'degradation' in par:
        title+=par+' '

bugPlot(r,filename,title)

l = list(range(1,26))
#sd, denominator = seqDict(r,filename,80)

#d = seqDictToData(sd,denominator)
#nd = normalize(d,np.mean(d[0]))
##pickle.dump(nd,open('nd22-1000.p','wb'))
#boxplotThem(nd,title)

#sums = []
#for i in d:
#    sums.append(sum(i))
#s = sum(sums)
#plt.clf()
#distr = [i/s for i in sums]
#plt.plot(l,distr,linewidth=4)
#plt.yscale('log')
#plt.title(title,fontsize=30)
#plt.savefig(r.outputDir+'lenDistr.png')
#sds = {}
#for seq in sd.keys():
#    sds[seq]=sum(sd[seq])/denominator

#p, fr = getFreqs(sds,maxLength)
#fits =  fitInLen(fr)
#plotInLen(r,fr,fits,title)



