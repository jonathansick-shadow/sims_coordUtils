from __future__ import with_statement
import os
import numpy
import unittest
import lsst.utils.tests as utilsTests
from lsst.utils import getPackageDir

from lsst.sims.utils import ObservationMetaData
from lsst.sims.coordUtils.utils import ReturnCamera
from lsst.sims.coordUtils import findChipNameFromRaDec, \
                                 findChipNameFromPupilCoords, \
                                 _findChipNameFromRaDec

class FindChipNameTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cameraDir = getPackageDir('sims_coordUtils')
        cameraDir = os.path.join(cameraDir, 'tests', 'cameraData')
        cls.camera = ReturnCamera(cameraDir)

    def setUp(self):
        numpy.random.seed(45532)

    def testExceptions(self):
        """
        Test that exceptions are raised when they should be
        """

        nStars = 10
        xpList = numpy.random.random_sample(nStars)*0.1
        ypList = numpy.random.random_sample(nStars)*0.1

        obs = ObservationMetaData(unrefractedRA=25.0, unrefractedDec=112.0, mjd=42351.0,
                                  rotSkyPos=35.0)

        # verify that an exception is raised if you do not pass in a camera
        with self.assertRaises(RuntimeError) as context:
            findChipNameFromPupilCoords(xpList, ypList)
        self.assertTrue('No camera defined' in context.exception.message)

        with self.assertRaises(RuntimeError) as context:
            findChipNameFromRaDec(xpList, ypList, obs_metadata=obs, epoch=2000.0)
        self.assertTrue('No camera defined' in context.exception.message)

        with self.assertRaises(RuntimeError) as context:
            _findChipNameFromRaDec(xpList, ypList, obs_metadata=obs, epoch=2000.0)
        self.assertTrue('No camera defined' in context.exception.message)

        # verify that an exception is raised if you do not pass in a numpy array
        with self.assertRaises(RuntimeError) as context:
            findChipNameFromPupilCoords(list(xpList), ypList)
        self.assertTrue('numpy arrays' in context.exception.message)

        with self.assertRaises(RuntimeError) as context:
            _findChipNameFromRaDec(list(xpList), ypList, obs_metadata=obs, epoch=2000.0)
        self.assertTrue('numpy arrays' in context.exception.message)

        with self.assertRaises(RuntimeError) as context:
            findChipNameFromPupilCoords(xpList, list(ypList))
        self.assertTrue('numpy arrays' in context.exception.message)

        with self.assertRaises(RuntimeError) as context:
            _findChipNameFromRaDec(xpList, list(ypList), obs_metadata=obs, epoch=2000.0)
        self.assertTrue('numpy arrays' in context.exception.message)

        # verify that an exception is raised if the two coordinate arrays contain
        # different numbers of elements
        xpDummy = numpy.random.random_sample(nStars/2)
        with self.assertRaises(RuntimeError) as context:
            findChipNameFromPupilCoords(xpDummy, ypList, camera=self.camera)
        self.assertTrue('xPupils' in context.exception.message)
        self.assertTrue('yPupils' in context.exception.message)

        with self.assertRaises(RuntimeError) as context:
            findChipNameFromRaDec(xpDummy, ypList, obs_metadata=obs, epoch=2000.0,
                                  camera=self.camera)
        self.assertTrue('RAs' in context.exception.message)
        self.assertTrue('Decs' in context.exception.message)

        with self.assertRaises(RuntimeError) as context:
            _findChipNameFromRaDec(xpDummy, ypList, obs_metadata=obs, epoch=2000.0,
                                   camera=self.camera)
        self.assertTrue('RAs' in context.exception.message)
        self.assertTrue('Decs' in context.exception.message)


        # verify that an exception is raised if you call findChipNameFromRaDec
        # without an epoch
        with self.assertRaises(RuntimeError) as context:
            findChipNameFromRaDec(xpList, ypList, obs_metadata=obs, camera=self.camera)
        self.assertTrue('epoch' in context.exception.message)
        self.assertTrue('findChipName' in context.exception.message)

        with self.assertRaises(RuntimeError) as context:
            _findChipNameFromRaDec(xpList, ypList, obs_metadata=obs, camera=self.camera)
        self.assertTrue('epoch' in context.exception.message)
        self.assertTrue('findChipName' in context.exception.message)

        # verify that an exception is raised if you call findChipNameFromRaDec
        # without an ObservationMetaData
        with self.assertRaises(RuntimeError) as context:
            findChipNameFromRaDec(xpList, ypList, epoch=2000.0, camera=self.camera)
        self.assertTrue('ObservationMetaData' in context.exception.message)
        self.assertTrue('findChipName' in context.exception.message)

        with self.assertRaises(RuntimeError) as context:
            _findChipNameFromRaDec(xpList, ypList, epoch=2000.0, camera=self.camera)
        self.assertTrue('ObservationMetaData' in context.exception.message)
        self.assertTrue('findChipName' in context.exception.message)

        # verify that an exception is raised if you call findChipNameFromRaDec
        # with an ObservationMetaData that has no mjd
        obsDummy = ObservationMetaData(unrefractedRA=25.0, unrefractedDec=-112.0,
                                       rotSkyPos=112.0)
        with self.assertRaises(RuntimeError) as context:
            findChipNameFromRaDec(xpList, ypList, epoch=2000.0, obs_metadata=obsDummy,
                                  camera=self.camera)
        self.assertTrue('mjd' in context.exception.message)
        self.assertTrue('findChipName' in context.exception.message)

        with self.assertRaises(RuntimeError) as context:
            _findChipNameFromRaDec(xpList, ypList, epoch=2000.0, obs_metadata=obsDummy,
                                  camera=self.camera)
        self.assertTrue('mjd' in context.exception.message)
        self.assertTrue('findChipName' in context.exception.message)

        # verify that an exception is raised if you all findChipNameFromRaDec
        # using an ObservationMetaData without a rotSkyPos
        obsDummy = ObservationMetaData(unrefractedRA=25.0, unrefractedDec=-112.0,
                                       mjd=52350.0)
        with self.assertRaises(RuntimeError) as context:
            findChipNameFromRaDec(xpList, ypList, epoch=2000.0, obs_metadata=obsDummy,
                                  camera=self.camera)
        self.assertTrue('rotSkyPos' in context.exception.message)
        self.assertTrue('findChipName' in context.exception.message)

        with self.assertRaises(RuntimeError) as context:
            _findChipNameFromRaDec(xpList, ypList, epoch=2000.0, obs_metadata=obsDummy,
                                  camera=self.camera)
        self.assertTrue('rotSkyPos' in context.exception.message)
        self.assertTrue('findChipName' in context.exception.message)




def suite():
    utilsTests.init()
    suites = []
    suites += unittest.makeSuite(FindChipNameTest)
    return unittest.TestSuite(suites)

def run(shouldExit=False):
    utilsTests.run(suite(),shouldExit)

if __name__ == "__main__":
    run(True)
