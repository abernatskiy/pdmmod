import random

from sklearn import svm
import numpy as np

maxLength = 4

def convertNative(natListFile,minLength,maxLength):
    def func(letter):
        if letter == 'H':
            return 0
        elif letter == 'P':
            return 1
        else:
            print(letter)
            raise ValueError
        
    nativeList = []
    nativeBool = []
    with open (natListFile,'r') as natList:
        for line in natList:
            seq = (line.split(' '))[0]
            if len(seq)<=maxLength and len(seq)>=minLength:
                nativeList.append(seq)
    for word in nativeList[1:]:
        wList = [func(x) for x in list(word)]
        if len(wList)<maxLength:
            wList = wList+[-1]*(maxLength-len(wList))
        nativeBool.append(wList)
    return nativeBool
        


def formRandomWord(minLength,maxLength):
    length = random.randint(minLength,maxLength)
    word = list(np.random.choice([0, 1], size=(length,)))
    if length<maxLength:
        addition = [-1]*(maxLength-length)
        word = word+addition
    return word

def formRandomSet(minLength,maxLength,setSize):
    maxSetSize=sum([2**i for i in range(minLength,maxLength+1)])
    print('max size: ',maxSetSize)
    if setSize>maxSetSize:
        raise ValueError(
            'setSize is too big, it must be less or equal than '+str(maxSetSize)
            )
    theSet = []
    while len(theSet)<setSize:
        word = formRandomWord(minLength,maxLength)
        if not word in theSet:
            theSet.append(word)
    
    return theSet

def formTarget(randomList,nativeList):
    l=len(nativeList)
    random.shuffle(nativeList)
    train = nativeList[:int(l/2)]
    predict = nativeList[int(l/2):]
    for word in train:
        if not word in randomList:
            randomList.append(word)
    
    target=[0]*len(randomList)
    for i in range(len(randomList)):
        if randomList[i] in nativeList:
            target[i]=1
            
    return target, predict

def revomeFold(randomList,nativeList):
    newList = []
    for word in randomList:
        if not word in nativeList:
            newList.append(word)
    return newList

mL = 18
ml = 12
size = 10000

n = convertNative('nativeList20.txt',ml,mL)

r = formRandomSet(ml,mL,size)



t,p = formTarget(r,n)

rt = revomeFold(formRandomSet(ml,mL,size),n)

clf = svm.SVC(gamma=0.001, C=100.,kernel='rbf')
clf.fit(r,t)
pr=clf.predict(p)
rr = clf.predict(rt)
print('foded ',sum(pr)/len(pr))
print('plain ',1-sum(rr)/len(rr))
#print(sum(pr)/len(pr)+sum(rr)/len(rr))
print('natList: ',len(n))
print(len(n)/2/len(r))

#modifyRandom(r,t,mL)

#X = [[0, 0], [1, 1]]
#y = [0, 1]
#clf = svm.SVC()
#clf.fit(X, y)  



