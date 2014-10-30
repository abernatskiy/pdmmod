#/usr/bin/python

import matplotlib.pyplot as plt


def readData(filename):
    times = []
    specPop = {}
    dataFile = open(filename, "rt")
    count = 0
    for line in dataFile:
        if not line=='\n':
            count+=1
            raw = (line.rstrip('\n')).split(',')
            times.append(float(raw[0]))
            for item in raw[1:len(raw)-1]:
                point=item.split(' ')
                if point[0] not in specPop:
                    specPop[point[0]]=[int(point[1])]
                else:
                    specPop[point[0]].append(int(point[1]))
            for val in specPop.values():
                if len(val)==count:
                    continue
                elif len(val)==count-1:
                    val.append(0)
                else:
                    raise ValueError("!")
            
    
    return times,specPop

def plotData(times,specPop):
    fig=plt.figure(figsize=(8,6))
    for key in specPop.keys():
        plt.plot(times,specPop[key],label=key)
    plt.legend(fontsize='small') 
    plt.savefig('x.pdf')


times, specPop = readData("x")
plotData(times, specPop)