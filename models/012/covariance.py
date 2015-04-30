#!/usr/bin/python
import os
import sys
import numpy as np
import scipy.sparse as sps
import os

sys.path.append('../../')
import dictUtils

path='012_output10/'

def traj2matrix(trajname,numOfTimePoints):
    trajFile = open(os.path.join(path,trajname),'r')
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
            raw = (line.rstrip(',\n')).split(',')
            timePoint=float(raw[0])
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
                    try:
                        evolutions+=sps.coo_matrix(
                            ([int(point[1])],([seq2num[point[0]]],[lineCount])),
                            shape=evolutions.shape)
                    except:
                        print(point)
                        print(evolutions)
                        print(lineCount)
                        print(seqCount)
                    
            lineCount+=1
                    
    return evolutions



trajname='traj0'
numOfTimePoints=201
evo = traj2matrix(trajname,numOfTimePoints)
mu = evo.mean(1)

emu=evo-mu
norm = emu.shape[1]-1.
C=np.dot(emu,emu.T.conjugate())/norm



