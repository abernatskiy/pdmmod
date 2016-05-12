#!/usb/bin/python

"""
This file creates several vesicles and
evolves them through time.
It is used to make populational anasysis of the
innovative and evolutionary properties of hp-vesicles
"""

import os
import sys
import pickle
import matplotlib.pyplot as plt

sys.path.append('../')
import routes

sys.path.extend(routes.routeVesicles)
import hpClasses
from vesicles import vesicle
from vesicles import helperFunctions
from vesicles import vTrajectory
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

    def initPopFiles(self, endTime):  # TESTED
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
            os.mkdir(os.path.join(outputDir, '0000'))
            # make a initial populations file
            inF = os.path.join(outputDir, '0000', 'initPop00000')
            initFiles.append(inF)
            helperFunctions.makeInitPopFile(seqsAtTime, inF)
            print('file ' + inF + ' created')
            os.remove(trFile)

        return initFiles

    def runSimulations(self, initFiles, keepAll='select'):  # TEST
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
        pickle.dump(allVesicles, open(os.path.join(self.path, 'allVesicles.p'), 'wb'))
        return allVesicles

    def producePickles(self, allVesicles):
        """
        goes through all the vesicles produced and selected
        analyzes data and creates pickles
        Args:
            allVesicles: list of lists [[Vesicle]]
        Returns:
            None
        """
        natData = hpClasses.readNativeList(25)
        seqShapeDict = pickle.load(open('../seqShapeDict.p', 'rb'))
        headVTrajectories = []
        for vs in allVesicles:
            headVTrajectories.append(vTrajectory.VTrajectory(
                self.modelNum, 0, 0, 0, self.matureWeight, vs[0].path))
            for v in vs:
                vt = vTrajectory.VTrajectory(
                    v.modelNum, v.generation, v.idInGen, v.motherIdInGen, v.matureWeight, v.path
                )
                vt.pickleGeneration(vt.seqDict(0), 'sd')
                trajectory = vt.getTrajectory()
                pickle.dump(trajectory, open(os.path.join(vt.outputDir, 'traj.p'), 'wb'))
                vt.pickleGeneration(vt.getMassTrajectory(), 'mt')
                vt.pickleGeneration(vt.getPersistenceGn(0, trajectory, natData, 0), 'gf')
                vt.pickleGeneration(vt.getPersistenceGn(1, trajectory, natData, 0), 'ga')
                vt.pickleGeneration(vt.getPersistencePh(0, trajectory, natData, 0), 'pf')
                vt.pickleGeneration(vt.getPersistencePh(1, trajectory, natData, 0), 'pa')
                vt.pickleGeneration(vt.getShapeTrajectories(seqShapeDict, natData), 'sTraj')
        pickle.dump(headVTrajectories, open(os.path.join(self.path, 'headVts.p'), 'wb'))
        return headVTrajectories

    def plotGraphics(self, headVTrajectories):
        for vt in headVTrajectories:
            vt.plotMasesChildren(self.numGen, scaled=True)
            plt.clf()
            vt.plotMasesChildren(self.numGen, scaled=False)
            plt.clf()
            gfs = vt.getGenotypesChildren(0, self.numGen)
            pickle.dump(gfs, open(os.path.join(vt.path, 'gfs.p'), 'wb'))
            gas = vt.getGenotypesChildren(1, self.numGen)
            pickle.dump(gas, open(os.path.join(vt.path, 'gas.p'), 'wb'))
            pfs = vt.getPhenotypesChildren(0, self.numGen)
            pickle.dump(pfs, open(os.path.join(vt.path, 'pfs.p'), 'wb'))
            pas = vt.getPhenotypesChildren(1, self.numGen)
            pickle.dump(pas, open(os.path.join(vt.path, 'pas.p'), 'wb'))
            vt.plotGnNumChildren(gas, 1)
            plt.clf()
            vt.plotGnNumChildren(gfs, 0)
            plt.clf()
            vt.plotPhenoChildren(pfs, 0, scaled=True)
            plt.clf()
            vt.plotPhenoChildren(pas, 1, scaled=True)
            plt.clf()
            vt.plotPhenoGenerations(pfs, 0)
            plt.clf()
            vt.plotPhenoGenerations(pas, 1)
            plt.clf()
            vt.plotGnFreqDistr(gas, 1)
            plt.clf()
            vt.plotGnFreqDistr(gfs, 0)
            plt.clf()

        return None


# Inits and Attributes #
# VTrajectory(modelNum, generation,idInGen,motherIdInGen,matureWeight,path)
# VPoulation(numGen, numInstance, modelNum, matureWeight, termTime, timeStep, path)
# self.idInGen,  self.sequencesAtBirth, self.motherIdInGen,
# self.generation, self.matureWeight = matureWeight, self.modelNum,
# self.path, self.outPath, self.initFile
############################

if __name__ == "__main__":
    vp = VPopulation(50, 30, 18, 20000, 5, 0.0001, './multirun1')
    initFiles = vp.initPopFiles(7)
    allVesicles = vp.runSimulations(initFiles, 'select')
    #allVesicles = pickle.load(open(os.path.join(vp.path, 'allVesicles.p'), 'rb'))
    # headTraj = vp.producePickles(allVesicles)
    #headTraj = pickle.load(open(os.path.join(vp.path, 'headVts.p'), 'rb'))
