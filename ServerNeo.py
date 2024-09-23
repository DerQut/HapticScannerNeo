import random
import socket
import os
from sys import platform
import threading
from datetime import datetime
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from time import gmtime, strftime

from logFileAppend import *
from ScanChannel import *
from missingXMLFallback import *

import xml.etree.ElementTree as ET


class ServerNeo(QObject):
    def __init__(self):
        super().__init__()

        self.channels: [ScanChannel] = []

        self.isBusy: bool = False

        self.port: int = 0
        self.host: str = ""

        self.configAutoSave: bool = False
        self.configCreateNewFolder: bool = False

        self.saveDir: str = ""

        self.pidSetpoint: int = 0
        self.pidSetpointLowerBound: int = 0
        self.pidSetpointUpperBound: int = 0

        self.proportionalGain: int = 0
        self.proportionalGainLowerBound: int = 0
        self.proportionalGainUpperBound: int = 0

        self.integralGain: int = 0
        self.integralGainLowerBound: int = 0
        self.integralGainUpperBound: int = 0

        self.differentialGain: int = 0
        self.differentialGainLowerBound: int = 0
        self.differentialGainUpperBound: int = 0

        self.isPIDOnline: bool = False

        if not os.path.isfile("config.xml"):
            missingXMLFallback()

        try:
            self.readXML()
        except Exception as e:
            print(e)

        self.logFile = ""
        self.reInitialiseLogFile()

        self.receivedData = 0
        self.sentCommand = None

        self.waitingForAnswer: bool = False

        self.socket: socket.socket = None
        self.conn: socket.socket = None
        self.addr = None

    def reInitialiseLogFile(self):
        if not self.saveDir:
            self.saveDir = os.get
        if list(self.saveDir)[len(self.saveDir)-1] != "/":
            self.saveDir += "/"

        if not os.path.isdir(self.saveDir):
            os.mkdir(self.saveDir)

        self.logFile = f"{self.saveDir}log-{strftime("%Y-%m-%d--%H-%M-%S", gmtime())}.txt"

        logFileAppend(self.logFile, "Initial configuration:")
        logFileAppend(self.logFile, "IP: " + self.host)
        logFileAppend(self.logFile, "Port: " + str(self.port))
        logFileAppend(self.logFile, "SaveDir: " + self.saveDir)
        logFileAppend(self.logFile, "configCreateNewFolder: " + str(self.configCreateNewFolder))
        logFileAppend(self.logFile, "configAutoSave: " + str(self.configAutoSave))
        logFileAppend(self.logFile, f"Kp: {self.proportionalGain}, Ki: {self.integralGain}, Kd: {self.differentialGain}")
        logFileAppend(self.logFile, f"pidSetpoint: {self.pidSetpoint}")
        logFileAppend(self.logFile, f"isPIDOnline: {self.isPIDOnline}\n")

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(2)
        self.conn, self.addr = self.socket.accept()

        with self.conn:
            self.handshake()
            print('\nConnected by', self.addr)
            while True:
                self.receivedData = self.conn.recv(1024)
                if self.receivedData:
                    self.gettingMessage()

    def requestScannerPosition(self):
        data = b'\xC0\x10'
        self.conn.sendall(data)

    def handshake(self):
        data = 0x00014841
        data = data.to_bytes(4, byteorder='big')
        self.sentCommand = b'\x00\x01'
        logFileAppend(self.logFile, "Trying to connect with microscope...")
        self.conn.sendall(data)
        self.waitingForAnswer = True
        self.waitForAnswer()

    def gettingMessage(self):
        ...

    def waitForAnswer(self):
        ...

    def writeConfigXML(self):
        logFileAppend(self.logFile, "Saving configuration to config.xml...")
        tree = ET.parse('config.xml')
        root = tree.getroot()
        for child in root:
            if child.tag != 'config':
                continue

            for key in child:
                if key.tag == "nixsavedir" and platform in ["darwin", "linux", "linux2"]:
                    key.text = self.saveDir
                elif key.tag == "winsavedir" and platform == "win32":
                    key.text = self.saveDir.replace("\\", "/")
                elif key.tag == "host":
                    key.text = self.host
                elif key.tag == "port":
                    key.text = str(self.port)
                elif key.tag == "createnewfolder":
                    key.text = str(int(self.configCreateNewFolder))
                elif key.tag == "autosave":
                    key.text = str(int(self.configAutoSave))

        tree.write("config.xml")
        logFileAppend(self.logFile, "Configuration successfully saved to config.xml.")

    def writePIDXML(self):
        logFileAppend(self.logFile, "Saving PID settings to config.xml...")
        tree = ET.parse('config.xml')
        root = tree.getroot()
        for child in root:
            if child.tag != 'pid':
                continue

            for superchild in child:
                if superchild.tag == 'setpoint':
                    superchild.text = str(self.pidSetpoint)

                elif superchild.tag == "setpointlowerlimit":
                    superchild.text = str(self.pidSetpointLowerBound)

                elif superchild.tag == "setpointupperlimit":
                    superchild.text = str(self.pidSetpointUpperBound)

                elif superchild.tag == "isonline":
                    superchild.text = str(int(self.isPIDOnline))
                elif superchild.tag == 'gain':
                    name = superchild.attrib.get("name")
                    for key in superchild:
                        if name == "proportional":
                            if key.tag == "value":
                                key.text = str(self.proportionalGain)
                            elif key.tag == "upperlimit":
                                key.text = str(self.proportionalGainUpperBound)
                            elif key.tag == "lowerlimit":
                                key.text = str(self.proportionalGainLowerBound)
                        elif name == "integral":
                            if key.tag == "value":
                                key.text = str(self.integralGain)
                            elif key.tag == "upperlimit":
                                key.text = str(self.integralGainUpperBound)
                            elif key.tag == "lowerlimit":
                                key.text = str(self.integralGainLowerBound)
                        elif name == "differential":
                            if key.tag == "value":
                                key.text = str(self.differentialGain)
                            elif key.tag == "upperlimit":
                                key.text = str(self.differentialGainUpperBound)
                            elif key.tag == "lowerlimit":
                                key.text = str(self.differentialGainLowerBound)

        tree.write("config.xml")
        logFileAppend(self.logFile, "PID settings successfully saved to config.xml.")

    def writeChannelsXML(self):
        logFileAppend(self.logFile, "Saving channel names and gain settings to config.xml...")
        tree = ET.parse('config.xml')
        root = tree.getroot()
        for child in root:
            if child.tag != 'channels':
                continue

            for superchild in child:
                for key in superchild:
                    if key.tag == "name":
                        key.text = self.channels[int(superchild.attrib.get("id"))-1].name()
                    elif key.tag == "gain":
                        gain = self.channels[int(superchild.attrib.get("id"))-1].gain()
                        key.text = str(float(gain)) if gain < 1 else str(int(gain))
                    elif key.tag == "enabled":
                        key.text = str(int(bool(self.channels[int(superchild.attrib.get("id"))-1].enabled())))

        tree.write("config.xml")
        logFileAppend(self.logFile, "Channel names successfully saved to config.xml.")

    def startInitialScan(self, scanName: str, operatingMode: str, curveDensity: float, speed: float):
        logFileAppend(self.logFile, f"Starting initial scan named \"{scanName}\" with given parameters: operatingMode=\"{operatingMode}\", curveDensity={curveDensity}%, speed={speed}%")
        self.isBusy = True
        ...

    def stopInitialScan(self):
        logFileAppend(self.logFile, "Stopping initial scan...")
        self.isBusy = False
        ...

    def startRasterScan(self, scanName: str, operatingMode: str, traceTime: int, retraceTime: int, interval: int):
        logFileAppend(self.logFile, f"Starting raster scan named \"{scanName}\" with given parameters: operatingMode=\"{operatingMode}\", traceTime={traceTime}ms, retraceTime={retraceTime}ms, interval={interval}ms")
        self.isBusy = True
        ...

    def stopRasterScan(self):
        logFileAppend(self.logFile, "Stopping raster scan...")
        self.isBusy = False
        ...

    def startHapticScan(self):
        logFileAppend(self.logFile, "Starting haptic scan...")
        self.isBusy = True

    def stopHapticScan(self):
        logFileAppend(self.logFile, "Stopping haptic scan...")
        self.isBusy = False

    def getCE(self):
        # THIS IS A TEMPORARY FUNCTION
        return random.randrange(0, 1000000, 1) / 10001

    def getCV(self):
        # THIS IS A TEMPORARY FUNCTION
        return random.randrange(0, 1000000, 1) / 10001

    def getBusy(self):
        # THIS IS A TEMPORARY FUNCTION
        return self.isBusy

    def getRasterProgress(self):
        # THIS IS A TEMPORARY FUNCTION
        return random.randint(0, 100)

    def getAvgRasterTime(self) -> int:
        """
        THIS IS A TEMPORARY FUNCTION
        :return: Average time between lines when the microscope is in Raster mode (in milliseconds)
        """
        return random.randint(0, 100)

    def getTotalRasterTime(self) -> int:
        """
        THIS IS A TEMPORARY FUNCTION
        :return: Total duration of the last scan conducted in Raster mode (in seconds)
        """
        return random.randint(0, 100)

    def getAvgHapticTime(self) -> int:
        """
        THIS IS A TEMPORARY FUNCTION
        :return: Average time between points when the microscope is in Haptic mode (in milliseconds)
        """
        return random.randint(0, 100)

    def getTotalHapticTime(self) -> int:
        """
        THIS IS A TEMPORARY FUNCTION
        :return: Total duration of the last scan conducted in Haptic mode (in seconds)
        """
        return random.randint(0, 100)

    def getOnlinePID(self) -> (int, int, int):
        """
        THIS IS A TEMPORARY FUNCTION
        :return: PID settings arranged in a tuple containing integers in range from 0 to 65535: (kp, ki, kd)
        """
        kp = random.randrange(0, 65535, 1)
        ki = random.randrange(0, 65535, 1)
        kd = random.randrange(0, 65535, 1)

        self.proportionalGain = kp
        self.integralGain = ki
        self.differentialGain = kd

        return kp, ki, kd

    def readXML(self):
        tree = ET.parse('config.xml')
        root = tree.getroot()
        for child in root:
            if child.tag == 'pid':

                for superchild in child:
                    if superchild.tag == 'setpoint':
                        self.pidSetpoint = int(superchild.text)
                    elif superchild.tag == "setpointlowerlimit":
                        self.pidSetpointLowerBound = float(superchild.text)
                    elif superchild.tag == "setpointupperlimit":
                        self.pidSetpointUpperBound = float(superchild.text)
                    elif superchild.tag == 'isonline':
                        self.isPIDOnline = bool(int(superchild.text))
                    elif superchild.tag == 'gain':

                        if superchild.attrib.get('name') == "proportional":
                            for value in superchild.iter('value'):
                                self.proportionalGain = int(value.text)
                            for lowerBound in superchild.iter('lowerlimit'):
                                self.proportionalGainLowerBound = float(lowerBound.text)
                            for upperBound in superchild.iter('upperlimit'):
                                self.proportionalGainUpperBound = float(upperBound.text)

                        elif superchild.attrib.get('name') == "integral":
                            for value in superchild.iter('value'):
                                self.integralGain = int(value.text)
                            for lowerBound in superchild.iter('lowerlimit'):
                                self.integralGainLowerBound = float(lowerBound.text)
                            for upperBound in superchild.iter('upperlimit'):
                                self.integralGainUpperBound = float(upperBound.text)

                        elif superchild.attrib.get('name') == "differential":
                            for value in superchild.iter('value'):
                                self.differentialGain = int(value.text)
                            for lowerBound in superchild.iter('lowerlimit'):
                                self.differentialGainLowerBound = float(lowerBound.text)
                            for upperBound in superchild.iter('upperlimit'):
                                self.differentialGainUpperBound = float(upperBound.text)

            elif child.tag == "config":
                for superchild in child:
                    if superchild.tag == "winsavedir" and platform == "win32":
                        self.saveDir = superchild.text
                    elif superchild.tag == "nixsavedir" and platform in ["linux", "darwin", "linux2"]:
                        self.saveDir = superchild.text
                    elif superchild.tag == "host":
                        self.host = superchild.text
                    elif superchild.tag == "port":
                        self.port = int(superchild.text)
                    elif superchild.tag == "createnewfolder":
                        self.configCreateNewFolder = bool(int(superchild.text))
                    elif superchild.tag == "autosave":
                        self.configAutoSave = bool(int(superchild.text))

            elif child.tag == "channels":
                for superchild in child:
                    gain = None
                    name = None
                    enabled = None
                    for key in superchild:
                        if key.tag == 'name':
                            name = key.text
                        elif key.tag == 'gain':
                            gain = float(key.text)
                        elif key.tag == 'enabled':
                            enabled = bool(int(key.text))
                    self.channels.append(ScanChannel(name, gain, enabled))
