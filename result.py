#/usr/bin/python

#format of the file is the following:
# time,specName specPopulation,specName specPopulation .....

#specPop -- {name: [populations during time steps]}
import routes
import matplotlib.pyplot as plt
from statistics import mean
from statistics import variance
from collections import OrderedDict
from os import system as system

class Result(object):
    def __init__(self,modelNum,simNum):
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
        self.simNum = simNum
        self.howTerm, self.whenTerm, self.records, self.numOfRuns, self.traj = self.readSimData()
        self.path2Folder = routes.routePDM+'models/'+str("%03d" %self.modelNum)+'/'
        self.means = self.readMeans()
        self.stds = self.readStds()
        
    def readMeans(self):
        evolutions = {}
        f = open(self.path2Folder+str("%03d" %self.modelNum)+'_output'+str(self.simNum)+'/means.txt','r')
        for line in f:
            raw = (line.rstrip('\n')).split(' ')
            evolutions[raw[0]]=[float(item) for item in raw[1:]]
        
        return evolutions
    
    def readStds(self):
        evolutions = {}
        f = open(self.path2Folder+str("%03d" %self.modelNum)+'_output'+str(self.simNum)+'/standDivs.txt','r')
        for line in f:
            raw = (line.rstrip('\n')).split(' ')
            evolutions[raw[0]]=[float(item) for item in raw[1:]]
        
        return evolutions
    
    def readSimData(self):#TODO
        
        return 'time', 100, 1, 10, True

    def readNativeList(self):
        ''' None -> {string: (int, string)}
        converts nativeList.txt to a dictionary from hp-string to a tuple of their native energies and catalytic patterns
        '''
        dataFile = open(routes.routePDM+'nativeList.txt', "rt")
        count = 0
        natData ={}
        for line in dataFile:
            if not count == 0:
                raw = (line.rstrip('\n')).split(' ')
                natData[raw[0]]=(int(raw[1]),raw[2])
            count +=1
        
        return natData

    def printHPstats(self,show=True):#FIXME I am aweful
        '''means/stds -- {name: [populations during time steps]}'''
        print("total number of species in all runs is "+str(len(self.means.keys())))
        natData=self.readNativeList()
        times = [0]
        i=0
        m = 0
        while m < self.whenTerm-1:#FIXME this definitely can be done better
            i+=1
            times.append(self.records*i)
            m = times[-1]
        print(times)
        lengths=[]
        countAll = [(0)]*(len(times)) 
        countFold = [(0)]*(len(times)) 
        countCat = [(0)]*(len(times)) 
        countAuto = [(0)]*(len(times)) 
        popStats={}
        lengthDistr={}
        total=[0]*(len(times))
        for key in self.means.keys():
            if key.find('f')==-1:
                polLen=len(key)
                lengths.append(len(key))
            else:
                lengths.append(len(key)-1)
                polLen=len(key)-1
            
            #total=[total[i]+self.means[key][i] for i in range(len(total))]
            for i in range(len(times)):
                countAll[i]+=self.means[key][i]
                if not key.find('f')==-1:
                    #print(key)
                    countFold[i]+=self.means[key][i]
                    if not natData[key[1:]][1]=='N':
                        countCat[i]+=self.means[key][i]
                        if not key.find('HHH')==-1:
                            countAuto[i]+=self.means[key][i]
            
            
            if not polLen in popStats.keys():
                #add dict entry and population of the first n-mer of the given length
                popStats[polLen]=self.means[key][-1]
            else:
                #add to the population of n-mers a population of another n-mer
                popStats[polLen]+=self.means[key][-1]
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
        ax0.plot(times,countAll)
        ax1.plot(times,countFold,label='folded')
        ax1.plot(times,countCat,label='catalysts')
        ax1.plot(times,countAuto,label='autocats')
        ax2.plot(list(popStats.copy().keys()),lengthsD,label=str(mL)+'/'+str(len(self.means.keys())))
        ax2.legend()
        ax1.legend()
        ax0.set_yscale('log')
        #ax1.set_yscale('log')
        ax2.grid(True)
        ax2.set_yscale('log')
        ax0.set_title("Total count of molecules at each moment")
        ax1.set_title("count of molecules of various types at each moment")
        ax2.set_title("Length distribution in the last moment")
        title = ''
        #for val in self.parameters.values():
            #title+=("%.2f" % float(val))+' '
        #fig.suptitle(self.modelName +' with '+title)
        if show:
            plt.show()
        
        
        return hist
    
    
    
    def getSteady(self,nonSteadyPercent=0.9):
        border=int(nonSteadyPercent*len(self.times))
        steady={}
        for seq in self.means.keys():
            points=self.means[seq][border:]
            steady[seq]=mean(points)
        
        steadySorted = OrderedDict(sorted(steady.items(), key=lambda t: t[1],reverse=True))
        
        return steadySorted
    
    
    
    #def makeDictOfLengths(self,steadyAndVar):#TODO
        #'''returns dictionary of ordereder dictionaries
        #{steady: OrderedDict{seq: float}}
        #'''
        
        #steadyLen={}
        #for i in range(1,int(self.parameters['maxLength'])+1):
            #steadyLen[i]={}
        
        ##get sorted dictionary for every key of steadyLen
        #for seq in steadyAndVar:
            #if seq.find('f')==-1:
                #sLen=len(seq)
            #else:
                #sLen=len(seq)-1
            #steadyLen[sLen][seq]=steadyAndVar[seq]
        
        #for length in steadyLen.keys():
            #tmp = OrderedDict(sorted(steadyLen[length].items(), key=lambda t: t[1],reverse=True))
            #steadyLen[length]=tmp
        
        #return steadyLen

    #def plotData(self,steady,show=True):
        #natData = self.readNativeList()
        #def getColor(seq,natData):
            #if not seq.find('f')==-1:
                #temp = seq[1:]
                #if temp.find('HHH')==-1 or natData[temp][1]=='N':
                    #col = 'blue'
                #elif temp.find('HHH')==-1 and (not natData[temp][1]=='N'):
                    #col = 'green'
                #else:
                    #col = 'red'
            #else:
                #col = 'gray'
            
            #return col
        
        #def f(key,steady,topTen):
            #try:
                #topTen.index(key)
            #except:
                #return None
            #else:
                #return str(key)+'='+str("%.2f" % steady[key])
        #fig=plt.figure(figsize=(8,6))
        #if not steady==None:
            #steadyKeys=[item for item in steady]
            ##print(steadyKeys)
            #topTen=steadyKeys[0:10]
            
            #for key in steady.keys():
                #col = getColor(key,natData)
                #plt.plot(self.times,self.specPop[key],label=f(key,steady,topTen),color=col)
        #else:
            #for key in self.specPop.keys():
                #plt.plot(self.times,self.specPop[key])
        ##plt.legend(fontsize='small') 
        #title = self.modelName+'\n'
        #for val in self.parameters.values():
            #title+=' '+("%.2f" % float(val))
        #plt.title("Populations of species"+title)
        #plt.xlim(0,self.times[-1])
        #if not steady==None:
            #plt.legend(fontsize='small')
        #if show:
            #plt.show()
        #else:
            #plt.savefig(self.directory + "all.png")
        
    #def getLenSteady(self,steady):
        #'''steady: OrderedDict{seq: float}
        #'''
        
        #steadyLen={}
        #for i in range(1,int(self.parameters['maxLength'])+1):
            #steadyLen[i]={}
        
        ##get sorted dictionary for every key of steadyLen
        #for seq in steady:
            #if seq.find('f')==-1:
                #sLen=len(seq)
            #else:
                #sLen=len(seq)-1
            #steadyLen[sLen][seq]=steady[seq]
        
        #for length in steadyLen.keys():
            #tmp = OrderedDict(sorted(steadyLen[length].items(), key=lambda t: t[1],reverse=True))
            #steadyLen[length]=tmp
        
        #return steadyLen
        
        
    
    
    #def plotHPlengths(self,steady,show=True):
        #steadyLen=self.getLenSteady(steady)
        #natData = self.readNativeList()
        #def f(key,steadyLen):
            #if key.find('f')==-1:
                #sLen=len(key)
            #else:
                #sLen=len(key)-1
            #if list(steadyLen[sLen].keys()).index(key)<3:
                #return str(key)+'='+str("%.2f" % steadyLen[sLen][key])
            #else:
                #return None
        
        #def getColor(seq,natData):
            #if not seq.find('f')==-1:
                #temp = seq[1:]
                #if temp.find('HHH')==-1 or natData[temp][1]=='N':
                    #col = 'blue'
                #elif temp.find('HHH')==-1 and (not natData[temp][1]=='N'):
                    #col = 'green'
                #else:
                    #col = 'red'
            #else:
                #col = 'gray'
            
            #return col
                    
            
        ##fig=plt.figure(figsize=(8,6))
        ##for every length of polymers
        #for length in steadyLen.keys():
            #lbl=None
            #fig=plt.figure(figsize=(8,6))
            ##if there are polymers of theat length
            #if not steadyLen[length]=={}:
                ##for every sequence in the dictionary
                #for seq in steadyLen[length].keys():
                    #lbl=f(seq,steadyLen)
                    #col=getColor(seq,natData)
                    #plt.plot(self.times,self.specPop[seq],label=lbl,color=col)
                    
                #title = self.modelName+'\n'
                #for val in self.parameters.values():
                    #title+=' '+("%.2f" % float(val))
                #plt.title("Populations of species of length "+str(length)+' '+title)
                #plt.xlim(0,self.times[-1])
                #plt.legend(fontsize='small')
                #if show:
                    #plt.show()
                    ##plt.savefig(self.directory+'len'+str(length)+".png")
                #else:
                    #plt.savefig(self.directory+str("%02d" % length)+".png")
                
        #return None

modelNum=12
simNum =0
r=Result(modelNum,simNum)
r.printHPstats(True)



