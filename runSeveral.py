#!/usr/bin/python
import subprocess
from os import system as system



def runSeveral(name,runs,time,steps):
    #create a folder with relusts
    system('mkdir'+str(name))
    for i in range(runs):
        subprocess.call('./pdmmod '+str(time)+' '+str(steps)+' '+name+str(i)+'.dat')
    
    return None

def getStats(name, runs):
    for i in range(runs):
        dataFile = open(filename, "rt")

def readData(filename):
    #times at which we are recording
    times = []
    specPop = {}
    dataFile = open(filename, "rt")
    #counting time instances
    count = 0
    for line in dataFile:
        if not line=='\n':
            count+=1
            #get a line of raw information splitted by ","
            raw = (line.rstrip('\n')).split(',')
            times.append(float(raw[0]))
            for item in raw[1:len(raw)-1]:
                #get a couple specie -- its population
                point=item.split(' ')
                #if the name of the specie hasn't appear yet
                if point[0] not in specPop:
                    #add it and its population
                    #also add 0s as prev times populations
                    if not count==1:
                        specPop[point[0]]=[0]*(count-1)
                        specPop[point[0]].append(int(point[1]))
                    else:
                        specPop[point[0]]=[int(point[1])]
                else:
                    #otherwise append new point to the existing list of points
                    specPop[point[0]].append(int(point[1]))
            #now let's check if every particle has a record at this time
            for spec in specPop.keys():
                if len(specPop[spec])==count:
                    continue
                elif len(specPop[spec])==count-1:
                    specPop[spec].append(0)
                else:
                    print(spec)
                    print('length',len(specPop[spec]))
                    print('count',count)
                    raise ValueError("!")
    
    return times,specPop



