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
    specTypes=[0]*len(times)
    total=[0]*(len(times))
    lengths = []
    for key in specPop.keys():
        total=[total[i]+specPop[key][i] for i in range(len(total))]
        specTypes=[specTypes[i]+int(bool(specPop[key][i])) for i in range(len(total))]
        lengths.append(len(key))
    maxLength = max(lengths)
    allSeq = 0
    for i in range(maxLength):
        allSeq+=2**(i+1)
    print('maximum length reached '+str(maxLength))
    if plot:
        fig, (ax0, ax1) = plt.subplots(nrows=2)
        ax1.plot(times,specTypes)
        ax0.plot(times,total)
        ax1.plot([0,times[-1]],[allSeq,allSeq],label ='number of seq. type with lengths up to '+str(maxLength))
        ax1.set_yscale('log')
        #ax2.plot(list(popStats.copy().keys()),lengthsD,label=str(mL)+'/'+str(len(specPop.keys())))
        ax1.legend(loc=4)
        #ax1.grid(True)
        ax0.set_title("Total count of molecules at each moment")
        ax1.set_title("Total count of species types at each moment, max. length reached "+str(maxLength))
        #ax2.set_title("Length distribution in the last moment")
        fig.suptitle("Binary polymers with hydrolysis. They grow when meet monomers\n Growth rate = fast growth = 0.1, hydrolysis = 0.001")
        #plt.savefig("stats.pdf")
        plt.show()
    
    return None

    

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
#plotData(times, specPop)