from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *

import assets
from assets import MacColoursDark
from Color import *
from ContentView import *
from ConfigDetailView import *


class SidebarView(QWidget):
    def __init__(self, parent: QWidget, color=MacColoursDark.side_bar_inactive_colour):
        super().__init__(parent)

        zStack = QStackedLayout()
        vStack = QVBoxLayout()
        vContainer = QWidget()
        vContainer.setLayout(vStack)

        mainLabel = QLabel("HapticScannerNeo")
        mainLabel.setFont(QFont("Helvetica", 32))
        vStack.addWidget(mainLabel)

        vStack.addWidget(Divider(assets.MacColoursDark.gray))

        entry1 = SidebarEntryView(self.parent(), "Configuration", ConfigDetailView(self.parent()))
        vStack.addWidget(entry1)

        spacer = QWidget()
        spacer.setFixedSize(1, 560)
        vStack.addWidget(spacer)

        buttonHStack = QHBoxLayout()
        clearDataButton = QPushButton("Clear Data")
        clearDataButton.setFixedHeight(50)
        clearDataButton.setStyleSheet("background-color: rgba(255,0,0,0);")
        clearLogButton = QPushButton("Clear Log")
        clearLogButton.setFixedHeight(50)
        buttonHStack.addWidget(clearDataButton)
        buttonHStack.addWidget(clearLogButton)

        vStack.addLayout(buttonHStack)

        bgColor = Color(color)
        zStack.addWidget(bgColor)
        zStack.addWidget(vContainer)
        zStack.setStackingMode(QStackedLayout.StackingMode.StackAll)

        vStack.setSpacing(0)
        self.setLayout(zStack)

        self.setFixedSize(QSize(400, 800))

        clearDataButton.clicked.connect(self.clearData)

    def clearData(self):
        print("Clearing Data")

    def changeDetailView(self, newDetailView: QWidget):
        self.parent().changeDetailView(newDetailView)


class SidebarEntryView(QWidget):
    def __init__(self, parent: QWidget, label: str, newDetailView: QWidget):
        super().__init__(parent)

        self.cv = parent
        self.label = label
        self.newDetailView = newDetailView

        self.hStack = QHBoxLayout()

        self.button = QPushButton("+")
        self.hStack.addWidget(self.button)
        self.qlabel = QLabel(self.label)
        self.hStack.addWidget(self.qlabel)

        self.button.clicked.connect(self.sendDetailView)
        self.button.setFixedSize(32, 32)

        self.setLayout(self.hStack)

    def sendDetailView(self):
        self.cv.nsv.changeDetailView(self.newDetailView)
