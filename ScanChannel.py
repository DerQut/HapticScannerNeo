import random
import numpy as np


class ScanChannel:
    def __init__(self, name: str, gain: float, enabled: bool):
        self.__name = name
        self.__gain = gain
        self.__enabled = enabled
        self.scanPoints = set()
        self.__isLoopRunning = False
        self.resolution = 128
        self.preload()

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

    def isLoopRunning(self):
        return self.__isLoopRunning

    def setLoopRunning(self, isRunning: bool):
        self.__isLoopRunning = isRunning

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

    def getArray(self):

        xResolution = max(self.getXValues())
        yResolution = max(self.getYValues())

        array = np.zeros((yResolution+1, xResolution+1))
        scanPointsLocal = set()
        scanPointsLocal.update(self.scanPoints)

        for point in scanPointsLocal:
            array[point[1]][point[0]] = point[2]

        return array

    def preload(self):
        self.scanPoints = set()
        i = 0
        j = 0
        while j < self.resolution:
            while i < self.resolution:
                i = i + 1
                self.scanPoints.add((i, j, i*j/self.resolution/self.resolution*255))
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
            self.scanPoints.add((random.randint(0, xResolution-1), (random.randint(0, yResolution-1)), random.randint(0,255)))
            i = i + 1
