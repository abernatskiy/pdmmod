#!/usr/bin/python

class Vesicle(object):
    '''class representing a vesicle containing some sequences
     * matureWeight - Int. -  weight in terms of number of monomers,
        at which vesicles divide. They split into 2 vesicles with equal weights.
     * generation - Int. - we start from mother vesicles (generation 0), 
        its daughter is generation 1, ect
     * sequences - Dict. - {sequnce name: sequnce population}#TODO SeqInClust??
     * modelNum - Int. - model, which governs chemistry in the vesicle
    '''
    #__slots__ = ['population','generation','matureWeight']
    def __init__(self,sequences, generation,matureWeight,modelNum,path):
        self.sequences=sequences
        self.generation=generation
        self.matureWeight=matureWeight
        self.modelNum = modelNum
        self.path = path
        
    def __str__(self):
        str1='Vesicle '+str(self.generation)+' of mature weight '+\
            str(self.matureWeight)+\
                ' with '+str(len(self.sequences.keys()))+' sequeneces'
        return str1
    
    def __repr__(self):
        str1='Vesicle '+str(self.generation)
        return str1

    def storeCell(self,dictOfCells):#TODO
        '''adds a cell into a dictionary, which contains all possible cells
        '''
        if self.population in dictOfCells:
            dictOfCells[self.population]+=1
        else:
            dictOfCells[self.population]=1
    
        return dictOfCells
    
    
    def storeInitPop(self):#TODO
        f=open(routes.routeCellsTmp+"%03d" % self.origTraj+'_'+str(self.generation)+'.txt',"wb")
        str1=''
        for item in self.population:
            str1+=str(item)+' '
        str1=str1.rstrip(' ')
        f.write(bytes(str1, 'UTF-8'))
        f.close()
        return routes.routeCellsTmp+"%03d" % self.origTraj+'_'+str(self.generation)+'.txt'
    
    def writePython(self,maxLength,kinetics,simParams,typeOfSim,procNumber):#TODO
        pyFile=routes.routeCells+'tmp/'+"%03d" % self.origTraj+'_'+str(self.generation)+'.py'
        pathToXml=routes.routeCells+'simulations/'+"%03d" % self.origTraj+'_'+str(self.generation)+'.xml'
        pyF=open(pyFile,'w')
        pyF.write('#! /usr/bin/python2\n')
        pyF.write('\n')
        pyF.write('import sys\n')
        pyF.write('import pickle\n')
        pyF.write('sys.path.append(\'../\')\n')
        pyF.write('sys.path.append(\'../../\')\n')
        pyF.write('import routes\n')
        pyF.write('sys.path.append'+'('+'routes.routeHP'+')\n')
        pyF.write('import '+str(typeOfSim)+'\n')
        #pyF.write('dreload('+str(typeOfSim)+')\n')
        pyF.write('from nativeChain import *\n')
        pyF.write('maxLength='+str(maxLength)+'\n')
        pyF.write('kinetics='+str(kinetics)+'\n')
        pyF.write('simParams='+str(simParams)+'\n')
        pyF.write('directOrTau=\'direct\''+'\n')
        pyF.write('procNumber='+str(procNumber)+'\n')
        pyF.write('keepTraj=False'+'\n')
        pyF.write('nativeList=pickle.load(open(\"'+routes.route+'nativeList\"+str(maxLength)+\".p\",\"rb\"))')
        pyF.write('\n')
        pyF.write('model='+str(typeOfSim)+'.Mod'+str(typeOfSim)[0].upper()+str(typeOfSim)[1:]+\
            '(maxLength,kinetics,nativeList,True)\n')
        pyF.write('sim='+str(typeOfSim)+'.Sim'+str(typeOfSim)[0].upper()+str(typeOfSim)[1:]+\
            '(model,simParams,directOrTau,procNumber)\n')
        pyF.write('ipFile=open(routes.routeCellsTmp+\''+"%03d" % self.origTraj+'_'+str(self.generation)+'.txt\',\"r\")\n')
        pyF.write('initPopList=(ipFile.readline().rstrip(\' \')).split(\' \')\n')
        pyF.write('for i in range(len(initPopList)):\n')
        pyF.write('    initPopList[i]=int(initPopList[i])\n')
        pyF.write('sim.writeFile(\"'+pathToXml+'\",initPopList)\n')
        pyF.close()
                
                
        return pyFile, pathToXml
    

    def growCell(self,termTime,timeStep):#TODO
        '''
        form Simulation with special path
        run until some known time
        find time, when the mass of the vesicle == matureWeight
        rewrite trajectory till this time as generation 0
        split randomly
        '''
        sDef = libSimulate.Simulation(
                self.modelNum,
                termCond=('simulateTime',termTime,timeStep),
                rewrite=False,
                specialPath=self.path,
                numOfRuns=1,
                traj=True,
                log_level='INFO')
        populationFile = self.makeInitPopFile()
        sDef.runSeveralSeries(paramFile=None,populFile=populationFile)
        
        return None
    
    def growAndSplit(self,termTime,timeStep,numOfGenerations,keepAll):#TEST
        '''
        '''
        vesicles = [self]
        currGeneration = 0
        while currGeneration < numOfGenerations:
            nextGen = []
            for vesicle in vesicles:
                daughter1, daughter2 = self.growCell(termTime,timeStep)
                nextGen.append(daughter1)
                if keepAll:
                    nextGen.append(daughter2)
            vesicles = nextGen
            currGeneration+=1
        
        return vesicles
    
if __name__ == "__main__":     
    sequences = {'a': 1}
    generation = 0
    matureWeight = 10
    modelNum = 12
    path = './'
    v = Vesicle(sequences, generation,matureWeight,modelNum,path)
    print(v)
    
    