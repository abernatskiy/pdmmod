#!/usr/bin/python
import subprocess
from os import system as system
#from statistics import mean
#from statistics import stdev
import numpy as np
from math import sqrt as sqrt
#import matplotlib.pyplot as plt
#import scipy.optimize as optimization
from numpy import array
from numpy import polyfit
from numpy import poly1d
from numpy import linspace

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
* arrayOfChanges -- one of:
  - currPops
  - species
'''




def getSimTime(command):
    '''
    runs the simulation and then retrieves its running time
    '''
    print(subprocess.call('env'))
    retValue=subprocess.call(command)
    
    timeFile = open("runtime.txt")
    time = float(timeFile.readline().rstrip('\n'))
    
    return time, retValue

def getTimeStat(command,numSpec,population,collRate,runs):
    '''runs the simulation several times with fixed parameters and then returns average time of running
    '''
    filewriter(filename,numSpec,population,collRate)
    times=[]
    for i in range(runs):
        time, retValue = getSimTime(command)
        while retValue == 2:#WTF
            print('rerun')
            time, retValue = getSimTime(command)
            
        times.append(time)
    
    ave = np.mean(times)
    stdDev = np.std(times)
    print(ave, stdDev)
    return ave, stdDev


def runSeveralChangeNumSpec(command,runs,population,collRate,species):#TEST
    '''runs several simulations with different number of species but fixed population of every specie
    '''
    system('rm runTemp.txt && touch runTemp.txt' )
    for numSpec in species:
        pair=getTimeStat(command,numSpec,population,collRate,runs)#average time and standard deviation of it.
        with open("runTemp.txt", "a") as myfile:
            myfile.write(str(numSpec)+' '+str(pair[0])+' '+str(pair[1])+'\n')
        #numSpec=numSpec+steps[i]

    
    return None



def analyzeRuntime(command,runs,numOfPoints,filename):
    '''
    '''
    runtimes=[]
    myfile = open(filename,'rt')
        
    for i in range(numOfPoints):
        raw=((myfile.readline()).rstrip('\n')).split(' ')
        if not raw ==['']:
            runtimes.append((int(raw[0]),float(raw[1]),float(raw[2])))
    
    
    
    ratios=[]
    for i in range(1,len(runtimes)):
        m=(runtimes[i][1]-runtimes[i-1][1])/(runtimes[i][0]-runtimes[i-1][0])
        e=sqrt((runtimes[i][2])**2+(runtimes[i-1][2])**2)/(runtimes[i][0]-runtimes[i-1][0])
        ratios.append((runtimes[i][0],m,e))
    
    print(ratios)
    
    return runtimes, ratios
    
def plotRuntimes(runtimes,ratios,title):
    '''runtimes fitting'''
    x=[r[0] for r in runtimes]
    y=[r[1]*10**6 for r in runtimes]
    y_err=[r[2]*10**6 for r in runtimes]
    
    z = polyfit(x, y, 1)
    f = poly1d(z)
    
    z2 = polyfit(x, y, 2)
    f2 = poly1d(z2)
    
    x_new = linspace(x[0], x[-1], 50)
    y_new = f(x_new)
    y_new2= f2(x_new)
    
    '''ratios fitting'''
    xr=[r[0] for r in ratios[2:]]
    yr=[r[1] for r in ratios[2:]]
    zr=polyfit(xr, yr, 1)
    fr = poly1d(zr)
    xr_new = linspace(xr[0], xr[-1], 50)
    yr_new = fr(xr_new)
    
    fig, (ax0, ax1) = plt.subplots(nrows=2,sharex=False)
    
    
    ax0.errorbar(x,y,yerr=y_err,fmt='o')
    ax0.plot(x_new,y_new,label='y = '+'%.2e' %z[0]+' x +'+'%.2e' %z[1])
    ax0.plot(x_new,y_new2,label='y = '+'%.2e' %z2[0]+' x^2 +'+'%.2e' %z2[1]+' x '+'%.2e' %z2[2])
    ax1.plot(xr_new,yr_new,label='y = '+'%.2e' %zr[0]+' x +'+'%.2e' %zr[1])
    for i in range(len(runtimes)):
        element=runtimes[i]
    
        rat=ratios[i-1]
        ax1.errorbar(rat[0],rat[1],yerr=rat[2],fmt='-o')
        
    #ax0.set_yscale('log')
    #ax0.set_xscale('log')
    #ax1.set_xscale('log')
    ax0.legend(loc=4)
    ax1.legend(loc=4)
    ax0.set_title('Simulation run time vs number species types in the simulation')
    ax1.set_title('Current slope of the graph above')
    ax0.set_ylabel('runtime, microseconds')
    #plt.savefig('timeStats.pdf')
    fig.suptitle(title)
    plt.show()
    return None

def analyzeFile(filename):
    runtimes=[]
    myfile = open(filename,'rt')
    for line in myfile:
        raw=(line.rstrip('\n')).split(' ')
        if not raw ==['']:
            runtimes.append((int(raw[0]),float(raw[1]),float(raw[2])))
    ratios=[]
    for i in range(1,len(runtimes)):
        m=(runtimes[i][1]-runtimes[i-1][1])/(runtimes[i][0]-runtimes[i-1][0])
        e=sqrt((runtimes[i][2])**2+(runtimes[i-1][2])**2)/(runtimes[i][0]-runtimes[i-1][0])
        ratios.append((runtimes[i][0],m,e))
    
    x=[r[0] for r in runtimes]
    y=[r[1]*10**6 for r in runtimes]
    y_err=[r[2]*10**6 for r in runtimes]
    
    z = polyfit(x, y, 1)
    f = poly1d(z)
    
    z2 = polyfit(x, y, 2)
    f2 = poly1d(z2)
    
    x_new = linspace(x[0], x[-1], 50)
    y_new = f(x_new)
    y_new2= f2(x_new)
    
    '''ratios fitting'''
    xr=[r[0] for r in ratios[2:]]
    yr=[r[1] for r in ratios[2:]]
    zr=polyfit(xr, yr, 1)
    fr = poly1d(zr)
    xr_new = linspace(xr[0], xr[-1], 50)
    yr_new = fr(xr_new)
    print(ratios)    
    return (x,y,y_err),(x_new, y_new, y_new2), (xr_new, yr_new), ratios,(z,z2,zr)

def plotSeveral(filenames):#TODO
    '''filenames = [string]
    '''
    fig, (ax0, ax1) = plt.subplots(nrows=2,sharex=False)
    for filename in filenames:
        data, lines, slope, ratios, fits = analyzeFile(filename)

        ax0.errorbar(data[0],data[1],yerr=data[2],fmt='o')
        #ax0.plot(lines[0],lines[1],label='y = '+'%.2e' %fits[0][0]+' x +'+'%.2e' %fits[0][1])
        ax0.plot(lines[0],lines[2],label='y = '+'%.2e' %fits[1][0]+' x^2 +'+'%.2e' %fits[1][1]+' x '+'%.2e' %fits[1][2])
        #ax1.plot(slope[0],slope[1],label='y = '+'%.2e' %fits[2][0]+' x +'+'%.2e' %fits[2][1])
        for i in range(len(data[1])):
            element=data[1][i]
        
            rat=ratios[i-1]
            ax1.errorbar(rat[0],rat[1],yerr=rat[2],fmt='-o')
        
    
    ax0.legend(loc=4)
    ax1.legend(loc=4)
    ax0.set_title('Simulation run time vs number species types in the simulation')
    ax1.set_title('Current slope of the graph above')
    ax0.set_ylabel('runtime, microseconds')
    #plt.savefig('timeStats.pdf')
    fig.suptitle(title)
    plt.show()
    return None

###Change Number of species###
population=50
filename = 'b.xml'
command = '/cavern/eliza/origins/pdmmod/stochKit/StochKit2.0.11/custom_drivers/single_trajectory/bin/single_trajectory_debug', 'simulateReactions', '-m', filename, '-t', '2000'

runs = 3
collRate = 0.5

species=[2,3,4,5,10,12,14,16,18,20,30,40,50,60,70,80,90,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000,1100,1150,1200,1250,1300,1350,1400,1450,1500]
#,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500,2600,2700,2800,2900,3000]

numOfPoints = len(species)
title = ''

runSeveralChangeNumSpec(command,runs,population,collRate,species)
#runtimes, ratios = analyzeRuntime(command,runs,numOfPoints,'runTemp.txt')
#plotRuntimes(runtimes,ratios,title)
filenames = ['runTemp.txt','pdmmodBalls.txt']

#plotSeveral(filenames)









