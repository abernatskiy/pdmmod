#! /usr/bin/python2
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import subprocess
import os
import result
import hpClasses

from collections import OrderedDict

class ClusteredResults(result.Result):
    def __init__(self,modelNum,simNum,minLength,maxLength,
                     nonSteadyPercent=0.9,samp=None,epsilonModifyer={0:0}):
        print('about to create a Result instance')
        result.Result.__init__(self,modelNum,simNum)
        print('this is simulation '+str(self.modelNum)+'.'+str(self.simNum))
        self.minLength=minLength
        self.maxLength=maxLength
        self.natData = hpClasses.readNativeList(self.maxLength)
        self.means = self.readMeans()
        self.stds = self.readStds()
        self.jointLabels, self.epsilons = self.clustLengths(minLength,maxLength,
                     nonSteadyPercent,samp,epsilonModifyer)
                    #labels for each length
        self.clustDict=self.makeClustDict()
    
    def getClusters(self,length):
        return self.clustDict[length]
    
    def getCluster(self,length,label):
        return self.clustDict[length].theClusters[label]
    
    def makeClustDict(self):
        print('making clustDict')
        clustDict={}
        for length in range(self.minLength,self.maxLength+1):
            clustDict[length]=Clusters(length,self)
            
        return clustDict
    
    
    def plot2DClustLen(self,minLength=None,maxLength=None,saveFig=False):
        '''plots sequences as dots of various shape
        lists outstanders.
        '''
        if minLength == None:
            minLength = self.minLength
        if maxLength == None:
            maxLength = self.maxLength
        numPlots=maxLength-minLength+1
        numRows=int((numPlots-1)/2)+1
        #plt.clf()
        f, names = plt.subplots(numRows, 2, figsize=(18,14))
        for length in range(minLength, maxLength+1):
            grInd=length-minLength #grid index
            labels=self.jointLabels[length]
            
            unique_labels = list(set(labels))
            #unique_labels.append(-2.0)
            n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            labCols = dict(zip( unique_labels,cm.rainbow(np.linspace(0, 1, len(unique_labels)))))
            metClusts=set([])
            
            if grInd<numRows:
                name=names[grInd,0]
            else:
                name=names[grInd-numRows,1]
            for clustIndx in self.clustDict[length].clusters:
                cluster = self.clustDict[length].clusters[clustIndx]
                def plotClusterSeqsAsDots(cluster,name):
                    for seq in cluster.sequences:
                        mark, markersize, col = seq.howPlotAsDots(labCols)
                        Legend=None
                        x=seq.meanPop
                        name.plot(x, 0, mark, markerfacecolor=col,
                                        markeredgecolor='k', 
                                        markersize=markersize,label=Legend)
                    return None
                plotClusterSeqsAsDots(cluster,name)
            for seq in self.clustDict[length].outstanders:
                mark, markersize, col = seq.howPlotAsDots(labCols)
                Legend=seq.hpstring+'='+str('%.2e' % seq.meanPop)
                x = seq.meanPop
                name.plot(x, 0, mark, markerfacecolor=col,
                                    markeredgecolor='k', 
                                    markersize=markersize,label=Legend)
        
            name.legend(prop={'size':8},ncol=2)
            name.set_ylim((-0.1,0.5))
            anno = None
            if not anno==None:
                name.annotate(anno,xy=(x, 0),xytext=(x, 0.1),textcoords='figure fraction')
            theTitle='Length '+str(length)+'. Est. number of clusters: '+str(n_clusters)
            name.set_title(theTitle)
        
        plt.setp([a.get_yticklabels() for a in f.axes], visible=False)
        
        if not saveFig:
            plt.show()
        else:
            plt.suptitle(self._kin2str(), fontsize=20)
            plt.savefig(self._writeGraphFilename())
        return None
    
    def bioMassDistr(self,minLen,topN,saveFig):
        plt.clf()
        lenMass ={}
        topMass={}
        n=topN
        for length in self.jointData:
            if length >= minLen:
                lenMass[length]=sum([item[0] for item in self.jointData[length].values()])
                topMass[length]=sum(sorted([item[0] for item in self.jointData[length].values()])[-n:])
        y=[]
        x=[]
        for i in topMass.keys():
            x.append(i)
            y.append(topMass[i]/lenMass[i])
        fig = plt.figure(figsize=(18,14))
        plt.plot(x,y,linewidth=4)
        plt.xlabel('length')
        plt.ylabel('fraction of mass')
        if not saveFig:
            plt.show()
        else:
            plt.title('Fraction of mass in the top '+
                      str(topN)+' sequences'+'\n'+self._kin2str(), fontsize=20)
            plt.savefig(self._writeGraphFilename())
        return x, y
    
    def getCustomMean(self,firstTime,lastTime):
        border0=self.times.index(float(firstTime))
        border1=self.times.index(float(lastTime))
        steady={}
        for seq in self.means.keys():
            means=self.means[seq].A[0]
            points=means[border0:(border1+1)]
            steady[seq]=np.mean(points)#mean/median question
        
        steadySorted = OrderedDict(
            sorted(steady.items(), key=lambda t: t[1],reverse=True)
            )
        
        return steadySorted
    
    def makeCustomSteady(self,maxLength,firstTime,lastTime):
        '''returns dictionary of ordereder dictionaries
        {length: OrderedDict{seq: float}}
        '''
        
        steadyMean = self.getCustomMean(firstTime,lastTime)   #sortedDict
        #steadyStd = self.getSteadyStd(nonSteadyPercent)     #sortedDict
        steadyLen={}
        for i in range(1,maxLength+1):      #initialyze dicts
            steadyLen[i]={}
        
        #get sorted dictionary for every key of steadyLen
        for seq in steadyMean:
            if seq.find('f')==-1:
                sLen=len(seq)
            else:
                sLen=len(seq)-1
            if not (steadyMean[seq])==0.0:
                steadyLen[sLen][seq]=steadyMean[seq]
        
        for length in steadyLen.keys():
            tmp = OrderedDict(
                sorted(steadyLen[length].items(), key=lambda t: t[1],reverse=True)
                )
            steadyLen[length]=tmp
        
        return steadyLen
    
    def bioMassSlides(self,minLen,maxLength,topN,startTime,stopTime,recTime,dirname):
        firstTime=startTime
        try:
            os.makedirs(os.path.join(self.outputDir,'figures',dirname))
        except:
            print('directory likely exists already')
        while not firstTime==(stopTime-recTime+self.times[1]):
            steadyLen = self.makeCustomSteady(
                maxLength,firstTime,firstTime+recTime)
        
            plt.clf()
            fig = plt.figure(figsize=(16,12))
            lenMass ={}
            topMass={}
            top5={}
            n=topN
            name2numDict = self.enumerateAll(num2name=False,name2num=True)
            for length in steadyLen:
                if length >= minLen:
                    lenMass[length]=sum([item for item in steadyLen[length].values()])
                    topMass[length]=sum(
                        [item for item in steadyLen[length].values()][0:4])
                    count=0.0
                    for name in [item for item in steadyLen[length].keys()][0:4]:
                        plt.text(length,count,str(name2numDict[name]))
                        count+=0.1
                    
            y=[]
            x=[]
            for i in topMass.keys():
                x.append(i)
                y.append(topMass[i]/lenMass[i])
            
            plt.plot(x,y,linewidth=4)
            
            plt.xlabel('length')
            plt.ylabel('fraction of mass')
            plt.ylim((0.0, 1.0))
            plt.title('Fraction of mass in the top '+
                      str(topN)+' sequences, at time '+str(firstTime)+'\n'+self._kin2str(), fontsize=20)
            
            plt.savefig(
                self._writeGraphFilename(
                    os.path.join(self.outputDir,'figures',dirname))
                )
            firstTime+=self.times[1]
        
        return None
        
    def plotSpecific(self,names):
        arrays=[self.means[name] for name in names]
        for (name,data) in zip (names,arrays):
            if not 'f' in name:
                plt.plot(self.times,data,label=name,color='0.85',linewidth=3)
            else:
                plt.plot(self.times,data,label=name,linewidth=3)
        plt.legend()
        plt.title('Time evolutions of selected sequences',fontsize=30)
        plt.ylabel('Population',fontsize=22,linewidth=3)
        plt.xlabel('Time',fontsize=22)
        plt.xlim((0,100))
        plt.show()
        return None
    
    def plotOutstanders(self,natData):
        '''
        takes clustDict, gets outstanders for all the clusters and puts them 
        on the graph population vs length
        '''
        points = []
        lengths = list(self.clustDict.keys())
        regMedianPops = []
        for (length,clusters) in self.clustDict.items():
            for seq in clusters.outstanders:
                if seq.autocat:
                    points.append(seq)
                else:
                    pass
            #now calculate median value of populations of regular sequences
            regulars = []
            for (clusterNum, cluster) in clusters.clusters.items():
                for seq in cluster.sequences:
                    regulars.append(seq.meanPop)
            regMedianPops.append(np.median(regulars))
        
        plt.plot(lengths,regMedianPops)
        for seq in points:
            plt.scatter(seq.length,seq.meanPop,s=20,c='b',marker='v',label=seq.hpstring)
        plt.yscale('log')
        plt.xlim(self.minLength,self.maxLength)
        plt.savefig(self.outputDir+'outstanders.png')
        
        return points, regMedianPops
            
        
        
class Clusters(object):
    '''class Clusters(length,clustResults)
    the clusters belonging to certain length
    '''
    def __init__(self,length,clustResults):
        self.length=length
        #self.epsilon=clustResults.jointEpsilon[length] Should we?
        self.clusters, self.noise=self.makeClusters(length,clustResults)
        self.minClustered, self.maxClustered=self.findMinMax()
        self.outstanders=self.findOutst()
        self.absMax=self.findAbsMax()
        #self.totalSeqs=sum([cl.numOfseqs for cl in self.clusters.values()])+self.outstanders.numOfseqs
        
    
    def __repr__(self):
        str1=str(len(self.clusters.keys()))+' clusters, '+\
            str(len(self.noise.sequences))+' outstanders'
        
        return str1
    
    def makeClusters(self,length,clustResults):#TESTED
        clusters={}
        outstanders=Cluster(length,-1.0,clustResults,True)
        for label in clustResults.jointLabels[length].keys():
            if not label==-1.0:
                clusters[label]=Cluster(length,label,clustResults)
            else:
                outstanders=Cluster(length,-1.0,clustResults)
        return clusters, outstanders
    
    def findMinMax(self):#TESTED
        if not self.clusters=={}:
            theMin=min([clust.borders[0] for clust in self.clusters.values()])
            theMax=max([clust.borders[1] for clust in self.clusters.values()])
        else:
            theMin, theMax = (0,0)
        
        return theMin, theMax
    
    def findOutst(self):#TEST
        outstanders=[]
        for seq in self.noise.sequences:
            if seq.meanPop>self.maxClustered:
                outstanders.append(seq)
        
        return outstanders
    
    def findAbsMax(self):#TEST
        if not self.outstanders==[]:
            absMax=max(self.maxClustered,max([seq.meanPop for seq in self.outstanders]))
        else:
            absMax=self.maxClustered
        return absMax
    
    def statsOfClust(self,median=False):
        if not median:
            med = (self.maxClustered+self.minClustered)/2.0
            return self.minClustered, med, self.maxClustered
        else:#FIXME
            raise NotImplementedError
    
    def statsOfOuts(self):
        pops=[seq.meanPop for seq in self.outstanders]
        med = np.median(pops)
        return min(pops), med, max(pops)
        
    
    #def genSurfaceOfOutst(self,nativeList):#!!!interesting!!!
        #'''Clusters, List -> Dict
        #generates a list of the sequences of the surfaces of the outstanders
        #'''
        #surfaces={}
        #nativeStrings=[ns.hpstring for ns in nativeList]
        #for seq in self.outstanders.values():
            #try:
                #indx=nativeStrings.index(seq.binarySeq.hpstring)
            #except:
                #continue
                ##print(str(seq.indx)+' doesn\'t fold' )
            #else:
                #surfaces[seq.indx]=nativeList[indx].surfaceSequenceMaker()
        
        #return surfaces
    
    
    def __len__(self):
        return len(self.clusters.keys())
    
    def __getitem__(self,key):
        if not key == -1:
            return self.clusters[key]
        else:
            return self.noise
    
    #def __setitem__(self, key, value):
        #self.clusters[key] = value
        
    #def __iter__(self):
        #return iter(self.clusters.values())
    
    #def index(self,value):
        #return self.listOfClust.index(value)
    
    #def getStatistics():
        #y=0
        
        #return None
    
class Cluster(object):#TEST
    '''class Cluster(length,label,clustResults)
    '''
    def __init__(self,length,label,clustResults,empty=False):
        self.length=length
        self.label=label
        if empty:
            self.sequences={}
            self.numOfseqs=0
            self.borders=(0.0,0.0)
        else:
            self.sequences=self.makeSequences(clustResults)
            self.borders=self.getBorders()
            self.numOfseqs=len(self.sequences)
    
    def short(self):
        str1='clust #'+str(self.label)+': '+str(self.numOfseqs)+' seqs.\n'
        return str1
    
    def __str__(self):
        str1='length '+str(self.length)+'. Cluster #'+str(self.label)+' lays in '+repr(self.borders)
        str1+=' and has '+str(self.numOfseqs)+' seqs.'
        return str1
    
    def __repr__(self):
        return self.__str__()
    
    def makeSequences(self,clustResults):#TESTED
        sequences=[]
        for seq in clustResults.jointLabels[self.length][self.label]:
            hp_classes = hpClasses.getHPClassOfSeq(seq,clustResults.natData)
            sequences.append(
                SeqInClust(seq,
                           self.length,
                           clustResults.jointData[self.length][seq][0],
                           clustResults.jointData[self.length][seq][1],
                           self.label,hp_classes))
        if sequences==[]:
            raise ValueError('The cluster '+str(self.label)+' is empty')
        return sequences
    
    def getBorders(self):#TESTED
        pops=[seq.meanPop for seq in self.sequences]
        borders=(min(pops),max(pops))
        return borders
        
    #def genSurfOfCLust(self,nativeList):#interesting!!
        #'''Clusters, List -> Dict
        #generates a list of the sequences of the surfaces of the outstanders
        #'''
        #surfaces={}
        #nativeStrings=[ns.hpstring for ns in nativeList]
        #for seq in self.sequences.values():
            #try:
                #indx=nativeStrings.index(seq.binarySeq.hpstring)
            #except:
                #continue
                ##print(str(seq.indx)+' doesn\'t fold' )
            #else:
                #surfaces[seq.indx]=nativeList[indx].surfaceSequenceMaker()
        
        #return surfaces
    
    def __len__(self):
        return len(self.sequences)
    
    def __getitem__(self,key):
        return self.sequences[i]
    

class SeqInClust(object):
    def __init__(self,hpstring,length,meanPop,std,cluster,hp_classes):
        self.hpstring = hpstring
        self.length = length
        self.meanPop = meanPop
        self.std = std
        self.cluster = cluster
        self.fold, self.cat, self.autocat = hp_classes
        
    def __str__(self):
        str1 = 'Sequence with\n'
        for key in self.__dict__:
            str1+=key+' = '+str(self.__dict__[key])+'\n'
        return str1
    
    def __repr__(self):
        return self.hpstring+': '+str(self.meanPop)+' '+str(self.cluster)
    
    
    def howPlotAsDots(self,labCols):
        if self.autocat:
            markersize = 12
            mark='v'
            if self.cluster==-1.0:#TEST
                col='k'
            else:
                col=labCols[self.cluster]#TEST
            
        elif self.cluster==-1.0:#TEST
            markersize = 4
            mark = 'o'
            col = 'k'
            if 'f' in self.hpstring:
                markersize = 5
                mark = 'D'
            
        else:
            markersize = 8
            mark = 'o'
            if 'f' in self.hpstring:
                mark = 'D'
                markersize = 9
            col = labCols[self.cluster]
            
            
        return mark, markersize, col


def plotStandardFirstTime(
    startSim,endSim,modelNum,minLength=4,maxLength=25,nonSteadyPercent=0.5
    ):
    for simNum in range(startSim,endSim):
        print('newPlot of '+str(simNum))
        try:
            os.mkdir(str("%03d" %modelNum)+'_output'+str(simNum)+'/figures/')
        except:
            print('folder exists')
        save = True
        try:
            cr = ClusteredResults(
                modelNum,simNum,minLength,maxLength,nonSteadyPercent=0.5
                )
            cr.plotHPstats(natData,None,saveFig=save,nonSteadyPercent=0.5)
            cr.plot2DClustLen(4,7,saveFig=save)
            cr.plot2DClustLen(8,13,saveFig=save)
            cr.plot2DClustLen(14,19,saveFig=save)
            cr.plot2DClustLen(20,25,saveFig=save)
        except:
            print(str(simNum)+' not finished')
            subprocess.call(['touch',str("%03d" %modelNum)+'_output'+str(simNum)+'/not_done'])
            r = Result(modelNum,simNum,reorganize=True,numOfRuns=3,traj=True)
            cr = ClusteredResults(
                modelNum,simNum,minLength,maxLength,nonSteadyPercent=0.5
                )
            cr.plotHPstats(natData,None,saveFig=save,nonSteadyPercent=0.5)
            cr.plot2DClustLen(4,7,saveFig=save)
            cr.plot2DClustLen(8,13,saveFig=save)
            cr.plot2DClustLen(14,19,saveFig=save)
            cr.plot2DClustLen(20,25,saveFig=save)
        else:
            print(str(simNum)+' done')
            
def plotStandardReplot(
        startSim,endSim,modelNum,formResult=False,numOfRuns=1,traj=True,
        minLength=4,maxLength=25,nonSteadyPercent=0.5):
    save = True
    redone=[]
    new=[]
    for simNum in range(startSim,endSim):
        print('plotReplot of '+str(simNum))
        commonPath =  str("%03d" %modelNum)+'_output'+str(simNum)+'/'
        if os.path.isfile(commonPath+'figures/000.png'):
            if os.path.isfile(commonPath+'not_done'):
                subprocess.call(['rm','-r',commonPath+'figures'])
                subprocess.call(['mkdir',commonPath+'figures'])
                if formResult:
                    r = Result(modelNum,simNum,reorganize,numOfRuns,traj)
                cr = ClusteredResults(
                    modelNum,simNum,minLength,maxLength,nonSteadyPercent)
                cr.plotHPstats(natData,None,saveFig=save,nonSteadyPercent)
                cr.plot2DClustLen(6,9,saveFig=save)
                cr.plot2DClustLen(10,13,saveFig=save)
                cr.plot2DClustLen(14,17,saveFig=save)
                cr.plot2DClustLen(18,21,saveFig=save)
                cr.plot2DClustLen(22,25,saveFig=save)
                subprocess.call(['rm','-r',commonPath+'not_done'])
                redone.append(simNum)
            else:
                print(str(simNum)+' already has been done')
                continue
        else:
            new.append(simNum)
            plotStandardFirstTime(
                simNum,simNum+1,
                modelNum,minLength=4,maxLength=25,nonSteadyPercent=0.5
                )
    print('redone',redone)
    print('new',new)
    



