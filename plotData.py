#/usr/bin/python

#format of the file is the following:
# time,specName specPopulation,specName specPopulation .....

import matplotlib.pyplot as plt


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

def printStats(times,specPop):
    print("total number of species is "+str(len(specPop.keys())))
    lengths=[]
    for key in specPop.keys():
        lengths.append(len(key))
    print("maximum length of a polymer is "+str(max(lengths)))
    
    return None

def plotData(times,specPop):
    fig=plt.figure(figsize=(8,6))
    for key in specPop.keys():
        plt.plot(times,specPop[key],label=key)
    #plt.legend(fontsize='small') 
    
    plt.title("Populations of species")
    plt.xlim(0,times[-1])
    plt.savefig('y.pdf')


times, specPop = readData("x")
printStats(times,specPop)
#plotData(times, specPop)