#!/usr/bin/python
'''Library for a script which runs simulations 
'''
from os import system as system
from os import walk as walk
import numpy as np
import logging
#import cProfile
import math
import time
import subprocess
import itertools

from log_utils import init_log
import routes
try:
    from parameters import correspond
except:
    correspond = {}

def castType(typeName,string):
    if typeName == 'int':
        return int(string)
    elif typeName == 'float':
        return float(string)
    elif typeName == 'bool':
        return bool(string)

class Simulation(object):
    def __init__(self,modelNum,termCond,rewrite,
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
        self.outputDir = self.makeOutputFolder(rewrite)
        
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
    
    def _formCommand(self,trajNum,paramFile,populFile):
        command = (self.path2Folder+'pdmmod',
                    str(self.howTerm), 
                    str(self.whenTerm), 
                    str(self.records),
                    self.outputDir+'traj'+str(trajNum),
                    '-c',paramFile,
                    '-i',populFile)
        return command
        
    
    def runSeveralSeries(self,paramFile=None,populFile=None):
        '''runs several simulations sequentially, 
        stores average, st.deviation and optionally trajectories
        '''
        if paramFile == None:
            paramFile = self.path2Folder+'parameters.ini'
        if populFile == None:
            populFile = self.path2Folder+'populations.txt'
        for trajNum in range(self.numOfRuns):
            command = self._formCommand(trajNum,paramFile,populFile)
            subprocess.call(command)
            self.log.info(str(command))
            subprocess.call(("mv",
                             self.path2Folder+"runtime.txt",
                             self.outputDir+"timePerReac"+str(trajNum)))
            
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
    
    def _writeRuntimesStats(self):
        runtimes = []
        files = [self.outputDir+'timePerReac'+str(i) 
                 for i in range(self.numOfRuns)]
        for f in files:
            with open(f,'r') as cf:
                runtimes.append(float(cf.read().rstrip('\n')))
            cf.close()
        mean = np.mean(runtimes)
        std = np.std(runtimes)
        with open(self.outputDir+'runtimeStat.txt','w') as wf:
            wf.write(str(mean)+' '+str(std))
        wf.close()
        
        return None
    
    def _delRuntimes(self):
        files = [self.outputDir+'timePerReac'+str(i) 
                 for i in range(self.numOfRuns)]
        for f in files:
            system('rm '+f)
        return None
        
    
    def reorganizeOutput(self,outputDir=None):
        if outputDir == None:
            outputDir = self.outputDir
        self._makeHeader(outputDir)
        self._writeEvolutions(outputDir)
        self._writeTimes(outputDir)
        self._writeRuntimesStats()
        if not self.traj:
            self._deleteTraj(outputDir)
            self._delRuntimes()
        return None
    
    def _makeShell(self,outputDir,kernelNum,pythonFile,onNode):
        shell = self.outputDir+'shell'+str(kernelNum)
        inFile = open(shell,'w')
        infile.close()
        inFile = open(shell,'a')
        inFile.write('#!/bin/bash\n')
        inFile.write('#$ -S /bin/bash\n')
        inFile.write('#$ -N simpdm'+str(kernelNum)+'\n')
        inFile.write('#$ -cwd\n')
        if onNode == 0:
            inFile.write('#$ -q cpu_long\n')
        else:
            inFile.write('#$ -q cpu_long@node'+str("%03d" %onNode)+'\n')
        inFile.write('#$ -P kenprj\n')
        inFile.write('\n')
        inFile.write('cd '+self.path2Folder+'\n')
        inFile.write(routes.path2python+' '+str(pythonFile)+'\n')
        inFile.close()
        
        
        return shell
    
    def _writePython(self,outputDir,kernelNum,trajFirst,trajLast):
        pythonFile = self.outputDir+'run'+str(kernelNum)+'.py'
        #system('echo "" > '+str(pythonFile))
        inFile = open(pythonFile,'a')
        inFile.write('#!'+routes.path2python+'\n')
        inFile.write('import subprocess\n')
        inFile.write('subprocess.call("pwd",)'+'\n')
        #inFile.write('subprocess.call(("cp","../parameters.ini","./"))'+'\n')
        
        for j in range(trajFirst,trajLast+1):
            command = (self.path2Folder+'pdmmod',
                        str(self.howTerm), 
                        str(self.whenTerm), 
                        str(self.records),
                        self.outputDir+'traj'+str(j))
            inFile.write('subprocess.call('+str(command)+')'+'\n')
            inFile.write('subprocess.call(("mv","'+
                            self.path2Folder+'runtime.txt","'+
                            self.outputDir+"timePerReac"+str(j)+'"))'+'\n')
            
            
        inFile.close()
        return pythonFile
    
    def _addToQueue(self,outputDir,kernelNum,trajFirst,trajLast,jobsRun,onNode):
        pythonFile = self._writePython(outputDir,kernelNum,trajFirst,trajLast)
        shell = self._makeShell(outputDir,kernelNum,pythonFile,onNode)
        #system('cat '+pythonFile)
        #system('cat '+shell)
        print(str(shell))
        p =subprocess.Popen(('qsub',shell),
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
        out, err = p.communicate() 
        self.log.info(out.decode())
        self.log.warning(err.decode())
        output = out.decode().split(' ')
        print(output)
        jobsRun.append(int(output[2]))
            
        return None
    
    def _wait(self,jobsRun):#FIXME termination condition
        '''waits until all the simulations done running'''
        def checkJobsOnClust():
            p = subprocess.Popen('qstat', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()

            lines = (out.decode().split('\n'))[2:]
            jobsOnClust = []
            for line in lines:
                items =line.split(' ')
                try:
                    jobsOnClust.append(int(items[1]))
                except:
                    continue
            return jobsOnClust
        
        def ifJobsDone(jobsOnClust,jobsRun):
            jobsDoneList = []
            for job in jobsRun:
                if job in jobsOnClust:
                    return False
                else:
                    jobsDoneList.append(job)
            if set(jobsRun)==set(jobsDoneList):
                return True
            
            
        
        jobsDone = False
        while not jobsDone:
            time.sleep(10)
            jobsOnClust = checkJobsOnClust()
            jobsDone = ifJobsDone(jobsOnClust,jobsRun)
            
        return None
    
    def runSeveralParallelCluster(self,kernels=None,onNode=0):
        jobsRun = []
        if kernels == None:
            kernels = self.numOfRuns
        perKernel = int(math.ceil(self.numOfRuns/kernels))
        lastKernel = self.numOfRuns - perKernel*(kernels-1)
        
        for i in range(kernels-1):
            trajFirst = i*perKernel
            trajLast = int((i+1)*perKernel - 1)
            self.log.info('kernel'+str(i))
            self._addToQueue(self.outputDir,i,trajFirst,trajLast,jobsRun,onNode)
        if kernels == 1:
            i = -1
            trajLast = -1
        self.log.info('last kernel')
        self._addToQueue(self.outputDir,i+1,trajLast+1,self.numOfRuns-1,jobsRun,onNode)
        self._wait(jobsRun)
        self.log.warning('all simulation finished running. calculationg averages and stds')
        return None
        
    
    def runSeveralParallelPC():#TODO
        '''
        '''
        
        return None
    

class SimulationsSet(object):
    '''reads parameters from file paramSpace.txt, forms parmeters.ini
    creates Simulation with given parameters
    ??
    '''
    def __init__(self,modelNum,termCond,
                 numOfRuns=1,traj=False,log_level='WARNING'):
        self.modelNum = modelNum
        self.termCond = termCond
        self.numOfRuns = numOfRuns
        self.traj = traj
        self.log_level = log_level
        self.path2Folder = \
            routes.routePDM+'models/'+str("%03d" %self.modelNum)+'/'
        
        self.correspond = correspond
        if self.correspond == {}:
            raise ValueError('I need to have a parameters.py file'+
                             'to read set of parameters')
        
    def readSet(self):#TODO
        parameters = {}
        for i in correspond.keys():
            parameters[correspond[i][0]]=[]
        pf = open('paramSet.txt','r')
        for line in pf:
            raw = line.rstrip('\n').split(' ')
            for i in range(len(raw)):
                parameters[correspond[i][0]] = \
                    castType(correspond[i][1],raw[i])
        
    
    
    
        
    
    
    def initParams(self,simulation):
        return None
    
    
    def runSimsOnPC(self):
        #read file with parameters 
        #for line in the file:
            #form simulation
            #run simulation
            #put it into database
        return None
    
    def runSimsOnCluster(self):
        #read file with parameters
        #for line in the file:
            #form simulation
            #submit simulation
            #put it into database
        return None
    
        
        

#TESTING
if __name__ == "__main__":
    modelNum = 12
    termCond = ('simulateTime',30,3)
    numOfRuns = 3
    traj = False
    #rewrite = True
    log_level = 'INFO'
    s = Simulation(modelNum,termCond,rewrite,numOfRuns,traj,log_level)
    #s.runSeveralSeries()
    ##s.runSeveralParallelCluster(kernels=3, onNode=0)
    #s.reorganizeOutput()
    #ss = SimulationsSet(modelNum,termCond,numOfRuns,traj,log_level)
















