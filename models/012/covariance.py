#!/usr/bin/python
import os
import sys
import numpy as np
import scipy.sparse as sps
import os
import matplotlib.pyplot as plt
from pylab import pcolor, show, colorbar, xticks, yticks
#matplotlib.use('Agg')
import scipy
import pylab
import scipy.cluster.hierarchy as sch
import pickle


sys.path.append('../../')
import dictUtils
import hpClasses

path='012_output22/'

def traj2matrix(trajname,startTime,finishTime,timeStep):
    trajFile = open(os.path.join(path,trajname),'r')
    numOfTimePoints=int((finishTime - startTime)/timeStep)+1
    shape = (1,numOfTimePoints)
    evolutions = sps.coo_matrix(shape,dtype='int8')
    seq2num={'H':0}
    breakCondition = False
    seqCount=1
    lineCount=0
    while not breakCondition:
        line = trajFile.readline()
        if line =='':
            breakCondition = True
            print(
                'Termination condition is met on line '+
                str(lineCount)+' in '+str(trajFile))
        elif line[0]=="#":
            continue
        else:
            #print('data at line '+str(lineCount))
            raw = (line.rstrip(',\n')).split(',')
            timePoint=float(raw[0])
            if not timePoint<startTime:
                data = raw[1:]
                for item in data:
                    point=item.split(' ')
                    if point[0] not in seq2num.keys():
                        seq2num[point[0]]=seqCount
                        evolutions = sps.vstack([
                            evolutions,
                            sps.coo_matrix(shape,dtype='int8')
                            ])
                        evolutions+=sps.coo_matrix(
                            ([int(point[1])],([seqCount],[lineCount])),
                            shape=evolutions.shape
                            )
                        seqCount+=1
                    else:
                        evolutions+=sps.coo_matrix(
                            ([int(point[1])],([seq2num[point[0]]],[lineCount])),
                            shape=evolutions.shape)
                    
                    
                lineCount+=1
                if lineCount>=numOfTimePoints:
                    breakCondition=True
                    
    return seq2num,evolutions

def sparseCovMat(matrix):
    mu = matrix.mean(1)
    emu=matrix-mu
    norm = emu.shape[1]-1.
    C=np.dot(emu,emu.T.conjugate())/norm
    return C

def sparseCorrMat(C):#C -- covariance matrix
    d = np.diag(C)
    coeffs = C / np.sqrt(np.outer(d, d))
    return coeffs

def meansOverLen(seq2num,evolutions):
    def getSeqLen(seq):
        if not seq.find('f')==-1:
            seqLen=len(seq)-1
        else:
            seqLen=len(seq)
        return seqLen
    mu = evolutions.mean(1)
    means={}
    for (seq, num) in seq2num.items():
        seqLen=getSeqLen(seq)
        dictUtils.addToDictList(means,seqLen,(num,mu[num].item()))
    return means

def getTop(means,topN):
    top={}
    for seqLen in means:
        means[seqLen] = sorted(means[seqLen], key=lambda t: t[1],reverse=True)
        top[seqLen] = means[seqLen][0:topN]
    return top

def getTopEvolutions(top,evolutions):
    shape=(1,evolutions.shape[1])
    #topEvo=sps.coo_matrix((1,evolutions.shape[1]),dtype='int8')
    empty = True
    count = 0
    indxTop2Indx={}
    for (seqLen, seqList) in top.items():
        for item in seqList:
            indxTop2Indx[count]=item[0]
            count+=1
            if empty:
                topEvo = evolutions.getrow(item[0])
                empty = False
            else:
                topEvo = sps.vstack([
                    topEvo,
                    evolutions.getrow(item[0])
                    ])
    return topEvo, indxTop2Indx
            
    

def convertTopNums2Seqs(num2seq,indxTop2Indx):
    '''returns sequences a dictionary: 
    {indexes of sequences from top: their names}
    '''
    topIndx2Seq={}
    for (topIndx,indx) in indxTop2Indx.items():
        topIndx2Seq[topIndx]=num2seq[indx]
    return topIndx2Seq

def indxZ2Seqs(topIndx2Seq,Z):
    '''indexes of the reordered D matrix -> seq.names
    '''
    reorderedNames={}
    zIndex = Z['leaves']
    for (num, seq) in topIndx2Seq.items():
        reorderedNames[zIndex.index(num)]=seq
    return reorderedNames

def plotBlockCorrMatrix(D,num2seq,indxTop2Indx):
    fig = pylab.figure()
    axdendro = fig.add_axes([0.09,0.1,0.2,0.8])
    Y = sch.linkage(D, method='single', metric = 'correlation')
    Y = Y.clip(0,1000000)
    #make dendrogram matrix
    Z = sch.dendrogram(Y, orientation='right')
    axdendro.set_xticks([])
    axdendro.set_yticks([])
    #
    index = Z['leaves']
    #reorder correlation matrix
    D = D[index,:]
    D = D[:,index]
    #
    axmatrix = fig.add_axes([0.3,0.1,0.6,0.8])
    im = axmatrix.matshow(D, aspect='auto', origin='lower')
    labels = Z['leaves']
    axmatrix.set_xticks(range(0,D.shape[0],20))
    axmatrix.set_yticklabels([])
    axmatrix.grid(False)
    # Plot colorbar.
    axcolor = fig.add_axes([0.91,0.1,0.02,0.8])
    pylab.colorbar(im, cax=axcolor)
    topIndx2Seq = convertTopNums2Seqs(num2seq,indxTop2Indx)
    reorderedNames = indxZ2Seqs(topIndx2Seq,Z)
    # Display and save figure.
    fig.show()
    return reorderedNames, D

def mapSeqsAndIndexes(D,seq2num,reorderedNames):
    maps=[]
    for (indx,seq) in reorderedNames.items():
        maps.append((indx,seq,seq2num[seq]))
    return maps



def plotSlice(D,firstNum,lastNum,natData,maps):
    sliceD=D[firstNum:(lastNum+1),firstNum:(lastNum+1)]
    fig = pylab.figure()
    axmatrix = fig.add_axes([0.05,0.1,0.55,0.7])
    lbs = [item[2] for item in  maps[firstNum:(lastNum+1)]]
    #lbs.reverse()
    axseqs = fig.add_axes([0.6,0.1,0.3,0.7])
    axseqs.set_xticks([])
    tests = [item[1] for item in  maps[firstNum:(lastNum+1)]]
    tests.reverse()
    hpclasses = [hpClasses.getUserFriendData(seq,natData) for seq in tests]
    axseqs.set_yticks(np.arange(len(tests)) * -1)
    for i, s in enumerate(tests):
        #print (i, s.encode("ascii", "backslashreplace"))
        plt.text(
            0.03, -i+0.5, s+':'+(' '*(27-len(s)))+hpclasses[i], 
            fontsize=16,
            family='monospace'
            )
    axseqs.yaxis.grid(True)
    axseqs.set_yticks([])
    im = axmatrix.matshow(sliceD, aspect='auto', origin='lower')
    major_ticks = np.arange(0,len(tests),1)
    axmatrix.set_yticks(major_ticks)
    axmatrix.set_xticks(major_ticks)
    lbs2=[str(item[2]) for item in  maps[firstNum:(lastNum+1)]]
    #lbs2.reverse()
    axmatrix.set_yticklabels(lbs2)
    axmatrix.set_xticklabels(lbs2)
    axcolor = fig.add_axes([0.9,0.1,0.02,0.7])
    pylab.colorbar(im, cax=axcolor)
    fig.show()

if __name__ == "__main__":
    maxLength = 25
    natData = hpClasses.readNativeList(25)
    trajname='traj0'
    seq2num,evolutions =  traj2matrix(trajname,50,550,0.5)
    num2seq = dict(zip(seq2num.values(),seq2num.keys()))
    means =  meansOverLen(seq2num,evolutions)
    topN = 15
    top = getTop(means,topN)
    topEvo, indxTop2Indx = getTopEvolutions(top,evolutions)
    C = sparseCovMat(topEvo)
    D = np.array(sparseCorrMat(C))
    reorderedNames, D = plotBlockCorrMatrix(D,num2seq,indxTop2Indx)
    maps = mapSeqsAndIndexes(D,seq2num,reorderedNames)
    firstNum=170
    lastNum=196
    #plotSlice(D,firstNum,lastNum,'',maps)
    
    
#fig = pylab.figure()
#ax = fig.add_axes([0.3,0.1,0.6,0.8])
#major_ticks = np.arange(0,11,1)
#ax.set_yticks(major_ticks)
#x=np.arange(0,12)
#y=np.arange(0,12)
#ax.plot(x,y)
#plt.show()
