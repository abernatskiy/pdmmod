#!/usr/bin/python
'''Library for a script which runs simulations 
'''
from os import system as system
from os import walk as walk
import numpy as np

import cProfile

import subprocess
import routes
import itertools

class Simulation(object):
    def __init__(self,modelNum,termCond,numOfRuns=1,traj=False):
        '''
            modelNum: int
            termCond: is a Tuple representing termination condition. It's one of:
              * ('simulateTime',int:simulation time,int: how often to record)
              * ('simulateReactions',int:number of reactions,int: how often to record)
              * ('simulateTillSteady',int: how often to record (time))
            numOfRuns: is Int repr. number of runs of the simulation
            traj: Bool, repr.:
              * True: keep data from individual runs
              * False: do not keep them, only mean and st.dev.
        '''
        self.modelNum = modelNum
        self.howTerm, self.whenTerm, self.records = self.getTermConds(termCond)
        self.numOfRuns = numOfRuns
        self.traj = traj
        self.path2Folder = routes.routePDM+'models/'+str("%03d" %self.modelNum)+'/'
        
    def __str__(self):
        str1 = 'Simulation of the model '+str(self.modelNum)+'. Termination condition: '+str(self.howTerm)\
            +' ('+str(self.whenTerm)+' rec. every '+str(self.records)+') with '+str(self.numOfRuns)+' repetitions. '
        if self.traj:
            str1+='Trajectories are kept\n'
        else:
            str1+='Trajectories are NOT kept\n'
        return str1
    
    def __repr__(self):
        str1 = 'Simulation of the model '+str(self.modelNum)+'. Termination condition: '+str(self.howTerm)\
            +' ('+str(self.whenTerm)+' rec. every '+str(self.records)+') with '+str(self.numOfRuns)+' repetitions. '
        if self.traj:
            str1+='Trajectories are kept\n'
        else:
            str1+='Trajectories are NOT kept\n'
        return str1
    
    def getTermConds(self,termCond):
        if termCond[0]=='simulateTime':
            return 'simulateTime', termCond[1],termCond[2]
        elif termCond[0]=='simulateReactions':
            return 'simulateReactions', termCond[1],termCond[2]
        elif termCond[0]=='simulateTillSteady':
            return 'simulateTillSteady', '',termCond[2]#FIXME '' won't do in the future
        else:
            raise ValueError("Unknown termination condition, check if typo")
    
    def makeOutputFolder(self,rewrite):#seems to be working OK
        path = str(routes.routePDM+'models/'+str("%03d" %self.modelNum)+'/')
        if rewrite:
            system('rm -r '+path+str("%03d" %self.modelNum)+'_output*')
            system('mkdir '+path+str("%03d" %self.modelNum)+'_output0/')
            print('rm -r '+path+str("%03d" %self.modelNum)+'_output*')
            print('mkdir '+path+str("%03d" %self.modelNum)+'_output0/')
            currentRun = 0
        else:
            dirs=(next(walk(path))[1])
            print(dirs)
            nums = []
            for directory in dirs:
                if '_output' in directory:
                    tmp = directory.replace(str("%03d" %self.modelNum)+'_output','')
                    if tmp == '':
                        nums.append(0)
                    else:
                        nums.append(int(tmp))
            if nums ==[]:
                currentRun = 0
            else:
                currentRun = max(nums)+1
            system('mkdir '+path+str("%03d" %self.modelNum)+'_output'+str(currentRun)+'/')
            print('mkdir '+path+str("%03d" %self.modelNum)+'_output'+str(currentRun)+'/')
        
        outputDir = path+str("%03d" %self.modelNum)+'_output'+str(currentRun)+'/'
        self.outputDir = outputDir
        return outputDir
    
    def runSeveralSeries(self,rewrite):
        '''runs several simulations sequentially, store average, st.deviation and optionally trajectories
        '''
        outputDir = self.makeOutputFolder(rewrite)
        for i in range(numOfRuns):
            command = (self.path2Folder+'pdmmod'),str(self.howTerm), str(self.whenTerm), str(self.records),outputDir+'traj'+str(i)
            subprocess.call(command)
            print(command)
            
        return None
    
    def makeHeader(self,outputDir=None):
        filename = 'traj0'
        system('rm '+outputDir+'parameters.txt')
        header = open(outputDir+'parameters.txt','a')
        f =open(outputDir+filename,'r')
        for line in f:
            if line[0]=='#':
                raw = (line[2:].rstrip('\n')).split(' ')
                group = '=='+raw[0].rstrip(':')+'==\n'
                header.write(group)
                if raw[0]=='Model:':
                    header.write(raw[1]+'\n')
                elif raw[0]=='Parameters:':
                    for item in raw[1:]:
                        pair = item.split('=')
                        header.write(pair[0]+' '+pair[1]+'\n')
                elif raw[0]=='Command:':
                    header.write('howTerm '+raw[2]+'\n')
                    header.write('whenTerm '+raw[3]+'\n')
                    header.write('records '+raw[4]+'\n')
                    
            else:
                break
        
        header.write('==Simulation Parameters==\n')
        header.write('numOfRuns '+str(self.numOfRuns )+'\n')
        header.write('keepTrajectories '+str(self.traj)+'\n')
            
        return None
            
    
    def makeStatistics(self,outputDir=None):
        if outputDir == None:
            outputDir = self.outputDir
        files = [outputDir+'traj'+str(i) for i in range(self.numOfRuns)]
        handles = [open(t, 'r') for t in files]
        print(files)
        count = 0 #counts time instances
        evolutions = {}
        records = set([])
        breakCondition = False
        while not breakCondition:
            #print(count)
            points = {}#keeps populations of species at the given moment across files
            fileCount = 0
            for inFile in handles:
                line = inFile.readline()
                if line =='':
                    breakCondition = True
                    print('i met condition in ',count,'line, in',str(inFile))
                elif line[0]=="#":
                    continue
                else:
                    if fileCount ==0:
                        count+=1
                    fileCount += 1
                    #count+=1
                    raw = (line.rstrip('\n')).split(',')
                    records.add(float(raw[0]))
                    for item in raw[1:len(raw)-1]:
                        #get a couple specie -- its population
                        point=item.split(' ')
                        if point[0] not in points:
                            #add it and its population
                            #also add 0s as prev times populations
                                #print('point in the second file',point)
                                points[point[0]]=np.zeros(self.numOfRuns)
                                points[point[0]][fileCount-1]=int(point[1])#TEST
                        else:
                            points[point[0]][fileCount-1]=int(point[1])
            if not breakCondition:
                #print('b',count,str(points['P']))
                for spec in points.keys():
                    if self.numOfRuns ==1:
                        points[spec]=(np.mean(points[spec]),0)
                    else:
                        points[spec]=(np.mean(points[spec]),np.std(points[spec]))
                    
                    if spec not in evolutions:
                        #add it and its population
                        #also add 0s as prev times populations
                        evolutions[spec]=np.zeros(int(self.whenTerm/self.records), dtype=(float,2))#FIXME this one has to be fluid to handle simulateTillSteady
                        evolutions[spec][count-1]=points[spec]
                    else:
                        #otherwise append new point to the existing list of points
                        evolutions[spec][count-1]=points[spec]
            else:
                actRecords = count -1
                print('number of points is',actRecords)
                break
        
        [t.close() for t in handles]
        
        return evolutions, actRecords
    
    def reorganizeOutput(self,outputDir=None):
        if outputDir == None:
            outputDir = self.outputDir
        def writeEvolutions(evolutions,actRecords,outputDir):
            system('rm '+outputDir+'means.txt')
            system('rm '+outputDir+'standDivs.txt')
            fMeans = open(outputDir+'means.txt','a')
            fStd = open(outputDir+'standDivs.txt','a')
            for spec in evolutions:
                printMean = spec
                printStd = spec
                for item in evolutions[spec][0:actRecords]:
                    printMean+=' '+str(item[0])
                    printStd+=' '+str(item[1])
                fMeans.write(printMean+'\n')
                fStd.write(printStd+'\n')
            fMeans.close()
            fStd.close()
            
            return None
        evolutions, actRecords = self.makeStatistics(outputDir)
        if traj:
            writeEvolutions(evolutions,actRecords,outputDir)
        else:
            writeEvolutions(evolutions,actRecords,outputDir)
            deleteTraj()#TODO

    def runSeveralParallelPC():#TODO
        '''
        '''
        
        return None

if __name__ == "__main__":
    modelNum = 12
    termCond = ('simulateTime',200,2)
    numOfRuns = 10
    traj = True
    rewrite = False
    s = Simulation(modelNum,termCond,numOfRuns,traj)
    s.runSeveralSeries(rewrite)
    s.makeHeader(outputDir)
    #evo = s.makeStatistics()
    s.reorganizeOutput(outputDir)
















