#!/usr/bin/python
import pickle
import subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import clusteredHP


#cr2 = clusteredHP.ClusteredResults(modelNum=12,simNum=10,minLength=4,maxLength=25,nonSteadyPercent=0.5)
#cr0 = clusteredHP.ClusteredResults(modelNum=12,simNum=12,minLength=4,maxLength=25,nonSteadyPercent=0.5)
#pickle.dump(cr2,open('compareTmp/cr2.p','wb'))
#pickle.dump(cr0,open('compareTmp/cr0.p','wb'))
cr2=pickle.load( open( "compareTmp/cr2.p", "rb" ) )
cr0=pickle.load( open( "compareTmp/cr0.p", "rb" ) )

#subprocess.call(('mkdir',cr.outputDir+'figures/'))
#cr.plotHPstats(saveFig=True)
#cr.plot2DClustLen(4,9,True)
#cr.plot2DClustLen(10,15,True)
#cr.plot2DClustLen(16,21,True)
#cr.plot2DClustLen(22,25,True)
#cr.bioMassDistr(6,10,True)
#cr.bioMassDistr(6,5,True)
##plt.show()
