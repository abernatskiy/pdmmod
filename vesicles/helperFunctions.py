#!/usr/bin/python

"""
File with helper functions for analyzing and running vesicle simulations
"""

import sys
sys.path.append('../')
import libSimulate


def runInitSimulation(modelNum, path, endTime, timeStep=0.0001):  #TESTED
    """
    helper function, which runs simulation to produce different starters initPopulation files
    Args:
        modelNum: int. - number of the epdm model
        path: str. - folder where simulation results will be located
        endTime: float - time to end simulation
        timeStep: flota - time step of the simulation

    Returns:
        None
    """
    sDef = libSimulate.Simulation(
        modelNum,
        termCond=('simulateTime', endTime, timeStep),
        rewrite=False,
        specialPath=path,
        numOfRuns=1,
        traj=True,
        log_level='WARNING')
    sDef.runSeveralSeries(paramFile=None, populFile=None)

    return None


def findMatureSeqs(trajFile, startWeight):  #TEST
    """
    Receives a trajectory file and start weight, at which vesicles start to grow
    returns sequences at the time when start weight is reached
    Args:
        trajFile: str. - is located in self.path+'test' and named 'traj0'
        startWeight: int. - usually self.matureWeight/2

    Returns:

    """

    def line2Data(rawList):  #TESTED
        """
        gets as input list of data points from a trajectory file, returns a dict. of populations of the sequences
        Args:
            rawList: list. [str 'seq pop']
        Returns:
            timeMature: float. -- time at which we stop and get sequneces
            seqsAtTime:  dict. {str. sequences: int. population}

        """
        points = {}
        for item in rawList[1:len(rawList) - 1]:
            # get a couple specie -- its population
            point = item.split(' ')
            points[point[0]] = int(point[1])
        return points

    simRes = open(trajFile, 'r')
    timeMature = -1
    seqsAtTime = {}
    weight = 0
    for line in simRes:
        if line[0] == "#":
            continue
        else:
            raw = (line.rstrip('\n')).split(',')
            seqsAtTime = line2Data(raw)
            weight = countWeight(seqsAtTime)
            # print(weight)
            if weight >= startWeight:
                timeMature = float(raw[0])
                break
    simRes.close()

    if timeMature == -1 or seqsAtTime == {}:
            raise ValueError(
                "Simulation was too short to get to the specified weight of " + str(startWeight) +
                ". It's only " + str(weight)
            )

    return timeMature, seqsAtTime


def getSeq(seq):
    """
    Arguments:
     - seq -- str. sequence as depicted in trajectory file
    Returns:
     - hps -- str. actual HP sequence
    """
    if 'f' in seq:
        if '*' in seq:
            hps = seq[2:]
        else:
            hps = seq[1:]
    else:
        hps = seq
    return hps


def makeInitPopFile(seqsAtTime, initFilePath):
    """
    from the dictionary of sequences and their populations makes a initial population file for the simulation run
    Args:
        seqsAtTime: dict. {str. seq: int. pop}
        initFilePath: str.
    Returns:
        None
    """
    initFile = open(initFilePath, 'w')
    initFile.close()
    initFile = open(initFilePath, 'a')
    for (seq, pop) in seqsAtTime.items():
        initFile.write(seq + ' ' + str(pop) + '\n')
    initFile.close()
    return None


def countWeight(seqsAtTime):
    """
    Calculates the weight of the sequences in the current times
    Args:
        seqsAtTime: dict. {str. sequences: int. population}
    Returns:
        weight: int. total weight of the sequences as a number of monomers in them
    """
    weight = 0
    for (seq, pop) in seqsAtTime.items():
        hps = getSeq(seq)
        weight += len(hps) * pop

    return weight


def readPopulations(popFile):
    """
    Coverts initPopFile into dictionary
    Args:
        popFile: str. population file path

    Returns:
        sequences: dict. {str. seq: int. pop}
    """
    sequences = {}
    with open(popFile) as infile:
        for line in infile:
            pair = line.rstrip('\n').split(' ')
            sequences[pair[0]] = int(pair[1])
    return sequences

