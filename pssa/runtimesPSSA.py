#!/usr/bin/python
import subprocess
import sys
from os import system as system
import numpy as np
from math import sqrt as sqrt
from numpy import array
from numpy import polyfit
from numpy import poly1d
from numpy import linspace

sys.path.append('../')
import routes
from balls import *

'''DATA
* numSpec -- int.
  interp. number of species types
* population -- int. 
  interp. the number of molecules of each monomer
* command -- string. 
  interp. simulation run command with parameters, like ./pdmmdo 10 1 x
* runs -- int.
  interp. the number of times simulation is being run
* currPops -- List [int.]
  interp. list of the populations with which simulations are being run
* species -- list [int.]  
  interp. list of number of species with which simulations are being run
'''


def getSimTime(command,numOfRuns):
    '''
    runs the simulation and then retrieves its running time
    '''
    retValue=subprocess.call(command)
    timeFile = open("out/PDM/"+str(numOfRuns)+"/PSSA_probability_timing.txt")
    times = []
    for i in range(numOfRuns):
        raw = (timeFile.readline().rstrip('\n')).split(' ')
        data = []
        for item in raw:
            if not item=='':
                data.append(float(item))
        times.append(data[0]/data[1])
    time = np.mean(times)
    std = np.std(times)
    return time, std

def runSeveralBallsVarNSpec(command,runs,population,collRate,species):#TEST
    '''runs several simulations with different number of species but fixed population of every specie
    '''
    system('rm runTemp.txt && touch runTemp.txt' )
    for numSpec in species:
        system('rm -r out/PDM')
        filewriter('b.sbml','balls',numSpec,population,collRate)
        pair=getSimTime(command,runs)
        with open("runTemp.txt", "a") as myfile:
            myfile.write(str(numSpec)+' '+str(pair[0])+' '+str(pair[1])+'\n')

    
    return None


runs = 5
population = 50
collRate = 0.5
command = '../libpssa-1.0.0RC/pssa_cli/pssa'

species = [2600,2700,2800,2900,3000,3100,3200,
         3300,3400,3500,3600,3700,3800,3900,4000,4100,4200,4300,4400,
         4600,4800,5000,5200,5400,5600,5800,6000,6250,6500,6750,7000] 

runSeveralBallsVarNSpec(command,runs,population,collRate,species)


