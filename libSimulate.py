#!/usr/bin/python
'''Library for a script which runs simulations 
'''
from os import system as system
from os import walk as walk
from statistics import mean
from statistics import variance
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
    
    def runSeveralSeries(self,rewrite):#TEST
        '''runs several simulations sequentially, store average, st.deviation and optionally trajectories
        '''
        outputDir = self.makeOutputFolder(rewrite)
        for i in range(numOfRuns):
            command = (self.path2Folder+'pdmmod'),str(self.howTerm), str(self.whenTerm), str(self.records),outputDir+'traj'+str(i)
            #subprocess.call(command)TODO
            print(command)
            
        return None
    
    def reorganizeOutput(self,outputDir=None):
        if outputDir == None:
            outputDir = self.outputDir
        files = [outputDir+'traj'+str(i) for i in range(self.numOfRuns)]
        handles = [open(t, 'r') for t in files]
        print(files)
        count = 0 #counts time instances
        evolutions = {}
        records = set([])#FIXME probably gonna be slow
        for i in range(4):#FIXME remove 10. this one has to be fluid to handle simulateTillSteady
            points = {}#keeps populations of species at the given moment across files
            fileCount = 0
            for inFile in handles:
                line = inFile.readline()
                if line[0]=="#":
                    continue
                else:
                    fileCount += 1
                    #count+=1
                    raw = (line.rstrip('\n')).split(',')
                    records.add(int(float(raw[0])))#FIXME remove int
                    for item in raw[1:len(raw)-1]:
                        #get a couple specie -- its population
                        point=item.split(' ')
                        if point[0] not in points:
                            #add it and its population
                            #also add 0s as prev times populations
                            if not fileCount==1:
                                #print('point in the second file',point)
                                points[point[0]]=[0]*(fileCount-1)
                                points[point[0]].append(int(point[1]))
                            else:
                                #print('point in the first file',point)
                                points[point[0]]=[int(point[1])]
                        else:
                            #otherwise append new point to the existing list of points
                            points[point[0]].append(int(point[1]))
            for spec in points.keys():
                if len(points[spec])==fileCount:
                    continue
                elif len(points[spec])==fileCount-1:
                    points[spec].append(0)
                else:
                    print(spec)
                    print('length',len(points[spec]))
                    print('fileCount',fileCount)
                    raise ValueError("!")
            if not self.numOfRuns ==1:
                for spec in points.keys():
                    insert into evolutions dict.
                
            
        print(points)
        print(records)
        [t.close() for t in handles]

    def runSeveralParallelPC():#TODO
        '''
        '''
        
        return None

modelNum = 12
termCond = ('simulateTime',500,5)
numOfRuns = 2
s = Simulation(modelNum,termCond,numOfRuns)
#s.runSeveralSeries(True)
outputDir = '/data/research/06.origins_of_life/pdmmod/models/012/012_output0/'
s.reorganizeOutput(outputDir)


















