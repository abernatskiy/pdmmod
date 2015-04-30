#!/usr/bin/python
import os
import sys
import numpy as np
import scipy.sparse as sps
import os
import matplotlib
matplotlib.use('Agg')

sys.path.append('../../')
import dictUtils

path='012_output10/'

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
    topEvo=sps.coo_matrix((1,evolutions.shape[1]),dtype='int8')
    for (seqLen, seqList) in top.items():
        for item in seqList:
            topEvo = sps.vstack([
                topEvo,
                evolutions.getrow(item[0])
                ])
    return topEvo
            
    
trajname='traj0'
numOfTimePoints=201
seq2num,evo = traj2matrix(trajname,50,100,0.5)
#C=sparseCovMat(topEvo)


