#! /usr/bin/python2
import result

class ClusteredResults(result.Result):
    def __init__(self,modelNum,simNum,minLength,maxLength,
                     nonSteadyPercent=0.9,samp=None,epsilonModifyer={0:0}):
        result.Result.__init__(self,modelNum,simNum)
        self.minLength=minLength
        self.maxLength=maxLength
        self.jointLabels = self.clustLengths(minLength,maxLength,
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
        
class Clusters(object):
    '''class Clusters(length,clustResults)
    the clusters belonging to certain length
    '''
    def __init__(self,length,clustResults):
        self.length=length
        #self.epsilon=clustResults.jointEpsilon[length] TODO Shoul we?
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
                #indx=nativeStrings.index(seq.binarySeq.HPsequence)
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
            sequences.append(
                SeqInClust(seq,
                           self.length,
                           clustResults.jointData[self.length][seq][0],
                           clustResults.jointData[self.length][seq][1],
                           self.label))
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
                #indx=nativeStrings.index(seq.binarySeq.HPsequence)
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
    def __init__(self,hpstring,length,meanPop,std,cluster):
        self.hpstring = hpstring
        self.length = length
        self.meanPop = meanPop
        self.std = std
        self.cluster = cluster
        
    def __str__(self):
        str1 = 'Sequence with\n'
        for key in self.__dict__:
            str1+=key+' = '+str(self.__dict__[key])+'\n'
        return str1
    
    def __repr__(self):
        return self.hpstring+': '+str(self.meanPop)+' '+str(self.cluster)

if __name__ == "__main__":
    modelNum = 12
    simNum = 1
    minLength = 4
    maxLength = 25
    cr = ClusteredResults(modelNum,simNum,minLength,maxLength)
    #cl4m1 = Cluster(4,-1,cr,empty=False)
    #cl40 = Cluster(4,0,cr,empty=False)
    cls = Clusters(6,cr)
    



