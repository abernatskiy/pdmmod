#/usr/bin/python

import unittest
from collections import OrderedDict
from trajectory import *
import routes

class TrajTest(unittest.TestCase):
    def testModelLocation(self):
        tr = Trajectory(3,2,0)
        self.assertEqual(tr.modelLocation,routes.routePDM+'models/003')
    
    def testSimLocation(self):
        tr = Trajectory(3,2,0)
        self.assertEqual(tr.outputDir,routes.routePDM+'models/003/003_output2')
        
    def testTrajLocation(self):
        tr = Trajectory(3,2,0)
        self.assertEqual(tr.trajFile,routes.routePDM+'models/003/003_output2/traj0')
    
    def testTrajInfo(self):
        tr = Trajectory(3,2,0)
        self.assertEqual(tr.trajectory,(3,2,0))
    
    def testSeqDictTime(self):
        tr = Trajectory(3,2,0)
        tr.trajFile = 'mockTraj'
        minTime = 0.1
        self.assertEqual(tr.seqDict(minTime)[1],2)
    
    def testSeqDictSeqs(self):
        tr = Trajectory(3,2,0)
        tr.trajFile = 'mockTraj'
        minTime = 0.0
        corrDict = {'H':[50,30,10],'P':[50,50],'HP':[20],'fHPPHPHPH':[5,7],
                    'fHPHPHPHHHHHHHHH':[2,3]}
        self.assertEqual(tr.seqDict(minTime)[0],corrDict)
        
    def testAveSeqDict(self):
        tr = Trajectory(3,2,0)
        tr.trajFile = 'mockTraj'
        inputDict = {'H':[30,10],'P':[50,50],'HP':[20],'fHPPHPHPH':[5,7],
                    'fHPHPHPHHHHHHHHH':[2,3]}
        records = 2
        corrDict =  {'H':20,'P':50,'HP':10,'fHPPHPHPH':6,
                    'fHPHPHPHHHHHHHHH':2.5}
        self.assertEqual(tr.aveSeqDict(inputDict,records),corrDict)

    def testGetFreqs(self):
        tr = Trajectory(3,2,0)
        tr.trajFile = 'mockTraj'
        inputDict = {'H':50,'P':50,'HP':10,'PP':10,'HH':8,'fHHHH':6,
                     'HPHH':6,'HPPH':8,'fHPHPH':2.5}
        freqs = {1: {50: 2}, 2: {8: 1, 10: 2}, 3: {}, 
                 4: {6: 2, 8: 1}, 5: {2.5: 1}}
        intFreqs = {1: {50: 2}, 2: {8: 3, 10: 2}, 3: {}, 
                    4: {6: 3, 8: 1}, 5: {2.5: 1}}
        #for (l, fr) in freqs.items():
            #freqs[l]=OrderedDict(sorted(fr.items(), key=lambda t: t[0], reverse=False))
        self.assertEqual(tr.getFreqs(inputDict,5),(freqs,intFreqs))

    def testSeqAvesNoFold(self):
        tr = Trajectory(3,2,0)
        inputDict = {'H':50,'P':50,'HP':10,'PP':10,'HH':8,'fHHHH':6,
                     'HHHH':4,'HPPH':8,'fHPHPH':2.5}
        corrDict = {'H':50,'P':50,'HP':10,'PP':10,'HH':8,'HHHH':10,
                     'HPPH':8,'HPHPH':2.5}
        self.assertEqual(tr.seqAvesNoFold(inputDict),corrDict)

    def testCategorizeForScatter(self):
        tr = Trajectory(3,2,0)
        saa = {'H':50,'P':50,'HPHH':10,
                     'HHPH':8,'HHHPH':2.5}
        natData = {'HHPH': [1,'HHH'],'HPHH':[1,'N'],'HHHPH':[1,'HHH']}
        autox = [5]
        autoy = [2.5]
        foldx = [4,4]
        foldy = [10,8]
        regx = [1,1]
        regy = [50,50]
        ax,ay,fx,fy,rx,ry = tr.categorizeForScatter(saa,natData)
        self.assertEqual((ax,ay,fx,set(fy),rx,ry),
                         (autox,autoy,foldx,set(foldy),regx,regy))


if __name__ == '__main__':
    unittest.main()
