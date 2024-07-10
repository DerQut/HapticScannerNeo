import socket
import os
import threading
from datetime import datetime
from PyQt6.QtCore import QObject, QThread, pyqtSignal


class ServerNeo(QObject):
    def __init__(self):
        super().__init__()

        print("Setting up server...")

        self.host = '192.168.1.103'
        self.port = 8881
        self.saveDir = "C:/"
        self.configCreateNewFolder = True
        self.configAutoSave = True

        self.proportionalGain = 1
        self.integralGain = 1
        self.differentialGain = 1
        self.pidSetpoint = 10
        self.isPIDOnline = True

        if os.path.isfile("config.txt"):
            print("Reading config.txt...")

            configFile = open("config.txt", "r")
            configDataRaw = configFile.readlines()
            configFile.close()

            configData = []

            for line in configDataRaw:
                configData.append(line.strip())

            if len(configData) < 5:
                print("Invalid config.txt file. Repairing...")
                self.fallbackConfigSetup()
            else:
                self.saveDir = configData[0]
                self.host = configData[1]
                self.port = int(configData[2])
                self.configCreateNewFolder = bool(int(configData[3]))
                self.configAutoSave = bool(int(configData[4]))
        else:
            print("No config.txt found. Creating...")
            self.fallbackConfigSetup()

        if os.path.isfile("pid.txt"):
            print("Reading pid.txt...")

            pidFile = open("pid.txt", "r")
            pidDataRaw = pidFile.readlines()
            pidFile.close()

            pidData = []

            for line in pidDataRaw:
                pidData.append(line.strip())

            if len(pidData) < 5:
                print("Invalid pid.txt file. Repairing...")
                self.fallbackPIDSetup()
            else:
                self.proportionalGain = int(pidData[0])
                self.integralGain = int(pidData[1])
                self.differentialGain = int(pidData[2])
                self.pidSetpoint = int(pidData[3])
                self.isPIDOnline = bool(int(pidData[4]))
        else:
            print("No pid.txt found. Creating...")
            self.fallbackPIDSetup()

        print("\nFinal configuration:")
        print("IP: " + self.host)
        print("Port: " + str(self.port))
        print("SaveDir: " + self.saveDir)
        print("NewFolder: " + str(self.configCreateNewFolder))
        print("AutoSave: " + str(self.configAutoSave))
        print(f"Kp: {self.proportionalGain}, Ki: {self.integralGain}, Kd: {self.differentialGain}")

        self.receivedData = 0
        self.sentCommand = None
        self.logArray = ''

        self.waitingForAnswer = False

    def autoDestruct(self):
        print("\nServerNeo is dead. Long live ServerNeo.\n\n")

    def fallbackConfigSetup(self):
        configFile = open("config.txt", "w+")
        configFile.write("C:/\n192.168.1.103\n8881\n1\n1")
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
