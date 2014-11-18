#!/usr/bin/python
import subprocess
from os import system as system
from statistics import mean
from statistics import stdev
from math import sqrt as sqrt
import matplotlib.pyplot as plt
import scipy.optimize as optimization
from numpy import array
from numpy import polyfit
from numpy import poly1d
from numpy import linspace

def changeInitPop(number):
    '''number -- int. the number of molecules of each monomer
    '''
    popFile = open("populations.txt", mode='w', encoding='utf-8')
    popFile.write("a0 "+str(number)+"\n")
    popFile.write("a1 "+str(number)+"\n")
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

def runSeveral(command,runs,minpop,multiplier,numPoints):
    system('rm runTemp.txt && touch runTemp.txt' )
    number=minpop
    for i in range(numPoints):
        pair=getTimeStat(command,number,runs)
        with open("runTemp.txt", "a") as myfile:
            myfile.write(str(number*2)+' '+str(pair[0])+' '+str(pair[1])+'\n')
        number=number*multiplier

    
    return None

def analyzeRuntime(command,runs,minpop,multiplier,numPoints):
    
    runtimes=[]
    myfile = open('runTemp.txt','rt')
        
    #number=minpop
    for i in range(numPoints):
        pair=((myfile.readline()).rstrip('\n')).split(' ')
        runtimes.append((int(pair[0]),float(pair[1]),float(pair[2])))
        #number=number*multiplier
    
    
    
    ratios=[]
    for i in range(1,len(runtimes)):
        m=runtimes[i][1]/runtimes[i-1][1]
        e=m*sqrt((runtimes[i][2]/runtimes[i][1])**2+(runtimes[i-1][2]/runtimes[i-1][1])**2)
        ratios.append((runtimes[i][0],m,e))
    
    return runtimes, ratios
    
def plotRuntimes(runtimes,ratios):
    #def func(x, a, b):
    #    return a*x + b
    #a, b = optimization.curve_fit(func, [r[0] for r in runtimes], [r[1] for r in runtimes],[0.0,0.0],[r[2] for r in runtimes])[0]
    
    x=[r[0] for r in runtimes]
    y=[r[1] for r in runtimes]
    
    z = polyfit(x, y, 1)
    f = poly1d(z)
    
    x_new = linspace(x[0], x[-1], 50)
    y_new = f(x_new)
    
    fig, (ax0, ax1) = plt.subplots(nrows=2,sharex=False)
    
    
    ax0.plot(x,y,'o', x_new, y_new)
    
    for i in range(len(runtimes)):
        element=runtimes[i]
        
        if not element[0]==minpop*2:
            rat=ratios[i-1]
            ax1.errorbar(rat[0],rat[1],yerr=rat[2],fmt='-o')
            
    #ax0.set_yscale('log')
    #ax0.set_xscale('log')
    #ax1.set_xscale('log')
    ax0.set_title('Simulation run time vs number of species in the simulation')
    ax1.set_title('Ratio of runtimes as number of species doubles')
    #plt.savefig('timeStats.pdf')
    plt.show()
    return None

number=20
command = './pdmmod', '3', '1', 'x'
runs = 3
minpop=number
multiplier=2
numPoints=10

runSeveral(command,runs,minpop,multiplier,numPoints)
runtimes, ratios = analyzeRuntime(command,runs,minpop,multiplier,numPoints)
plotRuntimes(runtimes,ratios)