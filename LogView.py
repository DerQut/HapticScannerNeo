from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *

import assets
from assets import MacColoursDark
from Color import *
from ServerNeo import *
import random


class LogView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.vStack = QVBoxLayout()
        self.setLayout(self.vStack)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(QLabel())

        self.vStack.addWidget(self.scrollArea)

        self.cv = parent
        self.server = self.cv.server

        self.timer = QTimer()
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.readLog)
        self.timer.start()

        self.scrollArea.verticalScrollBar().setValue(-1)

    def readLog(self):

        if not os.path.isfile(self.server.logFile):
            return -1
        file = open(self.server.logFile, "r")
        lines = file.readlines()
        file.close()

        xBuffer = self.scrollArea.horizontalScrollBar().value()
        yBuffer = self.scrollArea.verticalScrollBar().value()

        vStack = QVBoxLayout()
        vStack.setSpacing(0)
        vStack.addStretch()

        for line in lines:
            label = QLabel(line)
            label.setFont(QFont("Helvetica", 11))
            label.setFixedHeight(18)
            vStack.addWidget(label)

        shouldPush = (self.scrollArea.widget().height() - self.scrollArea.verticalScrollBar().height() == yBuffer) or (self.scrollArea.verticalScrollBar().value() == -1)

        container = QWidget()
        container.setLayout(vStack)
        self.scrollArea.setWidget(container)
        self.scrollArea.horizontalScrollBar().setValue(xBuffer)
        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.widget().height() - self.scrollArea.verticalScrollBar().height() if shouldPush else yBuffer)
