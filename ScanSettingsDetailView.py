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

        self.timer = QTimer()
        self.timer.timeout.connect(self.pollServerStatus)
        self.timer.setInterval(500)

        self.server: ServerNeo = parent.server

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

        self.initialScanBottomView.show()

        self.setLayout(zStack)
        self.hide()

    def hide(self):
        super().hide()
        self.timer.stop()

    def show(self):
        super().show()
        self.timer.start()

    def startInitialScan(self):
        self.server.startInitialScan(self.initialScanBottomView.nameField.text(), self.initialScanTopView.modePicker.currentText(), self.initialScanTopView.densityStepper.value(), self.initialScanTopView.speedStepper.value())

    def stopInitialScan(self):
        self.server.stopInitialScan()

    def startRasterScan(self):
        self.server.startRasterScan(self.rasterModeBottomView.nameField.text(), self.rasterModeTopView.modePicker.currentText(), self.rasterModeTopView.traceTimeStepper.value(), self.rasterModeTopView.retraceTimeStepper.value(), self.rasterModeTopView.intervalStepper.value())

    def stopRasterScan(self):
        self.server.stopRasterScan()

    def startHapticScan(self):
        self.server.startHapticScan()

    def stopHapticScan(self):
        self.server.stopHapticScan()

    def setInputsEnabled(self, enabled: bool):
        self.scanModePicker.setEnabled(enabled)

        self.initialScanBottomView.nameField.setEnabled(enabled)
        self.initialScanBottomView.startButton.setEnabled(enabled)
        self.initialScanBottomView.stopButton.setEnabled(not enabled)

        self.initialScanTopView.modePicker.setEnabled(enabled)
        self.initialScanTopView.densityStepper.setEnabled(enabled)
        self.initialScanTopView.speedStepper.setEnabled(enabled)

        self.rasterModeBottomView.nameField.setEnabled(enabled)
        self.rasterModeBottomView.startButton.setEnabled(enabled)
        self.rasterModeBottomView.stopButton.setEnabled(not enabled)

        self.rasterModeTopView.modePicker.setEnabled(enabled)
        self.rasterModeTopView.traceTimeStepper.setEnabled(enabled)
        self.rasterModeTopView.retraceTimeStepper.setEnabled(enabled)
        self.rasterModeTopView.intervalStepper.setEnabled(enabled)

        if self.scanModePicker.currentText() == "Initial scan":
            return 0

        for channelEntryView in self.channelsView.channelEntryViews:
            channelEntryView.gainPicker.setEnabled(enabled)

    def pollServerStatus(self):
        if self.server.getBusy():
            self.setInputsEnabled(False)
            self.rasterModeBottomView.progressBar.setValue(self.server.getRasterProgress())
        else:
            self.setInputsEnabled(True)

    def changeScanMode(self):
        scanMode = self.scanModePicker.currentText()

        self.rasterModeTopView.hide()
        self.rasterModeBottomView.hide()
        self.initialScanTopView.hide()
        self.initialScanBottomView.hide()
        self.hapticModeTopView.hide()
        self.hapticModeBottomView.hide()

        if scanMode == "Initial scan":
            self.initialScanTopView.show()
            self.initialScanBottomView.show()
        elif scanMode == "Raster mode":
            self.rasterModeTopView.show()
            self.rasterModeBottomView.show()
        elif scanMode == "Haptic mode":
            self.hapticModeTopView.show()
            self.hapticModeBottomView.show()


class ChannelsView(QWidget):
    def __init__(self, parent: ScanSettingsDetailView):
        super().__init__(parent)

        self.server: ServerNeo = parent.server
        self.channelEntryViews: [ChannelsView] = []

        dummyLayout = QVBoxLayout()
        dummyLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(dummyLayout)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setFixedWidth(340)
        self.scrollArea.setFixedHeight(200)
        dummyLayout.addWidget(self.scrollArea)

        self.setFixedHeight(250)
        self.setFixedWidth(340)

        self.mainContainer = QWidget(self)
        self.mainContainer.setFixedWidth(315)

        dummyLayout.addStretch()

        self.saveButton = QPushButton("Save to config.xml")
        self.saveButton.clicked.connect(self.saveNames)
        dummyLayout.addWidget(self.saveButton)

        mainVStack = QVBoxLayout()
        mainVStack.setSpacing(0)
        mainVStack.setContentsMargins(0, 0, 0, 0)

        i = 0
        while i < len(parent.server.channels):
            channelEntryView = ChannelEntryView(parent, parent.server.channels[i], i)
            mainVStack.addWidget(channelEntryView)
            self.channelEntryViews.append(channelEntryView)
            i = i + 1

        self.mainContainer.setLayout(mainVStack)
        self.scrollArea.setWidget(self.mainContainer)

    def saveNames(self):
        self.server.writeChannelsXML()


class ChannelEntryView(QWidget):
    def __init__(self, scanSettingsDetailView: ScanSettingsDetailView, channel: ScanChannel, number: int):
        super().__init__()

        self.scanSettingsDetailView = scanSettingsDetailView
        self.scanSettingsDetailView.scanModePicker.currentTextChanged.connect(self.setGainsEnabledDependingOnScanMode)

        self.channel = channel
        self.number = number

        hStack = QHBoxLayout()
        self.setLayout(hStack)

        numberLabel = QLabel(str(number + 1))
        numberLabel.setFixedWidth(25)
        hStack.addWidget(numberLabel)

        self.gainPicker = QComboBox()
        self.gainPicker.addItems([
            "Disabled",
            "0.25x",
            "0.5x",
            "1x",
            "2x",
            "4x",
            "8x",
            "16x"
        ])

        self.setGainsEnabledDependingOnScanMode()

        if self.channel.gain < 1:
            self.gainPicker.setCurrentText(f"{self.channel.gain}x" if self.channel.gain > 0 else "Disabled")
        else:
            self.gainPicker.setCurrentText(f"{int(self.channel.gain)}x")

        self.gainPicker.setCurrentText("Disabled" if self.channel.gain == 0 else (f"{self.channel.gain}x") if self.channel.gain < 1 else f"{int(self.channel.gain)}x")
        self.gainPicker.currentIndexChanged.connect(self.setGain)
        hStack.addWidget(self.gainPicker)

        self.textEntry = QLineEdit(self.channel.name)
        self.textEntry.textChanged.connect(self.sendName)
        hStack.addWidget(self.textEntry)
        self.textEntry.setFixedWidth(125)

        hStack.addStretch()

        button = QPushButton("⧉")
        button.setFont(QFont("Helvetica", 10))
        button.clicked.connect(self.summonWindow)
        button.setFixedSize(QSize(24, 24))
        hStack.addWidget(button)

        self.popupWindow = ChannelPopupWindow(self)

    def summonWindow(self):
        self.popupWindow.show()

    def setGainsEnabledDependingOnScanMode(self):
        enabled = False if self.scanSettingsDetailView.scanModePicker.currentText() == "Initial scan" else True
        self.gainPicker.setEnabled(enabled)

    def sendName(self):
        self.channel.name = self.textEntry.text()
        if self.channel.name != "":
            self.popupWindow.setWindowTitle(self.channel.name)
        else:
            self.popupWindow.setWindowTitle(f"Channel {self.number+1}")

    def setGain(self):
        if self.gainPicker.currentText() == "Disabled":
            self.channel.gain = 0
        else:
            transformedText = list(self.gainPicker.currentText())
            transformedText.pop()
            gain = float(''.join(transformedText))
            self.channel.gain = gain


class ChannelPopupWindow(QMainWindow):
    def __init__(self, channelEntryView: ChannelEntryView):
        super().__init__()
        self.hide()

        self.setWindowTitle(channelEntryView.channel.name)
        self.setFont(QFont("Helvetica", 12))

        self.channelEntryView = channelEntryView
        self.setFixedSize(QSize(400, 300))

        zStack = QStackedLayout()
        zStack.setStackingMode(QStackedLayout.StackingMode.StackAll)

        color = Color(MacColoursDark.bg_colour)
        zStack.addWidget(color)

        vStack = QVBoxLayout()
        vStack.setSpacing(15)

        titleLabel = QLabel("ChannelPopupWindow")
        titleLabel.setFont(QFont("Helvetica", 16))
        vStack.addWidget(titleLabel)
        vStack.addWidget(Divider(MacColoursDark.gray))

        vStack.addStretch()

        vContainer = QWidget(self)
        vContainer.setLayout(vStack)

        zStack.addWidget(vContainer)

        zContainer = QWidget(self)
        zContainer.setLayout(zStack)

        self.setCentralWidget(zContainer)


class InitialScanTopView(QWidget):
    def __init__(self, parent: ScanSettingsDetailView):
        super().__init__(parent)

        self.parent = parent
        self.setFixedHeight(250)

        dummyLayout = QVBoxLayout()
        dummyLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(dummyLayout)

        mainView = QWidget(self)
        mainVStack = QVBoxLayout()
        mainVStack.setSpacing(16)
        mainView.setLayout(mainVStack)

        modeHStack = QHBoxLayout()
        modeHStack.addWidget(QLabel("Operating mode:"))
        modeHStack.addStretch()
        self.modePicker = QComboBox()
        self.modePicker.addItems(["Lissajous curve", "Sine", "Other"])
        self.modePicker.setFixedWidth(200)
        modeHStack.addWidget(self.modePicker)
        mainVStack.addLayout(modeHStack)

        mainVStack.addWidget(Divider(MacColoursDark.gray))

        densityHStack = QHBoxLayout()
        densityHStack.addWidget(QLabel("Curve density [%]:"))
        self.densityStepper = QDoubleSpinBox()
        self.densityStepper.setRange(0, 100)
        self.densityStepper.setSingleStep(0.01)
        densityHStack.addWidget(self.densityStepper)
        mainVStack.addLayout(densityHStack)

        speedHStack = QHBoxLayout()
        speedHStack.addWidget(QLabel("Speed [%]:"))
        self.speedStepper = QDoubleSpinBox()
        self.speedStepper.setRange(0, 100)
        self.speedStepper.setSingleStep(0.01)
        speedHStack.addWidget(self.speedStepper)
        mainVStack.addLayout(speedHStack)

        mainVStack.addStretch()

        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(mainView)

        dummyLayout.addWidget(scrollArea)
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

        nameHStack = QHBoxLayout()
        nameHStack.addWidget(QLabel("Scan name:"))
        nameHStack.addStretch()
        self.nameField = QLineEdit()
        self.nameField.setFixedWidth(360)
        nameHStack.addWidget(self.nameField)

        buttonHStack = QHBoxLayout()
        self.startButton = QPushButton("Start")
        self.startButton.setStyleSheet(f"background-color: rgba{QPalette().accent().color().getRgb()};")
        self.stopButton = QPushButton("Stop")
        self.stopButton.setEnabled(False)
        buttonHStack.addWidget(self.startButton)
        buttonHStack.addWidget(self.stopButton)

        mainVStack.addLayout(nameHStack)
        mainVStack.addStretch()
        mainVStack.addLayout(buttonHStack)

        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(mainView)

        dummyLayout.addWidget(scrollArea)
        self.hide()

        self.startButton.clicked.connect(self.startInitialScan)
        self.stopButton.clicked.connect(self.stopInitialScan)

    def startInitialScan(self):
        self.parent.setInputsEnabled(False)
        self.parent.startInitialScan()

    def stopInitialScan(self):
        self.parent.setInputsEnabled(True)
        self.parent.stopInitialScan()


class RasterModeTopView(QWidget):
    def __init__(self, parent: ScanSettingsDetailView):
        super().__init__(parent)

        self.parent = parent
        self.setFixedHeight(250)

        dummyLayout = QVBoxLayout()
        dummyLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(dummyLayout)

        mainView = QWidget(self)
        mainVStack = QVBoxLayout()
        mainVStack.setSpacing(16)
        mainView.setLayout(mainVStack)

        modeHStack = QHBoxLayout()
        modeHStack.addWidget(QLabel("Operating mode:"))
        modeHStack.addStretch()
        self.modePicker = QComboBox()
        self.modePicker.addItems(["Trigger mode", "Continuous mode"])
        self.modePicker.setFixedWidth(200)
        modeHStack.addWidget(self.modePicker)
        mainVStack.addLayout(modeHStack)

        mainVStack.addWidget(Divider(MacColoursDark.gray))

        traceTimeHStack = QHBoxLayout()
        traceTimeHStack.addWidget(QLabel("Trace time [ms]:"))
        self.traceTimeStepper = QSpinBox()
        self.traceTimeStepper.setRange(1, 1000)
        self.traceTimeStepper.setValue(1)
        traceTimeHStack.addWidget(self.traceTimeStepper)
        mainVStack.addLayout(traceTimeHStack)

        retraceTimeHStack = QHBoxLayout()
        retraceTimeHStack.addWidget(QLabel("Retrace time [ms]:"))
        self.retraceTimeStepper = QSpinBox()
        self.retraceTimeStepper.setRange(1, 1000)
        self.retraceTimeStepper.setValue(1)
        retraceTimeHStack.addWidget(self.retraceTimeStepper)
        mainVStack.addLayout(retraceTimeHStack)

        intervalHStack = QHBoxLayout()
        intervalHStack.addWidget(QLabel("Interval [ms]:"))
        self.intervalStepper = QSpinBox()
        self.intervalStepper.setRange(1, 1000)
        self.intervalStepper.setValue(1)
        intervalHStack.addWidget(self.intervalStepper)
        mainVStack.addLayout(intervalHStack)

        mainVStack.addStretch()

        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(mainView)

        dummyLayout.addWidget(scrollArea)
        self.hide()


class RasterModeBottomView(QWidget):
    def __init__(self, parent: ScanSettingsDetailView):
        super().__init__()

        self.parent = parent

        dummyLayout = QVBoxLayout()
        dummyLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(dummyLayout)

        mainView = QWidget(self)
        mainVStack = QVBoxLayout()
        mainVStack.setSpacing(8)
        mainView.setLayout(mainVStack)

        nameHStack = QHBoxLayout()
        nameHStack.addWidget(QLabel("Scan name:"))
        nameHStack.addStretch()
        self.nameField = QLineEdit()
        self.nameField.setFixedWidth(360)
        nameHStack.addWidget(self.nameField)

        progressHStack = QHBoxLayout()
        progressHStack.addWidget(QLabel("Progress:"))
        progressHStack.addStretch()
        self.progressBar = QProgressBar()
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        self.progressBar.setFixedWidth(360)
        progressHStack.addWidget(self.progressBar)

        buttonHStack = QHBoxLayout()
        self.startButton = QPushButton("Start")
        self.startButton.setStyleSheet(f"background-color: rgba{QPalette().accent().color().getRgb()};")
        self.stopButton = QPushButton("Stop")
        self.stopButton.setEnabled(False)
        buttonHStack.addWidget(self.startButton)
        buttonHStack.addWidget(self.stopButton)

        mainVStack.addLayout(nameHStack)
        mainVStack.addWidget(Divider(MacColoursDark.gray))
        mainVStack.addLayout(progressHStack)
        mainVStack.addStretch()
        mainVStack.addLayout(buttonHStack)

        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(mainView)

        dummyLayout.addWidget(scrollArea)
        self.hide()

        self.startButton.clicked.connect(self.startRasterScan)
        self.stopButton.clicked.connect(self.stopRasterScan)

    def startRasterScan(self):
        self.parent.setInputsEnabled(False)
        self.parent.startRasterScan()

    def stopRasterScan(self):
        self.parent.setInputsEnabled(True)
        self.parent.stopRasterScan()


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

        self.parent = parent

        dummyLayout = QVBoxLayout()
        dummyLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(dummyLayout)

        mainView = QWidget(self)
        mainVStack = QVBoxLayout()
        mainView.setLayout(mainVStack)

        nameHStack = QHBoxLayout()
        nameHStack.addWidget(QLabel("Scan name:"))
        nameHStack.addStretch()
        self.nameField = QLineEdit()
        self.nameField.setFixedWidth(360)
        nameHStack.addWidget(self.nameField)

        buttonHStack = QHBoxLayout()
        self.startButton = QPushButton("Start")
        self.startButton.setStyleSheet(f"background-color: rgba{QPalette().accent().color().getRgb()};")
        self.stopButton = QPushButton("Stop")
        self.stopButton.setEnabled(False)
        buttonHStack.addWidget(self.startButton)
        buttonHStack.addWidget(self.stopButton)

        mainVStack.addLayout(nameHStack)
        mainVStack.addStretch()
        mainVStack.addLayout(buttonHStack)

        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(mainView)

        dummyLayout.addWidget(scrollArea)
        self.hide()

        self.startButton.clicked.connect(self.startHapticScan)
        self.stopButton.clicked.connect(self.stopHapticScan)

    def startHapticScan(self):
        self.parent.setInputsEnabled(False)
        self.parent.startInitialScan()

    def stopHapticScan(self):
        self.parent.setInputsEnabled(True)
        self.parent.stopInitialScan()
