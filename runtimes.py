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

def changeInitPop(numSpec,number):
    '''numSpec -- number of species types
    number -- int. the number of molecules of each monomer
    '''
    popFile = open("populations.txt", mode='w', encoding='utf-8')
    for i in range(numSpec):
        popFile.write(str(i)+" "+str(number)+"\n")
    popFile.close()
    
    return None
    

def getSimTime(command):
    '''command -- string. simulation run command with parameters
    '''
    retValue=subprocess.call(command)
    
    timeFile = open("runtime.txt")
    time = float(timeFile.readline().rstrip('\n'))
    
    return time, retValue

def getTimeStat(command,numSpec,number,runs):
    changeInitPop(numSpec,number)
    times=[]
    for i in range(runs):
        time, retValue = getSimTime(command)
        while retValue == 2:
            print('rerun')
            time, retValue = getSimTime(command)
            
        times.append(time)
    
    ave = mean(times)
    stdDev = stdev(times)
    print(ave, stdDev)
    return ave, stdDev

def runSeveral(command,runs,minNum,number,steps):
    system('rm runTemp.txt && touch runTemp.txt' )
    numPoints=len(steps)
    numSpec=minNum
    for i in range(numPoints):
        pair=getTimeStat(command,numSpec,number,runs)
        with open("runTemp.txt", "a") as myfile:
            myfile.write(str(number*numSpec)+' '+str(pair[0])+' '+str(pair[1])+'\n')
        numSpec=numSpec+steps[i]

    
    return None

def analyzeRuntime(command,runs,minpop,numPoints):
    
    runtimes=[]
    myfile = open('runTemp.txt','rt')
        
    #number=minpop
    for i in range(numPoints):
        pair=((myfile.readline()).rstrip('\n')).split(' ')
        runtimes.append((int(pair[0]),float(pair[1]),float(pair[2])))
        #number=number*multiplier
    
    
    
    ratios=[]
    for i in range(1,len(runtimes)):
        m=(runtimes[i][1]-runtimes[i-1][1])/(runtimes[i][0]-runtimes[i-1][0])
        e=sqrt((runtimes[i][2])**2+(runtimes[i-1][2])**2)/(runtimes[i][0]-runtimes[i-1][0])
        ratios.append((runtimes[i][0],m,e))
    
    print(ratios)
    
    return runtimes, ratios
    
def plotRuntimes(runtimes,ratios):
    '''runtimes fitting'''
    x=[r[0] for r in runtimes]
    y=[r[1] for r in runtimes]
    y_err=[r[2] for r in runtimes]
    
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
        
        if not element[0]==minpop*2:
            rat=ratios[i-1]
            ax1.errorbar(rat[0],rat[1],yerr=rat[2],fmt='-o')
            
    #ax0.set_yscale('log')
    #ax0.set_xscale('log')
    #ax1.set_xscale('log')
    ax0.legend(loc=4)
    ax1.legend(loc=4)
    ax0.set_title('Simulation run time vs number of species in the simulation')
    ax1.set_title('Current slope of the graph above')
    #plt.savefig('timeStats.pdf')
    plt.show()
    return None

minNum=5
number=10
command = './pdmmod', '1', '1', 'x'
runs = 5
minpop=number
steps=[5]*25
numPoints=len(steps)


runSeveral(command,runs,minNum,number,steps)
runtimes, ratios = analyzeRuntime(command,runs,minpop,numPoints)
plotRuntimes(runtimes,ratios)
