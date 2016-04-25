#!/usr/bin/python
import os
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
sys.path.append('../')
import routes

from vesicle import *
from trajectory import *
import hpClasses

class VTrajectory(Trajectory):
    '''
    '''
    def __init__(
        self, modelNum, generation,idInGen,motherIdInGen,matureWeight,path
        ):
        self.idInGen = idInGen
        self.motherIdInGen = motherIdInGen
        self.generation=generation
        self.matureWeight=matureWeight
        self.modelNum = modelNum
        self.path = path
        self.outputDir=os.path.join(self.path,str("%04d" %self.generation))
        self.trajFile = os.path.join(self.outputDir,'growth'+str("%05d" %self.idInGen))
    
    #seqDict(self,minTime)
    #getMassTrajectory()
    #getTrajectory()
    #getPersistenceGn(autoOrFold,trajectory,natData,minTime)
    #getPersistencePh(autoOrFold,trajectory,natData,minTime)
    #getShapeTrajectories(seqShapeDict,natData)
    
    def getPersistentShapes(self,shapeTraj,minTimeStep):#TODO
        '''self.shapeTraj -- list:
            [[('URD', 4), ('URULLD', 2),...],...]
        '''
        persistent = []
        for shape in shapeTraj[minTimeStep]:
            print(shape)
            sign = False
            for shapes in shapeTraj[minTimeStep:]:
                if shape[0] in [s[0] for s in shapes]:
                    sign = True
                else:
                    sign = False
                    break
            if sign == True:
                persistent.append(shape[0])
        return persistent
    
def getSeq(seq):
    '''
    Arguments:
     - seq -- str. sequence as depicted in trajectory file
    Returns:
     - hps -- str. actual HP sequence
    '''
    if 'f' in seq:
        if '*' in seq:
            hps = seq[2:]
        else:
            hps = seq[1:]
    else:
        hps = seq
    return hps

def testFunction(seq,natData):
    '''checks if the seq is either a folder or an autocat
    '''
    hps = getSeq(seq)
    if hps in natData.keys():
        if not natData[hps][-1] == 'N':
            return 1
        else:
            return 0
    else:
        return -1
    
def countSeqInstances(seq,listOfSeq):
    '''in time series a sequence can be present in activated form: f*<hp>,
    folded form f<hp> or unfolded form <hp>
    when we count sequences we need to account different forms as one.
    This function counts only folded versions.
    Arguments:
     - str. seq as present in trajectory
    Returns:
     - True, if add sequence to the count
     - False, if not to add
    '''
    if (
        ('f*' in seq) or
            (
            (('f' in seq) and (not 'f*' in seq)) and
            (not 'f*'+getSeq(seq) in listOfSeq)
            )
        ):
        return True
    else:
        return False

    def plotMasesChildren(self,numGen,scaled=False):
        mts = []
        for generation in range(genNum):
            outputDir = os.path.join(vt.path,str("%04d" %generation))
            mt = pickle.load(open(os.path.join(outputDir,'mt.p'),'rb'))
            time = len(mt)
            if scaled:
                timepoints = [i/time for i in range(time)]
            else:
                timepoints = list(range(time))
            plt.plot(timepoints,mt,linewidth=4,label=str(generation))
            plt.legend()
            plt.savefig(os.path.join(vt.path,'masses.png'))

if __name__ == "__main__":     
    idInGen =0
    matureWeight = 6000
    modelNum = 18
    path = routes.routePDM+'vesicles/secondTrial'
    genNum = 10
    natData = hpClasses.readNativeList(25)
    seqShapeDict = pickle.load(open('../seqShapeDict.p','rb'))
    for generation in range(genNum):
        #vt = VTrajectory(
            #modelNum, generation,idInGen,0,matureWeight,path
        #)
        #mt = pickle.load(open(os.path.join(vt.outputDir,'mt.p'),'rb'))
        #traj = pickle.load(open(os.path.join(vt.outputDir,'traj.p'),'rb'))
        #ga = pickle.load(open(os.path.join(vt.outputDir,'ga.p'),'rb'))
        #gf = pickle.load(open(os.path.join(vt.outputDir,'gf.p'),'rb'))
        #pa = pickle.load(open(os.path.join(vt.outputDir,'pa.p'),'rb'))
        #pf = pickle.load(open(os.path.join(vt.outputDir,'pf.p'),'rb'))
        #sTraj  =  pickle.load(open(os.path.join(vt.outputDir,'sTraj.p'),'rb'))











