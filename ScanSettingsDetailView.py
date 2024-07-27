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

        self.initialScanTopView = InitialScanTopView(self)
        self.rasterModeTopView = RasterModeTopView(self)
        self.hapticModeTopView = HapticModeTopView(self)

        self.initialScanBottomView = InitialScanBottomView(self)
        self.rasterModeBottomView = RasterModeBottomView(self)
        self.hapticModeBottomView = HapticModeBottomView(self)

        self.hStack = QHBoxLayout()
        self.vStack.addLayout(self.hStack)

        self.channelsView = ChannelsView(self)
        self.hStack.addWidget(self.channelsView)

        self.hStack.addWidget(self.initialScanTopView)
        self.hStack.addWidget(self.rasterModeTopView)
        self.hStack.addWidget(self.hapticModeTopView)
        self.initialScanTopView.show()

        self.vStack.addWidget(self.initialScanBottomView)
        self.vStack.addWidget(self.rasterModeBottomView)
        self.vStack.addWidget(self.hapticModeBottomView)
        self.vStack.addStretch()

        self.initialScanBottomView.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.pollServerStatus)
        self.timer.setInterval(500)

        self.setLayout(zStack)
        self.hide()

    def hide(self):
        super().hide()
        self.timer.stop()

    def show(self):
        super().show()
        self.timer.start()

    def lockInputs(self):
        self.scanModePicker.setEnabled(False)

        self.initialScanBottomView.nameField.setEnabled(False)
        self.initialScanBottomView.startButton.setEnabled(False)
        self.initialScanBottomView.stopButton.setEnabled(True)
        ...

    def unlockInputs(self):
        self.scanModePicker.setEnabled(True)

        self.initialScanBottomView.nameField.setEnabled(True)
        self.initialScanBottomView.startButton.setEnabled(True)
        self.initialScanBottomView.stopButton.setEnabled(False)

    def pollServerStatus(self):
        if self.server.getBusy():
            self.lockInputs()
        else:
            self.unlockInputs()

    def changeScanMode(self):
        self.scanMode = self.scanModePicker.currentText()

        self.rasterModeTopView.hide()
        self.rasterModeBottomView.hide()
        self.initialScanTopView.hide()
        self.initialScanBottomView.hide()
        self.hapticModeTopView.hide()
        self.hapticModeBottomView.hide()

        if self.scanMode == "Initial scan":
            self.initialScanTopView.show()
            self.initialScanBottomView.show()
        elif self.scanMode == "Raster mode":
            self.rasterModeTopView.show()
            self.rasterModeBottomView.show()
        elif self.scanMode == "Haptic mode":
            self.hapticModeTopView.show()
            self.hapticModeBottomView.show()


class ChannelsView(QWidget):
    def __init__(self, parent: ScanSettingsDetailView):
        super().__init__(parent)

        self.server: ServerNeo = parent.server

        dummyLayout = QVBoxLayout()
        dummyLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(dummyLayout)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setFixedWidth(300)
        self.scrollArea.setFixedHeight(200)
        dummyLayout.addWidget(self.scrollArea)

        self.setFixedHeight(250)
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
    def __init__(self, parent: ScanSettingsDetailView, channel: ScanChannel, number: int):
        super().__init__(parent)

        self.channel = channel

        hStack = QHBoxLayout()
        self.setLayout(hStack)

        self.toggle = QCheckBox()
        self.toggle.setChecked(channel.isEnabled)
        hStack.addWidget(self.toggle)

        numberLabel = QLabel(str(number + 1))
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

        zStack = QStackedLayout()
        zStack.setStackingMode(QStackedLayout.StackingMode.StackAll)

        zStack.addWidget(Color(MacColoursDark.green))

        vContainer = QWidget()
        vStack = QVBoxLayout()
        vContainer.setLayout(vStack)

        vStack.addWidget(QLabel("Initial Scan Top View"))
        vStack.addStretch()

        zStack.addWidget(vContainer)

        self.setLayout(zStack)

        self.setFixedHeight(250)

        self.hide()


class InitialScanBottomView(QWidget):
    def __init__(self, parent: ScanSettingsDetailView):
        super().__init__(parent)

        self.parent = parent

        dummyLayout = QVBoxLayout()
        dummyLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(dummyLayout)

        mainView = QWidget(self)
        mainVStack = QVBoxLayout()
        mainView.setLayout(mainVStack)
        mainView.setMinimumWidth(755)

        nameHStack = QHBoxLayout()
        nameHStack.addWidget(QLabel("Scan name:"))
        nameHStack.addStretch()
        self.nameField = QLineEdit()
        nameHStack.addWidget(self.nameField)

        buttonHStack = QHBoxLayout()
        self.startButton = QPushButton("Start")
        self.startButton.setStyleSheet(f"background-color: rgba{QPalette().accent().color().getRgb()};")
        self.stopButton = QPushButton("Stop")
        self.stopButton.setEnabled(False)
        buttonHStack.addWidget(self.startButton)
        buttonHStack.addWidget(self.stopButton)

        mainVStack.addLayout(nameHStack)
        spacer = QWidget()
        spacer.setFixedHeight(20)
        mainVStack.addWidget(spacer)
        mainVStack.addLayout(buttonHStack)

        scrollArea = QScrollArea(self)
        scrollArea.setWidget(mainView)

        dummyLayout.addWidget(scrollArea)
        self.hide()
        self.setFixedHeight(177)

        self.startButton.clicked.connect(self.startInitialScan)
        self.stopButton.clicked.connect(self.stopInitialScan)

    def startInitialScan(self):
        self.parent.lockInputs()
        self.parent.server.startInitialScan()

    def stopInitialScan(self):
        self.parent.unlockInputs()
        self.parent.server.stopInitialScan()


class RasterModeTopView(QWidget):
    def __init__(self, parent: ScanSettingsDetailView):
        super().__init__(parent)

        zStack = QStackedLayout()
        zStack.setStackingMode(QStackedLayout.StackingMode.StackAll)

        zStack.addWidget(Color(MacColoursDark.red))

        vContainer = QWidget()
        vStack = QVBoxLayout()
        vContainer.setLayout(vStack)

        vStack.addWidget(QLabel("Raster Mode Top View"))
        vStack.addStretch()

        zStack.addWidget(vContainer)

        self.setLayout(zStack)

        self.setFixedHeight(250)

        self.hide()


class RasterModeBottomView(QWidget):
    def __init__(self, parent: ScanSettingsDetailView):
        super().__init__(parent)

        dummyLayout = QVBoxLayout()
        dummyLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(dummyLayout)

        mainView = QWidget(self)
        mainVStack = QVBoxLayout()
        mainView.setLayout(mainVStack)
        mainView.setMinimumHeight(325)

        mainVStack.addWidget(QLabel("Raster Mode Bottom View"))
        mainVStack.addStretch()

        scrollArea = QScrollArea(self)
        scrollArea.setWidget(mainView)

        dummyLayout.addWidget(scrollArea)
        self.hide()


class HapticModeTopView(QWidget):
    def __init__(self, parent: ScanSettingsDetailView):
        super().__init__(parent)

        zStack = QStackedLayout()
        zStack.setStackingMode(QStackedLayout.StackingMode.StackAll)

        zStack.addWidget(Color(MacColoursDark.cyan))

        vContainer = QWidget()
        vStack = QVBoxLayout()
        vContainer.setLayout(vStack)

        vStack.addWidget(QLabel("Haptic Mode Top View"))
        vStack.addStretch()

        zStack.addWidget(vContainer)

        self.setLayout(zStack)

        self.setFixedHeight(250)

        self.hide()


class HapticModeBottomView(QWidget):
    def __init__(self, parent: ScanSettingsDetailView):
        super().__init__(parent)

        dummyLayout = QVBoxLayout()
        dummyLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(dummyLayout)

        mainView = QWidget(self)
        mainVStack = QVBoxLayout()
        mainView.setLayout(mainVStack)
        mainView.setMinimumHeight(325)

        mainVStack.addWidget(QLabel("Haptic Mode Bottom View"))
        mainVStack.addStretch()

        scrollArea = QScrollArea(self)
        scrollArea.setWidget(mainView)

        dummyLayout.addWidget(scrollArea)
        self.hide()
