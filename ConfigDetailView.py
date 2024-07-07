import serial, sys, glob

from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from assets import MacColoursDark
from Color import *

import platform, subprocess


class ConfigDetailView(QWidget):
    def __init__(self, color=MacColoursDark.bg_colour):
        super().__init__()

        self.COMPorts = []

        zStack = QStackedLayout()

        vStack = QVBoxLayout()

        nameLabel = QLabel("Configuration")
        nameLabel.setFont(QFont("Helvetica", 24))
        vStack.addWidget(nameLabel)

        divider1 = Divider(MacColoursDark.gray)
        vStack.addWidget(divider1)

        tcpipLabel = QLabel("Conection settings")
        vStack.addWidget(tcpipLabel)

        allConnectionsHStack = QHBoxLayout()
        allConnectionsVStack = QVBoxLayout()

        tcpipHStack = QHBoxLayout()

        self.ipField1 = QLineEdit()
        self.ipField1.setValidator(QIntValidator(0, 255, self))
        self.ipField2 = QLineEdit()
        self.ipField2.setValidator(QIntValidator(0, 255, self))
        self.ipField3 = QLineEdit()
        self.ipField3.setValidator(QIntValidator(0, 255, self))
        self.ipField4 = QLineEdit()
        self.ipField4.setValidator(QIntValidator(0, 255, self))
        self.portField = QLineEdit()
        self.portField.setValidator(QIntValidator(0, 65535, self))

        tcpipHStack.addWidget(self.ipField1)
        tcpipHStack.addWidget(QLabel("."))
        tcpipHStack.addWidget(self.ipField2)
        tcpipHStack.addWidget(QLabel("."))
        tcpipHStack.addWidget(self.ipField3)
        tcpipHStack.addWidget(QLabel("."))
        tcpipHStack.addWidget(self.ipField4)
        tcpipHStack.addWidget(QLabel("Port:"))
        tcpipHStack.addWidget(self.portField)
        self.tcpipConnectButton = QPushButton("Connect")
        self.tcpipConnectButton.setFixedWidth(120)
        tcpipHStack.addWidget(self.tcpipConnectButton)

        allConnectionsVStack.addLayout(tcpipHStack)

        comHStack = QHBoxLayout()

        self.COMPortsCombo = QComboBox()
        self.COMPortsCombo.addItems([])
        comHStack.addWidget(self.COMPortsCombo)

        comHStack.addWidget(QLabel("Baud rate:"))
        self.baudCombo = QComboBox()
        self.baudCombo.addItems(["600", "1200", "2400", "4800", "9600", "14400", "19200", "28800", "38400", "56000", "57600", "115200", "128000", "256000", "400000", "500000", "600000", "700000", "800000", "90000"])
        comHStack.addWidget(self.baudCombo)

        self.findCOMButton = QPushButton("Discover COM Ports")
        self.findCOMButton.setFixedWidth(240)
        comHStack.addWidget(self.findCOMButton)

        self.COMConnectButton = QPushButton("Connect")
        self.COMConnectButton.setFixedWidth(120)
        comHStack.addWidget(self.COMConnectButton)

        allConnectionsVStack.addLayout(comHStack)

        connectionLabelVStack = QVBoxLayout()
        connectionLabelVStack.addWidget(QLabel("IP:"))
        connectionLabelVStack.addWidget(QLabel("COM:"))
        allConnectionsHStack.addLayout(connectionLabelVStack)
        allConnectionsHStack.addLayout(allConnectionsVStack)
        vStack.addLayout(allConnectionsHStack)

        spacer1 = QWidget()
        vStack.addWidget(spacer1)

        spacer2 = QWidget()
        vStack.addWidget(spacer2)

        container = QWidget()
        container.setLayout(vStack)

        bgColor = Color(color)
        zStack.addWidget(bgColor)
        zStack.addWidget(container)
        zStack.setStackingMode(QStackedLayout.StackingMode.StackAll)

        self.portField.textChanged.connect(self.lineEditFormat)
        self.ipField1.textChanged.connect(self.lineEditFormat)
        self.ipField2.textChanged.connect(self.lineEditFormat)
        self.ipField3.textChanged.connect(self.lineEditFormat)
        self.ipField4.textChanged.connect(self.lineEditFormat)

        self.findCOMButton.clicked.connect(self.findCOMs)
        self.tcpipConnectButton.clicked.connect(self.tcpipConnect)

        self.setLayout(zStack)

    def lineEditFormat(self):
        arr = [self.ipField1, self.ipField2, self.ipField3, self.ipField4, self.portField]
        for lineEdit in arr:
            lineEdit.setText(lineEdit.text().strip())
            if lineEdit.text().strip() == "":
                continue
            lineEdit.setText(str(int(lineEdit.text())))
            if int(lineEdit.text()) > 255 and lineEdit is not self.portField:
                lineEdit.setText("255")
            elif int(lineEdit.text()) > 65535:
                lineEdit.setText("65535")

    def findCOMs(self):

        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        self.COMPorts = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                self.COMPorts.append(port)
            except (OSError, serial.SerialException):
                pass

        self.COMPortsCombo.clear()
        self.COMPortsCombo.addItems(self.COMPorts)

    def tcpipConnect(self):
        arr = [self.ipField1, self.ipField2, self.ipField3, self.ipField4, self.portField]
        for lineEdit in arr:
            if lineEdit.text().strip() == "":
                print("TCP/IP Connection error: incorrect address")
                return -1
        print(f"TCP/IP Connection at {self.ipField1.text()}.{self.ipField2.text()}.{self.ipField3.text()}.{self.ipField4.text()}:{self.portField.text()}")
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', f"{self.ipField1.text()}.{self.ipField2.text()}.{self.ipField3.text()}.{self.ipField4.text()}"]
        print(subprocess.call(command))

