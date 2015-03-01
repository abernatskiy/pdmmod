from os import system as system
from sys import argv as argv

def setModel(oldNumber,newNumber):
    system ('cp model.cpp model'+str('%03d' % oldNumber)+'.cpp')
    print('cp model.cpp model'+str('%03d' % oldNumber)+'.cpp')
    system ('cp model.h model'+str('%03d' % oldNumber)+'.h')
    print('cp model.h model'+str('%03d' % oldNumber)+'.h')
    system ('cp model'+str('%03d' % newNumber)+'.cpp model.cpp')
    print('cp model'+str('%03d' % newNumber)+'.cpp model.cpp')
    system ('cp model'+str('%03d' % oldNumber)+'.h model.h')
    print('cp model'+str('%03d' % newNumber)+'.h model.h')
    
    return None


oldNumber=int(argv[1]) 
newNumber=int(argv[2]) 

setModel(oldNumber,newNumber)
