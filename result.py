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
import math
import glob
import os

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

import routes
from dictUtils import *
#if dealing with HP-model import this
import hpClasses


class Result(object):
    def __init__(self,modelNum,simNum):
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
        self.parameters = self._readSimData()
        self.means= self._readMeans()
        self.stds = self._readStds()
        self.times = self._readTimes()
    
    def _readTimes(self):
        with open(self.outputDir+'times.txt','r') as content_file:
            content = content_file.read()
        times =[float(item) for item in content.split(' ')]
        return times
        
        
    def _readMeans(self):
        evolutions = {}
        f = open(self.path2Folder+str("%03d" %self.modelNum)+
                 '_output'+str(self.simNum)+'/means.txt','r')
        for line in f:
            raw = (line.rstrip('\n')).split(' ')
            evolutions[raw[0]]=[float(item) for item in raw[1:]]
            
        
        return evolutions
    
    def _readStds(self):
        evolutions = {}
        f = open(self.path2Folder+str("%03d" %self.modelNum)+
                 '_output'+str(self.simNum)+'/standDivs.txt','r')
        for line in f:
            raw = (line.rstrip('\n')).split(' ')
            evolutions[raw[0]]=[float(item) for item in raw[1:]]
        
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

    def makeStats(self): 
        '''return countAll, countFold, countCat, countAuto, length
        means/stds -- {name: [populations during time steps]}'''
        print("total number of species in all runs is "+str(len(self.means.keys())))
        natData=hpClasses.readNativeList(int(self.parameters['maxLength']))
        lengths=set([])     #keeps lengths present in simulation
        countAll = [(0)]*(len(self.times)) 
        countFold = [(0)]*(len(self.times)) 
        countCat = [(0)]*(len(self.times)) 
        countAuto = [(0)]*(len(self.times)) 
        #popStats={}#lengths distribution in the last moment of simulation
        for key in self.means.keys():
            if key.find('f')==-1:
                polLen=len(key)
                lengths.add(len(key))
            else:
                lengths.add(len(key)-1)
                polLen=len(key)-1
            for i in range(len(self.times)):
                    countAll[i]+=self.means[key][i] 
                    #adds population of current sequence at time i to 
                    #total population of all the sequences seen before 
                    fold, cat , autocat = hpClasses.getHPClassOfSeq(key,natData)
                    if fold:#TEST
                        countFold[i]+=self.means[key][i]
                        if cat:
                            countCat[i]+=self.means[key][i]
                            if autocat:
                                countAuto[i]+=self.means[key][i]
            #here we store lengths distribution in the last moment of simulation  
            #addToDictNum(popStats,polLen,self.means[key][-1])
            
            
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
        return None
    
    def _plotTypes(self,fig,countFold,countCat,countAuto):
        fig.plot(self.times,countFold,linewidth=4,label='folded')
        fig.plot(self.times,countCat,linewidth=4,label='catalysts')
        fig.plot(self.times,countAuto,linewidth=4,label='autocats')
        fig.legend()
        fig.set_ylabel('molecules count')
        fig.set_xlabel('time')
        fig.set_title("count of molecules of various types at each moment")
        return None
    
    def _plotLenDistr(self,fig,mL,lengths,lengthsDistr):
        fig.plot(lengths,lengthsDistr,linewidth=4,label=\
            str(mL)+'/'+str(len(self.means.keys())))
        fig.grid(True)
        fig.set_yscale('log')
        fig.set_ylabel('average population')
        fig.set_xlabel('length')
        fig.set_title("Length distribution in the last moment")
        return None
        
    def plotHPstats(self,jointData=None,saveFig=False,nonSteadyPercent=0.9):
        maxLength = int(self.parameters['maxLength'])
        countAll, countFold, countCat, countAuto, lengths = \
            self.makeStats()
        if jointData == None:
            try:
                jointData = self.jointData
                self.jointData.keys()
            except:
                self.jointData=self.makeDictOfLengths(maxLength,nonSteadyPercent)
                jointData=self.jointData
        
            
        mL=max(lengths)
        print("maximum length of a polymer is "+str(mL))
        #lengths = list(jointData.copy().keys())
        lenPops = [
            sum([jointData[length][name][0] 
                 for name in jointData[length].keys()]) 
            for length in jointData.keys()
            ]
        lengthsDistr=[ps/2**li for (ps,li) in 
                  zip(lenPops,list(lengths))]
        

        fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(18,14))
        self._plotTotalPop(ax0,countAll)
        self._plotTypes(ax1,countFold,countCat,countAuto)
        self._plotLenDistr(ax2,mL,list(lengths),lengthsDistr)
        
        title = 'Statistics of a HP-wordl simulation run'
        fig.suptitle(title + ' for '+self.name)
        if not saveFig:
            plt.show()
        else:
            plt.suptitle(self._kin2str(), fontsize=20)
            plt.savefig(self._writeGraphFilename())
        
        return None
    
    def plotLenEvolution(self,show=True):
        '''
        '''
        
        
        return None
        
    
    def getSteadyMean(self,nonSteadyPercent):
        border=int(nonSteadyPercent*len(self.times))
        steady={}
        for seq in self.means.keys():
            points=self.means[seq][border:]
            steady[seq]=np.mean(points)
        
        steadySorted = OrderedDict(
            sorted(steady.items(), key=lambda t: t[1],reverse=True)
            )
        
        return steadySorted
    
    def getSteadyStd(self,nonSteadyPercent):
        border=int(nonSteadyPercent*len(self.times))
        steady={}
        for seq in self.stds.keys():
            points=self.stds[seq][border:]
            steady[seq]=np.mean(points)
        
        steadySorted = OrderedDict(
            sorted(steady.items(), key=lambda t: t[1],reverse=True)
            )
        
        return steadySorted
    
    def makeDictOfLengths(self,maxLength,nonSteadyPercent):
        '''returns dictionary of ordereder dictionaries
        {length: OrderedDict{seq: float}}
        '''
        steadyMean = self.getSteadyMean(nonSteadyPercent)   #sortedDict
        steadyStd = self.getSteadyStd(nonSteadyPercent)     #sortedDict
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
    



def median(mylist):
    sorts = sorted(mylist)
    length = len(sorts)
    if not length % 2:
        med = (sorts[int(length / 2)] + sorts[int(length / 2) - 1]) / 2.0
    med=sorts[int(length / 2)]
    if med==0.0:
        i=1
        while med==0.0:
            med=sorts[int(length *i/(i+1))]
            i+=1
        print('variance at '+str(i)+'/'+str(i+1))
        if med==0.0:
            raise ValueError('Average=0!!!!!')
    
    return med

def clustList(means,stds,length,samp,epsilonModifyer):
    X=np.array([means,[1]*len(means)]).T
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
    modelNum = 13
    simNum = 2
    r = Result(modelNum,simNum)
    r.plotHPstats()
    #steadyLen = r.makeDictOfLengths(25)
    #jointLabels, epsilons = r.clustLengths(14,25)
    

