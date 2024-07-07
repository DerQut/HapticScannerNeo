import socket
import threading
from datetime import datetime
from PyQt6.QtCore import QObject, QThread, pyqtSignal


class ServerNeo:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8881

        self.receivedData = 0
        self.sentCommand = None
        self.logArray = ''

        self.waitingForAnswer = False

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
        self.logArray = current_time + ': ' + 'Trying to connect with microscope...'
        self.conn.sendall(data)
        self.waitingForAnswer = True
        self.waitForAnswer()

    def gettingMessage(self):
        ...

    def waitForAnswer(self):
        ...
