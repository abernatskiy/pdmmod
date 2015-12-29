#!/usr/bin/python
#move figures, so they are all together
import routes
import os
import glob
import shutil

def copyThem(modelNum,firstSim,lastSim,newLoc):
    '''copy figure files locate incoviniently in
    routes.routePDM+'models/'+str(modelNum)+<output folder/figures>
    to a place, where they'll be all together
    '''
    for i in range(firstSim,lastSim+1):
        path = routes.routePDM+'models/' + str('%03d' %modelNum) + '/' + \
            str('%03d' %modelNum) +'_output'+ str(i) + '/figures/'
            #print(path)
        for filename in glob.glob(os.path.join(path, '*.*')):
            shutil.copy(filename, os.path.join(newLoc,(str('%03d' %i)+'_'+filename[-7:]) ))
        
    return None

copyThem(16,0,30,'/tmp/fig')