#! /usr/bin/python2
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

import result
import hpClasses

class ClusteredResults(result.Result):
    def __init__(self,modelNum,simNum,minLength,maxLength,
                     nonSteadyPercent=0.9,samp=None,epsilonModifyer={0:0}):
        result.Result.__init__(self,modelNum,simNum)
        self.minLength=minLength
        self.maxLength=maxLength
        self.natData = hpClasses.readNativeList(self.maxLength)
        self.jointLabels, self.epsilons = self.clustLengths(minLength,maxLength,
                     nonSteadyPercent=0.9,samp=None,epsilonModifyer={0:0})
                    #labels for each length
        self.clustDict=self.makeClustDict()
    
    def getClusters(self,length):
        return self.clustDict[length]
    
    def getCluster(self,length,label):
        return self.clustDict[length].theClusters[label]
    
    def makeClustDict(self):
        clustDict={}
        for length in range(self.minLength,self.maxLength+1):
            clustDict[length]=Clusters(length,self)
            
        return clustDict
    
    def plotClustLen(self,saveFig=False):#FIXME I am aweful
        numPlots=self.maxLength-self.minLength+1
        numRows=int((numPlots-1)/2)+1#WTF
        f, names = plt.subplots(numRows, 2, figsize=(18,14))
        for length in range(self.minLength, len(self.jointData.keys())+1):
            grInd=length-self.minLength
            labels=self.jointLabels[length]
            
            unique_labels = list(set(labels))
            #unique_labels.append(-2.0)
            n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            labCols = dict(zip( unique_labels,cm.rainbow(np.linspace(0, 1, len(unique_labels)))))
            metClusts=set([])
            
            #plotOutstanders()#TODO #FINISH
            for clustIndx in self.clustDict[length].clusters:
                cluster = self.clustDict[length].clusters[clustIndx]
                for seq in cluster.sequences:
                    mark, marksize, col = seq.howPlot()
            
                    Legend=None
                    anno=None
                    x=self.jointData[length][seq][0]
                    
                    if grInd<numRows:
                        name=names[grInd,0]
                    else:
                        name=names[grInd-numRows,1]
                    name.plot(x, 0, mark, markerfacecolor=col,\
                                        markeredgecolor='k', markersize=markersize,label=Legend)
                name.legend(prop={'size':8},ncol=2)
                name.set_ylim((-0.1,0.5))
                if not anno==None:
                    name.annotate(anno,xy=(x, 0),xytext=(x, 0.1),textcoords='figure fraction')
            theTitle='Length '+str(length)+'. Est. number of clusters: '+str(n_clusters)
            name.set_title(theTitle)
        
        plt.setp([a.get_yticklabels() for a in f.axes], visible=False)
        
        if not saveFig:
            plt.show()
        else:
            #plt.set_size__inches(12,16)
            plt.suptitle(self.kin2str(), fontsize=20)
            plt.savefig(self.writeGraphFilename())
        return None
    
    
        
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
    
    
    def howPlot(self):
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
            
            
        return mark, marksize, col

if __name__ == "__main__":
    modelNum = 12
    simNum = 2
    minLength = 4
    maxLength = 25
    cr = ClusteredResults(modelNum,simNum,minLength,maxLength)
    cr.plotClustLen(False)
    
    



