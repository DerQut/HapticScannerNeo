import socket
import os
import threading
from datetime import datetime
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from time import gmtime, strftime

from logFileAppend import *
from ScanChannel import *


class ServerNeo(QObject):
    def __init__(self):
        super().__init__()

        self.host = '192.168.1.103'
        self.port = 8881
        self.saveDir = "C:/PomiaryHaptyczne"
        self.configCreateNewFolder = True
        self.configAutoSave = True

        self.proportionalGain = 1
        self.integralGain = 1
        self.differentialGain = 1
        self.pidSetpoint = 10
        self.isPIDOnline = True

        self.channels = []
        self.channelNamesPrepare()

        if os.path.isfile("config.txt"):
            configFile = open("config.txt", "r")
            configDataRaw = configFile.readlines()
            configFile.close()

            configData = []

            for line in configDataRaw:
                configData.append(line.strip())

            if len(configData) < 5:
                self.fallbackConfigSetup()
            else:
                self.saveDir = configData[0]
                self.host = configData[1]
                self.port = int(configData[2])
                self.configCreateNewFolder = bool(int(configData[3]))
                self.configAutoSave = bool(int(configData[4]))
        else:
            self.fallbackConfigSetup()

        if os.path.isfile("pid.txt"):

            pidFile = open("pid.txt", "r")
            pidDataRaw = pidFile.readlines()
            pidFile.close()

            pidData = []

            for line in pidDataRaw:
                pidData.append(line.strip())

            if len(pidData) < 5:
                self.fallbackPIDSetup()
            else:
                self.proportionalGain = int(pidData[0])
                self.integralGain = int(pidData[1])
                self.differentialGain = int(pidData[2])
                self.pidSetpoint = float(pidData[3])
                self.isPIDOnline = bool(int(pidData[4]))
        else:
            self.fallbackPIDSetup()

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

    def reSetup(self):
        if self.socket is not None:
            self.socket.close()

        self.__init__()

    def fallbackConfigSetup(self):
        configFile = open("config.txt", "w+")
        configFile.write("C:/PomiaryHaptyczne\n192.168.1.103\n8881\n1\n1")
        configFile.close()

    def fallbackPIDSetup(self):
        pidFile = open("pid.txt", "w+")
        pidFile.write("1\n1\n1\n10\n1")
        pidFile.close()

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

    def channelNamesPrepare(self):
        if not os.path.isfile("channelNames.txt"):
            channelNamesFIle = open("channelNames.txt", "w+")
            channelNamesFIle.close()

        channelNamesFile = open("channelNames.txt", "r")
        lines = channelNamesFile.readlines()
        channelNamesFile.close()

        if len(lines) < 10:
            channelNamesFile = open("channelNames.txt", "w+")
            i = 0
            while i < 10:
                channelNamesFile.write(f"Channel {i+1}")
                if i != 9:
                    channelNamesFile.write("\n")
                i = i + 1
            channelNamesFile.close()

        channelNamesFile = open("channelNames.txt", "r")
        linesRaw = channelNamesFile.readlines()
        channelNamesFile.close()

        lines = []
        for raw in linesRaw:
            rawList = list(raw)
            if rawList[-1] == "\n":
                rawList.pop()
            lines.append(''.join(rawList))

        while len(self.channels) < 10:
            channel = ScanChannel()
            channel.name = lines[len(self.channels)]
            self.channels.append(channel)


# I'm afraid this project will become just as horribly written and unstable as HapticScanner-1. may god have me in his mercy.
