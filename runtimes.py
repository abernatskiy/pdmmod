#!/usr/bin/python
import subprocess
from os import system as system
from statistics import mean
from statistics import stdev
from math import sqrt as sqrt
import matplotlib.pyplot as plt
import scipy.optimize as optimization
from numpy import array

def changeInitPop(number):
    '''number -- int. the number of molecules of each monomer
    '''
    popFile = open("populations.txt", mode='w', encoding='utf-8')
    popFile.write("0 "+str(number)+"\n")
    popFile.write("1 "+str(number)+"\n")
    popFile.close()
    
    return None

def getSimTime(command):
    '''command -- string. simulation run command with parameters
    '''
    subprocess.call(command)
    
    timeFile = open("runtime.txt")
    time = float(timeFile.readline().rstrip('\n'))
    
    return time

def getTimeStat(command,number,runs):
    changeInitPop(number)
    times=[]
    for i in range(runs):
        times.append(getSimTime(command))
    
    ave = mean(times)
    stdDev = stdev(times)
    print(ave, stdDev)
    return ave, stdDev

def analyzeRuntime(command,runs,minpop,multiplier,numPoints,plot=True):
    def func(x, a, b):
        return a + b*x
    
    runtimes=[]
    number=minpop
    for i in range(numPoints):
        pair=getTimeStat(command,number,runs)
        runtimes.append((number*2,pair[0],pair[1]))
        number=number*multiplier
    
    a, b = optimization.curve_fit(func, [r[0] for r in runtimes], [r[1] for r in runtimes],[0.0,0.0],[r[2] for r in runtimes])[0]
    
    ratios=[]
    for i in range(1,len(runtimes)):
        m=runtimes[i][1]/runtimes[i-1][1]
        e=m*sqrt((runtimes[i][2]/runtimes[i][1])**2+(runtimes[i-1][2]/runtimes[i-1][1])**2)
        ratios.append((runtimes[i][0],m,e))
    
    
    
    fig, (ax0, ax1) = plt.subplots(nrows=2,sharex=True)
    for i in range(len(runtimes)):
        element=runtimes[i]
        ax0.errorbar(element[0],element[1],yerr=element[2],  fmt='-o')
        
        if not element[0]==minpop*2:
            rat=ratios[i-1]
            ax1.errorbar(rat[0],rat[1],yerr=rat[2],fmt='-o')
            #ax1.set_yscale('log')
            #ax1.set_xscale('log')
    ys=[func(r[0],a,b) for r in runtimes]
    ax0.plot([r[0] for r in runtimes],ys,'r',label='%.2e'%b+'x'+'%.2e'%a)
    ax0.legend()
    ax0.set_title('Simulation run time vs number of species in the simulation')
    ax1.set_title('Ratio of runtimes as number of species doubles')
    plt.show()
    return runtimes

number=50
command = './pdmmod', '20', '1', 'x'
runs = 3
minpop=number
multiplier=2
numPoints=5

rD=analyzeRuntime(command,runs,minpop,multiplier,numPoints)

