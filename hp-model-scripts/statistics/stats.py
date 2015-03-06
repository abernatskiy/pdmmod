#/usr/bin/python
import matplotlib.pyplot as plt

def makeLenDict():
    '''takes a file with native hp-sequences, which has the following format:
     hpstring nativeEnergy catPattern 
    and makes a dictionary {length: [(hpstring, nativeEnergy,catPattern,autocat)]}
    {int:[(string,int,string,bool)]}
    '''
    theDict={}
    for i in range(1,26):
        theDict[i]=[]
    myfile = open('nativeList25.txt','rt')
    for line in myfile:
        try:
            raw = (line.rstrip('\n')).split(' ')
            int(raw[1])
        except:
            print(line)
        else:
            if raw[2]=='N':
                cat = 0
            else:
                cat = len(raw[2])
            auto = bool(cat and (raw[0].find('HHH')+1))
            theDict[len(raw[0])].append((raw[0],int(raw[1]),cat,auto))
            
    
    return theDict

def plotCommulStats(theDict):
    commulDict = {}
    for i in range(1,26):
        commulDict[i]=[0,0,0]#fold, cats autocats
    for i in range(2,26):
        numFolds = len(theDict[i])
        commulDict[i][0]=numFolds+commulDict[i-1][0]
        numCats = sum([bool(item[2]) for item in theDict[i]])
        commulDict[i][1]=numCats+commulDict[i-1][1]
        numAuto = sum([int(item[3]) for item in theDict[i]])
        commulDict[i][2]=numAuto+commulDict[i-1][2]
        
    fig, (ax0, ax1) = plt.subplots(nrows=2,sharex=False)
    ax0.plot(list(commulDict.keys()),[commulDict[i][0] for i in range(1,26)])
    ax0.plot(list(commulDict.keys()),[commulDict[i][1] for i in range(1,26)])
    ax0.plot(list(commulDict.keys()),[commulDict[i][2] for i in range(1,26)])
    ax0.set_yscale('log')
    plt.show()
    
    return commulDict

theDict= makeLenDict()
commulDict=plotCommulStats(theDict)
    