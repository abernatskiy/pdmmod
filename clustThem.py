#!/usr/bin/python
import subprocess

import clusteredHP



modelNum = 12
for i in range(9,10):
    simNum = i
    minL = 4
    maxL = 25
    cr = clusteredHP.ClusteredResults(modelNum,simNum,minL,25)
    subprocess.call(('mkdir',cr.outputDir+'figures/'))
    cr.plotHPstats(saveFig=True)
    cr.plot2DClustLen(4,9,True)
    cr.plot2DClustLen(10,15,True)
    cr.plot2DClustLen(16,21,True)
    cr.plot2DClustLen(22,25,True)
