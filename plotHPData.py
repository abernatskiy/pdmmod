#/usr/bin/python

#format of the file is the following:
# time,specName specPopulation,specName specPopulation .....

#specPop -- {name: [populations during time steps]}

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

def readNativeList():
    ''' None -> {string: (int, string)}
    converts nativeList.txt to a dictionary from hp-string to a tuple of their native energies and catalytic patterns
    '''
    dataFile = open('nativeList.txt', "rt")
    count = 0
    natData ={}
    for line in dataFile:
        if not count == 0:
            raw = (line.rstrip('\n')).split(' ')
            natData[raw[0]]=(int(raw[1]),raw[2])
        count +=1
    
    return natData
    

def printStats(times,specPop,natData,plot=True):
    '''specPop -- {name: [populations during time steps]}'''
    print("total number of species is "+str(len(specPop.keys())))
    lengths=[]
    countAll = [(0)]*(len(times)) 
    countFold = [(0)]*(len(times)) 
    countCat = [(0)]*(len(times)) 
    countAuto = [(0)]*(len(times)) 
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
        
        #total=[total[i]+specPop[key][i] for i in range(len(total))]
        for i in range(len(times)):
            countAll[i]+=specPop[key][i]
            if not key.find('f')==-1:
                #print(key)
                countFold[i]+=specPop[key][i]
                if not natData[key[1:]][1]=='N':
                    countCat[i]+=specPop[key][i]
                    if not key.find('HHH')==-1:
                        countAuto[i]+=specPop[key][i]
        
        
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
    #lengthsD=[ps/hi for (ps,hi) in zip(popStats.copy().values(),hist)]
    
    for i in range(1,mL+1):
        hist.append(lengths.count(i))
        histNorm.append(hist[i-1]/2**i)
    if plot:
        lengthsD=[ps/2**li for (ps,li) in zip(list(popStats.copy().values()),list(popStats.copy().keys()))]
        fig, (ax0, ax1, ax2) = plt.subplots(nrows=3)
        #ax1.plot(range(1,mL+1),histNorm,'o')
        ax0.plot(times,countAll)
        ax1.plot(times,countFold,label='folded')
        ax1.plot(times,countCat,label='catalysts')
        ax1.plot(times,countAuto,label='autocats')
        ax2.plot(list(popStats.copy().keys()),lengthsD,label=str(mL)+'/'+str(len(specPop.keys())))
        ax2.legend()
        ax1.legend()
        ax2.grid(True)
        ax2.set_yscale('log')
        ax0.set_title("Total count of molecules at each moment")
        ax1.set_title("count of molecules of various types at each moment")
        ax2.set_title("Length distribution in the last moment")
        fig.suptitle("hp-simple with folding, no unfolding")
        #plt.savefig("stats.pdf")
        plt.show()
    
    return hist



natData=readNativeList()
times, specPop = readData("x")
printStats(times,specPop,natData)
#plotData(times, specPop)