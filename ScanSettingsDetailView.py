from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

import pyqtgraph as pg
import numpy as np

from assets import MacColoursDark
from Color import *

from ServerNeo import *
from ScanChannel import *
import os


# Improve load time by disabling ChannelEntryView.popupWindow
NEODEBUG = False

class ScanSettingsDetailView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent

        self.timer = QTimer()
        self.timer.timeout.connect(self.pollServerStatus)
        self.timer.setInterval(250)

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

        #self.initialScanTopView.modePicker.setEnabled(enabled)
        #self.initialScanTopView.densityStepper.setEnabled(enabled)
        #self.initialScanTopView.speedStepper.setEnabled(enabled)

        self.rasterModeBottomView.nameField.setEnabled(enabled)
        self.rasterModeBottomView.startButton.setEnabled(enabled)
        self.rasterModeBottomView.stopButton.setEnabled(not enabled)

        #self.rasterModeTopView.modePicker.setEnabled(enabled)
        #self.rasterModeTopView.traceTimeStepper.setEnabled(enabled)
        #self.rasterModeTopView.retraceTimeStepper.setEnabled(enabled)
        #self.rasterModeTopView.intervalStepper.setEnabled(enabled)

        self.hapticModeBottomView.nameField.setEnabled(enabled)
        self.hapticModeBottomView.startButton.setEnabled(enabled)
        self.hapticModeBottomView.stopButton.setEnabled(not enabled)

        if self.scanModePicker.currentText() == "Initial scan":
            return 0

        for channelEntryView in self.channelsView.channelEntryViews:
            channelEntryView.gainPicker.setEnabled(enabled)

    def pollServerStatus(self):
        if self.server.getBusy():
            self.setInputsEnabled(False)
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
            "0.25x",
            "0.5x",
            "1x",
            "2x",
            "4x",
            "8x",
            "16x"
        ])

        self.setGainsEnabledDependingOnScanMode()

        if self.channel.gain() < 1:
            self.gainPicker.setCurrentText(f"{self.channel.gain()}x" if self.channel.gain() > 0 else "Disabled")
        else:
            self.gainPicker.setCurrentText(f"{int(self.channel.gain())}x")

        self.gainPicker.setCurrentText(f"{self.channel.gain()}x" if self.channel.gain() < 1 else f"{int(self.channel.gain())}x")
        self.gainPicker.currentIndexChanged.connect(self.setChannelGain)
        hStack.addWidget(self.gainPicker)

        self.enabledToggle = QCheckBox()
        self.enabledToggle.setChecked(self.channel.enabled())
        self.enabledToggle.clicked.connect(self.setChannelEnabled)
        hStack.addWidget(self.enabledToggle)

        self.textEntry = QLineEdit(self.channel.name())
        self.textEntry.textChanged.connect(self.sendName)
        hStack.addWidget(self.textEntry)
        self.textEntry.setFixedWidth(125)

        hStack.addStretch()

        button = QPushButton("⧉")
        button.setFont(QFont("Helvetica", 10))
        button.clicked.connect(self.summonWindow)
        button.setFixedSize(QSize(24, 24))
        hStack.addWidget(button)

        self.popupWindow = None
        if not NEODEBUG:
            self.popupWindow = ChannelPopupWindow(self)

    def summonWindow(self):
        if not NEODEBUG:
            self.popupWindow.show()

    def setGainsEnabledDependingOnScanMode(self):
        enabled = False if self.scanSettingsDetailView.scanModePicker.currentText() == "Initial scan" else True
        self.gainPicker.setEnabled(enabled)

    def sendName(self):
        if NEODEBUG:
            return

        self.channel.setName(self.textEntry.text())
        if self.channel.name() != "":
            self.popupWindow.setWindowTitle(self.channel.name())
            self.popupWindow.plot.setTitle(self.channel.name())
        else:
            self.popupWindow.setWindowTitle(f"Channel {self.number+1}")
            self.popupWindow.plot.setTitle(f"Channel {self.number+1}")

    def setChannelGain(self):
        transformedText = list(self.gainPicker.currentText())
        transformedText.pop()
        gain = float(''.join(transformedText))
        self.channel.setGain(gain)

    def setChannelEnabled(self):
        self.channel.setEnabled(bool(self.enabledToggle.isChecked()))


class ChannelPopupWindow(QMainWindow):
    def __init__(self, channelEntryView: ChannelEntryView):

        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.rePlot)
        self.timer.start()

        super().__init__()
        self.hide()

        self.setWindowTitle(channelEntryView.channel.name())
        self.setFont(QFont("Helvetica", 12))

        self.channelEntryView = channelEntryView
        self.setFixedSize(QSize(400, 400))

        zStack = QStackedLayout()
        zStack.setStackingMode(QStackedLayout.StackingMode.StackAll)

        color = Color(MacColoursDark.bg_colour)
        zStack.addWidget(color)

        vStack = QVBoxLayout()
        vStack.setSpacing(15)

        self.plot = pg.plot()
        self.plot.setBackground(MacColoursDark.bg_colour)
        self.plot.setTitle(self.channelEntryView.channel.name(), color="white", size="16pt")
        self.plot.setLabel("bottom", "x", color="white")
        self.plot.setLabel("left", "y", color="white")

        vStack.addWidget(self.plot)

        vContainer = QWidget(self)
        vContainer.setLayout(vStack)

        zStack.addWidget(vContainer)

        zContainer = QWidget(self)
        zContainer.setLayout(zStack)

        self.setCentralWidget(zContainer)

        self.channelEntryView.scanSettingsDetailView.parent.windowsToKillIfNeeded.append(self)

    def rePlot(self):
        self.plot.clear()

        if self.channelEntryView.channel.enabled():
            self.channelEntryView.channel.randomize()

        points = self.channelEntryView.channel.scanPoints
        spots = []
        for point in points:
            spot = {"symbol": "s", "pos": (point[0], point[1]), "size": 1, 'pen': {'color': (0, 0, 0, 0), 'width': 0},
                    'brush': (point[2], point[2], point[2])}
            spots.append(spot)

        scatter = pg.ScatterPlotItem(pxMode=False)
        scatter.addPoints(spots)
        self.plot.addItem(scatter)

    def hide(self):
        self.timer.stop()
        super().hide()

    def show(self):
        super().show()
        self.timer.start()

    def closeEvent(self, a0):
        self.timer.stop()


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
        self.modePicker.currentTextChanged.connect(self.sendInitialScanOperatingMode)
        self.modePicker.setFixedWidth(180)
        modeHStack.addWidget(self.modePicker)
        mainVStack.addLayout(modeHStack)

        mainVStack.addWidget(Divider(MacColoursDark.gray))

        densityHStack = QHBoxLayout()
        densityHStack.addWidget(QLabel("Curve density [%]:"))
        self.densityStepper = QDoubleSpinBox()
        self.densityStepper.setRange(0, 100)
        self.densityStepper.valueChanged.connect(self.sendInitialScanCurveDensity)
        self.densityStepper.setSingleStep(0.01)
        densityHStack.addWidget(self.densityStepper)
        mainVStack.addLayout(densityHStack)

        speedHStack = QHBoxLayout()
        speedHStack.addWidget(QLabel("Speed [%]:"))
        self.speedStepper = QDoubleSpinBox()
        self.speedStepper.valueChanged.connect(self.sendInitialScanSpeed)
        self.speedStepper.setRange(0, 100)
        self.speedStepper.setSingleStep(0.01)
        speedHStack.addWidget(self.speedStepper)
        mainVStack.addLayout(speedHStack)

        mainVStack.addStretch()

        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(mainView)

        dummyLayout.addWidget(scrollArea)

        self.sendInitialScanCurveDensity()
        self.sendInitialScanSpeed()
        self.sendInitialScanOperatingMode()

        self.hide()

    def sendInitialScanOperatingMode(self):
        self.parent.server.setInitialScanOperatingMode(self.modePicker.currentText())

    def sendInitialScanCurveDensity(self):
        self.parent.server.setInitialScanCurveDensity(self.densityStepper.value())

    def sendInitialScanSpeed(self):
        self.parent.server.setInitialScanSpeed(self.speedStepper.value())


class InitialScanBottomView(QWidget):
    def __init__(self, parent: ScanSettingsDetailView):
        super().__init__(parent)

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
        self.modePicker.addItems(["Trigger", "Continuous"])
        self.modePicker.currentTextChanged.connect(self.sendRasterModeOperatingMode)
        self.modePicker.setFixedWidth(180)
        modeHStack.addWidget(self.modePicker)
        mainVStack.addLayout(modeHStack)

        mainVStack.addWidget(Divider(MacColoursDark.gray))

        traceTimeHStack = QHBoxLayout()
        traceTimeHStack.addWidget(QLabel("Trace time [ms]:"))
        self.traceTimeStepper = QSpinBox()
        self.traceTimeStepper.setRange(1, 1000)
        self.traceTimeStepper.valueChanged.connect(self.sendRasterModeTraceTime)
        self.traceTimeStepper.setValue(1)
        traceTimeHStack.addWidget(self.traceTimeStepper)
        mainVStack.addLayout(traceTimeHStack)

        retraceTimeHStack = QHBoxLayout()
        retraceTimeHStack.addWidget(QLabel("Retrace time [ms]:"))
        self.retraceTimeStepper = QSpinBox()
        self.retraceTimeStepper.setRange(1, 1000)
        self.retraceTimeStepper.valueChanged.connect(self.sendRasterModeRetraceTime)
        self.retraceTimeStepper.setValue(1)
        retraceTimeHStack.addWidget(self.retraceTimeStepper)
        mainVStack.addLayout(retraceTimeHStack)

        intervalHStack = QHBoxLayout()
        intervalHStack.addWidget(QLabel("Interval [ms]:"))
        self.intervalStepper = QSpinBox()
        self.intervalStepper.setRange(1, 1000)
        self.intervalStepper.valueChanged.connect(self.sendRasterModeInterval)
        self.intervalStepper.setValue(1)
        intervalHStack.addWidget(self.intervalStepper)
        mainVStack.addLayout(intervalHStack)

        mainVStack.addStretch()

        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(mainView)

        dummyLayout.addWidget(scrollArea)

        self.sendRasterModeTraceTime()
        self.sendRasterModeRetraceTime()
        self.sendRasterModeOperatingMode()
        self.sendRasterModeInterval()

        self.hide()

    def sendRasterModeOperatingMode(self):
        self.parent.server.setRasterModeOperatingMode(self.modePicker.currentText())

    def sendRasterModeTraceTime(self):
        self.parent.server.setRasterModeTraceTime(self.traceTimeStepper.value())

    def sendRasterModeRetraceTime(self):
        self.parent.server.setRasterModeRetraceTime(self.retraceTimeStepper.value())

    def sendRasterModeInterval(self):
        self.parent.server.setRasterModeInterval(self.intervalStepper.value())


class RasterModeBottomView(QWidget):
    def __init__(self, parent: ScanSettingsDetailView):
        super().__init__()

        self.parent = parent
        self.timer = QTimer()
        self.timer.setInterval(250)

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

        statsVStack = QVBoxLayout()
        statsVStack.setSpacing(8)

        speedLHStack = QHBoxLayout()
        speedLHStack.addWidget(QLabel("Scan speed (L) [lines/s]:"))
        speedLHStack.addStretch()
        self.speedLReadout = QLabel("0")
        speedLHStack.addWidget(self.speedLReadout)
        statsVStack.addLayout(speedLHStack)

        speedRHStack = QHBoxLayout()
        speedRHStack.addWidget(QLabel("Scan speed (R) [lines/s]:"))
        speedRHStack.addStretch()
        self.speedRReadout = QLabel("0")
        speedRHStack.addWidget(self.speedRReadout)
        statsVStack.addLayout(speedRHStack)

        avgTimeHStack = QHBoxLayout()
        avgTimeHStack.addWidget(QLabel("Average time between lines [s]:"))
        avgTimeHStack.addStretch()
        self.avgTimeReadout = QLabel("0")
        avgTimeHStack.addWidget(self.avgTimeReadout)
        statsVStack.addLayout(avgTimeHStack)

        totalTimeHStack = QHBoxLayout()
        totalTimeHStack.addWidget(QLabel("Total scan duration [s]:"))
        totalTimeHStack.addStretch()
        self.totalTimeReadout = QLabel("0")
        totalTimeHStack.addWidget(self.totalTimeReadout)
        statsVStack.addLayout(totalTimeHStack)

        mainVStack.addLayout(nameHStack)
        mainVStack.addWidget(Divider(MacColoursDark.gray))
        mainVStack.addLayout(progressHStack)
        mainVStack.addWidget(Divider(MacColoursDark.gray))
        mainVStack.addLayout(statsVStack)
        mainVStack.addStretch()
        mainVStack.addWidget(QWidget())
        mainVStack.addLayout(buttonHStack)

        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(mainView)

        dummyLayout.addWidget(scrollArea)
        self.hide()

        self.startButton.clicked.connect(self.startRasterScan)
        self.stopButton.clicked.connect(self.stopRasterScan)
        self.timer.timeout.connect(self.pollStats)

    def startRasterScan(self):
        self.parent.setInputsEnabled(False)
        self.parent.startRasterScan()

    def stopRasterScan(self):
        self.parent.setInputsEnabled(True)
        self.parent.stopRasterScan()

    def pollStats(self):
        if not self.parent.server.getBusy():
            return -1

        self.progressBar.setValue(self.parent.server.getRasterProgress())
        self.avgTimeReadout.setText(str(self.parent.server.getAvgRasterTime()))
        self.totalTimeReadout.setText(str(self.parent.server.getTotalRasterTime()))
        self.speedRReadout.setText(str(self.parent.server.getRasterRSpeed()))
        self.speedLReadout.setText(str(self.parent.server.getRasterLSpeed()))

    def show(self):
        self.timer.start()
        super().show()

    def hide(self):
        self.timer.stop()
        super().hide()


class HapticModeTopView(QWidget):
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
        modeLabelVStack = QVBoxLayout()
        modeLabelVStack.addWidget(QLabel("Operating mode:"))
        modeLabelVStack.addStretch()
        modeHStack.addLayout(modeLabelVStack)
        modeHStack.addStretch()
        pickerVStack = QVBoxLayout()

        self.modePicker1 = QComboBox()
        self.modePicker1.addItems(["Trigger", "Continuous"])
        self.modePicker1.currentTextChanged.connect(self.sendOperatingMode1)
        self.modePicker1.setFixedWidth(180)
        pickerVStack.addWidget(self.modePicker1)

        self.modePicker2 = QComboBox()
        self.modePicker2.addItems(["Cycloid", "Other", "Off"])
        self.modePicker2.currentTextChanged.connect(self.sendOperatingMode2)
        self.modePicker2.setFixedWidth(180)
        pickerVStack.addWidget(self.modePicker2)

        self.modePicker3 = QComboBox()
        self.modePicker3.addItems(["Free mover", "Follower"])
        self.modePicker3.currentTextChanged.connect(self.sendOperatingMode3)
        self.modePicker3.setFixedWidth(180)
        pickerVStack.addWidget(self.modePicker3)

        modeHStack.addLayout(pickerVStack)
        mainVStack.addLayout(modeHStack)

        mainVStack.addWidget(Divider(MacColoursDark.gray))

        widthHStack = QHBoxLayout()
        widthHStack.addWidget(QLabel("Scan width:"))
        self.widthStepper = QSpinBox()
        self.widthStepper.setRange(1, 10000)
        self.widthStepper.valueChanged.connect(self.sendScanWidth)
        self.widthStepper.setValue(1)
        widthHStack.addWidget(self.widthStepper)
        mainVStack.addLayout(widthHStack)

        speedHStack = QHBoxLayout()
        speedHStack.addWidget(QLabel("Tip speed:"))
        self.speedStepper = QSpinBox()
        self.speedStepper.setRange(1, 10000)
        self.speedStepper.valueChanged.connect(self.sendTipSpeed)
        self.speedStepper.setValue(1)
        speedHStack.addWidget(self.speedStepper)
        mainVStack.addLayout(speedHStack)

        oversamplingHStack = QHBoxLayout()
        oversamplingHStack.addWidget(QLabel("Oversampling points:"))
        self.oversamplingStepper = QSpinBox()
        self.oversamplingStepper.setRange(1, 10000)
        self.oversamplingStepper.valueChanged.connect(self.sendOversamplingPoints)
        self.oversamplingStepper.setValue(10)
        self.oversamplingStepper.setEnabled(False)
        oversamplingHStack.addWidget(self.oversamplingStepper)
        mainVStack.addLayout(oversamplingHStack)

        mainVStack.addStretch()

        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(mainView)

        dummyLayout.addWidget(scrollArea)

        self.sendOperatingMode1()
        self.sendOperatingMode2()
        self.sendOperatingMode3()
        self.sendScanWidth()
        self.sendTipSpeed()
        self.sendOversamplingPoints()

        self.hide()

    def sendOperatingMode1(self):
        self.parent.server.setHapticModeOperatingMode1(self.modePicker1.currentText())

    def sendOperatingMode2(self):
        self.parent.server.setHapticModeOperatingMode2(self.modePicker2.currentText())

    def sendOperatingMode3(self):
        self.parent.server.setHapticModeOperatingMode3(self.modePicker3.currentText())

    def sendScanWidth(self):
        self.parent.server.setHapticModeScanWidth(self.widthStepper.value())

    def sendTipSpeed(self):
        self.parent.server.setHapticModeTipSpeed(self.speedStepper.value())

    def sendOversamplingPoints(self):
        self.parent.server.setHapticModeOversamplingPoints(self.oversamplingStepper.value())


class HapticModeBottomView(QWidget):
    def __init__(self, parent: ScanSettingsDetailView):
        super().__init__(parent)

        self.parent = parent

        self.timer = QTimer()
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.pollTimes)

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

        buttonHStack = QHBoxLayout()
        self.startButton = QPushButton("Start")
        self.startButton.setStyleSheet(f"background-color: rgba{QPalette().accent().color().getRgb()};")
        self.stopButton = QPushButton("Stop")
        self.stopButton.setEnabled(False)
        buttonHStack.addWidget(self.startButton)
        buttonHStack.addWidget(self.stopButton)

        mainVStack.addLayout(nameHStack)
        mainVStack.addWidget(Divider(MacColoursDark.gray))

        readoutVStack = QVBoxLayout()
        avgTimeHStack = QHBoxLayout()
        avgTimeHStack.addWidget(QLabel("Average time between points [s]:"))
        avgTimeHStack.addStretch()
        self.avgTimeReadout = QLabel("0.00")
        avgTimeHStack.addWidget(self.avgTimeReadout)
        readoutVStack.addLayout(avgTimeHStack)

        totalTimeHStack = QHBoxLayout()
        totalTimeHStack.addWidget(QLabel("Total scan duration [s]:"))
        totalTimeHStack.addStretch()
        self.totalTimeReadout = QLabel("00:00:00")
        totalTimeHStack.addWidget(self.totalTimeReadout)
        readoutVStack.addLayout(totalTimeHStack)

        mainVStack.addLayout(readoutVStack)

        mainVStack.addWidget(Divider(MacColoursDark.gray))

        mainVStack.addWidget(QLabel("Haptic feedback options:"))
        feedbackHStack = QHBoxLayout()
        self.forceToggle = QCheckBox("Force")
        self.forceToggle.clicked.connect(self.sendForceFeedback)
        feedbackHStack.addWidget(self.forceToggle)
        feedbackHStack.addStretch()

        self.vibrationsToggle = QCheckBox("Vibrations")
        self.vibrationsToggle.clicked.connect(self.sendVibrationsFeedback)
        feedbackHStack.addWidget(self.vibrationsToggle)
        feedbackHStack.addStretch()

        self.heatToggle = QCheckBox("Heat")
        self.heatToggle.clicked.connect(self.sendHeatFeedback)
        feedbackHStack.addWidget(self.heatToggle)
        feedbackHStack.addStretch()

        self.LEDToggle = QCheckBox("LED")
        self.LEDToggle.clicked.connect(self.sendLEDFeedback)
        feedbackHStack.addWidget(self.LEDToggle)

        mainVStack.addLayout(feedbackHStack)

        mainVStack.addStretch()
        mainVStack.addLayout(buttonHStack)

        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(mainView)

        dummyLayout.addWidget(scrollArea)
        self.hide()

        self.startButton.clicked.connect(self.startHapticScan)
        self.stopButton.clicked.connect(self.stopHapticScan)

        self.sendForceFeedback()
        self.sendVibrationsFeedback()
        self.sendHeatFeedback()
        self.sendLEDFeedback()

    def startHapticScan(self):
        self.parent.setInputsEnabled(False)
        self.parent.startHapticScan()

    def stopHapticScan(self):
        self.parent.setInputsEnabled(True)
        self.parent.stopHapticScan()

    def pollTimes(self):
        if not self.parent.server.getBusy():
            return -1

        avgTime = self.parent.server.getAvgHapticTime()
        totTime = self.parent.server.getTotalHapticTime()

        self.avgTimeReadout.setText(str(avgTime))
        self.totalTimeReadout.setText(str(totTime))

    def sendHeatFeedback(self):
        self.parent.server.setHapticModeHeatFeedback(self.heatToggle.isChecked())

    def sendLEDFeedback(self):
        self.parent.server.setHapticModeLEDFeedback(self.LEDToggle.isChecked())

    def sendVibrationsFeedback(self):
        self.parent.server.setHapticModeVibrationsFeedback(self.vibrationsToggle.isChecked())

    def sendForceFeedback(self):
        self.parent.server.setHapticModeForceFeedback(self.forceToggle.isChecked())

    def hide(self):
        self.timer.stop()
        super().hide()

    def show(self):
        self.timer.start()
        super().show()
