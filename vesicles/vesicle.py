#!/usr/bin/python
import os
import random
import sys
sys.path.append('../')

import libSimulate

def countWeight(points):
    weight = 0
    for (seq, pop) in points.items():
        if not seq[0] =='f':
            weight+=len(seq)*pop
        else:
            weight+=(len(seq)-1)*pop
    return weight

class Vesicle(object):
    '''class representing a vesicle containing some sequences
     * matureWeight - Int. -  weight in terms of number of monomers,
        at which vesicles divide. They split into 2 vesicles with equal weights.
     * generation - Int. - we start from mother vesicles (generation 0), 
        its daughter is generation 1, ect
     * sequences - Dict. - {sequnce name: sequnce population}#TODO SeqInClust??
     * modelNum - Int. - model, which governs chemistry in the vesicle
     * path - String. - containing folder.
    '''
    def __init__(self,generation,sequences,idInGen,motherIdInGen,matureWeight,modelNum,path):
        self.idInGen = idInGen
        self.sequencesAtBirth = sequences
        self.motherIdInGen = motherIdInGen
        self.generation=generation
        self.matureWeight=matureWeight
        self.modelNum = modelNum
        self.path = path
        self.outPath=os.path.join(self.path,str("%04d" %self.generation))
        self.initFile = self._getInitPopFile()
        
    def __str__(self):
        str1='Vesicle '+str(self.generation)+' of mature weight '+\
            str(self.matureWeight)
        return str1
    
    def __repr__(self):
        str1='Vesicle '+str(self.generation)
        return str1


    def _getInitPopFile(self):#TEST
        populFile = os.path.join(
            self.path,str("%04d" %self.generation),'initPop'+str("%05d" %self.idInGen))
        return populFile
    
    def _findMature(self):
        def line2Data(raw):
            points = {}
            for item in raw[1:len(raw)-1]:
                #get a couple specie -- its population
                point=item.split(' ')
                points[point[0]]=int(point[1])
            return points
        
        simRes = open(os.path.join(self.outPath,'traj0'),'r')
        growth = open(os.path.join(self.outPath,'growth'+str("%05d" %self.idInGen)),'w')
        growth.close()
        growth = open(os.path.join(self.outPath,'growth'+str("%05d" %self.idInGen)),'a')
        for line in simRes:
            if line[0]=="#":
                continue
            else:
                growth.write(line)
                raw = (line.rstrip('\n')).split(',')
                points = line2Data(raw)
                weight = countWeight(points)
                #print(weight)
                if weight>=self.matureWeight:
                    timeMature = float(raw[0])
                    break
        simRes.close()
        growth.close()
        return timeMature,points
        
        

    def growCell(self,termTime,timeStep):#TODO
        '''
        form Simulation with special path
        run until some known time
        find time, when the mass of the vesicle == matureWeight
        rewrite trajectory till this time as generation 0
        split randomly
        '''
        sDef = libSimulate.Simulation(
                self.modelNum,
                termCond=('simulateTime',termTime,timeStep),
                rewrite=False,
                specialPath = self.outPath,
                numOfRuns=1,
                traj=True,
                log_level='WARNING')
        sDef.runSeveralSeries(paramFile=None,populFile=self.initFile)
        timeMature, sequencesAtSplit = self._findMature()#TEST
        return sequencesAtSplit
        
        
    def splitCell(self,sequencesAtSplit):
        daughter1=Vesicle(
            self.generation+1,
            {},
            self.idInGen*2,
            idInGen,
            self.matureWeight,
            self.modelNum,
            path)
        daughter2=Vesicle(
            self.generation+1,
            {},
            self.idInGen*2+1,
            idInGen,
            self.matureWeight,
            self.modelNum,
            path)
        megaList = []
        for (seq, pop) in sequencesAtSplit.items():
            megaList+=[seq]*pop
        random.shuffle(megaList)
        list1=megaList[:int(len(megaList)/2)]
        list2=megaList[int(len(megaList)/2):]
        for item in list1:
            daughter1.sequencesAtBirth[item]=list1.count(item)
        for item in list2:
            daughter2.sequencesAtBirth[item]=list2.count(item)
        print('d1 weight: '+str(countWeight(daughter1.sequencesAtBirth)))
        print('d2 weight: '+str(countWeight(daughter2.sequencesAtBirth)))
        
        return daughter1, daughter2
    
    def growAndSplit(self,termTime,timeStep,numOfGenerations,keepAll):#TEST
        '''
        '''
        vesicles = [self]
        currGeneration = 0
        while currGeneration < numOfGenerations:
            nextGen = []
            for vesicle in vesicles:
                vesicle.sequencesAtSplit = vesicle.growCell(termTime,timeStep)#TEST
                daughter1, daughter2 = vesicle.splitCell(vesicle.sequencesAtSplit)
                #return daughter1, daughter2
                try:
                    os.makedirs(daughter1.outPath)
                except FileExistsError:
                    print('dir exists')
                #os.makedirs(daughter2.outPath)
                init1 = open(daughter1.initFile,'w')
                init1.close()
                init1 = open(daughter1.initFile,'a')
                for (seq, pop) in daughter1.sequencesAtBirth.items():
                    init1.write(seq+' '+str(pop)+'\n')
                init1.close()
                
                if keepAll:
                    init2 = open(daughter2.initFile,'w')
                    init2.close()
                    init2 = open(daughter2.initFile,'a')
                
                    for (seq, pop) in daughter2.sequencesAtBirth.items():
                        init2.write(seq+' '+str(pop)+'\n')
                    init2.close()
                
                
                nextGen.append(daughter1)
                if keepAll:
                    nextGen.append(daughter2)
            vesicles = nextGen
            currGeneration+=1
            
        
        return vesicles
    
if __name__ == "__main__":     
    idInGen =0
    sequences={'H':20,'P':20}
    motherIdInGen = 0
    generation = 0
    matureWeight = 300
    modelNum = 12
    path = './'
    termTime = 5
    timeStep = 0.5
    numOfGenerations = 3
    v = Vesicle(generation,sequences,idInGen,motherIdInGen,matureWeight,modelNum,path)
    vs = v.growAndSplit(termTime,timeStep,numOfGenerations,True)
    