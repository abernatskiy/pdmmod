#/usr/bin/python2

import sys
import pickle
sys.path.append('../codes/hp-model')
pickleFolder = ('../codes/hp-model/')
filename = ('nativeList.txt')

def convertHP(maxLength):
    nativeList = pickle.load(open(pickleFolder+'nativeList'+str(maxLength)+'.p','rb'))
    #print(nativeList)
    hpFile = open(filename, mode='w')
    hpFile.write('hpstring nativeEnergy \n')
    for sp in nativeList:
        if sp.ifCat:
            hpFile.write(sp.hpstring+' '+str(sp.nativeEnergy)+' '+sp.catalystPattern+'\n')
        else:
            hpFile.write(sp.hpstring+' '+str(sp.nativeEnergy)+' '+'N'+' '+'\n')
    
    hpFile.close()
    
    return nativeList


a=convertHP(18)