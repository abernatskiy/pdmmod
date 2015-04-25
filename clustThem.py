#!/usr/bin/python
import subprocess
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import clusteredHP



modelNum = 12
#for i in range(9,10):
simnum = 10
minl = 4
maxl = 25
cr = clusteredHP.ClusteredResults(modelNum,simnum,minl,maxl,nonSteadyPercent=0.5)
#subprocess.call(('mkdir',cr.outputDir+'figures/'))
#cr.plotHPstats(saveFig=True)
#cr.plot2DClustLen(4,9,True)
#cr.plot2DClustLen(10,15,True)
#cr.plot2DClustLen(16,21,True)
#cr.plot2DClustLen(22,25,True)
cr.bioMassDistr(6,10,True)
cr.bioMassDistr(6,5,True)


