#/usr/bin/python
"""
This module takes shape Trajectory pickle of a given Simulation trajectory 
and transforms them into desirable data. It also make various plots of data.
"""

import os
import pickle

import routes

class ShapeTrajectory(object):
    '''
    This class analyzes various aspects of stochastic simulations
    in the pdmmod framework
    '''
    def __init__(self, modelNum, simNum,trajNum,load=False):
        '''
         Arguments:
          - modelNum -- int, number of the model
          - simuNum -- int, number of the simulation, simulations within
          one model are usually differ by different parameters
          - trajNum -- int, number of trajectory. A simulation with a given set of the parameters can be run for several times to form an ensemble
        '''
        self.modelLocation = os.path.join(
             routes.routePDM , 'models', str("%03d" %modelNum))
        self.outputDir = os.path.join(
            self.modelLocation,str("%03d" %modelNum)+'_output'+str(simNum))
        self.trajFile = os.path.join(
            self.outputDir,'sTraj'+str(trajNum)+'.p')
        self.trajectory = (modelNum, simNum, trajNum)
        if load:
            self.shapeTraj = pickle.load(open(self.trajFile,'rb'))

    def getPersistentShapes(self,minTimeStep):#TODO
        '''self.shapeTraj -- list:
            [[('URD', 4), ('URULLD', 2),...],...]
        '''
        persistent = []
        for shape in self.shapeTraj[minTimeStep]:
            print(shape)
            sign = False
            for shapes in self.shapeTraj[minTimeStep:]:
                if shape[0] in [s[0] for s in shapes]:
                    sign = True
                else:
                    sign = False
                    break
            if sign == True:
                persistent.append(shape[0])
        return persistent


st = ShapeTrajectory(18,71,0,load=True)
