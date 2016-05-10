#!/usb/bin/python

"""
This file creates several vesicles and
evolves them through time.
It is used to make populational anasysis of the
innovative and evolutionary properties of hp-vesicles
"""

import os
#import random
import sys
sys.path.append('../')
import routes

import libSimulate


class VPopulation(object):
    """
    ??
    """
    def __init__(self, numGen, numInstance, modelNum, matureWeight, path):
        self.modelNum = modelNum
        self.numGen = numGen
        self.numInstance = numInstance
        self.path = path
        self.matureWeight = matureWeight

    def initPopFiles(self,endTime):
        """
        Initializes initPopFiles in the right directories for the future simulation runs
        Args:
            endTime:

        Returns:

        """


        return None

    def runSimulations(self):

        return None

    def trackDaughters(self):
        return None

    def producePickles(self):
        return None

    def plotGraphics(self):
        return None


def runInitSimulation(modelNum, path, endTime, timeStep=0.0001):
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

if __name__ == "__main__":
    runInitSimulation(18, 'test', 1, 0.1)



