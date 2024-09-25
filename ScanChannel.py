import random


class ScanChannel:
    def __init__(self, name: str, gain: float, enabled: bool):
        self.__name = name
        self.__gain = gain
        self.__enabled = enabled
        self.scanPoints = []
        while len(self.scanPoints) < 2137:
            self.scanPoints.append((random.randint(0, 32), random.randint(0, 32), random.randint(0, 255)))

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
