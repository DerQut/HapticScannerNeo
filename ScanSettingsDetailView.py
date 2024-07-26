from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from assets import MacColoursDark
from Color import *

from ServerNeo import *
from ScanChannel import *
import os


class ScanSettingsDetailView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.server: ServerNeo = parent.server

        self.scanMode = "Initial scan"

        zStack = QStackedLayout()
        zStack.setStackingMode(QStackedLayout.StackingMode.StackAll)

        zStack.addWidget(Color(MacColoursDark.bg_colour))
        vContainer = QWidget()
        self.vStack = QVBoxLayout()
        vContainer.setLayout(self.vStack)
        zStack.addWidget(vContainer)
        self.vStack.setSpacing(20)

        firstSpacer = QWidget()
        firstSpacer.setFixedHeight(7)
        self.vStack.addWidget(firstSpacer)

        pidLabel = QLabel("Scan settings")
        pidLabel.setFont(QFont("Helvetica", 24))
        self.vStack.addWidget(pidLabel)

        self.vStack.addWidget(Divider(MacColoursDark.gray))

        scanModeHStack = QHBoxLayout()
        scanModeHStack.addWidget(QLabel("Scan mode:"))
        scanModeHStack.addStretch()
        self.scanModePicker = QComboBox(self)
        self.scanModePicker.addItems(["Initial scan", "Raster mode", "Haptic mode"])
        self.scanModePicker.setFixedWidth(240)
        self.scanModePicker.currentIndexChanged.connect(self.changeScanMode)
        scanModeHStack.addWidget(self.scanModePicker)

        self.vStack.addLayout(scanModeHStack)

        self.initialScanView = InitialScanTopView(self)
        self.rasterModeView = RasterModeTopView(self)
        self.hapticModeView = HapticModeTopView(self)

        self.hStack = QHBoxLayout()
        self.vStack.addLayout(self.hStack)

        self.channelsView = ChannelsView(self)
        self.hStack.addWidget(self.channelsView)

        self.hStack.addWidget(self.initialScanView)
        self.hStack.addWidget(self.rasterModeView)
        self.hStack.addWidget(self.hapticModeView)
        self.initialScanView.show()

        self.vStack.addStretch()

        self.setLayout(zStack)
        self.hide()

    def changeScanMode(self):
        self.scanMode = self.scanModePicker.currentText()
        self.rasterModeView.hide()
        self.initialScanView.hide()
        self.hapticModeView.hide()
        if self.scanMode == "Initial scan":
            self.initialScanView.show()
        elif self.scanMode == "Raster mode":
            self.rasterModeView.show()
        elif self.scanMode == "Haptic mode":
            self.hapticModeView.show()


class ChannelsView(QWidget):
    def __init__(self, parent: ScanSettingsDetailView):
        super().__init__(parent)

        self.server: ServerNeo = parent.server

        dummyLayout = QVBoxLayout()
        dummyLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(dummyLayout)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setFixedWidth(300)
        self.scrollArea.setFixedHeight(250)
        dummyLayout.addWidget(self.scrollArea)

        self.setFixedHeight(300)
        self.setFixedWidth(300)

        self.mainContainer = QWidget(self)
        self.mainContainer.setFixedWidth(280)

        dummyLayout.addStretch()

        self.saveButton = QPushButton("Save to config.xml")
        self.saveButton.clicked.connect(self.saveNames)
        dummyLayout.addWidget(self.saveButton)

        mainVStack = QVBoxLayout()
        mainVStack.setSpacing(0)
        mainVStack.setContentsMargins(0, 0, 0, 0)

        i = 0
        while i < len(parent.server.channels):
            mainVStack.addWidget(ChannelEntryView(parent, parent.server.channels[i], i))
            i = i + 1

        self.mainContainer.setLayout(mainVStack)
        self.scrollArea.setWidget(self.mainContainer)

    def saveNames(self):
        self.server.writeChannelsXML()


class ChannelEntryView(QWidget):
    def __init__(self, parent: ScanSettingsDetailView, channel: ScanChannel, id: int):
        super().__init__(parent)

        self.channel = channel

        hStack = QHBoxLayout()
        self.setLayout(hStack)

        self.toggle = QCheckBox()
        self.toggle.setChecked(channel.isEnabled)
        hStack.addWidget(self.toggle)

        numberLabel = QLabel(str(id+1))
        numberLabel.setFixedWidth(25)
        hStack.addWidget(numberLabel)

        self.textEntry = QLineEdit(self.channel.name)
        self.textEntry.textChanged.connect(self.sendName)
        hStack.addWidget(self.textEntry)
        self.textEntry.setFixedWidth(175)

        hStack.addStretch()

        button = QPushButton("⧉")
        button.setFont(QFont("Helvetica", 10))
        button.clicked.connect(self.summonWindow)
        button.setFixedSize(QSize(24, 24))
        hStack.addWidget(button)

        self.toggle.clicked.connect(self.sendEnabled)

    def summonWindow(self):
        print(self.channel.name)

    def sendName(self):
        self.channel.name = self.textEntry.text()

    def sendEnabled(self):
        self.channel.isEnabled = self.toggle.isChecked()


class InitialScanTopView(QWidget):
    def __init__(self, parent: ScanSettingsDetailView):
        super().__init__(parent)

        vStack = QVBoxLayout()
        vStack.setContentsMargins(0, 0, 0, 0)
        vStack.addWidget(Color(MacColoursDark.green))
        self.setLayout(vStack)

        self.setFixedHeight(300)

        self.hide()


class RasterModeTopView(QWidget):
    def __init__(self, parent: ScanSettingsDetailView):
        super().__init__(parent)

        vStack = QVBoxLayout()
        vStack.setContentsMargins(0, 0, 0, 0)
        vStack.addWidget(Color(MacColoursDark.red))
        self.setLayout(vStack)

        self.setFixedHeight(300)

        self.hide()


class HapticModeTopView(QWidget):
    def __init__(self, parent: ScanSettingsDetailView):
        super().__init__(parent)

        vStack = QVBoxLayout()
        vStack.setContentsMargins(0, 0, 0, 0)
        vStack.addWidget(Color(MacColoursDark.cyan))
        self.setLayout(vStack)

        self.setFixedHeight(300)

        self.hide()
