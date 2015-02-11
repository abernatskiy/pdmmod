#/usr/bin/python

#format of the file is the following:
# time,specName specPopulation,specName specPopulation .....

#specPop -- {name: [populations during time steps]}

import matplotlib.pyplot as plt
from statistics import mean
from collections import OrderedDict
from os import system as system

class Result(object):
    def __init__(self,filename):
        self.times, self.specPop, self.modelName, self.parameters, self.simParams = self.readData(filename)
        self.directory, self.filename = self.createDestination(filename)
        

    def __repr__(self):
        return "the results of the simulation of the model \"" + self.modelName + "\" run over " + self.simParams["TotalTime"]
    
    def __str__(self):
        string = "the results of the simulation of the " + self.modelName + " with parameters:\n"
        for key in self.parameters:
            string+=key+" = "+self.parameters[key]+'\n'
        for key in self.simParams:
            string+=key+" = "+self.simParams[key]+'\n'
            
        return string

    def readData(self,filename):
        '''times at which we are recording'''
        times = []
        specPop = {}
        dataFile = open(filename, "rt")
        #counting time instances
        count = 0
        commentCount = 0
        paramDict={}
        simParamDict={}
        for line in dataFile:
            if not line=='\n':
                if line[0]=="#":
                    commentCount+=1
                    if commentCount == 1:
                        modelName = (line[2:].rstrip('\n')).lstrip('Model: ')
                    elif commentCount == 2:
                        rawList = (line[2:].rstrip('\n')).split(' ')
                        paramList = [item.split('=') for item in rawList]
                        for item in paramList:
                            paramDict[item[0]]=item[1]
                    elif commentCount == 3:
                        rawList = (line[25:].rstrip('\n')).split(' ')
                        if rawList[0]=='simulateTime':
                            simParamDict['time']=int(rawList[1])
                            simParamDict['interval']=float(rawList[2])
                            simParamDict['filename']=rawList[3]
                        elif rawList[0]=='simulateReactions':
                            simParamDict['numOfReacs']=int(rawList[1])
                            simParamDict['interval']=float(rawList[2])
                            simParamDict['filename']=rawList[3]
                else:
                    count+=1
                    #get a line of raw information splitted by ","
                    raw = (line.rstrip('\n')).split(',')
                    times.append(float(raw[0]))
                    for item in raw[1:len(raw)-1]:
                        #get a couple specie -- its population
                        point=item.split(' ')
                        #if the name of the specie hasn't appear yet
                        if point[0] not in specPop:
                            #add it and its population
                            #also add 0s as prev times populations
                            if not count==1:
                                specPop[point[0]]=[0]*(count-1)
                                specPop[point[0]].append(int(point[1]))
                            else:
                                specPop[point[0]]=[int(point[1])]
                        else:
                            #otherwise append new point to the existing list of points
                            specPop[point[0]].append(int(point[1]))
                    #now let's check if every particle has a record at this time
                    for spec in specPop.keys():
                        if len(specPop[spec])==count:
                            continue
                        elif len(specPop[spec])==count-1:
                            specPop[spec].append(0)
                        else:
                            print(spec)
                            print('length',len(specPop[spec]))
                            print('count',count)
                            raise ValueError("!")
        
        paramDict = OrderedDict(sorted(paramDict.items(), key=lambda t: t[0]))
        
        return times, specPop, modelName, paramDict, simParamDict
    
    def createDestination(self,filename):
        title=''
        for val in self.parameters.values():
            title+='_'+("%.2f" % float(val))
        
        directory = 'simulations/'+self.modelName+title+'/'
        newFilename = directory+'data.txt'
        system('mkdir '+str(directory))
        system('cp '+filename+' '+newFilename)
        
        return directory, newFilename
    
    def readNativeList(self):
        ''' None -> {string: (int, string)}
        converts nativeList.txt to a dictionary from hp-string to a tuple of their native energies and catalytic patterns
        '''
        dataFile = open('nativeList.txt', "rt")
        count = 0
        natData ={}
        for line in dataFile:
            if not count == 0:
                raw = (line.rstrip('\n')).split(' ')
                natData[raw[0]]=(int(raw[1]),raw[2])
            count +=1
        
        return natData

    def printHPstats(self,show=True):
        '''specPop -- {name: [populations during time steps]}'''
        print("total number of species is "+str(len(self.specPop.keys())))
        natData=self.readNativeList()
        lengths=[]
        countAll = [(0)]*(len(self.times)) 
        countFold = [(0)]*(len(self.times)) 
        countCat = [(0)]*(len(self.times)) 
        countAuto = [(0)]*(len(self.times)) 
        popStats={}
        lengthDistr={}
        total=[0]*(len(self.times))
        for key in self.specPop.keys():
            if key.find('f')==-1:
                polLen=len(key)
                lengths.append(len(key))
            else:
                lengths.append(len(key)-1)
                polLen=len(key)-1
            
            #total=[total[i]+self.specPop[key][i] for i in range(len(total))]
            for i in range(len(self.times)):
                countAll[i]+=self.specPop[key][i]
                if not key.find('f')==-1:
                    #print(key)
                    countFold[i]+=self.specPop[key][i]
                    if not natData[key[1:]][1]=='N':
                        countCat[i]+=self.specPop[key][i]
                        if not key.find('HHH')==-1:
                            countAuto[i]+=self.specPop[key][i]
            
            
            if not polLen in popStats.keys():
                #add dict entry and population of the first n-mer of the given length
                popStats[polLen]=self.specPop[key][-1]
            else:
                #add to the population of n-mers a population of another n-mer
                popStats[polLen]+=self.specPop[key][-1]
        mL=max(lengths)
        print("maximum length of a polymer is "+str(mL))
        hist=[]
        histNorm=[]
        #lengthsD=[ps/hi for (ps,hi) in zip(popStats.copy().values(),hist)]
        
        for i in range(1,mL+1):
            hist.append(lengths.count(i))
            histNorm.append(hist[i-1]/2**i)
        lengthsD=[ps/2**li for (ps,li) in zip(list(popStats.copy().values()),list(popStats.copy().keys()))]
        fig, (ax0, ax1, ax2) = plt.subplots(nrows=3)
        #ax1.plot(range(1,mL+1),histNorm,'o')
        ax0.plot(self.times,countAll)
        ax1.plot(self.times,countFold,label='folded')
        ax1.plot(self.times,countCat,label='catalysts')
        ax1.plot(self.times,countAuto,label='autocats')
        ax2.plot(list(popStats.copy().keys()),lengthsD,label=str(mL)+'/'+str(len(self.specPop.keys())))
        ax2.legend()
        ax1.legend()
        ax2.grid(True)
        ax2.set_yscale('log')
        ax0.set_title("Total count of molecules at each moment")
        ax1.set_title("count of molecules of various types at each moment")
        ax2.set_title("Length distribution in the last moment")
        title = ''
        for val in self.parameters.values():
            title+=("%.2f" % float(val))+' '
        fig.suptitle(self.modelName +' with '+title)
        if show:
            plt.show()
        else:
            plt.savefig('pics/stats/'+self.modelName+' '+title + ".png")
        
        return hist

    def getSteady(self,nonSteadyPercent=0.9):
        border=int(nonSteadyPercent*len(self.times))
        steady={}
        for seq in self.specPop.keys():
            points=self.specPop[seq][border:]
            steady[seq]=mean(points)
        
        steadySorted = OrderedDict(sorted(steady.items(), key=lambda t: t[1],reverse=True))
        
        return steadySorted
    


    def plotData(self,steady=None,show=True):
        def f(key,steady,topTen):
            try:
                topTen.index(key)
            except:
                return None
            else:
                return str(key)+'='+str("%.2f" % steady[key])
        fig=plt.figure(figsize=(8,6))
        if not steady==None:
            steadyKeys=[item for item in steady]
            #print(steadyKeys)
            topTen=steadyKeys[0:10]
            
            for key in steady.keys():
                plt.plot(self.times,self.specPop[key],label=f(key,steady,topTen))
        else:
            for key in self.specPop.keys():
                plt.plot(self.times,self.specPop[key])
        #plt.legend(fontsize='small') 
        title = self.modelName+'\n'
        for val in self.parameters.values():
            title+=' '+("%.2f" % float(val))
        plt.title("Populations of species"+title)
        plt.xlim(0,self.times[-1])
        if not steady==None:
            plt.legend(fontsize='small')
        if show:
            plt.show()
        else:
            plt.savefig(self.directory + "all.png")
        
    def getLenSteady(self,steady):
        '''steady: OrderedDict{seq: float}
        '''
        
        steadyLen={}
        for i in range(1,int(self.parameters['maxLength'])+1):
            steadyLen[i]={}
        
        #get sorted dictionary for every key of steadyLen
        for seq in steady:
            if seq.find('f')==-1:
                sLen=len(seq)
            else:
                sLen=len(seq)-1
            steadyLen[sLen][seq]=steady[seq]
        
        for length in steadyLen.keys():
            tmp = OrderedDict(sorted(steadyLen[length].items(), key=lambda t: t[1],reverse=True))
            steadyLen[length]=tmp
        
        return steadyLen
        
        
    
    
    def plotHPlengths(self,steady,show=True):
        steadyLen=self.getLenSteady(steady)
        natData = self.readNativeList()
        def f(key,steadyLen):
            if key.find('f')==-1:
                sLen=len(key)
            else:
                sLen=len(key)-1
            if list(steadyLen[sLen].keys()).index(key)<3:
                return str(key)+'='+str("%.2f" % steadyLen[sLen][key])
            else:
                return None
        
        def getColor(seq,natData):
            if not seq.find('f')==-1:
                temp = seq[1:]
                if temp.find('HHH')==-1 or natData[temp][1]=='N':
                    col = 'blue'
                else:
                    col = 'red'
            else:
                col = 'gray'
            
            return col
                    
            
        #fig=plt.figure(figsize=(8,6))
        #for every length of polymers
        for length in steadyLen.keys():
            lbl=None
            fig=plt.figure(figsize=(8,6))
            #if there are polymers of theat length
            if not steadyLen[length]=={}:
                #for every sequence in the dictionary
                for seq in steadyLen[length].keys():
                    lbl=f(seq,steadyLen)
                    col=getColor(seq,natData)
                    plt.plot(self.times,self.specPop[seq],label=lbl,color=col)
                    
                title = self.modelName+'\n'
                for val in self.parameters.values():
                    title+=' '+("%.2f" % float(val))
                plt.title("Populations of species of length "+str(length)+' '+title)
                plt.xlim(0,self.times[-1])
                plt.legend(fontsize='small')
                if show:
                    plt.show()
                    #plt.savefig(self.directory+'len'+str(length)+".png")
                else:
                    plt.savefig(self.directory+str("%02d" % length)+".png")
                
        return None

    
r=Result('x')
steady = r.getSteady()
r.plotData(steady,False)
r.plotHPlengths(steady,False)
