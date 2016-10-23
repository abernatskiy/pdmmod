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
import subprocess
import pandas as pd

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
            numGen: number of generations in every lineage
            numInstance: number of linages in the population
            modelNum: number of the model used to model vesicles chemistry
            matureWeight: weight at which vesicles split
            termTime: time at which simulations stop
            timeStep: the time step of the simulations
            path: path to the main folder containig lineage folders (must be full path!!!)
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


    def restoreInitFiles(self):
        initFiles = []
        for i in range(self.numInstance):
            outputDir = os.path.join(self.path, 'l' + str("%04d" % i))
            initFiles.append(os.path.join(outputDir, '0000', 'initPop00000'))
        return initFiles

    def writePythonFiles(self,initFiles,maxImportRate): #TESTED
        def wrp(infile,string):
            return infile.write(string+'\n')

        pythonFiles = []
        for i in range(self.numInstance):
            lineagePath = os.path.join(self.path, 'l' + str("%04d" % i))
            pythonFile = os.path.join(lineagePath,'run.py')
            pf = open(pythonFile,'w')
            pf.close()
            pythonFiles.append(pythonFile)
            with open(os.path.join(lineagePath,'run.py'),'a') as pf:
                wrp(pf,'import pickle')
                wrp(pf,'import sys')
                wrp(pf,'import os')
                wrp(pf,'sys.path.append("' + str(routes.routeVesicles) + '")')
                wrp(pf, 'sys.path.append("' + str(routes.routePDM) + '")')
                wrp(pf, 'import helperFunctions')
                wrp(pf,'from vesicles import vesicle')
                wrp(pf,'allVesicles = []')
                wrp(pf,'importRates = []')
                wrp(pf,'totalRates = []')
                wrp(pf,'seqs = helperFunctions.readPopulations("' +
                    str(initFiles[i]) +
                                   '")')
                wrp(pf,
                    'v=vesicle.Vesicle('+
                        'generation=0, sequences=seqs, idInGen=0, motherIdInGen=0,' +
                        'matureWeight=' + str(self.matureWeight) + ', modelNum=' + str(self.modelNum) + ',' +
                        'path="' + str(lineagePath) +
                        '", paramFile="'+
                        str(os.path.join(lineagePath,'parameters.ini')) + '")'
                    )
                wrp(pf,
                    'v.makeInitParamFile()')
                wrp(pf,
                    'vs, ir, tr = v.growSelectTime(' +
                    str(self.termTime) + ', ' +
                    str(self.timeStep) + ', ' + str(self.numGen) + ',' + str(maxImportRate) + ')'
                    )
                wrp(pf,'allVesicles.append(vs)')
                wrp(pf,'importRates.append(ir)')
                wrp(pf,'totalRates.append(tr)')
                wrp(pf,'pickle.dump(allVesicles, open(os.path.join("' +
                    str(lineagePath) + '", "allVesicles.p"), "wb"))')
                wrp(pf, 'pickle.dump(importRates, open(os.path.join("' +
                    str(lineagePath) + '", "importRates.p"), "wb"))')
                wrp(pf, 'pickle.dump(totalRates, open(os.path.join("' +
                    str(lineagePath) + '", "totalRates.p"), "wb"))')
        return pythonFiles

    def writeShells(self,pythonFiles,onNode=0):#TESTED
        """

        Args:
            pythonFiles:
            onNode:

        Returns:

        """
        shellFiles = []
        for i in range(self.numInstance):
            pythonFile = pythonFiles[i]
            shell = os.path.join(self.path, 'l' + str("%04d" % i),'shell.sh')
            shellFiles.append(shell)
            inFile = open(shell,'w')
            inFile.close()
            inFile = open(shell,'a')
            inFile.write('#!/bin/bash\n')
            inFile.write('#$ -S /bin/bash\n')
            inFile.write('#$ -N p' + str(self.modelNum)+'ves' + str(i) + '\n')
            inFile.write('#$ -cwd\n')
            if onNode == 0:
                inFile.write('#$ -q cpu_long\n')
            else:
                if not type(onNode)==int:
                    inFile.write('#$ -l highio=1\n')
                    inFile.write('#$ -q cpu_long\n')
                else:
                    inFile.write('#$ -q cpu_long@node'+str("%03d" %onNode)+'\n')
            inFile.write('#$ -P kenprj\n')
            inFile.write('\n')
            inFile.write('cd '+routes.routeVesicles+'\n')
            inFile.write(routes.path2python+' '+str(pythonFile)+'\n')
            inFile.close()

        return shellFiles

    def runSimulations(self, shellFiles):  # TEST
        jobsRun = []
        for i in range(self.numInstance):
            p = subprocess.Popen(('qsub', shellFiles[i]),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            out, err = p.communicate()
            #time.sleep(1)
            output = out.decode().split(' ')
            print(output)
            jobsRun.append(int(output[2]))

        return jobsRun

    def produceHeadTrajectories(self): #TEST
        """
        Produces head trajectories if allVesicles haven't been given
        Returns:
            [VTrajectory]
        """
        headVTrajectories = []
        for i in range(self.numInstance):
            path = os.path.join(self.path, 'l' + str("%04d" % i))
            vt = vTrajectory.VTrajectory(
                self.modelNum, 0, 0, 0, self.matureWeight, path
            )
            headVTrajectories.append(vt)


        return headVTrajectories

    def restoreAllVesicles(self):
        def selectWinner(currFolder, generation):
            out0 = subprocess.check_output(['tail','-1',os.path.join(currFolder,'weights00000.txt')])
            if not generation == 0:
                out1 = subprocess.check_output(['tail','-1',os.path.join(currFolder,'weights00001.txt')])
            else:
                return [1, 0], (float(str(out0).split(' ')[0][2:]), float(str(out0).split(' ')[0][2:]))
            splitTime0 = float(str(out0).split(' ')[0][2:])
            splitTime1 = float(str(out1).split(' ')[0][2:])
            if splitTime0 < splitTime1:
                return [1,0], (splitTime0, splitTime1)
            else:
                return [0,1], (splitTime0, splitTime1)

        vesiclesDF = pd.DataFrame({'ves_id':[],'linegae': [],'generation': [],'splitTime': [],'winner':[],
                                   'path_traj':[],'path_weight':[],'mother_id':[]},index=[])
        currId = 0
        # for every vesicle lineage
        for linage in range(self.numInstance):
            # find the head folder
            headFolder = os.path.join(self.path,'l'+str("%04d" % linage))
            # for every generation
            for generation in range(self.numGen):
                # find the folder which belongs to this generation
                currFolder = os.path.join(headFolder,str("%04d" % generation))
                winner, (splitTime0, splitTime1) = selectWinner(currFolder,generation)
                currentDF = pd.DataFrame({'ves_id': [currId,currId+1],
                                                     'linegae': [linage,linage],
                                                     'generation': [generation,generation],
                                                     'splitTime': [splitTime0,splitTime1],
                                                     'winner': winner,
                                                     'path_traj': [os.path.join(currFolder,'growth00000.txt'),
                                                                     os.path.join(currFolder, 'growth00001.txt')],
                                                     'path_weight': [os.path.join(currFolder,'weights00000.txt'),
                                                                     os.path.join(currFolder, 'weights00001.txt')]
                                                     }, index=[currId,currId+1]
                                                    )
                vesiclesDF = pd.concat(vesiclesDF,currentDF,axis=1)
                currId+=2
        return vesiclesDF

    def producePickles(self, allVesicles): #TEST
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
            headVT = vTrajectory.VTrajectory(
                self.modelNum, 0, 0, 0, self.matureWeight, vs[0].path)
            headVTrajectories.append(headVT)
            timeEvo, selected = headVT.getDivisionTimeEvolution(self.numGen)
            pickle.dump(timeEvo,open(os.path.join(vs[0].path,'divTimeEvo.p'),'wb'))
            pickle.dump(selected, open(os.path.join(vs[0].path, 'selected.p'), 'wb'))
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

    def plotIndividualGraphs(self, headVTrajectories): #TEST
        """

        Args:
            headVTrajectories: [VTrajectory]

        Returns:

        """
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

    def plotDivTimeEvolutions(self): #TODO
        plt.clf()
        for expt in range(self.numInstance):
            path = os.path.join(self.path, 'l' + str("%04d" % expt))
            evolution = pickle.load(open(os.path.join(path, 'divTimeEvo.p'),'rb'))
            plt.plot(list(range(len(evolution))),evolution,label='expt '+str(expt))

        plt.legend(loc='best',fontsize=8)
        plt.savefig(os.path.join(self.path,'timeEvo.png'))



# Inits and Attributes #
# VTrajectory(modelNum, generation,idInGen,motherIdInGen,matureWeight,path)
# VPoulation(numGen, numInstance, modelNum, matureWeight, termTime, timeStep, path)
# self.idInGen,  self.sequencesAtBirth, self.motherIdInGen,
# self.generation, self.matureWeight = matureWeight, self.modelNum,
# self.path, self.outPath, self.initFile
############################

if __name__ == "__main__":
    vp = VPopulation(numGen=25, numInstance=30, modelNum=18, matureWeight=20000, termTime=4, timeStep=0.0001,
                     path=os.path.join(routes.routeVesicles,'multirun2'))
    #vp.plotDivTimeEvolutions()
    # initFiles = vp.initPopFiles(endTime=7)
    # initFiles = ['1','2','3']
    # pfs = vp.writePythonFiles(initFiles,maxImportRate=10000)
    # shellFiles = vp.writeShells(pfs,0)
    #vp.runSimulations(shellFiles)
    # allVesicles = vp.runSimulations(initFiles)
    # pickle.dump(allVesicles,open('allVesicles1.p','wb'))
    #allVesicles = pickle.load(open(os.path.join(vp.path, 'allVesicles.p'), 'rb'))
    headTraj = vp.produceHeadTrajectories()
    #headTraj = pickle.load(open(os.path.join(vp.path, 'headVts.p'), 'rb'))
