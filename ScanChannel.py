import random


class ScanChannel:
    def __init__(self, name: str, gain: float, enabled: bool):
        self.__name = name
        self.__gain = gain
        self.__enabled = enabled
        self.scanPoints = set()
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

    def preload(self):
        self.scanPoints = set()
        i = 0
        j = 0
        while j < 128:
            while i < 128:
                i = i + 1
                self.scanPoints.add((i, j, i*j/128/128*255))
            j = j + 1
            i = 0

    def randomize(self):
        self.scanPoints = set()
        i = 0
        j = 0
        while j < 128:
            while i < 128:
                i = i + 1
                self.scanPoints.add((i, j, random.randint(0,255)))
            j = j + 1
            i = 0

    def addRandomDot(self):
        print(self.name())
        self.scanPoints.add((random.randint(0,128), random.randint(0,128), random.randint(0,255)))
