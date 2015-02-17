#! /usr/bin/python2
from result import *

class ClusteredResults(Result):
    def __init__(self,steady,minLength=6,epsilonModifyer={0:0},cluster=True):
        Result.__init__(self,filename)
        if cluster:
            self.minLength=minLength
            self.steady = self.getSteady()
            #self.jointData created in clustLengths(self,minLength=6,samp=None,epsilonModifyer={0:0})
            self.jointLabels, self.jointEpsilon=self.clustLengths(minLength,samp,epsilonModifyer)#labels for each length#BUG???
            self.clustDict=self.makeClustDict()
    
    def makeDictOfLengths(self,steady):#TODO
        '''returns dictionary of ordereder dictionaries
        {steady: OrderedDict{seq: float}}
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
    
    def clustLengths(self,minLength=6,samp=None,epsilonModifyer={0:0}):# returns dict jointLabels#TODO HERE
        self.jointData=self.makeDictOfLengths()
        jointLabels={}
        jointEpsilon={}
        
        def median(mylist):
            sorts = sorted(mylist)
            length = len(sorts)
            if not length % 2:
                med = (sorts[length / 2] + sorts[length / 2 - 1]) / 2.0
            med=sorts[length / 2]
            print('true median '+str(med))
            if med==0.0:
                i=1
                while med==0.0:
                    med=sorts[length *i/(i+1)]
                    i+=1
                print('variance at '+str(i)+'/'+str(i+1))
                if med==0.0:
                    raise ValueError('Average=0!!!!!')
            
            return med
        
        def clustList(myData,variances,length,samp,epsilonModifyer):
            X=array(zip(myData,[1]*len(myData)))
            med=median(variances)
            '''
            if length>8:
                epsilon=sqrt(med)*4
            elif length>12:
                epsilon=sqrt(med)*8
            else:
                epsilon=sqrt(med)
            '''
            epsilon=sqrt(med)
            if length in epsilonModifyer.keys():
                epsilon=epsilon*epsilonModifyer[length]
            print('epsilon='+str(epsilon))
            jointEpsilon[length]=epsilon
            Y=StandardScaler(copy=True, with_mean=True, with_std=True).fit_transform(X)
            db = DBSCAN(epsilon, min_samples=samp).fit(X)
            core_samples = db.core_sample_indices_
            labels = db.labels_
            
            return labels, core_samples
        
        for length in range(minLength,self.maxLength+1):
            print('plotting length '+str(length))
            grInd=length-minLength
            data=[seq.concentration for seq in self.jointData[length]]
            variances=[seq.variance for seq in self.jointData[length]]
            if length>14:
                if samp==None:
                    samp=20
                else:
                    samp=samp*2
            else:
                if samp==None:
                    samp=10
                else:
                    samp=samp
            jointLabels[length]=clustList(data,variances,length,samp,epsilonModifyer)[0]
            n_clusters = len(set(jointLabels[length])) - (1 if -1 in jointLabels[length] else 0)
            print('Estimated number of clusters: %d' % n_clusters)
            for i in xrange(len(self.jointData[length])):
                self.jointData[length][i].inClustLen=jointLabels[length][i]
        
        
        return jointLabels, jointEpsilon
        
    def getClustLen(self,length):
        return self.clustDict[length]
    
    def getCluster(self,length,label):
        return self.clustDict[length].theClusters[label]
    
    def rmGraphs(self):
        system('rm -r '+routes.routeModels+str(self.indx)+'_graphs/')
        
        return routes.routeModels+str(self.indx)+'_graphs/'
    
    def makeClustDict(self):
        clustDict={}
        for length in range(self.minLength,self.maxLength+1):
            clustDict[length]=Clusters(length,self)
            
        return clustDict
    
    def plotClustLen(self,saveFig=False):
        numPlots=self.maxLength-self.minLength+1
        numRows=(numPlots-1)/2+1
        f, names = plt.subplots(numRows, 2, figsize=(18,14))
        plt.title(self.kin2str())
        for length in range(self.minLength, len(self.jointData.keys())+1):
            grInd=length-self.minLength
            labels=self.jointLabels[length]
            
            unique_labels = list(set(labels))
            #unique_labels.append(-2.0)
            n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            labCols = dict(zip( unique_labels,cm.rainbow(np.linspace(0, 1, len(unique_labels)))))
            metClusts=set([])
            for seq in self.jointData[length]:
                Legend=None
                anno=None
                x=seq.concentration
                if seq.ifInAutoCatSet:
                    if 'f' in seq.HPsequence:
                        markersize = 12
                        mark='v'
                        Legend=str(seq.indx)+' '+str(seq.status)+': '+str( seq.concentration)#TODO format and seq.status
                        #anno=str(seq.indx)
                        if seq.inClustLen==-1.0:
                            col='k'
                        else:
                            col=labCols[seq.inClustLen]
                    else:
                        markersize = 14
                        mark='x'
                        col=labCols[seq.inClustLen]
                        #Legend=str(seq.indx)+' '+str(seq.status)+': '+str( seq.concentration)
                elif seq.inClustLen==-1.0:
                    markersize = 4
                    mark = 'o'
                    col = 'k'
                    if 'f' in seq.HPsequence:
                        markersize = 5
                        mark = 'D'
                    if (seq.indx in self.clustDict[length].outstanders.keys()) and (seq.concentration>self.clustDict[length].maxClustered+0.25*self.jointEpsilon[length]):
                        Legend=str(seq.indx)+' '+str(seq.status)+': '+str( seq.concentration)
                        if 'f' in seq.HPsequence:
                            Legend=str(seq.indx)+' F '+str(seq.status)+': '+str( seq.concentration)
                else:
                    markersize = 8
                    mark = 'o'
                    if 'f' in seq.HPsequence:
                        mark = 'D'
                        markersize = 9
                    col = labCols[seq.inClustLen]
                    currClNum=len(metClusts)
                    metClusts.add(seq.inClustLen)
                    newClNum=len(metClusts)
                    if not newClNum==currClNum:
                         Legend='cluster with '+str(self.clustDict[length].theClusters[seq.inClustLen].numOfseqs)+' seqs'
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
    
    def plotClustBar3D(self,minLen,maxLen,relHigh,relX,cubed,saveFig=False):
        def scatterOutst(clusters,outstanders,length,relX):
            for seq in outstanders:
                #if seq.concentration>self.clustDict[length].maxClustered+0.25*self.jointEpsilon[length]:
                if not relX:
                    conc=seq.concentration
                else:
                    conc=seq.concentration/clusters.absMax
                if seq.ifInAutoCatSet:
                    msize=60
                    mark='v'
                    Legend=str(seq.indx)+' '+str(seq.status)+': '+str( seq.concentration)
                    #ax.text(conc,y,0.05,str(seq.indx),color='r',fontsize=12)
                elif 'f' in seq.HPsequence:
                    msize=30
                    mark='D'
                    Legend=str(seq.indx)+' '+str(seq.status)+': '+str( seq.concentration)
                    #ax.text(conc,y,0.05,str(seq.indx),fontsize=8)
                else:
                    msize=20
                    mark='o'
                    Legend=None
                
                ax.scatter(conc,0,y,zdir='y',c=labCols[length],marker=mark,s=msize,label=Legend)
                
            return None
            
        #plt.clf()
        fig = plt.figure(figsize=(12,8))
        ax = fig.add_subplot(111, projection='3d')
        lenNum=maxLen-minLen+1
        labCols = dict(zip(range(minLen,maxLen+1) ,cm.rainbow(np.linspace(0, 1, lenNum))))
        mm=0
        for length in range(minLen,maxLen+1):
            c=labCols[length]
            clusters = self.clustDict[length]
            totSeq=clusters.totalSeqs
            mm=max(mm,clusters.absMax)
            
                
            y=length
            numOfbars=1
            for cl in clusters.theClusters.values():
                def findBarWid(cl,relX):
                    if not relX:
                        if cl.borders[1]==cl.borders[0]:
                            barWid=0.0001
                        else:
                            barWid=(cl.borders[1]-cl.borders[0])/numOfbars
                    else:
                        barWid=(cl.borders[1]/clusters.absMax-cl.borders[0]/clusters.absMax)/numOfbars
                        if barWid==0:
                            barWid=0.0001
                    return barWid
                #plotPoints.append(cl.borders,cl.numOfseqs)
                barWid=findBarWid(cl,relX)
                
                if relX:
                    xs=np.arange(cl.borders[0]/clusters.absMax,cl.borders[1]/clusters.absMax,barWid)
                else:
                    xs=np.arange(cl.borders[0],cl.borders[1],barWid)
                #REL Z
                if relHigh:
                    zs=np.array([float(cl.numOfseqs)/totSeq]*numOfbars)
                else:
                    zs=np.array([cl.numOfseqs]*numOfbars)
                #print(zs)
                if cubed:
                    ax.bar3d(xs, y, [0]*len(zs),barWid,0.5,zs, color=labCols[length], alpha=0.8 )
                else:
                    ax.bar(xs, zs, y, zdir='y', color=labCols[length], alpha=0.8,width=barWid)   
            
            scatterOutst(clusters,clusters.outstanders.values(),length,relX)
            
        if relHigh:
            ax.set_zlim3d(0, 1)                    
        else:
            zmax=max([cl.numOfseqs for cl in self.clustDict[maxLen].theClusters.values()])
            ax.set_zlim3d(0,zmax)
        ax.set_ylim3d(minLen, maxLen+1)                   
        if relX:
            ax.set_xlim3d(0, 1)
        else:
            ax.set_xlim3d(0, int(mm)+1) 
        #ax.w_xscale.set_scale('log')
        ax.set_xlabel("Population")
        ax.set_ylabel("Length")
        ax.set_zlabel("Number of sequences in clusters")
        ax.set_title(self.kin2str())
        if not saveFig:
            plt.legend(prop={'size':8},ncol=2)
            plt.show()
            
        else:
            plt.savefig(self.writeGraphFilename())
    
    def allSurfaceFolded(self,nativeList):
        allSurfaces={}
        nativeStrings=[ns.hpstring for ns in nativeList]
        for seq in self.allSpecies.allFolded:
            indx=nativeStrings.index(seq.binarySeq.HPsequence)
            allSurfaces[seq.indx]=nativeList[indx].surfaceSequenceMaker()
        
        return allSurfaces
    
    def allSurfaceOfOutst(self,nativeList): 
        ''' Results, List -> Dict
        generates contact surfaces of all the sequences 
        which have big populations for their length
        '''
        allSurfOutst={}
        for length in self.clustDict.keys():
            #print(length)
            tmp= self.clustDict[length].genSurfaceOfOutst(nativeList) 
            #print tmp
            allSurfOutst=dict(allSurfOutst.items()+tmp.items())
        return allSurfOutst
    
    def getDictPattern(self,patLen,nativeList,whichSet='allFold'): 
        ''' Results, Int -> Dict
        given a length of the pattern returns a dictionary
        {pattern: number of encounters} of all the possible surface patterns 
        (possible catalytic sites)
        '''
        patDict={}
        if whichSet=='allFold':
            doubled=[surf*2 for surf in (self.allSurfaceFolded(nativeList)).values()]
        else:
            doubled=[surf*2 for surf in (self.allSurfaceOfOutst(nativeList)).values()]
        for surface in doubled:
            subDict={}
            for i in range(len(surface)/2+1):
                subDict[surface[i:(i+patLen)]]=1
            for pattern in subDict.keys():
                if pattern in patDict.keys():
                    patDict[pattern]+=1
                else:
                    patDict[pattern]=1
        return patDict
    
    def findRarePattern(self,patLen,nativeList,numOfRare,whichSet='allFold'): 
        ''' Results, Int -> Dict
        given a length of the pattern returns a dictionary
        {pattern: number of encounters} of 5 the rarest patterns
        which represents patterns which can be catalyzed.
        I am looking for a pattern which can represent a good choice Catalytic Site of a folded chain
        which can be called a "HP-ribozyme"
        '''
        patDict=self.getDictPattern(patLen,nativeList,whichSet)
        subDict={}
        count=0
        for freq in range(1,40):
            for pattern in patDict.keys():
                if patDict[pattern]==freq:
                    subDict[pattern]=freq
                    count+=1
            if count>=numOfRare:
                break
            else:
                continue
        
        return subDict
        
    def findSeqByPattern(self,pattern,nativeList):#BUG
        '''Results, String, List -> List
        '''
        theseSeqs=[]
        def getSurface(seq,nativeList):
            for nativeChain in nativeList:
                if seq.binarySeq.HPsequence==nativeChain.hpstring:
                    surface=nativeChain.surfaceSequenceMaker()
                    break
            return surface
        
        for seq in self.allSpecies.allFolded:
            if pattern in (getSurface(seq,nativeList))*2: #BUG HERE <- look in SURFACE, not sequence
                theseSeqs.append( seq )
                #break
        if theseSeqs==[]:
            raise ValueError('The sequence isn\'t found')
        
        return theseSeqs
        
class Clusters(object):#TEST
    '''class Clusters(length,clustResults)
    the clusters belonging to certain length
    '''
    def __init__(self,length,clustResults):
        self.length=length
        self.epsilon=clustResults.jointEpsilon[length]
        self.theClusters, self.noise=self.makeClusters(length,clustResults)
        self.minClustered, self.maxClustered=self.findMinMax()
        self.outstanders=self.findOutst()
        self.totalSeqs=sum([cl.numOfseqs for cl in self.theClusters.values()])+self.noise.numOfseqs
        self.absMax=self.findAbsMax()
    
    def __repr__(self):
        str1=str(len(self.theClusters.keys()))+' clusters, '+str(len(self.outstanders.keys()))+' outstanders'
        
        return str1
    
    def makeClusters(self,length,clustResults):#TEST
        listOfClust={}
        noise=Cluster(length,-1.0,clustResults,True)
        for label in set(clustResults.jointLabels[length]):
            #print(label)
            if not label==-1.0:
                listOfClust[label]=Cluster(length,label,clustResults)
            else:
                noise=Cluster(length,-1.0,clustResults)
        return listOfClust, noise
    
    def findMinMax(self):#TEST
        if not self.theClusters.values()==[]:
            theMin=min([clust.borders[0] for clust in self.theClusters.values()])
            theMax=max([clust.borders[1] for clust in self.theClusters.values()])
        else:
            theMin, theMax = (0,0)
        
        return theMin, theMax
    
    def findAbsMax(self):
        if not self.outstanders.values()==[]:
            absMax=max(self.maxClustered,max([seq.concentration for seq in self.outstanders.values()]))
        else:
            absMax=self.maxClustered
        return absMax
    
    def findOutst(self):#TEST
        outstanders={}
        for seq in self.noise.sequences.values():
            if seq.concentration>self.maxClustered:
                outstanders[seq.indx]=seq
        
        return outstanders
    
    def genSurfaceOfOutst(self,nativeList):
        '''Clusters, List -> Dict
        generates a list of the sequences of the surfaces of the outstanders
        '''
        surfaces={}
        nativeStrings=[ns.hpstring for ns in nativeList]
        for seq in self.outstanders.values():
            try:
                indx=nativeStrings.index(seq.binarySeq.HPsequence)
            except:
                continue
                #print(str(seq.indx)+' doesn\'t fold' )
            else:
                surfaces[seq.indx]=nativeList[indx].surfaceSequenceMaker()
        
        return surfaces
    
    
    def __len__(self):
        return len(self.theClusters.keys())
    
    def __getitem__(self,key):
        return self.theClusters[key]
    
    def __setitem__(self, key, value):
        self.theClusters[key] = value
        
    def __iter__(self):
        return iter(self.theClusters.values())
    
    def index(self,value):
        return self.listOfClust.index(value)
    
    def getStatistics():
        y=0
        
        return None
    
class Cluster(object):#TESTED
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
            self.sequences=self.seqsInClust(clustResults)
            self.borders=self.getBorders()
            self.numOfseqs=len(self.sequences.keys())
    
    def short(self):
        str1='clust #'+str(self.label)+': '+str(self.numOfseqs)+' seqs.\n'
        return str1
    
    def __repr__(self):
        str1='length '+str(self.length)+'. Cluster #'+str(self.label)+' lays in '+repr(self.borders)
        str1+=' and has '+str(self.numOfseqs)+' seqs.'
        return str1
    
    def seqsInClust(self,clustResults):#TESTED
        sequences={}#defaultdict(list)
        for seq in clustResults.jointData[self.length]:
            if seq.inClustLen==self.label:
                sequences[seq.indx]=seq
        if sequences.keys()==[]:
            raise ValueError('The cluster '+str(self.label)+' is empty')
        return sequences
    
    def getBorders(self):#TESED
        cons=[seq.concentration for seq in self.sequences.values()]
        borders=(min(cons),max(cons))
        return borders
        
    def genSurfOfCLust(self,nativeList):
        '''Clusters, List -> Dict
        generates a list of the sequences of the surfaces of the outstanders
        '''
        surfaces={}
        nativeStrings=[ns.hpstring for ns in nativeList]
        for seq in self.sequences.values():
            try:
                indx=nativeStrings.index(seq.binarySeq.HPsequence)
            except:
                continue
                #print(str(seq.indx)+' doesn\'t fold' )
            else:
                surfaces[seq.indx]=nativeList[indx].surfaceSequenceMaker()
        
        return surfaces

