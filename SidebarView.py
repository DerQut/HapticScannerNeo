from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *

import assets
from assets import MacColoursDark
from Color import *


class SidebarView(QWidget):
    def __init__(self, color=MacColoursDark.side_bar_inactive_colour):
        super().__init__()

        zStack = QStackedLayout()
        vStack = QVBoxLayout()
        vContainer = QWidget()
        vContainer.setLayout(vStack)

        mainLabel = QLabel("HapticScannerNeo")
        mainLabel.setFont(QFont("Helvetica", 28))
        vStack.addWidget(mainLabel)

        vStack.addWidget(Divider(assets.MacColoursDark.gray))

        spacer = QWidget()
        spacer.setFixedSize(1, 600)
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
