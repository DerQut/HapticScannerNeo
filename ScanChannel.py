import random
import numpy as np


class ScanChannel:
    def __init__(self, name: str, gain: float, enabled: bool):
        self.__name = name
        self.__gain = gain
        self.__enabled = enabled
        self.scanPoints = set()
        self.resolution = 128
        self.preload()

        self.__zCutMin = 0
        self.__zCutMax = 10000

    def zCut(self):
        return self.__zCutMin, self.__zCutMax

    def zCutMin(self):
        return self.__zCutMin

    def zCutMax(self):
        return self.__zCutMax

    def name(self):
        return self.__name

    def enabled(self):
        return self.__enabled

    def gain(self):
        return self.__gain

    def setGain(self, gain: float):
        self.__gain = gain

    def setEnabled(self, enabled: bool):
        self.__enabled = enabled

    def setName(self, name: str):
        self.__name = name

    def setZCut(self, zCutMin: float, zCutMax: float):
        self.__zCutMin = zCutMin
        self.__zCutMax = zCutMax

    def setZCutMin(self, zCutMin: float):
        self.__zCutMin = zCutMin

    def setZCutMax(self, zCutMax: float):
        self.__zCutMax = zCutMax

    def getXValues(self):
        xList = []
        scanPointsLocal = set()
        scanPointsLocal.update(self.scanPoints)
        for point in scanPointsLocal:
            xList.append(point[0])
        return xList

    def getYValues(self):
        yList = []
        scanPointsLocal = set()
        scanPointsLocal.update(self.scanPoints)
        for point in scanPointsLocal:
            yList.append(point[1])
        return yList

    def getZValues(self):
        zList = []
        scanPointsLocal = set()
        scanPointsLocal.update(self.scanPoints)
        for point in scanPointsLocal:
            zList.append(point[2])
        return zList

    def getAllValues(self):
        xList = []
        yList = []
        zList = []
        scanPointsLocal = set()
        scanPointsLocal.update(self.scanPoints)
        for point in scanPointsLocal:
            xList.append(point[0])
            yList.append(point[1])
            zList.append(point[2])
        return xList, yList, zList

    def getPlotArray(self) -> np.ndarray:
        """
        Returns: Numpy array containing all scanPoints, arranged in a 2D grid, with an applied zCut setting
        """

        xResolution = max(self.getXValues())
        yResolution = max(self.getYValues())

        array = np.zeros((yResolution+1, xResolution+1))
        scanPointsLocal = set()
        scanPointsLocal.update(self.scanPoints)

        for point in scanPointsLocal:
            array[point[1]][point[0]] = min(self.zCutMax(), point[2]) if point[2] > self.zCutMin() else self.zCutMin()
        return array

    def preload(self):
        self.scanPoints = set()
        i = 0
        j = 0
        while j < self.resolution:
            while i < self.resolution:
                i = i + 1
                self.scanPoints.add((i, j, i*j/self.resolution/self.resolution*10000))
            j = j + 1
            i = 0

    def randomize(self):
        self.scanPoints = set()
        i = 0
        j = 0
        while j < self.resolution:
            while i < self.resolution:
                i = i + 1
                self.scanPoints.add((i, j, random.randint(0,255)))
            j = j + 1
            i = 0

    def addRandomDot(self, count=1):
        i = 0
        xResolution = max(self.getXValues())
        yResolution = max(self.getYValues())
        while i < count:
            self.scanPoints.add((random.randint(0, xResolution-1), (random.randint(0, yResolution-1)), random.randint(0,10000)))
            i = i + 1
