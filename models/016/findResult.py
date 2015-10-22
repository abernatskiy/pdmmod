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
minLength=6
maxLength=25
noR=1
cr = ClusteredResults(
                modelNum,69,minLength,maxLength,nonSteadyPercent=0.5
                )
#startSim = 0
#endSim = 78
#plotStandardReplot(startSim,endSim,
                   #modelNum,minLength=4,maxLength=25,nonSteadyPercent=0.5)

