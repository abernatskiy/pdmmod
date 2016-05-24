"""
This module defines class Experiment to run several pdmMod simulations 
with different simulation parameters on biocomp cluster
"""

import routes
import sys
import subprocess
import os
import pickle
import itertools

sys.path.append('../../')  # BUG potentially
import libSimulate
import math
import result
import time
import pandas as pn


class Experiment(object):
    '''class Experiment
    during one experiment values of parameters change
    a vector of changes is giving.
    According to it simulations are run.
    Files MUST be located in the directory with the name of experimentName
    Args:
        experimentName (str): 
        name of the folder in which experiment parameters are.
        modelNum (int): the number of the model in the pdmMod directory 'models'
        new (bool): is experiment new or we are restoring data
    Attributes:
        experiment (str): name of the folder in which experiment parameters are.
        modelNum (int): the number of the model in the pdmMod directory 'models'
        new (bool): is experiment new or we are restoring data
        termCond (tuple): (str, float, float) -- termination condition 
        (how to terminate, when to terminate, how often to record data), 
        see pdmmod usage
        numOfRuns (int):
        traj -- bool
    '''

    # pylint: disable=too-many-instance-attributes
    def __init__(self, experimentName, modelNum, new):
        self.experiment = experimentName
        self.modelNum = modelNum
        self.new = new
        if not new:
            self.restore()  # TODO

    def __str__(self):
        return self.experiment + ' for the model #' + str(self.modelNum)

    def initNew(self, termCond, numOfRuns, traj):  # TODO
        '''initiates new Experiment instance to run in future
        * termCond -- Tuple ()
        '''
        self.termCond = termCond
        self.numOfRuns = numOfRuns
        self.traj = traj
        self.makeParams()
        self.writeSimParams()

    def writeSimParams(self):
        paramFileName = os.path.join(self.experiment, 'simParams.txt')
        paramFile = open(paramFileName, 'w')
        paramFile.write(
            'termCond = ' + str(self.termCond[0]) + ' ' +
            str(self.termCond[1]) + ' ' +
            str(self.termCond[2]) + '\n')
        paramFile.write('traj = ' + str(self.traj) + '\n')
        paramFile.write('numOfRuns = ' + str(self.numOfRuns) + '\n')
        paramFile.close()
        return None

    def readParameters(self):
        '''reads variable and static parameters of the simulation from the
        corresponding files
        '''
        # types = {'float':float, 'int':int, 'bool':bool, 'str':str}
        try:
            p = subprocess.check_call(
                ['mkdir', self.experiment], stderr=subprocess.PIPE
            )
        except:
            pass
        else:
            raise FileNotFoundError(
                "There is no directory \"" + self.experiment + "\".\n " +
                "You must have this directory. We created it for you.\n " +
                "Put there files constant.ini and variable.ini.\n constant.ini" +
                " has the formant of parameters.ini and has all the parameters" +
                " which are kept constant during the experiment.\n variable.ini" +
                " has variable parameters it's format is the following:\n" +
                "parameter1_type parameter1_name\n val1 val2 val3 ...\n" +
                "parameter2_type parameter2_name\n val1 val2 val3 ...\n" +
                " types are python types: float, int, bool(0, 1), str")

        # read constants
        with open(os.path.join(self.experiment, 'constant.ini'), 'r') as content_file:
            constant = content_file.read()

        # read variables
        self.numOfExperiments = 1
        variables = []  # list of lists of values of variables
        with open(os.path.join(self.experiment, 'variable.ini'), 'r') as content_file:
            variableSep = (content_file.read()).split('\n')
            if not len(variableSep) % 2 == 0:
                print(variableSep)
                if not variableSep[-1] == '':  # dealing with extra empty line
                    raise ValueError(
                        'Wrong number of lines in \"variable.ini\" file'
                    )
                else:
                    print('extra line in \"variable.ini\". ignoring')
                    variableSep.pop(-1)  # dealing with extra empty line
            for i in range(int(len(variableSep) / 2)):
                # varValues are lists of strings of format varName = value
                line1 = variableSep[2 * i].split(' ')
                line2 = variableSep[2 * i + 1].split(' ')
                varValues = [line1[1] + ' = ' + val for val in line2]
                self.numOfExperiments = self.numOfExperiments * len(varValues)
                variables.append(varValues)
        variables = list(itertools.product(*variables))

        return constant, variables

    def getSimNums(self):
        '''simulations of the experiment will have some numbers, which 
        are set during the simulations' initiation. this function determines
        these numbers
        Returns:
            int -- the number of the first simulation to run
        '''
        path = './'  # BUG potentially: FIX
        dirs = (next(os.walk(path))[1])
        nums = []
        for directory in dirs:
            if '_output' in directory:
                tmp = directory.replace(str("%03d" % self.modelNum) + '_output', '')
                if tmp == '':
                    nums.append(0)
                else:
                    nums.append(int(tmp))
        if nums == []:
            currentRun = 0
        else:
            currentRun = max(nums) + 1
        print('first run #: ' + str(currentRun))
        return currentRun

    def makeParams(self):
        '''writes a parameters files for all the simulation.
        format of the file: parameters<simulation number>.ini
        '''
        constant, variables = self.readParameters()
        print(variables)
        firstSim = self.getSimNums()
        self.firstSim = firstSim
        sFile = open(
            os.path.join(self.experiment, 'simParams.txt'),
            'a'
        )
        sFile.write('termCond = ' +
                    str(self.termCond[0]) + ' ' +
                    str(self.termCond[1]) + ' ' +
                    str(self.termCond[2]) + '\n')
        sFile.write('numOfRuns = ' + str(self.numOfRuns) + '\n')
        sFile.write('traj = ' + str(self.traj) + '\n')
        sFile.close()
        for i in range(firstSim, firstSim + self.numOfExperiments):
            pFile = open(
                os.path.join(self.experiment, 'parameters' + str(i) + '.ini'),
                'a'
            )
            pFile.write(constant)
            for line in variables[i - firstSim]:
                pFile.write(line + '\n')
        pFile.close()

    def initAndRun(self, kernels, onNode=0):
        '''initiates and submits jobs to the cluster
        Args:
            kernels (int): how many kernels to use for 1 simulation
            onNode (int): if specified, tells on which node to run
        '''
        jobs = {}
        for i in range(self.firstSim, self.firstSim + self.numOfExperiments):
            s = libSimulate.Simulation(
                self.modelNum,
                self.termCond,
                rewrite=False,
                specialPath=None,
                numOfRuns=self.numOfRuns,
                traj=self.traj, log_level='INFO')
            jobs[i] = []
            paramFile = os.path.join(
                routes.routePDM,
                'models',
                str("%03d" % self.modelNum),
                self.experiment,
                'parameters' + str(i) + '.ini'
            )
            populFile = os.path.join(
                routes.routePDM,
                'models',
                str("%03d" % self.modelNum),
                self.experiment,
                'populations.txt')
            perKernel = int(math.ceil(s.numOfRuns / kernels))
            # lastKernel = s.numOfRuns - perKernel*(kernels-1)
            for ker in range(kernels - 1):
                time.sleep(1)
                trajFirst = ker * perKernel
                trajLast = int((ker + 1) * perKernel - 1)
                s.log.info('kernel' + str(ker))
                s.addToQueue(
                    s.outputDir, ker, trajFirst, trajLast, jobs[i], onNode,
                    paramFile, populFile)
                print(str(i) + ' has been submitted')
            if kernels == 1:
                ker = -1
                trajLast = -1
            s.log.info('last kernel')
            s.addToQueue(
                s.outputDir, ker + 1, trajLast + 1, self.numOfRuns - 1, jobs[i],
                onNode, paramFile, populFile
            )
        print(jobs)
        return jobs

    def _getTrialParameters(self,trialNum):#TEST
        # paramFile = os.path.join(
        #     routes.routePDM,
        #     'models',
        #     str("%03d" % expt.modelNum),
        #     expt.experiment,
        #     'parameters' + str(trialNum) + '.ini'
        # )
        outputDir = os.path.join(routes.routePDM, 'models',
                                 str("%03d" % self.modelNum),
                                 str("%03d" % self.modelNum) + '_output' + str(trialNum)
                                 )
        params = {}
        params['simNum'] = trialNum
        f = open(os.path.join(outputDir, 'traj0'), 'r')
        for line in f:
            if line[0] == '#':
                raw = (line[2:].rstrip('\n')).split(' ')
                if raw[0] == 'Model:':
                    continue
                elif raw[0] == 'Parameters:':
                    for item in raw[1:]:
                        pair = item.split('=')
                        params[pair[0]] = float(pair[1])
                elif raw[0] == 'Command:':
                    continue

            else:
                break
        f.close()
        return params

    def getExptParameters(self,dataBasePickle):#TEST
        """

        Args:
            dataBasePickle: path to data base pickle where it is or where it should be

        Returns:

        """
        try:
            dataBase = pickle.load(open(dataBasePickle,'rb'))
        except FileNotFoundError:
            dataBase = pn.DataFrame({},index=[])
            currIndx = -1
        else:
            currIndx = dataBase.index[-1]
            print('data base pickle loaded')

        for trialNum in range(self.firstSim, self.firstSim+self.numOfExperiments):
            trialDict = pn.DataFrame(self._getTrialParameters(trialNum), index=[currIndx+1])
            dataBase = pn.concat([dataBase,trialDict], axis=0)
            currIndx+=1

        pickle.dump(dataBase,open(dataBasePickle,'wb'))
        return dataBase

    def reorganize(self, jobs):#Not used
        '''for all the jobs when they are done permorms simulation.reorganize():
        writes means, stds and supplementary files
        '''

        def checkJobsOnClust():
            '''checks which jobs are still running
            Returns:
                [int]: job numbers
            '''
            p = subprocess.Popen('qstat',
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            out, err = p.communicate()

            lines = (out.decode().split('\n'))[2:]
            jobsOnClust = []
            for line in lines:
                items = line.split(' ')
                try:
                    jobsOnClust.append(int(items[1]))
                except:
                    continue
            return jobsOnClust

        def ifJobsDone(jobsOnClust, jobNum):
            '''
            Returns:
                True if all the jobs done returns, False otherwise 
            '''
            jobsDoneList = []
            for job in jobs[jobNum]:
                if job in jobsOnClust:
                    return False
                else:
                    jobsDoneList.append(job)
            if set(jobs[jobNum]) == set(jobsDoneList):
                return True

        allJobsDone = False
        jobVector = list(jobs.keys())
        doneVector = []
        while not allJobsDone:
            for i in range(self.firstSim, self.firstSim + self.numOfExperiments):
                time.sleep(10)
                jobsOnClust = checkJobsOnClust()
                jobIsDone = ifJobsDone(jobsOnClust, i)
                if jobIsDone and (not i in doneVector):
                    print('job ' + str(i) + ' is done, calculating means')
                    doneVector.append(i)
                    r = result.Result(
                        self.modelNum, i, True, self.numOfRuns, traj=True
                    )
                    print('means are calculated. continue')
            if set(doneVector) == set(jobVector):
                allJobsDone = True
                print('done')

    def _readSimParam(self):
        '''reads simParams.txt
        in order to restore Experiment instance
        '''
        # print(self.experiment)
        with open(os.path.join(self.experiment, 'simParams.txt'), 'r') as content_file:
            content = content_file.read()
        contList = [item.split(' = ') for item in content.split('\n')]
        for item in contList:
            if item[0] == 'termCond':
                data = item[1].split(' ')
                self.termCond = (data[0], float(data[1]), float(data[2]))
            elif item[0] == 'traj':
                self.traj = (item[1] == 'True')
            elif item[0] == 'numOfRuns':
                self.numOfRuns = int(item[1])
            else:
                continue

        return None

    def _restoreSimNums(self):
        '''
        reads content of the experiment containing folder and from the 
        parameters<num>.ini determines the output files of all the simulation 
        of the experiment
        
        Returns:
            list[int]: list of the numbers of the simulation which were run
            for the experiment
        '''
        path = self.experiment + '/'  # WARNING local path
        simNums = []
        for file in os.listdir(path):
            if file.startswith("parameters"):
                simNums.append(int((file[10:])[:-4]))
        return simNums

    def simulationDataBase(self):
        db = {}
        simNums = self._restoreSimNums()
        for num in simNums:
            with open(
                    os.path.join(self.experiment, 'parameters' + str(num) + '.ini'),
                    'r'
            ) as content_file:
                parameters = (content_file.read()).split('\n')[1:]
            try:
                if parameters[-1] == '':
                    parameters.pop(-1)
            except IndexError:
                print('for the simulation ' + str(num) + ' parameter file is empty' +
                      ' not adding it to the database:\n' +
                      ' parameters = ' + str(parameters))
            else:
                db[num] = parameters
        db = DataBase(db, self.experiment)
        return db

    def restore(self):  # TODO
        '''given the name of experiment and corresponding _output directories
        restores Experiment instance
        '''
        self._readSimParam()
        simNums = self._restoreSimNums()
        # db = self.simulationDataBase()
        finished = self._ifFinished()
        plots = self._ifPlots()
        return None


class DataBase(object):
    '''stores parameters of simulations in the experiment
    '''

    def __init__(self, dbDict, experiment):
        '''class DataBase
        Args:
            dbDict dict[int]=list[str]:
                dictkey is a number of simulation,
                dictvalue is the list of strings 'param_name = param_value'
        Attributes:
            db = argument dbDict
        '''
        self.db = dbDict
        self.experiment = experiment

    def getSimNums(self, silent=False):
        string = ''
        for key in self.db.keys():
            string += str(key) + ' '
        if not silent:
            print(string)
        return set(list(self.db.keys()))

    def getParamNames(self):
        paramList = next(iter(self.db.values()))
        paramNames = paramList.copy()
        for i in range(len(paramList)):
            string = paramNames[i]
            paramNames[i] = string[:(string.index('=') - 1)]
            print(paramNames[i])
        return paramNames

    def getParamValues(self, paramName):
        string = paramName + ': '
        values = set([])
        for (simNums, params) in self.db.items():
            for param in params:
                if paramName in param:
                    values.add(param[(param.index('=') + 2):])
        print(string)
        print(values)

    def getVariables(self):
        with open(
                os.path.join(self.experiment, 'variable.ini'),
                'r'
        ) as content_file:
            print('\n')
            print('Parameters which are variable')
            print(content_file.read())

    def getWithParameter(self, paramName, paramValue, silent=False):
        result = set([])
        for (simNum, paramList) in self.db.items():
            for param in paramList:
                if paramName in param:
                    if str(paramValue) in param:
                        result.add(simNum)
        if not silent:
            print('Simulations with ' + paramName + ' = ' + str(paramValue) + ':')
            print(result)
        return result

    def getSimsWithSeveralParams(self, listOfTuples):
        results = self.getSimNums(silent=True)
        print('\n')
        print('Simulations with')
        for tup in listOfTuples:
            result = self.getWithParameter(tup[0], tup[1], silent=True)
            results = results.intersection(result)
            print(tup[0] + ' = ' + str(tup[1]))

        print(results)
        return results

    def getParamsOfSeletcted(self, simList):
        common = set(next(iter(self.db.values())))
        for simNum in simList:
            common = common.intersection(set(self.db[simNum]))
        separate = {}
        for simNum in simList:
            separate[simNum] = set(self.db[simNum]).difference(common)
        print('Common parameters')
        print(common)
        print('Specific parametres')
        print(separate)

        return common, separate
