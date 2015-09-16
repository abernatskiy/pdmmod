#/usr/bin/python

#format of the file is the following:
# time,specName specPopulation,specName specPopulation .....

#specPop -- {name: [populations during time steps]}
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import OrderedDict
from os import system as system
import numpy as np
import scipy
import math
import glob
import os
import subprocess

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

import routes
from dictUtils import *
#if dealing with HP-model import this
import hpClasses


class Result(object):
    def __init__(self,modelNum,simNum,reorganize=False,numOfRuns=None,traj=None):
        '''
            modelNum: int
            termCond: is a Tuple representing termination condition. It's one of:
              * ('simulateTime',int:simulation time,int: how often to record)
              * ('simulateReactions',int:number of reactions,int: 
                    how often to record)
              * ('simulateTillSteady',int: how often to record (time))
            numOfRuns: is Int repr. number of runs of the simulation
            traj: Bool, repr.:
              * True: keep data from individual runs
              * False: do not keep them, only mean and st.dev.
        '''
        self.modelNum = modelNum
        self.simNum = simNum
        self.path2Folder = routes.routePDM+'models/'+str("%03d" %self.modelNum)+'/'
        self.outputDir = self.path2Folder+\
            str("%03d" %self.modelNum)+'_output'+str(self.simNum)+'/'
        if not reorganize:
            self.parameters = self._readSimData()
            #self.means= self.readMeans()
            #self.stds = self.readStds()
            self.times = self._readTimes()
        else:
            self.reorganizeOutput(numOfRuns,traj)
            self.parameters = self._readSimData()
            self.times = self._readTimes()


    def _makeHeader(self,numOfRuns,traj):
        filename = 'traj0'
        proc =subprocess.call(
            ('rm '+self.outputDir+'parameters.txt'),shell=True)
        header = open(self.outputDir+'parameters.txt','a')
        f =open(self.outputDir+filename,'r')
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
                    self.howTerm = str(raw[2])
                    header.write('whenTerm '+raw[3]+'\n')
                    self.whenTerm = float(raw[3])
                    header.write('records '+raw[4]+'\n')
                    self.records = float(raw[4])
                    
            else:
                break
        
        header.write('==Simulation Parameters==\n')
        header.write('numOfRuns '+str(numOfRuns )+'\n')
        header.write('keepTrajectories '+str(traj)+'\n')
            
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
        for item in raw[1:len(raw)]:#TEST
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
    
    
    def _makeStatistics(self):
        files = [self.outputDir+'traj'+str(i) for i in range(self.numOfRuns)]
        handles = [open(t, 'r') for t in files]
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
                    print(
                        'Termination condition is met on line '+
                        str(count)+' in '+str(inFile))
                elif line[0]=="#":
                    continue
                else:
                    raw = (line.rstrip(',\n')).split(',')#TEST
                    if fileCount == 0:
                        count+=1
                        self.times.append(float(raw[0]))
                    fileCount += 1
                    self._line2Data(raw,points,fileCount)
            
            if not breakCondition:
                self._points2Evolutions(points,evolutions,count)
            else:
                actRecords = count+1
                print('number of points is '+str(actRecords))
                break
        
        [t.close() for t in handles]
        
        return evolutions, actRecords
    
    def _deleteTraj(self,outputDir):
        files = [outputDir+'traj'+str(i) for i in range(self.numOfRuns)]
        for traj in files:
            system('rm '+traj)
        
        return None
    
    def _writeEvolutions(self):#TODO
        evolutions, actRecords = self._makeStatistics()
        system('rm '+self.outputDir+'means.txt')
        system('rm '+self.outputDir+'standDivs.txt')
        fMeans = open(self.outputDir+'means.txt','a')
        fStd = open(self.outputDir+'standDivs.txt','a')
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
        
    def _writeTimes(self):
        string = str(self.times[0])
        for item in self.times[1:]:
            string += ' '+str(item)
        fTimes = open(self.outputDir+'times.txt','w')
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
        
    
    def reorganizeOutput(self,numOfRuns,traj):
        self.numOfRuns=numOfRuns
        self.traj=traj
        self._makeHeader(numOfRuns,traj)
        self._writeEvolutions()
        print('means and stds are written')
        self._writeTimes()
        #try:
            #self._writeRuntimesStats()
        #except:
            #self.log.warning('runtimes weren\'t saved. something went wrong. Perhabs you were running jobs in parallel.')
        if not self.traj:
            self._deleteTraj(outputDir)
            self._delRuntimes()
        system('rm '+self.outputDir+'shell*')
        system('rm '+self.outputDir+'run*')
        return None
    
    def _readTimes(self):
        with open(self.outputDir+'times.txt','r') as content_file:
            content = content_file.read()
        times =[float(item) for item in content.split(' ')]
        return times
    
    def readMeans(self):
        evolutions = {}
        f = open(self.path2Folder+str("%03d" %self.modelNum)+
                 '_output'+str(self.simNum)+'/means.txt','r')
        for line in f:
            raw = (line.rstrip('\n')).split(' ')
            #evolutions[raw[0]]=scipy.sparse.csr_matrix(np.array([float(item) for item in raw[1:]]))
            evolutions[raw[0]]=np.array([float(item) for item in raw[1:]])
            
        
        return evolutions
    
    def readStds(self):
        evolutions = {}
        f = open(self.path2Folder+str("%03d" %self.modelNum)+
                 '_output'+str(self.simNum)+'/standDivs.txt','r')
        for line in f:
            raw = (line.rstrip('\n')).split(' ')
            #evolutions[raw[0]]=scipy.sparse.csr_matrix(np.array([float(item) for item in raw[1:]]))
            evolutions[raw[0]]=np.array([float(item) for item in raw[1:]])
        
        return evolutions
    
    def _readSimData(self):
        header = open(self.outputDir+'parameters.txt','r')
        line = header.readline()
        parameters ={}
        while not line =='==Parameters==\n':
            self.name = line.rstrip('\n')
            line = header.readline()
        line = header.readline()
        while not line =='==Command==\n':
            _list = line.rstrip('\n').split(' ')
            parameters[_list[0]]=float(_list[1])
            line = header.readline()
        line = header.readline()
        self.howTerm = line.rstrip('\n').replace('howTerm ','')
        line = header.readline()
        self.whenTerm = int(line.rstrip('\n').replace('whenTerm ',''))
        line = header.readline()
        self.records = float(line.rstrip('\n').replace('records ',''))
        line = header.readline()
        line = header.readline()
        self.numOfRuns = int(line.rstrip('\n').replace('numOfRuns ',''))
        self.traj = bool(line.rstrip('\n').replace('keepTrajectories ',''))
        return parameters

    def makeStats(self,natData): 
        '''return countAll, countFold, countCat, countAuto, length
        means/stds -- {name: [populations during time steps]}'''
        try:
            print("total number of species in all runs is "+str(len(self.means.keys())))
        except:
            self.means= self.readMeans()
            self.stds = self.readStds()
            print("total number of species in all runs is "+str(len(self.means.keys())))
        natData=hpClasses.readNativeList(int(self.parameters['maxLength']))
        lengths=set([])     #keeps lengths present in simulation
        countAll = [(0)]*(len(self.times)) 
        countFold = [(0)]*(len(self.times)) 
        countCat = [(0)]*(len(self.times)) 
        countAuto = [(0)]*(len(self.times)) 
        #popStats={}#lengths distribution in the last moment of simulation
        #FIXME modify for sparse
        for key in self.means.keys():
            #means=self.means[key].A[0]
            means=self.means[key]
            if key.find('f')==-1:
                polLen=len(key)
                lengths.add(len(key))
            else:
                lengths.add(len(key)-1)
                polLen=len(key)-1
            for i in range(len(self.times)):
                    countAll[i]+=means[i] 
                    #adds population of current sequence at time i to 
                    #total population of all the sequences seen before 
                    fold, cat , autocat = hpClasses.getHPClassOfSeq(key,natData)
                    if fold:#TEST
                        countFold[i]+=means[i]
                        if cat:
                            countCat[i]+=means[i]
                            if autocat:
                                countAuto[i]+=means[i]
            #here we store lengths distribution in the last moment of simulation  
            #addToDictNum(popStats,polLen,self.means[key][-1])
            
        print('len',lengths)
        
        return countAll, countFold, countCat, countAuto, lengths
        
    
    def _kin2str(self):
        title = 'Model #'+str(self.modelNum)+'.'+str(self.simNum)+':\n'
        for parameter in self.parameters:
            title+=str(self.parameters[parameter])+', '
        return title
    
    def _writeGraphFilename(self,specDir=None):
        '''Results -> String (filename)
        
        '''
        def ifNameExists(name,specDir):
            sR=glob.glob(os.path.join(specDir,name))
            if sR==[]:
                return False
            else:
                return True
            
        if specDir==None:
            specDir = self.outputDir+'figures/'
        s='000'
        while ifNameExists(s+'.png',specDir):
            i=int(s)
            i+=1
            if len(str(i))==1:#LAME
                s='00'+str(i)
            elif len(str(i))==2:
                s='0'+str(i)
            elif len(str(i))>2:
                s=str(i)
        #if not ifNameExists(s)
        name=s+'.png'
            #if ifNameExists(name):
            #    raise('plot has been overwritten')
            
            
        path=os.path.join(specDir,name)
        
        return path
    
    def _plotTotalPop(self,fig,countAll):
        fig.plot(self.times,countAll,linewidth=4)
        fig.set_yscale('log')
        fig.set_ylabel('molecules count')
        fig.set_xlabel('time')
        fig.set_title("Total count of molecules at each moment")
        return None#times, countAll
    
    def _plotTypes(self,fig,countFold,countCat,countAuto):
        fig.plot(self.times,countFold,linewidth=4,label='folded')
        fig.plot(self.times,countCat,linewidth=4,label='catalysts')
        fig.plot(self.times,countAuto,linewidth=4,label='autocats')
        fig.legend()
        fig.set_ylabel('molecules count')
        fig.set_xlabel('time')
        fig.set_title("count of molecules of various types at each moment")
        return None#(times,countFold), (times,countCat), (times,countAuto)
    
    def _plotLenDistr(self,fig,mL,lengths,lengthsDistr):
        fig.plot(lengths,lengthsDistr,linewidth=4,label=\
            str(mL)+'/'+str(len(self.means.keys())))
        fig.grid(True)
        fig.set_yscale('log')
        fig.set_ylabel('average population')
        fig.set_xlabel('length')
        fig.set_title("Length distribution in the last moment")
        return None
        
    def plotHPstats(self,natData,jointData=None,
                    saveFig=False,nonSteadyPercent=0.9):
        maxLength = int(self.parameters['maxLength'])
        countAll, countFold, countCat, countAuto, lengths = \
            self.makeStats(natData)
        if jointData == None:
            try:
                jointData = self.jointData
                self.jointData.keys()
            except:
                self.jointData=self.makeDictOfLengths(maxLength,nonSteadyPercent)
                jointData=self.jointData
        
            
        mL=max(lengths)
        print("maximum length of a polymer is "+str(mL))
        lengths = list(jointData.copy().keys())
        lenPops = [
            sum([jointData[length][name][0] 
                 for name in jointData[length].keys()]) 
            for length in jointData.keys()
            ]
        tp=sum(lenPops)
        lengthsDistr=[ps/tp for ps in 
                  lenPops]
        

        fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(18,14))
        self._plotTotalPop(ax0,countAll)
        self._plotTypes(ax1,countFold,countCat,countAuto)
        print(lengthsDistr)
        print(list(lengths))
        self._plotLenDistr(ax2,mL,list(lengths),lengthsDistr)
        
        title = 'Statistics of a HP-wordl simulation run'
        fig.suptitle(title + ' for '+self.name)
        if not saveFig:
            plt.show()
        else:
            plt.suptitle(self._kin2str(), fontsize=20)
            plt.savefig(self._writeGraphFilename())
        
        return (countAll, countFold, countCat, countAuto), (list(lengths),lengthsDistr)

    def plotLenEvolution(self,show=True):
        '''
        '''
        return None


    def plotSpecific(self,listOfSeq,timeLims):
        arrays=[self.means[name] for name in listOfSeq]
        for (name,data) in zip (listOfSeq,arrays):
            if not 'f' in name:
                plt.plot(self.times,data,label=name,color='0.85',linewidth=3)
            else:
                plt.plot(self.times,data,label=name,linewidth=3)
        plt.legend()
        plt.title('Time evolutions of selected sequences',fontsize=30)
        plt.ylabel('Population',fontsize=22)
        plt.xlabel('Time',fontsize=22)
        plt.xlim(timeLims)
        plt.show()
        return None
    
    def getSteadyMeanStd(self,nonSteadyPercent):
        border=int(nonSteadyPercent*len(self.times))
        steadyMean={}
        steadyStd={}
        for seq in self.means.keys():
            #means=self.means[seq].A[0]
            means=self.means[seq]
            points=means[border:]
            steadyMean[seq]=np.mean(points)
            steadyStd[seq]=np.std(points)
        
        steadyMeanSorted = OrderedDict(
            sorted(steadyMean.items(), key=lambda t: t[1],reverse=True)
            )
        steadyStdSorted = OrderedDict(
            sorted(steadyStd.items(), key=lambda t: t[1],reverse=True)
            )
        
        return steadyMeanSorted, steadyStdSorted
    
    #def getSteadyStd(self,nonSteadyPercent):
        #border=int(nonSteadyPercent*len(self.times))
        #steady={}
        #for seq in self.means.keys():
            ##stds=self.stds[seq].A[0]
            #stds=self.means[seq]
            #points=stds[border:]
            #steady[seq]=np.mean(points)
        
        #steadySorted = OrderedDict(
            #sorted(steady.items(), key=lambda t: t[1],reverse=True)
            #)
        
        #return steadySorted
    
    def makeDictOfLengths(self,maxLength,nonSteadyPercent):
        '''returns dictionary of ordereder dictionaries
        {length: OrderedDict{seq: float}}
        '''
        steadyMean,steadyStd = self.getSteadyMeanStd(nonSteadyPercent)   #sortedDict
        
        steadyLen={}
        for i in range(1,maxLength+1):      #initialyze dicts
            steadyLen[i]={}
        
        #get sorted dictionary for every key of steadyLen
        for seq in steadyMean:
            if seq.find('f')==-1:
                sLen=len(seq)
            else:
                sLen=len(seq)-1
            if not (steadyMean[seq],steadyStd[seq])==(0.0,0.0):
                steadyLen[sLen][seq]=(steadyMean[seq],steadyStd[seq])
        
        for length in steadyLen.keys():
            tmp = OrderedDict(
                sorted(steadyLen[length].items(), key=lambda t: t[1],reverse=True)
                )
            steadyLen[length]=tmp
        
        return steadyLen
    
    def clustLengths(self,minLength,maxLength,
                     nonSteadyPercent,samp=None,epsilonModifyer={0:0}):#TEST
        ''' returns dict jointLabels'''
        if self.numOfRuns == 1:
            raise ValueError('I cannot cluster data from 1 simulation:'+
                ' standard deviation isn\'t defined')
        try:
            type(self.jointData)
        except:
            self.jointData=self.makeDictOfLengths(maxLength,nonSteadyPercent)
        jointLabels={}
        _labels={}
        labels={}
        epsilons = {}
        
        for length in range(minLength,maxLength+1):
            _labels[length] = []
            labels[length] = {}
            if not self.jointData[length]=={}:
                print('analyzing length '+str(length))
                lenOffset=length-minLength
                means = []
                stds = []
                indxes = {}
                i=-1
                for seq in self.jointData[length].keys():
                    i+=1
                    means.append(self.jointData[length][seq][0])
                    stds.append(self.jointData[length][seq][1])
                    indxes[i]=seq
                print('passed means')
                if samp == None:
                    samp = 10
                jointLabels[length], epsilons[length]=clustList(
                        means,stds,length,samp,epsilonModifyer)
                
                n_clusters = len(set(jointLabels[length])) - (1 if -1 in jointLabels[length] else 0)
                print('Estimated number of clusters: %d' % n_clusters)
            else:
                jointLabels[length] = np.array([])
            #i=-1
            for (i,seq) in indxes.items():
                try:
                    _labels[length].append((seq, jointLabels[length][i]))
                except IndexError:
                    if not self.jointData[length]==OrderedDict():
                        raise IndexError
                    else:
                        continue
                    
            if not _labels[length]==[]:
                for couple in _labels[length]:
                    addToDictList(labels[length],couple[1],couple[0])
            
            
        return labels, epsilons
    
    def enumerateAll(self,num2name=False,name2num=False):
        i=0
        if name2num and num2name:
            num2nameDict={}
            name2numDict={}
            for key in self.means.keys():
                num2nameDict[i]=key
                name2numDict[key]=i
                i+=1
            return name2numDict, num2nameDict
        elif name2num and (not num2name):
            name2numDict={}
            for key in self.means.keys():
                name2numDict[key]=i
                i+=1
            return name2numDict
        elif num2name and (not name2num):
            num2nameDict={}
            for key in self.means.keys():
                num2nameDict[i]=key
                i+=1
            return num2nameDict
        else:
            raise('what to do?')
            
            
            
    def getInitPopFromTraj(self,trajNum,atTime,initFileName):
        trajFile = open(os.path.join(self.path2Folder,
                    (str("%03d" %self.modelNum)+'_output'+str(self.simNum)),
                    'traj'+str(trajNum)),'r')
        time=0
        while not time == atTime:
            line = (trajFile.readline()).rstrip('\n')
            if line[0]=='#':
                continue
            else:
                raw = line.split(',')
                data = raw[1:]
                time = float(raw[0])
                print(time)
        initFile = open( os.path.join(self.path2Folder,
                    initFileName),'a')
        for point in data:
            initFile.write(point+'\n')
        return None    

#######EXTRA FUNCTIOS######

def median(mylist):
    sorts = sorted(mylist)
    length = len(sorts)
    if not length % 2:
        med = (sorts[int(length / 2)] + sorts[int(length / 2) - 1]) / 2.0
    med=sorts[int(length / 2)]
    if med==0.0:
        i=1
        while i<1000:
            med=sorts[int(length *i/(i+1))]
            i+=1
        if med==0.0:
            med = 0.0001
            print('artificial median of 0.0001 is set up')
        else:
            print('variance at '+str(i)+'/'+str(i+1))
    
    return med

def clustList(means,stds,length,samp,epsilonModifyer):
    X=np.array([means,[1]*len(means)]).T
    print('got X')
    med=median(stds)
    '''
    if length>8:
        epsilon=sqrt(med)*4
    elif length>12:
        epsilon=sqrt(med)*8
    else:
        epsilon=sqrt(med)
    '''
    epsilon=med
    if length in epsilonModifyer.keys():
        epsilon=epsilon*epsilonModifyer[length]
    print('epsilon='+str(epsilon))
    #jointEpsilon[length]=epsilon
    Y=StandardScaler(copy=True, with_mean=True, with_std=True).fit_transform(X)
    db = DBSCAN(epsilon, min_samples=samp).fit(X)
    core_samples = db.core_sample_indices_
    labels = db.labels_
    
    return labels, epsilon



if __name__ == "__main__":
    modelNum = 12
    simNum = 22
    r = Result(modelNum,simNum)
    r.getInitPopFromTraj(0,50.0,'populations50.txt')
    #r.plotHPstats()
    #steadyLen = r.makeDictOfLengths(25)
    #jointLabels, epsilons = r.clustLengths(14,25)
    

