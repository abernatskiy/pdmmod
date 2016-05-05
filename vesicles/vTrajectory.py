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

    def getPersistentShapes(self,shapeTraj,minTimeStep):
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

    def plotMasesChildren(self,numGen,scaled=False):
        plt.clf()
        mts = []
        for generation in range(numGen):
            outputDir = os.path.join(self.path,str("%04d" %generation))
            mt = pickle.load(open(os.path.join(outputDir,'mt.p'),'rb'))
            time = len(mt)
            if scaled:
                timepoints = [i/time for i in range(time)]
            else:
                timepoints = list(range(time))
            plt.plot(timepoints,mt,linewidth=4,label=str(generation))
            plt.legend()
            plt.savefig(os.path.join(self.path,'masses'+str(scaled)+'.png'))

    def getGenotypesChildren(self,autoOrFold,numGen):
        gas = []
        for generation in range(numGen):
            outputDir = os.path.join(self.path,str("%04d" %generation))
            if autoOrFold == 1:
                gen = pickle.load(open(os.path.join(outputDir,'ga.p'),'rb'))
            elif autoOrFold == 0:
                gen = pickle.load(open(os.path.join(outputDir,'gf.p'),'rb'))
            else:
                raise ValueError('autoOrFold must be either 0 or 1, but it is '+str(autoOrFold))
            time = max(gen.values())
            ga = []
            for (seq,freq) in gen.items():
                if freq==time:
                    ga.append(seq)
            gas.append(ga)

        return gas

    def getPhenotypesChildren(self,autoOrFold,numGen):
        pas = []
        for generation in range(numGen):
            outputDir = os.path.join(self.path,str("%04d" %generation))
            if autoOrFold == 1:
                pa = pickle.load(open(os.path.join(outputDir,'pa.p'),'rb'))
            elif autoOrFold == 0:
                pa = pickle.load(open(os.path.join(outputDir,'pf.p'),'rb'))
            else:
                raise ValueError('autoOrFold must be either 0 or 1, but it is '+str(autoOrFold))

            pas.append(pa)

        return pas

    def plotGnNumChildren(self,gas,autoOrFold):
        plt.clf()
        counts = [len(ga) for ga in gas]
        plt.plot(list(range(len(gas))),counts,linewidth=4)
        if autoOrFold == 1:
            af = 'autocatalytic'
        elif autoOrFold == 0:
            af = 'foldarmeric'
        else:
            raise ValueError('autoOrFold must be either 0 or 1, but it is '+str(autoOrFold))
        plt.title('Number of '+af+' genotypes for different generations')
        plt.savefig(os.path.join(self.path,'geno-quant-'+af+'.png'))

    def plotPhenoChildren(self,pas,autoOrFold,scaled=False):
        plt.clf()
        if autoOrFold == 1:
            af = 'autocatalytic'
        elif autoOrFold == 0:
            af = 'foldarmeric'
        else:
            raise ValueError('autoOrFold must be either 0 or 1, but it is '+str(autoOrFold))
        generation = 0
        for pa in pas:
            time = len(pa)
            if scaled:
                timepoints = [i/time for i in range(time)]
            else:
                timepoints = list(range(time))
            plt.plot(timepoints,pa,linewidth=2,label=str(generation))
            generation+=1

        plt.title('Number of '+af+' phenotype variants for different generations')
        plt.legend()
        plt.savefig(os.path.join(self.path,'pheno-'+af+str(scaled)+'.png'))

    def plotPhenoGenerations(self,pas,autoOrFold):
        plt.clf()
        if autoOrFold == 1:
            af = 'autocatalytic'
        elif autoOrFold == 0:
            af = 'foldarmeric'
        else:
            raise ValueError('autoOrFold must be either 0 or 1, but it is '+str(autoOrFold))
        numGen = len(pas)
        mins = [min(pa) for pa in pas]
        plt.plot(list(range(numGen)),mins)
        plt.title('Minimum number of '+af+' phenotype variants vs generations')
        plt.savefig(os.path.join(self.path,'pheno-'+af+'min.png'))




    def generationGnFreqDistr(self,gas):#TEST
        theSet = set([])
        freqDict = {}
        for ga in gas:
            theSet= theSet | set(ga)
        for seq in theSet:
            states = []
            for ga in gas:
                if seq in ga:
                    states.append(1)
                else:
                    states.append(0)
            freqDict[seq] = states

        return freqDict

    def plotGnFreqDistr(self,gas,autoOrFold):
        plt.clf()
        if autoOrFold == 1:
            af = 'autocatalytic'
        elif autoOrFold == 0:
            af = 'foldarmeric'
        else:
            raise ValueError('autoOrFold must be either 0 or 1, but it is '+str(autoOrFold))
        numGen = len(gas)
        freqDict = self.generationGnFreqDistr(gas)
        seqGenCount = {}
        persistent = []
        for (seq, distr) in freqDict.items():
            seqGenCount[seq]=sum(freqDict[seq])
            if sum(freqDict[seq])==numGen:
                persistent.append(seq)

        values = list(seqGenCount.values())
        theSum = sum(values)
        hst = [val/len(gas) for val in values]
        plt.hist(hst,100,cumulative=False,normed=False)
        plt.savefig(os.path.join(self.path,'genoFreq'+af    +'.png'))
        return persistent

    def getShapesChildren(self,numGen):#BUG
        '''for every generation reads shape trajectory pickle sTraj.p
        calculates persistent shapes for this generation and adds to the list
        Arguments:
         - numGen: int
        Returns:
         - []
        '''
        persistChildren = []
        for gen in range(numGen):
            shapeTraj = pickle.load(open(os.path.join(self.outputDir,'sTraj.p'),'rb'))
            persistChildren.append(self.getPersistentShapes(shapeTraj,0))
        return persistChildren

    def generationPhenotypes(pas):#TODO
        return None

    def geneShapesFreqs(self,shapes):#TODO
        '''returns distribution of number of persistent shapes
        across generations
        '''
        theSet = set([])
        freqDict = {}
        for listShape in shapes:
            theSet = theSet | set(listShape)
        for shape in theSet:
            states = []
            for listShape in shapes:
                if shape in listShape:
                    states.append(1)
                else:
                    states.append(0)
            freqDict[shape] = states

        return freqDict
    
    def pickleGeneration(self,output,name):
        pickle.dump(output,open(
            os.path.join(self.outputDir,name+'.p'),'wb'
            ))
    

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



#if __name__ == "__main__":
    #seqDict(self,minTime)
    #getMassTrajectory()
    #getTrajectory()
    #getPersistenceGn(autoOrFold,trajectory,natData,minTime)
    #getPersistencePh(autoOrFold,trajectory,natData,minTime)
    #getShapeTrajectories(seqShapeDict,natData)

