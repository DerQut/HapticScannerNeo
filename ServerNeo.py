import socket
import os
import threading
from datetime import datetime
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from time import gmtime, strftime

from logFileAppend import *
from ScanChannel import *

import xml.etree.ElementTree as ET


class ServerNeo(QObject):
    def __init__(self):
        super().__init__()

        self.channels = []

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
                    if superchild.tag == "savedir":
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
                    enabled = None
                    name = None
                    for key in superchild:
                        if key.tag == 'name':
                            name = key.text
                        elif key.tag == 'enabled':
                            enabled = bool(int(key.text))
                    self.channels.append(ScanChannel(name, enabled))

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

        self.receivedData = 0
        self.sentCommand = None
        self.logArray = ''

        self.waitingForAnswer = False

        self.socket: socket.socket = None
        self.conn: socket.socket = None
        self.addr = None

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
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.logArray = current_time + ': Trying to connect with microscope...'
        self.conn.sendall(data)
        self.waitingForAnswer = True
        self.waitForAnswer()

    def gettingMessage(self):
        ...

    def waitForAnswer(self):
        ...

    def writeConfigXML(self):
        tree = ET.parse('config.xml')
        root = tree.getroot()
        for child in root:
            if child.tag != 'config':
                continue

            for key in child:
                if key.tag == "savedir":
                    key.text = self.saveDir
                elif key.tag == "host":
                    key.text = self.host
                elif key.tag == "port":
                    key.text = str(self.port)
                elif key.tag == "createnewfolder":
                    key.text = str(int(self.configCreateNewFolder))
                elif key.tag == "autosave":
                    key.text = str(int(self.configAutoSave))

        tree.write("config.xml")

    def writePIDXML(self):
        tree = ET.parse('config.xml')
        root = tree.getroot()
        for child in root:
            if child.tag != 'pid':
                continue

            for superchild in child:
                if superchild.tag == 'setpoint':
                    superchild.text = str(self.pidSetpoint)
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

    def writeChannelsXML(self):
        ...




# I'm afraid this project will become just as horribly written and unstable as HapticScanner-1. may god have me in his mercy.
