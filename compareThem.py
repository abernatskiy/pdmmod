#!/usr/bin/python
import pickle
import subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import clusteredHP
import numpy as np

#cr2 = clusteredHP.ClusteredResults(modelNum=12,simNum=10,minLength=4,maxLength=25,nonSteadyPercent=0.5)
#cr0 = clusteredHP.ClusteredResults(modelNum=12,simNum=12,minLength=4,maxLength=25,nonSteadyPercent=0.5)
cr2 = pickle.load(open('compareTmp/cr2.p','rb'))
cr0 = pickle.load(open('compareTmp/cr0.p','rb'))

def getBase(cr2):
    bases={}
    for (length, clust) in cr2.clustDict.items():
        bases[length]=(
                clust.minClustered,
                np.mean([seq.meanPop for seq in clust.clusters[0].sequences]),
                clust.maxClustered)
    return bases

def getNumGood(cr0,bases,nTimes):#BUG
    numGood = {}
    for (length, clust) in cr0.clustDict.items():
        numGood[length]=0
        #for clustNum in clust.clusters.keys():
        #    pops=sorted([seq.meanPop for seq in clust.clusters[clustNum].sequences])
        #    numGood[length] += len(list(filter(lambda x: x > nTimes*bases[length][2], pops)))
        pops=sorted([seq.meanPop for seq in clust.outstanders])
        numGood[length] += len(list(filter(lambda x: x > nTimes*bases[length][2], pops)))
    return numGood

def doClustMatch(cr0,bases):
    match = {}
    for (length, clust) in cr0.clustDict.items():
        if not length == 4:
            match[length]=(clust.maxClustered>=bases[length][2])
    return match

<<<<<<< HEAD
=======
#cr2 = clusteredHP.ClusteredResults(modelNum=12,simNum=10,minLength=4,maxLength=25,nonSteadyPercent=0.5)
#cr0 = clusteredHP.ClusteredResults(modelNum=12,simNum=12,minLength=4,maxLength=25,nonSteadyPercent=0.5)
#pickle.dump(cr2,open('compareTmp/cr2.p','wb'))
#pickle.dump(cr0,open('compareTmp/cr0.p','wb'))
cr2=pickle.load( open( "compareTmp/cr2.p", "rb" ) )
cr0=pickle.load( open( "compareTmp/cr0.p", "rb" ) )
>>>>>>> ca3c8de2354e823911875f5b63edbb893e31bc6e

#subprocess.call(('mkdir',cr.outputDir+'figures/'))
#cr.plotHPstats(saveFig=True)
#cr.plot2DClustLen(4,9,True)
#cr.plot2DClustLen(10,15,True)
#cr.plot2DClustLen(16,21,True)
#cr.plot2DClustLen(22,25,True)
#cr.bioMassDistr(6,10,True)
#cr.bioMassDistr(6,5,True)
##plt.show()
