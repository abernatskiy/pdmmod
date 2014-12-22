#! /usr/bin/python

import routes
import sys
from os import system as system
from glob import glob as glob
from random import randint as randint
from math import sqrt as sqrt
from collections import defaultdict as defaultdict
import numpy as np
from numpy import array


from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

from numpy import matrix as matrix
import matplotlib.pyplot as plt

###Results###

class Results(object):
    '''class Results(simIndx)
    '''
    def __init__(self,resultsFile):#TODO fix maxLength
        self.modelName=None      #TODO
        self.kinetics={}    #TODO
        self.simParams=None #TODO
        self.resultsFile=resultsFile
        self.times, self.allSpeciesDict=self.readData()
        self.maxLength, self.lengthsDistr=self.lengthsData()
        self.natData=self.readNativeList()

    def __str__(self):
        str1='Results for the simulation '+str(modelName)+'\n '
        str2='with kinetics '+str(self.kinetics)+', simParams'+str(self.simParams)+'\n'
        return str1+str2
    
    def __repr__(self):
        str1='Results for the simulation '+str(modelName)+'\n '
        return str1
    
    def readData(self):#return List:times, Dict:specPop
        '''Results -> List [times], Dict {sequence: [populations]}
        '''
        #times at which we are recording'''
        times = []
        specPop = {}
        dataFile = open(self.resultsFile, "rt")
        #counting time instances
        count = 0
        for line in dataFile:
            if not line=='\n':
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
        
        return times,specPop
    
    def readNativeList(self):
        ''' None -> {string: (int, string)}
        converts nativeList.txt to a dictionary from hp-string to a tuple of their native energies and catalytic patterns
        '''
        dataFile = open(routes.routePDM+'nativeList'+str("%02d" % self.maxLength)+'.txt', "rt")
        count = 0
        natData ={}
        for line in dataFile:
            if not count == 0:
                raw = (line.rstrip('\n')).split(' ')
                natData[raw[0]]=(int(raw[1]),raw[2])
            count +=1
        
        return natData
    
    def lengthsData(self):#return mL, lengthsDistr
        lengths=[]
        hist={}
        lengthsDistr={}
        for key in self.allSpeciesDict.keys():
            if key.find('f')==-1:
                polLen=len(key)
                lengths.append(len(key))
            else:
                lengths.append(len(key)-1)
                polLen=len(key)-1
            if not polLen in hist.keys():
                hist[polLen]=self.allSpeciesDict[key][-1]
            else:
                hist[polLen]+=self.allSpeciesDict[key][-1]
        mL=max(lengths)
        for key in hist.keys():
            lengthsDistr[key]=float(hist[key])/2**key
        
        
        
        
        return mL, lengthsDistr

    def countTypes(self):
        '''Results,
        '''
        countAll = [(0)]*(len(self.times)) 
        countFold = [(0)]*(len(self.times)) 
        countCat = [(0)]*(len(self.times)) 
        countAuto = [(0)]*(len(self.times)) 
        for key in self.allSpeciesDict.keys():
            for i in range(len(self.times)):
                countAll[i]+=self.allSpeciesDict[key][i]
                if not key.find('f')==-1:
                    #print(key)
                    countFold[i]+=self.allSpeciesDict[key][i]
                    if not self.natData[key[1:]][1]=='N':
                        countCat[i]+=self.allSpeciesDict[key][i]
                        if not key.find('HHH')==-1:
                            countAuto[i]+=self.allSpeciesDict[key][i]
        
        return countAll, countFold, countCat, countAuto
    
    def plotStats(self):
        countAll, countFold, countCat, countAuto = self.countTypes()
        fig, (ax0, ax1, ax2) = plt.subplots(nrows=3)
        ax0.plot(self.times,countAll)
        ax1.plot(self.times,countFold,label='folded')
        ax1.plot(self.times,countCat,label='catalysts')
        ax1.plot(self.times,countAuto,label='autocats')
        x=[]
        y=[]
        for key in self.lengthsDistr.keys():
            x.append(key)
            y.append(self.lengthsDistr[key])
        ax2.plot(x,y)
        ax2.legend()
        ax1.legend()
        ax2.grid(True)
        ax2.set_yscale('log')
        ax0.set_title("Total count of molecules at each moment")
        ax1.set_title("count of molecules of various types at each moment")
        ax2.set_title("Length distribution in the last moment")
        fig.suptitle(self.modelName)
        #plt.savefig("stats.pdf")
        plt.show()
    
    
r=Results(routes.routeResults+'x')
    
#TODO WTF AND BELOW
    #def getPopulations(self):
        #return [seq.concentration for seq in self.allSpecies.listOfAllSpec]
    
    #def getVariances(self):
        #return [seq.variance for seq in self.allSpecies.listOfAllSpec]
    
    #def getSigmas(self):
        #return [sqrt(seq.variance) for seq in self.allSpecies.listOfAllSpec]
    
    #def findSpecies(self,howMany=0.01):
        #allSpecies=pickle.load(open( self.picklePath, "rb" ))
        #sp=allSpecies.listOfAllSpec[0]
        #try:
            #sp.variance>=0.0
        #except:
            #listOfVars=self.findVars(howMany)
            #for i in xrange(len(allSpecies.listOfAllSpec)):
                #(allSpecies.listOfAllSpec[i]).variance=listOfVars[i]
            #route2Pickle=routes.routeModels+str(self.indx)+".p"
            #pickle.dump(self.allSpecies,open(route2Pickle, "wb" ), -1)
            #allSpecies=pickle.load(open( self.picklePath, "rb" ))
            
        
        #return allSpecies

    #def findVars(self,howMany=0.01):#OK
        #'''Results -> List of Lists of Floats
        #the first list is evolution of time
        #next lists are evolution of the species populations
        #'''
        #varsPath=routes.routeModels+str(self.indx)+'_output/stats/variances.txt'
        #f=open(varsPath,'r')
        ##convert list of strings into matrix of floats
        #matOfvars=matrix([map(float, line.rstrip('\t\n').split('\t')) for line in f])
        #last=len(matOfvars)
        #first=last-int(last*howMany)
        #lenOfVars=int(last*howMany)
        ##take only the ends of variables, exlude time
        #listOfVars=map(lambda x: float(x)/lenOfVars, (sum(matOfvars[first:,1:])).tolist()[0])
        
        #return listOfVars

    #def addVars(self,howMany=0.01):
        #try:
            #sp=self.allSpecies.listOfAllSpec[0]
            #sp.variance>=0.0
        #except:
            #listOfVars=self.findVars(howMany)
            #for i in xrange(len(self.allSpecies.listOfAllSpec)):#possibly BUG here, .len()??
                #(self.allSpecies.listOfAllSpec[i]).variance=listOfVars[i]
            
            #route2Pickle=routes.routeModels+str(self.indx)+".p"
            #pickle.dump(self.allSpecies,open(route2Pickle, "wb" ), -1)
        #else:
            #print('variances seem to be present')
            #print('var of '+str(sp)+' = '+str(sp.variance))
        
        #return None
  
    

    #def writeGraphFilename(self):
        #'''Results -> String (filename)
        #'''
        #def ifNameExists(name):
            #sR=glob(routes.routeModels+str(self.indx)+'_graphs/'+name)
            #if sR==[]:
                #return False
            #else:
                #return True
        #s='000'
        #while ifNameExists(s+'.png'):
            #i=int(s)
            #i+=1
            #if len(str(i))==1:
                #s='00'+str(i)
            #elif len(str(i))==2:
                #s='0'+str(i)
            #elif len(str(i))>2:
                #s=str(i)
        ##if not ifNameExists(s)
        #name=s+'.png'
            ##if ifNameExists(name):
            ##    raise('plot has been overwritten')
            
            
        #path=routes.routeModels+str(self.indx)+'_graphs/'+name
        
        #return path

    #def kin2str(self):
        #title='('+str(self.indx)+') '
        #if self.name=='e':
            #title+='E:'+str(self.maxLength)+' Growth, catalysis, folding, unfolding(z^n)\n'
            #title+='Import='+str(self.kinetics[0])
            #title+='  growth='+str(self.kinetics[1])
            #title+='  degr='+str(self.kinetics[2])+ '\n'
            #title+='eH='+str(self.kinetics[3])
            #title+='  z='+str(self.kinetics[4])
            #title+='  foldDegr='+str(self.kinetics[5])
        #elif self.name=='f':
            #title+='F:'+str(self.maxLength)+' Growth, catalysis, folding, unfolding\n'
            #title+='Import='+str(self.kinetics[0])
            #title+='  growth='+str(self.kinetics[1])
            #title+='  degr='+str(self.kinetics[2])+ '\n'
            #title+='eH='+str(self.kinetics[3])
            #title+='  k_unf='+str(self.kinetics[4])
            #title+='  foldDegr='+str(self.kinetics[5])
        #elif self.name=='g':
            #title+='G:'+str(self.maxLength)+' Growth, folding, contst. unfolding\n'
            #title+='Import='+str(self.kinetics[0])
            #title+='  growth='+str(self.kinetics[1])
            #title+='  degr='+str(self.kinetics[2])+ '\n'
            #title+='eH='+str(self.kinetics[3])
            #title+='  kf0='+str(self.kinetics[4])
            #title+='  ku0='+str(self.kinetics[5])
            #title+='  foldDegr='+str(self.kinetics[6])
        #elif self.name=='i':
            #title+='I:'+str(self.maxLength)+' Growth, catalysis, folding after len='+str(int(self.kinetics[6]))+', unfolding(z^n)\n'
            #title+='Import='+str(self.kinetics[0])
            #title+='  growth='+str(self.kinetics[1])
            #title+='  degr='+str(self.kinetics[2])+ '\n'
            #title+='eH='+str(self.kinetics[3])
            #title+='  z='+str(self.kinetics[4])
            #title+='  foldDegr='+str(self.kinetics[5])
        #else:
            #title+=str(self.name)+' '+str(self.maxLength)+' '+str(self.kinetics)
        
        #return title
    
    #def results2Plot(self,evolutions,re=False,show=False,cutOff=0.0):
        #plt.clf()
        #''' Results, Non-negative -> None (plots graphs)
        #given the file with results of the simulation (means) and the list of species 
        #plots dependence of the mean (over the ensemble) concentrations of species as function of time
        #'''
        ##list of times is produced by the function results2evol
        #if re:
            #self.delGraphs()
            #system('mkdir '+routes.routeModels+str(self.indx)+'_graphs')
            
        #Times=evolutions[0]
        ##list of lists of species concentrations is produced by the function results2evol
        #speciesTraj=evolutions[1:]
        ##set counter to 0
        #i=0
        ##print(i)
        #drop=int(self.simParams[2]*cutOff/100.0)
        ##for every species in the list of species
        #print(self.name)
        #for species in self.allSpecies.listOfAllSpec:
            ##increase value of the counter
            #i=species.indx
            #if i%1000==0:
                #print(i)
            ##plot species number i vs time with label which is sequence of the species number i
            #plt.plot(Times[drop:],speciesTraj[i][drop:])#
            
        #plt.ylabel('populations of sequences')
        #plt.xlabel('time')
        
        #plt.title(self.kin2str())
        #plt.savefig(self.writeGraphFilename())
        #if show:
            #plt.show()
        #else:
            #plt.close()
        
        
        #return None
    ##TEST
    #def plotAutocats(self,evolutions,cutOff=0.0):
        #plt.clf()
        #fig=plt.figure(figsize=(8,6))
        #Times=evolutions[0]
        ##list of lists of species concentrations is produced by the function results2evol
        #speciesTraj=evolutions[1:]
        #drop=int(self.simParams[2]*cutOff/100.0)
        ##for every species in the list of species
        #labCols = dict(zip( range(9,self.maxLength+1),cm.rainbow(np.linspace(0, 1, self.maxLength-8))))
        ##print(labCols)
        #if not self.allSpecies.allAutocats==[]:
            #for species in self.allSpecies.allAutocats:
                #i=species.indx
                #plt.plot(Times[drop:],speciesTraj[i][drop:],c=labCols[species.length],label=repr(species.length))
                #legend=(species.HPsequence)
            #print('autocats plotted')
            #plt.legend(fontsize='small')
            #plt.ylabel('populations of autocats')
            #plt.xlabel('time')
            #plt.title(self.kin2str())
            #plt.savefig(self.writeGraphFilename())
            #plt.close()
        
        
        #return None
    
    #def plotActivated(self,evolutions,cutOff=0.0):
        #plt.clf()
        #fig=plt.figure(figsize=(12,9))
        #Times=evolutions[0]
        #speciesTraj=evolutions[1:]
        #try:
            #self.allSpecies.activated==[]
        #except:
            #print('No Activated Monomers')
        #else:
            #if self.allSpecies.activated==[]:
                #print('Panic!!! No Activated Monomers')
            #else:
                #print('Printing '+str(self.allSpecies.listOfAllSpec[-1])+ ' and '+str(self.allSpecies.listOfAllSpec[-2]))
                #drop=int(self.simParams[2]*cutOff/100.0)
                #col='r'
                #plt.plot(Times[drop:],speciesTraj[-1][drop:],'r',label=repr(self.allSpecies.listOfAllSpec[-1].HPsequence))
                #plt.plot(Times[drop:],speciesTraj[-2][drop:],'b',label=repr(self.allSpecies.listOfAllSpec[-2].HPsequence))
                
                #plt.legend(fontsize='small')
                #plt.ylabel('populations of activated monomers')
                #plt.xlabel('time')
                #plt.title(self.kin2str())
                #plt.savefig(self.writeGraphFilename())
                #plt.close() 
        #return None
                
    #def plotLength(self,evolutions,length,cutOff=0.0):
        #plt.clf()
        #fig=plt.figure(figsize=(8,6))
        #Times=evolutions[0]
        ##list of lists of species concentrations is produced by the function results2evol
        #speciesTraj=evolutions[1:]
        ##set counter to 0
        #i=0
        ##print(i)
        #drop=int(self.simParams[2]*cutOff/100.0)
        ##for every species in the list of species
        #for species in self.allSpecies.listOfAllSpec:
            ##increase value of the counter
            #if not species.ifInAutoCatSet:
                #col='0.75'
                #if 'f' in species.HPsequence:
                    #col='b'
            #else:
                #col='r'
            #i=species.indx
            #if species.length==length:
                #if length==1:
                    #if not (species.HPsequence=='P*' or species.HPsequence=='H*'):
                        #plt.plot(Times[drop:],speciesTraj[i][drop:],col,label=species.HPsequence)
                #else:        
                    #plt.plot(Times[drop:],speciesTraj[i][drop:],col)
        
        #plt.legend(fontsize='small')        
        #plt.ylabel('populations of sequences with length '+str(length))
        #plt.xlabel('time')
        #plt.title(self.kin2str())
        #plt.savefig(self.writeGraphFilename())
        #plt.close()
        
        #return None
    
    #def plotAllLengths(self,evolutions,cutOff=0.0):
        #for length in range(1,self.maxLength+1):
            #self.plotLength(evolutions,length,cutOff)
            #print(str(length)+' printed')
        
        #return None
    
    #def makeDictOfLengths(self):
        #data=zip([seq.length for seq in self.allSpecies.listOfAllSpec], self.allSpecies.listOfAllSpec)
        #dictOfLenghts = defaultdict(list)
        #for length, seq in data:
            #dictOfLenghts[length].append(seq)
        
        #return dictOfLenghts
    

    
    #def clustAll(self):
        #data=[spec.concentration for spec in self.allSpecies.listOfAllSpec]
        #variances=[spec.variance for spec in self.allSpecies.listOfAllSpec]
        #labels, core_samples=plot_dbscan.clustList(data,variances)#CLUSTERED
        #n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        #print('Estimated number of clusters: %d' % n_clusters)
        #for i in xrange(len(self.allSpecies.listOfAllSpec)):
            #self.allSpecies.listOfAllSpec[i].inClustAll=labels[i]
        
        #return labels, core_samples
    
    #def clustLengths(self,minLength=6,samp=None,epsilonModifyer={0:0}):# returns dict jointLabels
        #self.jointData=self.makeDictOfLengths()
        #jointLabels={}
        #jointEpsilon={}
        
        #def median(mylist):
            #sorts = sorted(mylist)
            #length = len(sorts)
            #if not length % 2:
                #med = (sorts[length / 2] + sorts[length / 2 - 1]) / 2.0
            #med=sorts[length / 2]
            #print('true median '+str(med))
            #if med==0.0:
                #i=1
                #while med==0.0:
                    #med=sorts[length *i/(i+1)]
                    #i+=1
                #print('variance at '+str(i)+'/'+str(i+1))
                #if med==0.0:
                    #raise ValueError('Average=0!!!!!')
            
            #return med


        #def clustList(myData,variances,length,samp,epsilonModifyer):
            #X=array(zip(myData,[1]*len(myData)))
            #med=median(variances)
            #'''
            #if length>8:
                #epsilon=sqrt(med)*4
            #elif length>12:
                #epsilon=sqrt(med)*8
            #else:
                #epsilon=sqrt(med)
            #'''
            #epsilon=sqrt(med)
            #if length in epsilonModifyer.keys():
                #epsilon=epsilon*epsilonModifyer[length]
            #print('epsilon='+str(epsilon))
            #jointEpsilon[length]=epsilon
            #Y=StandardScaler(copy=True, with_mean=True, with_std=True).fit_transform(X)
            #db = DBSCAN(epsilon, min_samples=samp).fit(X)
            #core_samples = db.core_sample_indices_
            #labels = db.labels_
            
            #return labels, core_samples
        
        #for length in range(minLength,self.maxLength+1):
            #print('plotting length '+str(length))
            #grInd=length-minLength
            #data=[seq.concentration for seq in self.jointData[length]]
            #variances=[seq.variance for seq in self.jointData[length]]
            #if length>14:
                #if samp==None:
                    #samp=20
                #else:
                    #samp=samp*2
            #else:
                #if samp==None:
                    #samp=10
                #else:
                    #samp=samp
            #jointLabels[length]=clustList(data,variances,length,samp,epsilonModifyer)[0]
            #n_clusters = len(set(jointLabels[length])) - (1 if -1 in jointLabels[length] else 0)
            #print('Estimated number of clusters: %d' % n_clusters)
            #for i in xrange(len(self.jointData[length])):
                #self.jointData[length][i].inClustLen=jointLabels[length][i]
        
        
        #return jointLabels, jointEpsilon
    
    
    #def plotClustAll(self,labels, core_samples,saveFig=False):
        #unique_labels = list(set(labels))
        #unique_labels.append(-2.0)
        #n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        #labCols = dict(zip( unique_labels,cm.rainbow(np.linspace(0, 1, len(unique_labels)+1))))
        #fig=plt.figure(figsize=(16,12))
        #name=fig.add_subplot(111)
        #print('plotting clusterde lengths')
        #for seq in self.allSpecies.listOfAllSpec:
            #x=seq.concentration
            #if seq.ifInAutoCatSet:
                #if 'f' in seq.HPsequence:
                    #print('an autocat met')
                    #markersize = 24
                    #mark='v'
                    #col=labCols[seq.inClustAll]
                #else:
                    #markersize = 24
                    #mark='x'
                    #col=labCols[seq.inClustAll]
            #elif seq.inClustAll==-1.0:
                #markersize = 6
                #mark = 'o'
                #col = 'k'
            #else:
                #markersize = 14
                #mark = 'o'
                #col = labCols[seq.inClustAll]
                
            #name.plot(x, 0, mark, markerfacecolor=col,\
                                    #markeredgecolor='k', markersize=markersize)    
        #plt.title(self.kin2str()+'\n'+'Estimated number of clusters: '+str(n_clusters))
        #if not saveFig:
            #plt.show()
        #else:
            #plt.savefig(self.writeGraphFilename())
        #return labCols
    
    #def getClustConcD(self,minLength=6):
        #jointClustConcD=defaultdict(list)
        #for length in range(minLength, self.maxLength+1):
            #clustConcD = defaultdict(list)
            #for index, pop in zip([seq.inClustLen for seq in self.jointData[length]],[seq.concentration for seq in self.jointData[length]]):
                #clustConcD[index].append(pop)
            #jointClustConcD[length].append(clustConcD)
        
        #return jointClustConcD
    
    #def getClustBorders(self,joiclustConcD,minLength=6):#TEST
        #bordDict=defaultdict(list)
        #for length in range(minLength, self.maxLength+1):
            #for index in (jointClustConcD[length]).keys():
                #if not index==-1.0:
                    #bordDict[length].append((min(clustConcD[index]),max(clustConcD[index])))
        
        #return bordDict
    
    #def getOutstanding(self,joiclustConcD,bordDict,minLength=6):#TODO
        #outstD=defaultdict(list)
        #for length in bordDict:
            #border=max([b[1] for b in bordDict[length]])
            
        
        #return outstD
    
    #def plotClustLen(self,jointLabels,minLength=6,saveFig=False):
        #numPlots=self.maxLength-minLength+1
        #numRows=(numPlots-1)/2+1
        #f, names = plt.subplots(numRows, 2, figsize=(18,14))
        #plt.title(self.kin2str())
        #for length in range(minLength, len(self.jointData.keys())+1):
            #grInd=length-minLength
            #labels=jointLabels[length]
            
            #unique_labels = list(set(labels))
            ##unique_labels.append(-2.0)
            #n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            #labCols = dict(zip( unique_labels,cm.rainbow(np.linspace(0, 1, len(unique_labels)))))
            #for seq in self.jointData[length]:
                #Legend=None
                #anno=None
                #x=seq.concentration
                #if seq.ifInAutoCatSet:
                    #if 'f' in seq.HPsequence:
                        #markersize = 12
                        #mark='v'
                        #Legend=str(seq.indx)+' '+str(seq.status)+': '+str( seq.concentration)#TODO format and seq.status
                        ##anno=str(seq.indx)
                        #if seq.inClustLen==-1.0:
                            #col='k'
                        #else:
                            #col=labCols[seq.inClustLen]
                    #else:
                        #markersize = 14
                        #mark='x'
                        #col=labCols[seq.inClustLen]
                        ##Legend=str(seq.indx)+' '+str(seq.status)+': '+str( seq.concentration)
                #elif seq.inClustLen==-1.0:
                    #markersize = 4
                    #mark = 'o'
                    #col = 'k'
                #else:
                    #markersize = 8
                    #mark = 'o'
                    #col = labCols[seq.inClustLen]
                #if grInd<numRows:
                    #name=names[grInd,0]
                #else:
                    #name=names[grInd-numRows,1]
                #name.plot(x, 0, mark, markerfacecolor=col,\
                                    #markeredgecolor='k', markersize=markersize,label=Legend)
                #name.legend(prop={'size':8},ncol=2)
                #name.set_ylim((-0.1,0.5))
                #if not anno==None:
                    #name.annotate(anno,xy=(x, 0),xytext=(x, 0.1),textcoords='figure fraction')
            
            #name.set_title('Length '+str(length)+'. Est. number of clusters: '+str(n_clusters))
        
        #plt.setp([a.get_yticklabels() for a in f.axes], visible=False)
        
        #if not saveFig:
            #plt.show()
        #else:
            ##plt.set_size__inches(12,16)
            #plt.savefig(self.writeGraphFilename())
        #return None
    
    #def plot3D(self):
        #jointLabels=self.clustLengths()
        #dictOfLenghts=self.makeDictOfLengths()
        #for length in jointLabels.keys():
            #labelsL=labels.tolist()#list of labels
            #groups=zip(labelsL,dictOfLenghts[length])
            #dictClust = defaultdict(list)#label 2 sequence dictionaly
            #for label, seq in groups:
                #dictClust[label].append(seq)
            #dictQuant={}
            #dictValues={}
            #dictBorders={}
            #for i in range(len(dictClust.keys())):
                #dictQuant[dictClust.keys()[i]]=len(dictClust.values()[i])
                #dictValues[dictClust.keys()[i]]=[seq.concentration for seq in dictClust.values()[i]]
                #dictBorders[dictClust.keys()[i]]=[min(dictValues[dictClust.keys()[i]]),max(dictValues[dictClust.keys()[i]])]
                
            
        #fig = plt.figure()
        #ax = fig.gca(projection='3d')
        #X, Y, Z = axes3d.get_test_data(0.05)
        #ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.3)
        #cset = ax.contour(X, Y, Z, zdir='z', offset=-100, cmap=cm.coolwarm)
        #cset = ax.contour(X, Y, Z, zdir='x', offset=-40, cmap=cm.coolwarm)
        #cset = ax.contour(X, Y, Z, zdir='y', offset=40, cmap=cm.coolwarm)

        #ax.set_xlabel('X')
        #ax.set_xlim(-40, 40)
        #ax.set_ylabel('Y')
        #ax.set_ylim(-40, 40)
        #ax.set_zlabel('Z')
        #ax.set_zlim(-100, 100)

        #plt.show()
    
    #def findLinage(self,seqParam):#TODO So far abandoned
        #foldedAncestors=[]
        #if type(seqParam)==int:
            #bs=self.allSpecies.listOfAllSpec[seqParam].binarySeq
        #elif type(seqParam)==str:
            #if 'f' in seqParam:
                #bs=seqParam[1:]
            #else:
                #bs=seqParam
        #for i in range(1,bs.length-3):
            #ts=binSeq.BinSeq(bs[0:-i])
            #fts=binSeq.FoldedSeq(ts)
            #if fts in self.allSpecies.allFolded:
                #foldedAncestors.append(self.allSpecies.listOfAllSpec[self.allSpecies.listOfAllSpec.index(fts)])
                #print(str(self.allSpecies.listOfAllSpec[self.allSpecies.listOfAllSpec.index(fts)]))
        
    
#################################    
    ##FIX from here, written not for the Results class
    #def getVarAve(self,varEvol,howMany):
        #last=len(varEvol)
        ##print(last)
        #first=last-int(last*howMany)
        ##print(first)
        #lenOfSteady=int(last*howMany)
        ##print(lenOfSteady)
        #steadyVals=varEvol[first:]
        ##print(steadyVals)
        #average= sum(steadyVals) / float(lenOfSteady)
        #return average

    #def getSteadyPops(self,howMany=0.1):#OK
        #''' list of lists, dict -> list of floats
        #evolutions is list of lists of floats. each list corresponds to the time evolution of the variable
        #get average stea
        #'''
        #steadyPops=[self.getVarAve(varEvol,howMany) for varEvol in self.evolutions[1:]]
        
        
        #return steadyPops

    #def indx2EvolNum(self):#Selected only!
        #indxes = [spec.indx for spec in self.simulation.model.selected]
        #indxDict= dict(zip(indxes,range(len(self.simulation.model.selected))))
        
        #return indxDict
    
    #def getSteadyDict(self):#
        #try: 
            #temp=self.simulation.model.selected
        #except:
            #hpSeqs=[spec for spec in self.simulation.model.allSpeciesList]
        #else:
            #hpSeqs=[spec for spec in self.simulation.model.selected]
        #steadyDict=dict(zip(hpSeqs,self.steadyPops))
        
        #return steadyDict
    
    #def getIndxDict(self):
        #indxDict={}
        #for i in xrange(len(self.steadyPops)):
            #indxDict[self.simulation.model.allSpeciesList[i].indx]=self.steadyPops[i]
        
        #return indxDict

    #def whoAreYou(self,interval,length):#TEST
        #'''dict, tuple of 2 floats, length -> list of nmers
        #length is one of:
        #- 'all'
        #- Natural
        #'''
        #sequences=[]
        #if length=='all':
            #for key in self.steadyDict.keys():
                #if self.steadyDict[key]>interval[0] and self.steadyDict[key] < interval[1]:
                    #sequences.append((key,self.steadyDict[key]))
        #else:
            #for key in self.steadyDict.keys():
                #if key.length==length:
                    #if self.steadyDict[key]>interval[0] and self.steadyDict[key] < interval[1]:
                        #sequences.append((key,self.steadyDict[key]))
        
        #return sequences

    #def findSpec(sequence,num2SeqDict):#
        #for key in num2SeqDict.keys():
            #if num2SeqDict[key]==sequence:
                #number=key
                #break
        #return number

    
