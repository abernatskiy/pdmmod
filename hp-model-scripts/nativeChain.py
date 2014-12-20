#! /usr/bin/python

import sys
import coordinate

def HP2Bin(HPstring):
    """Convert a string of type 'HPHPHPPPHHP' to a string of 1s and 0s.""" 
    binseq =''
    for i in range(0,len(HPstring)):
            if HPstring[i] == 'H':
                binseq = binseq+'1'    
            else:
                binseq = binseq+'0'     
    return binseq


class NativeChain(object):
    """
    NativeChain(hpstring,vector,nativeEnergy)
    An object to represent the 2D HP lattice chain's sequence, conformation and free energy
    """ 
    __slots__ = ['hpstring','n','vec','coordinates','nativeEnergy','generatedNumber','subPattern','catPattern']
    def __init__(self,hpstring,vector,nativeEnergy):
        self.hpstring = hpstring.upper()  # The HP sequence as a string
        self.n = len(self.hpstring)                 # the chain length
        self.vec = vector.upper()                      # an (n-1)-dimensional vector representation of the chain
        self.coordinates=self.vec2coords()
        self.nativeEnergy=int(nativeEnergy)
        self.generatedNumber=None
        self.subPattern=self.findPattern('subPattern')
        self.catPattern=self.findPattern('catPattern')
        
      
        
    def __repr__(self):
        if self.vec==[]:
            return "vector isn't determined"
        else:
            line1='#'+str(self.generatedNumber)+' '+self.hpstring+' with nat.energy '+str(self.nativeEnergy)+'\n'
            line2="Sub: "+str(self.subPattern)+" Cat: "+str(self.catPattern)+" Vec: "+self.vec+'\n'
            return line1+line2
    
    def __str__(self):
        if self.vec==[]:
            return "vector isn't determined"
        else:
            line1='#'+str(self.generatedNumber)+' '+self.hpstring+' with nat.energy '+str(self.nativeEnergy)+'\n'
            line2="Sub: "+str(self.subPattern)+" Cat: "+str(self.catPattern)+" Vec: "+self.vec
            return line1+line2
          
    def vec2coords(self):
        """Convert a list of chain vectors to a list of coordinates (duples).""" 
        coordList = [coordinate.Coordinate((0,0))]
        x = 0
        y = 0
        if self.vec==[]:
            print("no vector is given!")
        else:
            for i in range(0,len(self.vec)):
                if self.vec[i] == 'U':
                    y = y + 1
                if self.vec[i] == 'R':
                    x = x + 1
                if self.vec[i] == 'D':
                    y = y - 1
                if self.vec[i] == 'L':
                    x = x - 1
                coordList.append(coordinate.Coordinate((x,y)))
        return coordList




    def allContactFinder(self):
        allContacts=[]
        for item in self.coordinates:
            contactList=item.allNeighborsFinder()
            #print contactList
            for pair in contactList:
                if not (pair in self.coordinates):
                    #print(str(pair)+' '+str(self.coordinates))
                    if not pair in allContacts:
                        allContacts.append(pair)
        return allContacts
    
    def hpstr2bin(self):
        """Convert a string of type 'HPHPHPPPHHP' to a list of 1s and 0s.""" 
        binseq =''
        for i in range(0,len(self.hpstring)):
             if self.hpstring[i] == 'H':
                binseq = binseq+'1'       
             else:
                binseq = binseq+'0' 
        return binseq
    
###Comments, debugging
    #Returns the list of coordinates of the surface of a given sequence
    
    def surfaceConnector(self):#First, looking for the all points contacting a given sequence
        allContacts=self.allContactFinder()
        #Here will be a list of surface coordinates in the order, in which one can walk the whole surface around with only allowedSteps
        surfaceCoordinates=[]
        #Starting from the first point in the list
        surfaceCoordinates.append(allContacts[0])
        currentStep=allContacts[0]
        nextStep=None
        count=0
        #While uncounted contacts present
        while count<=len(allContacts):
            #count counted contacts
            count+=1
            allowedSteps=currentStep.allowedStepsFinder()
            #Looking for all possible steps from the given point
            for step in allowedSteps:
                # if the step in the surface and not mentioned yet
                if (step in allContacts) and (not step in surfaceCoordinates):
                    #the first one is fine
                    surfaceCoordinates.append(step)
                    #moving to this coordinate
                    currentStep=step
                    #print currentStep
                    break
                
        return surfaceCoordinates

    #Finds the coordinates of non-polar monomers
    def hCoordFinder(self):
        hList=[]
        sequenceListed=list(self.hpstring)
        #Check every letter in the sequence
        for i in range(len(sequenceListed)):
            if sequenceListed[i]=='H':
                #append a coordinate of another H
                hList.append(self.coordinates[i])
        return hList

    #Finds coordinates of the free cells contacting hydrophobes            
    def hContactFinder(self):#hList is the list of all H's in the sequence
        hList=self.hCoordFinder()
        hContactList=[]
        #For every H in sequence
        for item in hList:
            #Find primary contacts of this H. This is a list
            HContacts=item.primaryNeighborsFinder()
            #For every pair in the contact list
            for pair in HContacts:
                #If this pair doesn't belong to the sequence
                if not pair in self.coordinates:
                    #and if it's not in the list of contacts of all H's
                    if not pair in hContactList:
                        #Then add it to the list
                        hContactList.append(pair)
        return hContactList
###Comments, debugging
    #From the coordinates of the hydrophobes and all surface coordinates calculates surface sequence
    def surfaceSequenceMaker(self):#Get the list of coordinates of the surface of a given sequence
        surfaceCoordinates=self.surfaceConnector()
        #Find H-contacting coordinates
        hContactList=self.hContactFinder()
        #Initialize the surface sequence
        surfaceSequence=''
        #for every coordinate in the surface coordinate list
        for i in range(len(surfaceCoordinates)):
            #if the coordinate belongs to H-contacting coordinates
            if surfaceCoordinates[i] in hContactList:
                #Then add 'H' to the sequence
                surfaceSequence=surfaceSequence+'H'
            # and if the coordinate doesn't contact 'H'
            else:
                #add 'P'
                surfaceSequence=surfaceSequence+'P'
                
        return surfaceSequence


    def findPattern(self,whatPattern):
        '''
        NativeChain, string (cases) -> string (cases)
        determines if a given type of pattern present in the sequence
        whatPattern: 
         - 'catPattern'
         - 'subPattern'
         it returns:
         -the pattern, if the pattern present
         -'N', if not
        '''
        if whatPattern=='catPattern':
            sequence=self.surfaceSequenceMaker()*2
        elif whatPattern=='subPattern':
            sequence=self.hpstring
        for i in range(8,1,-1):
            pat = 'H'*i #pattern is sequence of 'H' of length i
            if not sequence.find(pat)==-1:
                #print('pattern found and length is '+str(len(pat)))
                #print('looking for '+whatPattern+' in '+self.hpstring+' with '+sequence)
                #print(' ')
                if whatPattern=='catPattern' and len(pat)<3:
                    answer = 'N'
                else:
                    return pat
            
            else:
                answer = 'N'
        
        return answer
            


