#/usr/bin/python
"""
This module takes in results of *pdmmod* simulations, 
and transforms them into desirable data. It also make various plots of data.
"""

#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from os import system as system
import numpy as np
import glob
import os
import subprocess
import routes
import pickle
import numpy as np
from collections import OrderedDict
import math
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
import scipy.stats
from sklearn import cluster
from matplotlib import colors
import sys
from collections import Counter

import hpClasses
from result import *
from clusteredHP import *

sys.path.append('hp-model-scripts')

class Trajectory(object):
    '''
    This class analyzes various aspects of stochastic simulations
    in the pdmmod framework
    '''
    def __init__(self, modelNum, simNum,trajNum):
        '''
         Arguments:
          - modelNum -- int, number of the model
          - simuNum -- int, number of the simulation, simulations within
          one model are usually differ by different parameters
          - trajNum -- int, number of trajectory. A simulation with a given set of the parameters can be run for several times to form an ensemble
        '''
        self.modelLocation = os.path.join(
             routes.routePDM , 'models', str("%03d" %modelNum))
        self.outputDir = os.path.join(
            self.modelLocation,str("%03d" %modelNum)+'_output'+str(simNum))
        self.trajFile = os.path.join(self.outputDir,'traj'+str(trajNum))
        self.trajectory = (modelNum, simNum, trajNum)
        self.trajNum = trajNum
        #self.parameters = self.readParams()
    
    def readParams(self):
        '''reads parameters from the header of the trajectory file
        '''
        with open(self.trajFile) as infile:
            for line in infile:
                if line[0]=='#':
                    data = line.split(' ')
                    if not data[1] == 'Parameters:':
                        continue
                    else:
                        parameters = data[2:]
                else:
                    return parameters
    
    def seqDict(self,minTime):
        '''
        Arguments:
         - minTime -- time at which we start the record
        Returns:
         - seqDict -- dict. {str sequence name: [int population]}
         lists populations over time for all sequences ever met since minTime
         - records -- number of records
        '''
        seqDict = {}
        times = []
        with open(self.trajFile) as infile:
            for line in infile:
                #skip comments
                if not line[0]=='#':
                    dlist=line.split(',')[0:-1]
                    time = float(dlist[0])
                    if time >= minTime:
                        times.append(time)
                        for couple in dlist[1:]:
                            pair = couple.split(' ')
                            #if we saw this sequence
                            if pair[0] in seqDict.keys():
                                seqDict[pair[0]].append(int(pair[1]))
                            else:
                                #if new seq doesn't have *
                                if not '*' in pair[0]:
                                    try:
                                        seqDict[pair[0]]=[int(pair[1])]
                                    except:
                                        print(time)
                                        print(pair)
                                        raise ValueError
                                else:
                                    theKey = ('f'+(pair[0])[2:])
                                    if not 'f' in pair[0]:
                                        print(time)
                                        raise ValueError(pair[0])

                                    elif theKey in seqDict.keys():
                                        seqDict[theKey].append(int(pair[1]))
                                    else:
                                        seqDict[theKey]=[int(pair[1])]

        records = len(times)
        print('number of records: ',records)
        return seqDict, records
    
    def aveSeqDict(self,seqDict,records):
        '''caluculates average over the time records for every population
        Arguments: (outputs of self.seqDict(minTime)
         - records -- int, number of the records
         - seqDict -- dict. {str sequence name: [int population]}
         lists populations over time for all sequences even met since minTime
         Returns:
         - aveSeqDict -- dict, {str sequence name: float average population}
        '''
        aveSeqDict = {}
        for seq in seqDict.keys():
            aveSeqDict[seq]=sum(seqDict[seq])/records
        return aveSeqDict
    
    def getFreqs(self,seqAveDict,maxLength):
        '''returns a distribution of populations for every length up to
        maxLength, and an integral of it
        Arguments:
         - seqAveDict -- dict, {str sequence name: float average population}
         - maxLength -- int, maximum length of polymers in the simulation
        Returns:
         - freqs -- dict, {int length:{float population, int frequency}}
         - intFr -- dict, {int length:{float population, int frequency integral}}
        '''
        freqs = dict([(i,{}) for i in  range(1,maxLength+1)])
        for (seq, pop) in seqAveDict.items():
            if 'f' in seq:
                if '*' in seq:
                    l = len(seq)-2
                else:
                    l = len(seq)-1
            else:
                l = len(seq)
            #if sequences with the same population've been met
            if pop in freqs[l].keys():
                (freqs[l])[pop]+=1
            else:
                (freqs[l])[pop]=1
        newFreqs = {}
        for (l, fr) in freqs.items():
            newFreqs[l]=OrderedDict(sorted(fr.items(), key=lambda t: t[0], reverse=False))
        intFr = {}
        for (l, fr) in newFreqs.items():
            intFr[l]={}
            for (freq,count) in fr.items():
                counts = list(fr.values())
                f = list(fr.keys())
                i = f.index(freq)
                intFr[l][freq]=sum(counts[i:])
        
        return freqs, intFr
    
    def fitInLen(self,intFr):
        '''fits integrals of frequencies from 
        self.getFreqs(aveSeqDict,maxLength) to polynomial functions
        '''
        fits = {}
        for (length, values) in intFr.items():
            xx = []
            yy = []
            for (pop,freq) in values.items():
                xx.append(math.log10(pop))
                yy.append(math.log10(freq))
                x = np.array(xx)
                y = np.array(yy)
                A = np.vstack([x, np.ones(len(x))]).T
                fits[length] = np.linalg.lstsq(A, y)[0]
        return fits

    def plotInLen(self,freqs,fits,title,minLength,maxLength):
        '''plots integrals of the frequencies and their fits
        '''
        nc = 3
        fig, axes = plt.subplots(
            nrows=int((maxLength-minLength+1)/2/nc), ncols=nc, figsize=(12, 12)
            )
        index = 0
        for (length,freqs) in freqs.items():
            if length>=minLength and length<=maxLength and length%2==1:
                sortedFreqs = OrderedDict(sorted(freqs.items(),key=lambda t: t[0], reverse=False))
                axes[int((index)/nc),(index)%(nc)].plot(
                    list(sortedFreqs.keys()),list(sortedFreqs.values()),'o'
                    )
                try:
                    m, c = fits[length-1]
                except KeyError:
                    m, c = (0,0)
                else:
                    axes[int((index)/nc),(index)%(nc)].plot(
                        list(sortedFreqs.keys()),
                        [(10**(c)*xi**(m)) for xi in sortedFreqs.keys()],
                        linewidth = 3,
                        label = 'y = '+str("%.2f" %(10**c))+'x^'+str("%.2f" %m)
                        )
                axes[int((index)/nc),(index)%(nc)].set_yscale('log')
                axes[int((index)/nc),(index)%(nc)].set_xscale('log')
                #axes[int((index)/nc),(index)%(nc)].legend()
                axes[int((index)/nc),(index)%(nc)].set_title(str(length)+'-mers')
                index+=1
        
        plt.suptitle(title,fontsize=25)
        plt.savefig(os.path.join(
            self.outputDir,'inlen'+str(self.trajectory[2])+'.pdf'))
        plt.savefig(os.path.join(self.outputDir,'inlen'+str(self.trajectory[2])+'.png'))

    def seqAvesNoFold(self,aveSeqDict):
        '''unites folded and unfolded versions of the sequences 
        in the same key of the dictionary
        '''
        saa = {}
        for (seq,pop) in aveSeqDict.items():
            if 'f' in seq:
                if '*' in seq:
                    hps = seq[2:]
                else:
                    hps = seq[1:]
            else:
                hps = seq

            if hps in saa.keys():
                saa[hps]+=pop
            else:
                saa[hps]=pop
        return saa
    
    def categorizeForScatter(self,saa,natData):
        autox = []
        autoy = []
        foldx = []
        foldy = []
        regx = []
        regy = []
        for (seq,pop) in saa.items():
            l = len(seq)
            #if sequence is foldable
            if seq in natData.keys():
                if (not natData[seq][1] == 'N') and (not seq.find('HHH')==-1):
                    autox.append(l)
                    autoy.append(pop)
                    #ax.scatter(l,pop,color='r')
                else:
                    foldx.append(l)
                    foldy.append(pop)
                #ax.scatter(l,pop,color='b')
            else:
                regx.append(l)
                regy.append(pop)
                    #ax.scatter(l,pop,color='0.75')
        return autox,autoy,foldx,foldy,regx,regy
    
    def plotSeqsAvesLen(self,categories):
        (autox,autoy,foldx,foldy,regx,regy) = categories
        plt.gcf().subplots_adjust(bottom=0.15)
        plt.gcf().subplots_adjust(left=0.15)
        fig = plt.figure(1, figsize=(9,6))
        ax = fig.add_subplot(111)
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')

        ax.scatter(regx,regy,color='0.4')
        ax.scatter(foldx,foldy,color='b')
        ax.scatter(autox,autoy,color='r')

        ax.set_yscale('log')
        ax.set_xticks([1,5,10,15,20,25])
        ax.set_xticklabels([r"$1",r"$5$",r"$10$",r"$15$",r"$20$",r"$25$"],fontsize = 25)
        ax.set_yticks([0.000001,0.0001,0.01,1,100])
        ax.set_yticklabels(
           [r"$10^{-6}$",r"$10^{-4}$",r"$10^{-2}$",r"$1$",r"$10^2$"],
           fontsize = 25)
        ax.get_yaxis().get_major_formatter().labelOnlyBase = False
        ax.xaxis.set_tick_params(width=1.5)
        ax.yaxis.set_tick_params(width=1.5)
        ax.set_ylabel('population',fontsize = 30)
        ax.set_xlabel(r'length',fontsize = 30)
        ax.set_xlim(0,26)
        ax.set_ylim(0.000001)
        plt.savefig(os.path.join(
            self.outputDir,'scatter'+str(self.trajectory[2])+'.pdf'))
        plt.savefig(os.path.join(
            self.outputDir,'scatter'+str(self.trajectory[2])+'.png'))
        
    def getShapeTrajectories(self,seqShapeDict,natData):#TESTED
        '''instead of keeping track of sequences
        this funtion produces trajectory of folds (shapes)
        Returns:
         - [[[int. shape number, int. number of realizations] ]]
        '''
        sTraj = []
        with open(self.trajFile) as infile:
            for line in infile:
                shapes = {}
                #skip comments
                if not line[0]=='#':
                    dlist=line.split(',')[0:-1]
                    time = float(dlist[0])
                    for couple in dlist[1:]:
                        seq = getSeq(couple.split(' ')[0])
                        if seq in natData:
                            shape = seqShapeDict[seq]
                            if shape not in shapes:
                                shapes[shape] = 1#add shape, it has one realization
                            else:
                                shapes[shape] += 1
                    
                    sTraj.append(list(shapes.items()))
    
        return sTraj

    def getMassTrajectory(self):
        mass = []
        with open(self.trajFile) as infile:
            for line in infile:
                #skip comments
                massAtTime = 0
                if not line[0]=='#':
                    dlist=line.split(',')[0:-1]
                    time = float(dlist[0])
                    for couple in dlist[1:]:
                        l = len(getSeq(couple.split(' ')[0]))
                        massAtTime += l*int(couple.split(' ')[1])
                    mass.append(massAtTime)
        return mass
    
    def getTrajectory(self,timeStep):
        '''
        returns dict {float time: [list of present sequences]}
        '''
        traj = {}
        time = 0
        with open(self.trajFile) as infile:
            for line in infile:
                #skip comments
                if not line[0] == '#':
                    dlist = line.split(',')[0:-1]
                    traj[time] = [item.split(' ')[0] for item in dlist[1:]]
                    time += timeStep
        return traj

    
    def getPersistencePh(self,autoOrFold,natData):#TEST
        '''
        calculates in how many variants either folds or autocats
        ale present in every moment
        Arguments:
         - autoOrFold is one of:
          * 1 for autocats
          * 0 for folders
          * -1 for all sequences
         - natData: dict {str. hpseq: (int. nativeEnergy, str. catPattern)}
        Returns:
         - persistence: 
        Notes:
         - requires trajectory pickle in the form traj<trajNum>.p
          {time: [hpseq1, hpseq2 ...]}
        '''
        trajectory = pickle.load(open(os.path.join(
            self.outputDir,
            'traj'+str(self.trajectory[-1])+'.p'
            ),'rb'))
        persistence = []
        for (time,listOfSeq) in trajectory.items():
            representations = 0
            for seq in listOfSeq:
                if test(testFunction(seq),natData)>=autoOrFold:
                    #if it's an active autocat, check if there's 
                    #an inactive version
                    if ('f*' in seq and (not 'f'+getSeq(seq) in listOfSeq)) or\
                        ('f' in seq and (not 'f*' in seq)):
                        representations+=1
                    elif ('f*' in seq and ('f'+getSeq(seq) in listOfSeq)):
                        continue
                    else:
                        continue
            persistence.append(representations)
        return persistence
    
    def getPersistenceGn(self,autoOrFold,trajectory,natData,minTime):#TEST
        '''requires pickle of trajectory.
        returns how many time each sequence (either folded or auto)
        occurs during the time since minTime
        autoOrFold is one of:
         - 1 for 'auto'
         - 0 for 'fold'
         - -1 for all sequences
        '''
        #trajectory = pickle.load(open(os.path.join(
            #self.outputDir,
            #'traj'+str(self.trajectory[-1])+'.p'
            #),'rb'))
        genotypes = []
        for (time,listOfSeq) in trajectory.items():
            if time>=minTime:
                selected = []
                for seq in listOfSeq:
                    if testFunction(seq,natData)>=autoOrFold:
                        #count only folded variants
                        if ('f*' in seq and (not 'f'+getSeq(seq) in listOfSeq)) or\
                            ('f' in seq and (not 'f*' in seq)):
                            selected.append(getSeq(seq))
                        elif ('f*' in seq and ('f'+getSeq(seq) in listOfSeq)):
                            continue
                        else:
                            continue
                genotypes+=selected
        return Counter(genotypes)

def getSeq(seq):
    '''
    Arguments:
     - seq -- str. sequence as depicted in trajectory file
    Returns:
     - hps -- str. actual HP sequence
    '''
    if 'f' in seq:
        if '*' in seq:
            hps = seq[2:]
        else:
            hps = seq[1:]
    else:
        hps = seq
    return hps

def testFunction(seq,natData):
    '''checks if the seq is either a folder or an autocat
    '''
    hps = getSeq(seq)
    if seq in natData.keys():
        if not natData[seq[1:]][-1] == 'N':
            return 1
        else:
            return 0
    else:
        return -1

#natData = hpClasses.readNativeList(25)
#tr = Trajectory(18,37,0)
#autocats = tr.getAutcatsNumber(natData)

#from HPlibraryReader import *
#sds = pickle.load(open(os.path.join(tr.outputDir,'sds1.p'),'rb'))
#saa = tr.seqAvesNoFold(sds)
#tr.plotSeqsAvesLen(tr.categorizeForScatter(saa,natData))



