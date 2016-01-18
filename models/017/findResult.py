#!/usr/bin/python
import sys
sys.path.append('../../')
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import subprocess
import pickle

import hpClasses
from result import *
from clusteredHP import *

###EDIT HERE###


natData = hpClasses.readNativeList(25)

maxLength=25
noR=1
nonSteadyPercent = 0.15
minLength=1

fig = plt.figure(1, figsize=(9, 6))
ax = fig.add_subplot(111)

modelNum = 17
simNum = 1
r0 = Result(modelNum, simNum, reorganize=False, numOfRuns=3, traj=True)
jointData0 = pickle.load(open(r0.outputDir+'jointData.p','rb'))
dataToPlot = []
for length in range(minLength,maxLength+1):
    data = [item[0] for item in list(jointData0[length].values())]
    dataToPlot.append(data)
bp0 = ax.boxplot(dataToPlot,meanline=True,showmeans=True,whis=1.5,widths=0.1)
for box in bp0['means']:
    # change outline color
    box.set(color='b',linewidth=2)

for box in bp0['medians']:
    box.set(color='b',linewidth=2)
for box in bp0['fliers']:
    box.set(color='b')
    
    

