import socket
import os
import threading
from datetime import datetime
from PyQt6.QtCore import QObject, QThread, pyqtSignal


class ServerNeo:
    def __init__(self):

        print("Setting up server...")

        self.host = '127.0.0.1'
        self.port = 8881
        self.saveDir = "C:/"
        self.configCreateNewFolder = True
        self.configAutoSave = True

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

        print("\nFinal configuration:")
        print("IP: " + self.host)
        print("Port: " + str(self.port))
        print("SaveDir: " + self.saveDir)
        print("NewFolder: " + str(self.configCreateNewFolder))
        print("AutoSave: " + str(self.configAutoSave))

        self.receivedData = 0
        self.sentCommand = None
        self.logArray = ''

        self.waitingForAnswer = False

    def fallbackConfigSetup(self):
        configFile = open("config.txt", "w+")
        configFile.write("C:/\n127.0.0.1\n8881\n1\n1")
        configFile.close()

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
