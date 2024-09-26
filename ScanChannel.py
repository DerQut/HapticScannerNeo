import random


class ScanChannel:
    def __init__(self, name: str, gain: float, enabled: bool):
        self.__name = name
        self.__gain = gain
        self.__enabled = enabled
        self.scanPoints = set()
        self.__isLoopRunning = False
        self.resolution = 96
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
        for point in self.scanPoints:
            xList.append(point[0])
        return xList

    def getYValues(self):
        yList = []
        for point in self.scanPoints:
            yList.append(point[1])
        return yList

    def getZValues(self):
        zList = []
        for point in self.scanPoints:
            zList.append(point[2])
        return zList

    def getAllValues(self):
        xList = []
        yList = []
        zList = []
        for point in self.scanPoints:
            xList.append(point[0])
            yList.append(point[1])
            zList.append(point[2])
        return xList, yList, zList

    def preload(self):
        self.scanPoints = set()
        i = 0
        j = 0
        while j < self.resolution:
            while i < self.resolution:
                i = i + 1
                self.scanPoints.add((i/self.resolution, j/self.resolution, i*j/self.resolution/self.resolution*255))
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
        while i < count:
            self.scanPoints.add((random.randint(0, self.resolution)/self.resolution, random.randint(0, self.resolution)/self.resolution, random.randint(0,255)))
            i = i + 1
        print(len(self.scanPoints))
