#!/usb/bin/python

"""
This file creates several vesicles and
evolves them through time.
It is used to make populational anasysis of the
innovative and evolutionary properties of hp-vesicles
"""

import os
#import random
import sys
sys.path.append('../')
import routes

import libSimulate


class VPopulation(object):
    """
    ??
    """
    def __init__(self, numGen, numInstance, modelNum, matureWeight, path):
        self.modelNum = modelNum
        self.numGen = numGen
        self.numInstance = numInstance
        self.path = path
        self.matureWeight = matureWeight

    def initPopFiles(self,endTime):
        """
        Initializes initPopFiles in the right directories for the future simulation runs
        Args:
            endTime:

        Returns:

        """

        return None


