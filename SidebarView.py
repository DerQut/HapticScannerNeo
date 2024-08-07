from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *

import assets
from assets import MacColoursDark
from Color import *
from ContentView import *
from ConfigDetailView import *
from PIDDetailView import *
from ScanSettingsDetailView import *
from ToolsDetailView import *


class SidebarView(QWidget):
    def __init__(self, parent: QWidget, color=MacColoursDark.side_bar_inactive_colour):
        super().__init__(parent)

        zStack = QStackedLayout()
        vStack = QVBoxLayout()
        vContainer = QWidget()
        vContainer.setLayout(vStack)

        firstSpacer = QWidget()
        firstSpacer.setFixedHeight(0)
        vStack.addWidget(firstSpacer)

        mainLabel = QLabel("HapticScannerNeo")
        mainLabel.setFont(QFont("Helvetica", 28))
        vStack.addWidget(mainLabel)

        vStack.addWidget(Divider(assets.MacColoursDark.gray))

        vStack.addWidget(SidebarEntryView(self.parent(), "Configuration", ConfigDetailView(self.parent())))
        vStack.addWidget(SidebarEntryView(self.parent(), "PID Controller settings", PIDDetailView(self.parent())))
        vStack.addWidget(SidebarEntryView(self.parent(), "Scan settings", ScanSettingsDetailView(self.parent())))
        vStack.addWidget(SidebarEntryView(self.parent(), "Tools", ToolsDetailView(self.parent())))

        vStack.addStretch()

        buttonHStack = QHBoxLayout()
        leftButton = QPushButton("Button 1")
        leftButton.setFixedHeight(50)
        leftButton.setStyleSheet(f"background-color: rgba{QPalette().accent().color().getRgb()};")
        rightButton = QPushButton("Button 2")
        rightButton.setFixedHeight(50)
        buttonHStack.addWidget(leftButton)
        buttonHStack.addWidget(rightButton)

        vStack.addLayout(buttonHStack)

        bgColor = Color(color)
        zStack.addWidget(bgColor)
        zStack.addWidget(vContainer)
        zStack.setStackingMode(QStackedLayout.StackingMode.StackAll)

        vStack.setSpacing(0)
        self.setLayout(zStack)

        self.setFixedSize(QSize(400, 800))
        vStack.setSpacing(20)
        vStack.setContentsMargins(10, 10, 10, 10)

        leftButton.clicked.connect(self.leftButtonAction)

    def leftButtonAction(self):
        print("..?")

    def changeDetailView(self, newDetailView: QWidget):
        self.parent().changeDetailView(newDetailView)


class SidebarEntryView(QWidget):
    def __init__(self, parent: QWidget, label: str, newDetailView: QWidget):
        super().__init__(parent)

        self.cv: ContentView = parent
        self.label = label
        self.newDetailView = newDetailView

        self.hStack = QHBoxLayout()

        self.button = QPushButton("+")
        self.button.setFont(QFont("Helvetica", 10))
        self.button.setStyleSheet(f"background-color: rgba{QPalette().accent().color().getRgb()};")
        self.hStack.addWidget(self.button)
        self.qlabel = QLabel(self.label)
        self.hStack.addWidget(self.qlabel)

        self.button.clicked.connect(self.sendDetailView)
        self.button.setFixedSize(24, 24)

        self.setLayout(self.hStack)

    def sendDetailView(self):
        self.cv.nsv.changeDetailView(self.newDetailView)
