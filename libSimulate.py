#!/usr/bin/python
'''Library for a script which runs simulations 
'''
from os import system as system
from os import walk as walk
import numpy as np
import logging
#import cProfile

import subprocess
import itertools

from log_utils import init_log
import routes

class Simulation(object):
    def __init__(self,modelNum,termCond,
                 numOfRuns=1,traj=False,log_level='WARNING'):
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
        self.log_level = log_level
        
    def __str__(self):
        str1 = ('Simulation of the model '+str(self.modelNum)+
                '. Termination condition: '+str(self.howTerm)+
                ' ('+str(self.whenTerm)+' rec. every '+str(self.records)+')'+
                ' with '+str(self.numOfRuns)+' repetitions. ')
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
            return 'simulateTillSteady', '',termCond[2]
            #FIXME '' won't do in the future
        else:
            raise ValueError("Unknown termination condition, check if typo")
    
    def makeOutputFolder(self,rewrite):#seems to be working OK
        path = str(routes.routePDM+'models/'+str("%03d" %self.modelNum)+'/')
        if rewrite:
            system('rm -r '+path+str("%03d" %self.modelNum)+'_output*')
            system('mkdir '+path+str("%03d" %self.modelNum)+'_output0/')
            #print('rm -r '+path+str("%03d" %self.modelNum)+'_output*')
            #print('mkdir '+path+str("%03d" %self.modelNum)+'_output0/')
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
            system('mkdir '+path+str("%03d" %self.modelNum)+
                   '_output'+str(currentRun)+'/')
            #print('mkdir '+path+str("%03d" %self.modelNum)+
            #      '_output'+str(currentRun)+'/')
        
        outputDir = path+str("%03d" %self.modelNum)+'_output'+str(currentRun)+'/'
        self.outputDir = outputDir
        self.log = init_log(self.log_level,log_path=outputDir+'sim.log')
        return outputDir
    
    def runSeveralSeries(self,rewrite):
        '''runs several simulations sequentially, 
        stores average, st.deviation and optionally trajectories
        '''
        self.outputDir = self.makeOutputFolder(rewrite)
        for i in range(numOfRuns):
            command = (self.path2Folder+'pdmmod',
                        str(self.howTerm), 
                        str(self.whenTerm), 
                        str(self.records),
                        self.outputDir+'traj'+str(i))
            subprocess.call(command)
            self.log.info(str(command))
            
        return None
    
    def _makeHeader(self,outputDir):
        filename = 'traj0'
        proc =subprocess.call(
            ('rm '+outputDir+'parameters.txt'),shell=True)
        self.log.warning(proc)
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
    
    def _points2Evolutions(self,points,evolutions,count):
        for spec in points.keys():
                    if self.numOfRuns ==1:
                        points[spec]=(np.mean(points[spec]),0)
                    else:
                        points[spec]=(np.mean(points[spec]),np.std(points[spec]))
                    
                    if spec not in evolutions:
                        #add it and its population
                        #also add 0s as prev times populations
                        evolutions[spec]=np.zeros(
                            int(self.whenTerm/self.records+1), dtype=(float,2))
                        #FIXME this one has to be fluid to handle simulateTillSteady
                        evolutions[spec][count]=points[spec]
                    else:
                        #otherwise append new point to the existing list of points
                        evolutions[spec][count]=points[spec]

        return None
    
    def _line2Data(self,raw,points,fileCount):
        for item in raw[1:len(raw)-1]:
            #get a couple specie -- its population
            point=item.split(' ')
            if point[0] not in points:
                #add it and its population
                #also add 0s as prev times populations
                #print('point in the second file',point)
                points[point[0]]=np.zeros(self.numOfRuns)
                points[point[0]][fileCount-1]=int(point[1])
            else:
                points[point[0]][fileCount-1]=int(point[1])
        return None
    
    
    def _makeStatistics(self,outputDir):
        files = [outputDir+'traj'+str(i) for i in range(self.numOfRuns)]
        handles = [open(t, 'r') for t in files]
        self.log.info(str(files))
        count = -1 #counts time instances
        evolutions = {}
        self.times = []
        breakCondition = False
        while not breakCondition:
            points = {}
            #keeps populations of species at the given moment across files
            fileCount = 0
            for inFile in handles:
                line = inFile.readline()
                if line =='':
                    breakCondition = True
                    self.log.info(
                        'Termination condition is met on line '+
                        str(count)+' in '+str(inFile))
                elif line[0]=="#":
                    continue
                else:
                    raw = (line.rstrip('\n')).split(',')
                    if fileCount == 0:
                        count+=1
                        self.times.append(float(raw[0]))
                    fileCount += 1
                    self._line2Data(raw,points,fileCount)
            
            if not breakCondition:
                self._points2Evolutions(points,evolutions,count)
            else:
                actRecords = count+1
                self.log.info('number of points is '+str(actRecords))
                break
        
        [t.close() for t in handles]
        
        return evolutions, actRecords
    
    def _deleteTraj(self,outputDir):
        files = [outputDir+'traj'+str(i) for i in range(self.numOfRuns)]
        for traj in files:
            system('rm '+traj)
        
        return None
    
    def _writeEvolutions(self,outputDir):#TEST
        evolutions, actRecords = self._makeStatistics(outputDir)
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
        
    def _writeTimes(self,outputDir):
        string = str(self.times[0])
        for item in self.times[1:]:
            string += ' '+str(item)
        fTimes = open(outputDir+'times.txt','w')
        fTimes.write(string)
        fTimes.close()
        return None
    
    def reorganizeOutput(self,outputDir=None):
        if outputDir == None:
            outputDir = self.outputDir
        self._makeHeader(outputDir)
        self._writeEvolutions(outputDir)
        self._writeTimes(outputDir)
        if not self.traj:
            self._deleteTraj(outputDir)
        return None
    
    
        
    
    def runSeveralParallelPC():#TODO
        '''
        '''
        
        return None

if __name__ == "__main__":
    modelNum = 12
    termCond = ('simulateTime',20,1)
    numOfRuns = 3
    traj = False
    rewrite = False
    log_level = 'INFO'
    s = Simulation(modelNum,termCond,numOfRuns,traj,log_level)
    s.runSeveralSeries(rewrite)
    s.reorganizeOutput()
















