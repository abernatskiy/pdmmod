import routes
import sys
import subprocess
import os
import itertools
sys.path.append('../../')#BUG potentially
import libSimulate


class Experiment(object):
    '''class Experiment
    during one experiment values of parameters change
    a vector of changes is giving.
    According to it simulations are run.
    Files MUST be located in the directory with the name of experimentName
     * self.experiment -- string
     * self.modelNum -- int
     * self.now -- bool (is experiment new or we are restoring data)
     * self.termCond -- (str,float,float) -- termination condition
     * self.numOfRuns -- int
     * self.traj -- bool
     * self.
    '''
    def __init__(self,experimentName,modelNum,new):
        self.experiment = experimentName
        self.modelNum = modelNum
        self.new = new
        if not new:
            self.restore()#TODO
            
    
    def __str__(self):
        return self.experiment+' for the model #'+str(self.modelNum)
    
    def initNew(self,termCond,numOfRuns,traj):#TODO
        self.termCond = termCond
        self.numOfRuns = numOfRuns
        self.traj = traj
        self.makeParams()
        
        
    def readParameters(self):
        types = {'float':float, 'int':int, 'bool':bool, 'str':str}
        try:
            p = subprocess.check_call(
                ['mkdir',self.experiment],stderr=subprocess.PIPE
                )
        except:
            pass
        else:
            raise FileNotFoundError(
                "There is no directory \""+self.experiment+"\".\n "+
                "You must have this directory. We created it for you.\n "+ 
                "Put there files constant.ini and variable.ini.\n constant.ini has the formant of parameters.ini and has all the parameters which are kept constant during the experiment.\n variable.ini has variable parameters it's format is the following:\n parameter1_type parameter1_name\n val1 val2 val3 ...\n parameter2_type parameter2_name\n val1 val2 val3 ...\n types are python types: float, int, bool(0,1), str")
        
        #read constants
        with open(os.path.join(self.experiment,'constant.ini'), 'r') as content_file:
            constant = content_file.read()
        
        #read variables
        self.numOfExperiments = 1
        variables = [] #list of lists of values of variables
        with open(os.path.join(self.experiment,'variable.ini'), 'r') as content_file:
            variableSep = (content_file.read()).split('\n')
            if len(variableSep)%2==0:
                for i in range(int(len(variableSep)/2)):
                    #varValues are lists of strings of format varName = value
                    line1 = variableSep[2*i].split(' ')
                    line2 = variableSep[2*i+1].split(' ')
                    varValues=[line1[1]+' = '+ val for val in line2]
                    self.numOfExperiments=self.numOfExperiments*len(varValues)
                    variables.append(varValues)
            else:
                raise ValueError('Wrong number of lines in \"variable.ini\" file')
        variables = list(itertools.product(*variables))
        
        return constant, variables

    def getSimNums(self):
        path='./'#BUG potentially: FIX
        dirs=(next(os.walk(path))[1])
        nums = []
        for directory in dirs:
            if '_output' in directory:
                tmp = directory.replace(str("%03d" %self.modelNum)+'_output','')
                if tmp == '':
                    nums.append(0)
                else:
                    nums.append(int(tmp))
        if nums ==[]:
            currentRun = 0
        else:
            currentRun = max(nums)+1
        print('first run #: '+str(currentRun))
        return currentRun
    
    def makeParams(self):
        constant, variables = self.readParameters()
        print(variables)
        firstSim = self.getSimNums()
        self.firstSim = firstSim
        for i in range(firstSim,firstSim+self.numOfExperiments):
            pFile=open(
                os.path.join(routes.routePDM,'models',str("%03d" %self.modelNum),self.experiment,'parameters'+str(i)+'.ini'),
                'a'
                )
            pFile.write(constant)
            for line in variables[i-firstSim]:
                pFile.write(line+'\n')
        pFile.close()
            
    
    def printExperiment(self):#TODO
        return None
    
    def reorderSims(self):#TODO
        return None
    
    def initAndRun(self,numOfKernels,onNode=0):
        for i in range(self.firstSim,self.firstSim+self.numOfExperiments):
            s = libSimulate.Simulation(
                self.modelNum,
                self.termCond,
                rewrite=False,
                specialPath=None,
                numOfRuns=self.numOfRuns,
                traj=self.traj,log_level='INFO')
            s.runSeveralParallelCluster(
                numOfKernels, 
                onNode,
                paramFile=os.path.join(self.experiment,'paraeters'+str(i)+'.ini'),
                populFile=os.path.join(self.experiment,'populations.txt'))
            #s.reorganizeOutput()#BUG
        return None
    
    def restore(self):#TODO
        return None



if __name__ == "__main__":
    expt = Experiment('test',16,new=False)
    expt.initNew(('simulateTime',10,0.5),1,True)
    expt.initAndRun(1)

