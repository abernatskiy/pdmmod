#! /usr/bin/python2

class Coordinate(object):
    def __init__(self,coordTuple):
        self.coordTuple=coordTuple
        
##DOESN'T change(!!!) the coordinate
    def stepUp(self):
        return Coordinate((self.coordTuple[0],self.coordTuple[1]+1))
    def stepDown(self):
        return Coordinate((self.coordTuple[0],self.coordTuple[1]-1))
    def stepRight(self):
        return Coordinate((self.coordTuple[0]+1,self.coordTuple[1]))
    def stepLeft(self):
        return Coordinate((self.coordTuple[0]-1,self.coordTuple[1]))
    def stepUpRight(self):
        return Coordinate((self.coordTuple[0]+1,self.coordTuple[1]+1))
    def stepUpLeft(self):
        return Coordinate((self.coordTuple[0]-1,self.coordTuple[1]+1))
    def stepDownRight(self):
        return Coordinate((self.coordTuple[0]+1,self.coordTuple[1]-1))
    def stepDownLeft(self):
        return Coordinate((self.coordTuple[0]-1,self.coordTuple[1]-1))

    #for a given coord tuple returns the list of contacting cells
    def primaryNeighborsFinder(self):
        contactList=[]
        contactList.append(Coordinate((self.coordTuple[0],self.coordTuple[1]+1)))
        contactList.append(Coordinate((self.coordTuple[0],self.coordTuple[1]-1)))
        contactList.append(Coordinate((self.coordTuple[0]+1,self.coordTuple[1])))
        contactList.append(Coordinate((self.coordTuple[0]-1,self.coordTuple[1])))
        return contactList

    def allNeighborsFinder(self):
        neighborsList=self.primaryNeighborsFinder()
        neighborsList.append(Coordinate((self.coordTuple[0]+1,self.coordTuple[1]+1)))
        neighborsList.append(Coordinate((self.coordTuple[0]+1,self.coordTuple[1]-1)))
        neighborsList.append(Coordinate((self.coordTuple[0]-1,self.coordTuple[1]+1)))
        neighborsList.append(Coordinate((self.coordTuple[0]-1,self.coordTuple[1]-1)))
        return neighborsList
    
    def allowedStepsFinder(self):
        """
        Interface of the sequence must be continuous, so we can stop only if 4 directions, while going from one point to another
        """
        return [self.stepDown(),self.stepLeft(),self.stepUp(),self.stepRight()]
    
    def __repr__(self):
        return str(self.coordTuple)
    
    def __str__(self):
        return str(self.coordTuple)
    
    def __eq__(self, other):
        return self.coordTuple==other.coordTuple
    

