#/usr/bin/python

#format of the file is the following:
# time,specName specPopulation,specName specPopulation .....

import matplotlib.pyplot as plt


def readData(filename):
    '''times at which we are recording'''
    times = []
    specPop = {}
    dataFile = open(filename, "rt")
    #counting time instances
    count = 0
    for line in dataFile:
        if not line=='\n':
            if line[0]=="#":
                continue
            else:
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

def printStats(times,specPop,plot=True):
    print("total number of species is "+str(len(specPop.keys())))
    lengths=[]
    #dictionary where populations of all n-mers in the last moment is counted
    popStats={}
    lengthDistr={}
    total=[0]*(len(times))
    for key in specPop.keys():
        if key.find('f')==-1:
            polLen=len(key)
            lengths.append(len(key))
        else:
            lengths.append(len(key)-1)
            polLen=len(key)-1
        total=[total[i]+specPop[key][i] for i in range(len(total))]
        if not polLen in popStats.keys():
            #add dict entry and population of the first n-mer of the given length
            popStats[polLen]=specPop[key][-1]
        else:
            #add to the population of n-mers a population of another n-mer
            popStats[polLen]+=specPop[key][-1]
    mL=max(lengths)
    print("maximum length of a polymer is "+str(mL))
    hist=[]
    histNorm=[]
    lengthsD=[ps/hi for (ps,hi) in zip(popStats.copy().values(),hist)]
    
    for i in range(1,mL+1):
        hist.append(lengths.count(i))
        histNorm.append(hist[i-1]/2**i)
    if plot:
        lengthsD=[ps/hi for (ps,hi) in zip(list(popStats.copy().values()),hist)]
        fig, (ax0, ax1, ax2) = plt.subplots(nrows=3)
        ax1.plot(range(1,mL+1),histNorm,'o')
        ax0.plot(times,total)
        ax2.plot(list(popStats.copy().keys()),lengthsD,label=str(mL)+'/'+str(len(specPop.keys())))
        ax2.legend()
        ax1.grid(True)
        ax0.set_title("Types of n-mers and populations in the last moment")
        ax1.set_title("Total count of molecules at each moment")
        ax2.set_title("Length distribution in the last moment")
        fig.suptitle("hp-simple with folding, no unfolding")
        #plt.savefig("stats.pdf")
        plt.show()
    
    return hist

    

def plotData(times,specPop):
    def f(key):
        if key.find('f')==-1:
            return None
        else:
            return str(key)
    fig=plt.figure(figsize=(8,6))
    for key in specPop.keys():
        plt.plot(times,specPop[key],label=f(key))
    #plt.legend(fontsize='small') 
    
    plt.title("Populations of species")
    plt.xlim(0,times[-1])
    plt.show()


times, specPop = readData("x")
printStats(times,specPop)
plotData(times, specPop)