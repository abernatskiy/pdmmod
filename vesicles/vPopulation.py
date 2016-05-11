#!/usb/bin/python

"""
This file creates several vesicles and
evolves them through time.
It is used to make populational anasysis of the
innovative and evolutionary properties of hp-vesicles
"""

import os
import sys

sys.path.append('../')
# import routes
import vesicle
import helperFunctions
import vTrajectory
from subprocess import call


class VPopulation(object):
    """
    ??
    """

    def __init__(self, numGen, numInstance, modelNum, matureWeight, termTime, timeStep, path):
        """
        ??
        Args:
            numGen:
            numInstance:
            modelNum:
            matureWeight:
            termTime:
            timeStep:
            path:
        """
        self.modelNum = modelNum
        self.numGen = numGen
        self.numInstance = numInstance
        self.path = path
        self.matureWeight = matureWeight
        self.termTime = termTime
        self.timeStep = timeStep

    def initPopFiles(self, endTime):  #TESTED
        """
        Initializes initPopFiles in the right directories for the future simulation runs
        All the init trajectories must be in the self.path/test
        Args:
            endTime: the time at which simulations which make init files stop

        Returns:

        """
        initFiles = []
        for i in range(self.numInstance):
            # Run simulation
            helperFunctions.runInitSimulation(self.modelNum, os.path.join(self.path, 'test'), endTime, timeStep=0.0001)
            # Detect time and sequences
            trFile = os.path.join(self.path, 'test', 'traj0')
            time, seqsAtTime = helperFunctions.findMatureSeqs(
                trFile, self.matureWeight / 2
            )
            # make an output directory
            outputDir = os.path.join(self.path, 'l' + str("%04d" % i))
            try:
                os.mkdir(outputDir)
            except FileExistsError:
                print('dir ' + outputDir + ' exists')
                call(['rm', '-r', outputDir])
                os.mkdir(outputDir)
            os.mkdir(os.path.join(outputDir,'0000'))
            # make a initial populations file
            inF = os.path.join(outputDir, '0000', 'initPop00000')
            initFiles.append(inF)
            helperFunctions.makeInitPopFile(seqsAtTime, inF)
            print('file ' + inF + ' created')
            os.remove(trFile)

        return initFiles

    def runSimulations(self, initFiles, keepAll='select'):
        """

        Args:
            initFiles:
            keepAll: is one of:
                'random'
                True
                'select'

        Returns:
            allVesicles -- list of lists of objects type Vesicle
        """
        allVesicles = []
        for i in range(self.numInstance):
            seqs = helperFunctions.readPopulations(initFiles[i])
            v = vesicle.Vesicle(
                generation=0, sequences=seqs, idInGen=0, motherIdInGen=0,
                matureWeight=self.matureWeight, modelNum=self.modelNum,
                path=os.path.join(self.path, 'l' + str("%04d" % i))
            )
            allVesicles.append(v.growAndSplit(self.termTime, self.timeStep, self.numGen, keepAll))

        return allVesicles

    def trackDaughters(self):
        return None

    def producePickles(self, allVesicles):
        for vs in allVesicles:
            for v in vs:
                pass
        return None

    def plotGraphics(self):
        return None

# Vesicle Attributes ####
# self.idInGen,  self.sequencesAtBirth, self.motherIdInGen,
# self.generation, self.matureWeight = matureWeight, self.modelNum,
# self.path, self.outPath, self.initFile
############################

if __name__ == "__main__":
    vp = VPopulation(2,2,18,600,1,0.0001,'./test')
    initFiles = vp.initPopFiles(1)
