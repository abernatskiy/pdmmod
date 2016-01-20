#!/usr/bin/python
import sys
sys.path.append('../../')
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import subprocess
import pickle
import scipy.stats

import hpClasses
from result import *
from clusteredHP import *

###EDIT HERE###

modelNum = 16
natData = hpClasses.readNativeList(25)

maxLength=25
noR=1
nonSteadyPercent = 0.15
simNum = 6
r = Result(modelNum, simNum, reorganize=False, numOfRuns=1, traj=True)
#jointData = r.makeDictOfLengths(maxLength, nonSteadyPercent)
#pickle.dump(jointData,open('jointData6.p','wb'))
jointData = pickle.load(open('jointData6.p','rb'))
modelNum = 16
natData = hpClasses.readNativeList(25)

distr1 = dict(zip(list(range(1,26)),[0]*25))
distr2 = dict(zip(list(range(1,26)),[0]*25))
for (key, par) in natData.items():
    l = len(key)
    distr1[l]+=1
    if not par[1] == 'N':
        distr2[l]+=1
ll = list(range(1,26))

plt.plot(ll,list(distr1.values()),label='folded',linewidth=3)
plt.plot(ll,list(distr2.values()),label='cat',linewidth=3)
plt.plot(ll,[2**i for i in range(1,26)],label='all',linewidth=3)
plt.yscale('log')
plt.legend()
plt.show()

#minLength=1
#fig = plt.figure(1, figsize=(9, 6))
#dataToPlot = []
#for length in range(minLength,maxLength+1):
    #data = [item[0] for item in list(jointData[length].values())]
    #dataToPlot.append(data)

#ax = fig.add_subplot(111)
#bp = ax.boxplot(dataToPlot,meanline=True,showmeans=True,whis=1.5,widths=0.1)
#for box in bp['means']:
    ## change outline color
    #box.set(color='r',linewidth=2)

#for box in bp['medians']:
    #box.set(color='b',linewidth=2)

#ax.set_yscale('log')
#ax.set_xscale('log')
#ax.set_xticklabels(list(range(minLength,maxLength+1)))
#plt.show()


#for length in dataToPlot:
    

fig = plt.figure(1, figsize=(9, 6))
ax = fig.add_subplot(111)
#hs = ax.hist(logData,50)
#ax.set_yscale('log')
#plt.show()
#sData = set(data)
#linCounts= {}
#for i in sData:
    #linCounts[i] = data.count(i)

