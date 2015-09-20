 #!/usr/bin/python

import sys
import os
from routes import *
import nativeChain

def HPlengthReader(length):
    chainDict ={}
    try:
        print('length',length)
        inFile = open(routeHP+'HP_designing/HPn'+str("%02d" % length)+'.txt', 'rt')
        
    except:
        print('there are no foldable sequences among '+str(length)+'-mers.')
    else:
    #for every line in the file
        for line in inFile:
            #if line starts with the letter U
            if line[0]=='U':
                #then this is the vector string
                #we create a dictionary entry with this vector being a key and entry an empty list
                chainDict[line.rstrip('\n')]=[]
                currentConf=line.rstrip('\n')
            #if no, this is the sequence which has current conformation in the native state
            else:
                #in this case we add a list to an entry. 
                #the first element of the list is hpstring, the second native energy
                chainDict[currentConf].append(line.rstrip('\n').split(' ')[2:])
                
    return chainDict

def HPlibraryReader(maxLength):
    """
    From the data files generates the dictionary, which later is used to gererate
    a list of NativeChain objects
    The files look the following way
    URULLD
        PHPPHPH 2
        HHPPHPH 2
    URRDLD
        HPHPPHP 2
    lines starting with U represent the conformation of the sequence and called 'vector'
    """
    chainDict={}
    print(routeHP)
    for i in range(4,maxLength+1):
        #print(routeHP+'HP_designing/HPn'+str("%02d" % i)+'.txt')
        chainDict.update(HPlengthReader(length))
                    
    return chainDict

def HPlibrary2sequencesList(maxLength,subClasses=None,catClasses=None):
    """
    
    dictionary looks like 'URDDL...': [
                                    [HPHPH...., '<native energy>']
                                    .........
                                    ]
    dictEntry is the Value
    
    This function generates a list of sequences (type NativeChain) capable to fold into one native structure
    """
    
    
    #make temporary dictionary from which hpstrings and conformations can be extracted
    seqDict=HPlibraryReader(maxLength)
    #print(seqDict)
    
    #this will be a list of all the sequences in the library
    nativeList=[]
    count=0
    #for every key (which is vector 'URDDL...' describing the conformation)
    for key in seqDict:
        '''assign a name to an entry, which is a list of lists of the following type [HPHPH...., '<native energy>']
        several sequences can have the same conformation.'''
        dictEntry=seqDict[key]
        #then we take each list representing one sequence
        for i in range(len(dictEntry)):
            count+=1
            '''assign a temporary name to it'''
            sequence=nativeChain.NativeChain(dictEntry[i][0],key,dictEntry[i][1])
            sequence.generatedNumber=count
            nativeList.append(sequence)
            
            
    return nativeList
 

def print2File(nativeList,filename):
    hpFile = open(filename, mode='w')
    hpFile.write('hpstring nativeEnergy catPattern \n')
    for sp in nativeList:
        hpFile.write(sp.hpstring+' '+str(sp.nativeEnergy)+' '+sp.catPattern+'\n')
    
    return None

#nativeList=HPlibrary2sequencesList(12)
#print2File(nativeList,routePDM+'nativeList12.txt')

 
 
 
 
 
 
 
