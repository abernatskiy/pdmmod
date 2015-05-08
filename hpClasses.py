#!/usr/bin/python
#import logging

import routes
#from log_utils import init_log

#log = init_log(log_level='WARNING',logger='analysis')
catPattern = 'HHH'
    
def readNativeList(maxLength):
    ''' string, int -> {string: (int, string)}
    converts nativeList<maxLength>.txt to a dictionary from hp-string 
    to a tuple of their native energies and catalytic patterns
    '''
    try:
        dataFile = open(routes.routePDM+'nativeList'+str(maxLength)+'.txt', "rt")
    except:
        dataFile = open(routes.routePDM+'nativeList.txt', "rt")
    count = 0
    natData ={}
    for line in dataFile:
        if not count == 0:
            raw = (line.rstrip('\n')).split(' ')
            natData[raw[0]]=(int(raw[1]),raw[2])
        count +=1
    
    return natData

def getHPClassOfSeq(seq,natData):
    '''determins if a sequence is a foldamer, catalyst or an autocat
    '''
    # if it has 'f' it's folded. we count only them as cats etc
    # because folded sequences have higher populations than their
    # unfolded counterparts
    fold, cat, autocat = False, False, False
    if not seq.find('f')==-1:
        fold = True
        try:
            if not natData[seq[1:]][1]=='N':
                cat = True
                if not seq.find('HHH')==-1:
                    autocat = True
        except KeyError:
            fold, cat, autocat = False, False, False
            print('the sequence '+str(seq)+
                ' wasn\'t in the native List. '+
                'Something went wrong. all classes are False.')
            
    return fold, cat, autocat

def getUserFriendData(seq,natData):
    (let1, let2, let3) = ('','','')
    fold, cat, autocat = getHPClassOfSeq(seq,natData)
    if not seq.find('f')==-1:
        seqLen=len(seq)-1
    else:
        seqLen=len(seq)
    if fold:
        let1='F'
    if cat:
        let2='C'
    if autocat:
        let3='A'
    return 'len '+str(seqLen)+' '+let1+let2+let3
    

#TESTING
if __name__ == "__main__":
    maxLength = 25
    natData = readNativeList(25)
    fold, cat, autocat = getHPClassOfSeq('fHPPPHHPPHHHHPHHPPHHPHHH',natData)
    
    
    



    