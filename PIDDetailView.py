import time

from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from assets import MacColoursDark
from Color import *
from ServerNeo import *

from logFileAppend import *


class PIDDetailView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.server: ServerNeo = parent.server

        zStack = QStackedLayout()
        zStack.setStackingMode(QStackedLayout.StackingMode.StackAll)

        zStack.addWidget(Color(MacColoursDark.bg_colour))
        vContainer = QWidget()
        vStack = QVBoxLayout()
        vContainer.setLayout(vStack)
        zStack.addWidget(vContainer)
        vStack.setSpacing(20)

        firstSpacer = QWidget()
        firstSpacer.setFixedHeight(7)
        vStack.addWidget(firstSpacer)

        pidLabel = QLabel("PID Controller settings")
        pidLabel.setFont(QFont("Helvetica", 24))
        vStack.addWidget(pidLabel)

        vStack.addWidget(Divider(MacColoursDark.gray))

        gainHStack = QHBoxLayout()

        gainLabelsVStack = QVBoxLayout()
        gainLabelsVStack.addWidget(QLabel("Proportional Gain:"))
        gainLabelsVStack.addWidget(QLabel("Integral Gain:"))
        gainLabelsVStack.addWidget(QLabel("Differential Gain:"))
        gainLabelsVStack.addWidget(QLabel("Setpoint Value:"))
        gainHStack.addLayout(gainLabelsVStack)

        gainInputVStack = QVBoxLayout()
        self.proportionalGainSpinBox = QDoubleSpinBox()
        self.proportionalGainSpinBox.setMinimum(self.server.proportionalGainLowerBound)
        self.proportionalGainSpinBox.setMaximum(self.server.proportionalGainUpperBound)
        self.proportionalGainSpinBox.setSingleStep(0.1)
        self.proportionalGainSpinBox.setFixedWidth(100)
        gainInputVStack.addWidget(self.proportionalGainSpinBox)

        self.integralGainSpinBox = QDoubleSpinBox()
        self.integralGainSpinBox.setMinimum(self.server.integralGainLowerBound)
        self.integralGainSpinBox.setMaximum(self.server.integralGainUpperBound)
        self.integralGainSpinBox.setSingleStep(0.1)
        self.integralGainSpinBox.setFixedWidth(100)
        gainInputVStack.addWidget(self.integralGainSpinBox)

        self.differentialGainSpinBox = QDoubleSpinBox()
        self.differentialGainSpinBox.setMinimum(self.server.differentialGainLowerBound)
        self.differentialGainSpinBox.setMaximum(self.server.differentialGainUpperBound)
        self.differentialGainSpinBox.setSingleStep(0.1)
        self.differentialGainSpinBox.setFixedWidth(100)
        gainInputVStack.addWidget(self.differentialGainSpinBox)

        self.pidSetpointSpinBox = QDoubleSpinBox()
        self.pidSetpointSpinBox.setMinimum(self.server.pidSetpointLowerBound)
        self.pidSetpointSpinBox.setMaximum(self.server.pidSetpointUpperBound)
        self.pidSetpointSpinBox.setSingleStep(0.1)
        self.pidSetpointSpinBox.setFixedWidth(100)
        gainInputVStack.addWidget(self.pidSetpointSpinBox)
        gainHStack.addLayout(gainInputVStack)

        gainSliderVStack = QVBoxLayout()
        self.proportionalGainSlider = QSlider()
        self.proportionalGainSlider.setOrientation(Qt.Orientation.Horizontal)
        self.proportionalGainSlider.setMinimum(0)
        self.proportionalGainSlider.setMaximum(65535)
        self.proportionalGainSlider.setValue(self.server.proportionalGain)
        gainSliderVStack.addWidget(self.proportionalGainSlider)

        self.integralGainSlider = QSlider()
        self.integralGainSlider.setOrientation(Qt.Orientation.Horizontal)
        self.integralGainSlider.setMinimum(0)
        self.integralGainSlider.setMaximum(65535)
        self.integralGainSlider.setValue(self.server.integralGain)
        gainSliderVStack.addWidget(self.integralGainSlider)

        self.differentialGainSlider = QSlider()
        self.differentialGainSlider.setOrientation(Qt.Orientation.Horizontal)
        self.differentialGainSlider.setMinimum(0)
        self.differentialGainSlider.setMaximum(65535)
        self.differentialGainSlider.setValue(self.server.differentialGain)
        gainSliderVStack.addWidget(self.differentialGainSlider)

        self.pidSetpointSlider = QSlider()
        self.pidSetpointSlider.setOrientation(Qt.Orientation.Horizontal)
        self.pidSetpointSlider.setMinimum(0)
        self.pidSetpointSlider.setMaximum(65535)
        self.pidSetpointSlider.setValue(self.server.pidSetpoint)
        gainSliderVStack.addWidget(self.pidSetpointSlider)
        gainHStack.addLayout(gainSliderVStack)

        vStack.addLayout(gainHStack)

        autoHStack = QHBoxLayout()
        autoHStack.addWidget(QLabel("Online PID Setup:"))
        self.isPIDOnlineCheckBox = QCheckBox()
        autoHStack.addStretch()
        autoHStack.addWidget(self.isPIDOnlineCheckBox)

        vStack.addLayout(autoHStack)

        secondSpacer = QWidget()
        secondSpacer.setFixedHeight(0)
        vStack.addWidget(secondSpacer)

        self.showPopupButton = QPushButton("Change PID value ranges")
        vStack.addWidget(self.showPopupButton)

        self.applyGainButton = QPushButton("Save and apply")
        self.applyGainButton.setStyleSheet(f"background-color: rgba{QPalette().accent().color().getRgb()};")
        vStack.addWidget(self.applyGainButton)

        vStack.addWidget(Divider(MacColoursDark.gray))

        self.readoutTimer = QTimer()
        self.readoutTimer.setInterval(250)
        self.readoutTimer.timeout.connect(self.setReadout)

        readoutHStack = QHBoxLayout()
        readoutHStack.addStretch()

        readoutHStack.addWidget(QLabel("CE:"))
        self.CEReadout = QLabel()
        self.CEReadout.setFixedWidth(250)
        readoutHStack.addWidget(self.CEReadout)

        readoutHStack.addStretch()
        readoutHStack.addStretch()

        readoutHStack.addWidget(QLabel("CV:"))
        self.CVReadout = QLabel()
        self.CVReadout.setFixedWidth(250)
        readoutHStack.addWidget(self.CVReadout)

        readoutHStack.addStretch()

        thirdSpacer = QWidget()
        thirdSpacer.setFixedHeight(0)
        vStack.addWidget(thirdSpacer)

        vStack.addLayout(readoutHStack)

        vStack.addStretch()

        self.setLayout(zStack)

        self.proportionalGainSlider.valueChanged.connect(self.syncValuesFromSliders)
        self.integralGainSlider.valueChanged.connect(self.syncValuesFromSliders)
        self.differentialGainSlider.valueChanged.connect(self.syncValuesFromSliders)
        self.pidSetpointSlider.valueChanged.connect(self.syncValuesFromSliders)

        self.applyGainButton.clicked.connect(self.applyGain)

        self.isPIDOnlineCheckBox.clicked.connect(self.blockInputs)

        self.syncValuesFromSliders()
        self.hide()

        self.onlinePIDTimer = QTimer()
        self.onlinePIDTimer.setInterval(500)
        self.onlinePIDTimer.timeout.connect(self.onlinePIDSetup)

        self.popup = PIDPopupWindow(self)
        self.showPopupButton.clicked.connect(self.popup.show)


    def syncValuesFromSliders(self):
        self.proportionalGainSpinBox.setValue(self.proportionalGainSpinBox.minimum() + (self.proportionalGainSpinBox.maximum() - self.proportionalGainSpinBox.minimum()) * self.proportionalGainSlider.value() / 65535)
        self.integralGainSpinBox.setValue(self.integralGainSpinBox.minimum() + (self.integralGainSpinBox.maximum() - self.integralGainSpinBox.minimum()) * self.integralGainSlider.value() / 65535)
        self.differentialGainSpinBox.setValue(self.differentialGainSpinBox.minimum() + (self.differentialGainSpinBox.maximum() - self.differentialGainSpinBox.minimum()) * self.differentialGainSlider.value() / 65535)
        self.pidSetpointSpinBox.setValue(self.pidSetpointSpinBox.minimum() + (self.pidSetpointSpinBox.maximum() - self.pidSetpointSpinBox.minimum()) * self.pidSetpointSlider.value() / 65535)

        self.proportionalGainSpinBox.valueChanged.connect(self.syncValuesFromSpinBoxes)
        self.integralGainSpinBox.valueChanged.connect(self.syncValuesFromSpinBoxes)
        self.differentialGainSpinBox.valueChanged.connect(self.syncValuesFromSpinBoxes)
        self.pidSetpointSpinBox.valueChanged.connect(self.syncValuesFromSpinBoxes)

    def syncValuesFromSpinBoxes(self):
        self.proportionalGainSlider.setValue(int(65535 * (self.proportionalGainSpinBox.value()-self.proportionalGainSpinBox.minimum()) / (self.proportionalGainSpinBox.maximum() - self.proportionalGainSpinBox.minimum())))
        self.integralGainSlider.setValue(int(65535 * (self.integralGainSpinBox.value()-self.integralGainSpinBox.minimum()) / (self.integralGainSpinBox.maximum() - self.integralGainSpinBox.minimum())))
        self.differentialGainSlider.setValue(int(65535 * (self.differentialGainSpinBox.value()-self.differentialGainSpinBox.minimum()) / (self.differentialGainSpinBox.maximum() - self.differentialGainSpinBox.minimum())))
        self.pidSetpointSlider.setValue(int(65535 * (self.pidSetpointSpinBox.value()-self.pidSetpointSpinBox.minimum()) / (self.pidSetpointSpinBox.maximum() - self.pidSetpointSpinBox.minimum())))

    def sendGainToServer(self):
        self.server.proportionalGain = self.proportionalGainSlider.value()
        self.server.integralGain = self.integralGainSlider.value()
        self.server.differentialGain = self.differentialGainSlider.value()
        self.server.pidSetpoint = self.pidSetpointSlider.value()
        self.server.isPIDOnline = self.isPIDOnlineCheckBox.isChecked()

        self.server.proportionalGainLowerBound = self.proportionalGainSpinBox.minimum()
        self.server.integralGainLowerBound = self.integralGainSpinBox.minimum()
        self.server.differentialGainLowerBound = self.differentialGainSpinBox.minimum()
        self.server.pidSetpointLowerBound = self.pidSetpointSpinBox.minimum()

        self.server.proportionalGainUpperBound = self.proportionalGainSpinBox.maximum()
        self.server.integralGainUpperBound = self.integralGainSpinBox.maximum()
        self.server.differentialGainUpperBound = self.differentialGainSpinBox.maximum()
        self.server.pidSetpointUpperBound = self.pidSetpointSpinBox.maximum()

        logFileAppend(self.server.logFile, f"New PID settings applied: Kp: {self.server.proportionalGain} in range ({self.server.proportionalGainLowerBound} ; {self.server.proportionalGainUpperBound}), Ki: {self.server.integralGain} in range ({self.server.integralGainLowerBound} ; {self.server.integralGainUpperBound}), Kd: {self.server.differentialGain} in range ({self.server.differentialGainLowerBound} ; {self.server.differentialGainUpperBound}), pidSetpoint: {self.server.pidSetpoint} in range ({self.server.pidSetpointLowerBound} ; {self.server.pidSetpointUpperBound}), isPIDOnline: {self.server.isPIDOnline}")
        if self.isPIDOnlineCheckBox.isChecked():
            self.onlinePIDTimer.start()
        else:
            self.onlinePIDTimer.stop()

    def applyGain(self):
        self.sendGainToServer()
        self.server.writePIDXML()

    def blockInputs(self):
        self.proportionalGainSlider.setDisabled(self.isPIDOnlineCheckBox.isChecked())
        self.integralGainSlider.setDisabled(self.isPIDOnlineCheckBox.isChecked())
        self.differentialGainSlider.setDisabled(self.isPIDOnlineCheckBox.isChecked())

        self.proportionalGainSpinBox.setDisabled(self.isPIDOnlineCheckBox.isChecked())
        self.integralGainSpinBox.setDisabled(self.isPIDOnlineCheckBox.isChecked())
        self.differentialGainSpinBox.setDisabled(self.isPIDOnlineCheckBox.isChecked())

    def setReadout(self):
        self.CEReadout.setText(str(self.server.getCE()))
        self.CVReadout.setText(str(self.server.getCV()))

    def onlinePIDSetup(self):
        kp, ki, kd = self.server.getOnlinePID()
        self.proportionalGainSlider.setValue(kp)
        self.integralGainSlider.setValue(ki)
        self.differentialGainSlider.setValue(kd)

    def hide(self):
        super().hide()
        self.readoutTimer.stop()

    def show(self):
        super().show()
        self.readoutTimer.start()


class PIDPopupWindow(QMainWindow):
    def __init__(self, summoner: PIDDetailView):
        super().__init__()

        self.setWindowTitle("HapticScanner Neo PID Range Setup")
        self.setFont(QFont("Helvetica", 12))

        self.summoner = summoner
        self.setFixedSize(QSize(400, 300))

        zStack = QStackedLayout()
        zStack.setStackingMode(QStackedLayout.StackingMode.StackAll)

        color = Color(MacColoursDark.bg_colour)
        zStack.addWidget(color)

        vStack = QVBoxLayout()
        vStack.setSpacing(15)

        titleLabel = QLabel("PID Range settings")
        titleLabel.setFont(QFont("Helvetica", 16))
        vStack.addWidget(titleLabel)
        vStack.addWidget(Divider(MacColoursDark.gray))

        mainHStack = QHBoxLayout()
        labelsVStack = QVBoxLayout()
        labelsVStack.addWidget(QLabel("Proportional Gain:"))
        labelsVStack.addWidget(QLabel("Integral Gain:"))
        labelsVStack.addWidget(QLabel("Differential Gain:"))
        labelsVStack.addWidget(QLabel("Setpoint:"))
        mainHStack.addLayout(labelsVStack)

        mainHStack.addStretch()

        fromVStack = QVBoxLayout()
        self.proportionalGainMinDoubleSpinBox = QDoubleSpinBox()
        self.integralGainMinDoubleSpinBox = QDoubleSpinBox()
        self.differentialGainMinDoubleSpinBox = QDoubleSpinBox()
        self.pidSetpointMinDoubleSpinBox = QDoubleSpinBox()

        self.proportionalGainMinDoubleSpinBox.setMinimum(-25.0)
        self.integralGainMinDoubleSpinBox.setMinimum(-25.0)
        self.differentialGainMinDoubleSpinBox.setMinimum(-25.0)
        self.pidSetpointMinDoubleSpinBox.setMinimum(-25.0)

        self.proportionalGainMinDoubleSpinBox.setMaximum(25.0)
        self.integralGainMinDoubleSpinBox.setMaximum(25.0)
        self.differentialGainMinDoubleSpinBox.setMaximum(25.0)
        self.pidSetpointMinDoubleSpinBox.setMaximum(25.0)

        self.proportionalGainMinDoubleSpinBox.setSingleStep(0.1)
        self.integralGainMinDoubleSpinBox.setSingleStep(0.1)
        self.differentialGainMinDoubleSpinBox.setSingleStep(0.1)
        self.pidSetpointMinDoubleSpinBox.setSingleStep(0.1)

        fromVStack.addWidget(self.proportionalGainMinDoubleSpinBox)
        fromVStack.addWidget(self.integralGainMinDoubleSpinBox)
        fromVStack.addWidget(self.differentialGainMinDoubleSpinBox)
        fromVStack.addWidget(self.pidSetpointMinDoubleSpinBox)
        mainHStack.addLayout(fromVStack)

        minusVStack = QVBoxLayout()
        minusVStack.addWidget(QLabel("-"))
        minusVStack.addWidget(QLabel("-"))
        minusVStack.addWidget(QLabel("-"))
        minusVStack.addWidget(QLabel("-"))
        mainHStack.addLayout(minusVStack)

        toVStack = QVBoxLayout()
        self.proportionalGainMaxDoubleSpinBox = QDoubleSpinBox()
        self.integralGainMaxDoubleSpinBox = QDoubleSpinBox()
        self.differentialGainMaxDoubleSpinBox = QDoubleSpinBox()
        self.pidSetpointMaxDoubleSpinBox = QDoubleSpinBox()

        self.proportionalGainMaxDoubleSpinBox.setMinimum(-25.0)
        self.integralGainMaxDoubleSpinBox.setMinimum(-25.0)
        self.differentialGainMaxDoubleSpinBox.setMinimum(-25.0)
        self.pidSetpointMaxDoubleSpinBox.setMinimum(-25.0)

        self.proportionalGainMaxDoubleSpinBox.setMaximum(25.0)
        self.integralGainMaxDoubleSpinBox.setMaximum(25.0)
        self.differentialGainMaxDoubleSpinBox.setMaximum(25.0)
        self.pidSetpointMaxDoubleSpinBox.setMaximum(25.0)

        self.proportionalGainMaxDoubleSpinBox.setSingleStep(0.1)
        self.integralGainMaxDoubleSpinBox.setSingleStep(0.1)
        self.differentialGainMaxDoubleSpinBox.setSingleStep(0.1)
        self.pidSetpointMaxDoubleSpinBox.setSingleStep(0.1)

        toVStack.addWidget(self.proportionalGainMaxDoubleSpinBox)
        toVStack.addWidget(self.integralGainMaxDoubleSpinBox)
        toVStack.addWidget(self.differentialGainMaxDoubleSpinBox)
        toVStack.addWidget(self.pidSetpointMaxDoubleSpinBox)
        mainHStack.addLayout(toVStack)

        vStack.addLayout(mainHStack)
        vStack.addStretch()

        self.applyButton = QPushButton("Apply")
        self.applyButton.setStyleSheet(f"background-color: rgba{QPalette().accent().color().getRgb()};")
        vStack.addWidget(self.applyButton)

        vContainer = QWidget(self)
        vContainer.setLayout(vStack)

        zStack.addWidget(vContainer)

        zContainer = QWidget(self)
        zContainer.setLayout(zStack)

        self.setCentralWidget(zContainer)

        self.applyButton.clicked.connect(self.apply)

        self.proportionalGainMinDoubleSpinBox.valueChanged.connect(self.validateRanges)
        self.integralGainMinDoubleSpinBox.valueChanged.connect(self.validateRanges)
        self.differentialGainMinDoubleSpinBox.valueChanged.connect(self.validateRanges)
        self.pidSetpointMinDoubleSpinBox.valueChanged.connect(self.validateRanges)

        self.proportionalGainMaxDoubleSpinBox.valueChanged.connect(self.validateRanges)
        self.integralGainMaxDoubleSpinBox.valueChanged.connect(self.validateRanges)
        self.differentialGainMaxDoubleSpinBox.valueChanged.connect(self.validateRanges)
        self.pidSetpointMaxDoubleSpinBox.valueChanged.connect(self.validateRanges)

    def apply(self):

        self.summoner.proportionalGainSpinBox.valueChanged.disconnect(self.summoner.syncValuesFromSpinBoxes)
        self.summoner.integralGainSpinBox.valueChanged.disconnect(self.summoner.syncValuesFromSpinBoxes)
        self.summoner.differentialGainSpinBox.valueChanged.disconnect(self.summoner.syncValuesFromSpinBoxes)
        self.summoner.pidSetpointSpinBox.valueChanged.disconnect(self.summoner.syncValuesFromSpinBoxes)

        self.summoner.proportionalGainSpinBox.setMinimum(self.proportionalGainMinDoubleSpinBox.value())
        self.summoner.integralGainSpinBox.setMinimum(self.integralGainMinDoubleSpinBox.value())
        self.summoner.differentialGainSpinBox.setMinimum(self.differentialGainMinDoubleSpinBox.value())
        self.summoner.pidSetpointSpinBox.setMinimum(self.pidSetpointMinDoubleSpinBox.value())

        self.summoner.proportionalGainSpinBox.setMaximum(self.proportionalGainMaxDoubleSpinBox.value())
        self.summoner.integralGainSpinBox.setMaximum(self.integralGainMaxDoubleSpinBox.value())
        self.summoner.differentialGainSpinBox.setMaximum(self.differentialGainMaxDoubleSpinBox.value())
        self.summoner.pidSetpointSpinBox.setMaximum(self.pidSetpointMaxDoubleSpinBox.value())

        self.summoner.syncValuesFromSliders()

        logFileAppend(self.summoner.server.logFile, f"Changed PID value ranges (the changes are local- ServerNeo and config.xml remain unchanged!) Kp: ({self.proportionalGainMinDoubleSpinBox.value()} ; {self.proportionalGainMaxDoubleSpinBox.value()}), Ki: ({self.integralGainMinDoubleSpinBox.value()} ; {self.integralGainMaxDoubleSpinBox.value()}), Kd: ({self.differentialGainMinDoubleSpinBox.value()} ; {self.differentialGainMaxDoubleSpinBox.value()}), Setpoint: ({self.pidSetpointMinDoubleSpinBox.value()} ; {self.pidSetpointMaxDoubleSpinBox.value()})")

    def validateRanges(self):
        mins = [self.proportionalGainMinDoubleSpinBox, self.integralGainMinDoubleSpinBox, self.differentialGainMinDoubleSpinBox, self.pidSetpointMinDoubleSpinBox]
        maxs = [self.proportionalGainMaxDoubleSpinBox, self.integralGainMaxDoubleSpinBox, self.differentialGainMaxDoubleSpinBox, self.pidSetpointMaxDoubleSpinBox]

        for minBox in mins:
            minBox.setValue(round(minBox.value(), 2))
        for maxBox in maxs:
            maxBox.setValue(round(maxBox.value(), 2))

        self.applyButton.setEnabled(True)

        i = 0
        while i < len(mins):
            if mins[i].value() >= maxs[i].value():
                self.applyButton.setEnabled(False)
            i = i + 1

    def show(self):
        super().show()
        self.proportionalGainMinDoubleSpinBox.setValue(self.summoner.proportionalGainSpinBox.minimum())
        self.integralGainMinDoubleSpinBox.setValue(self.summoner.integralGainSpinBox.minimum())
        self.differentialGainMinDoubleSpinBox.setValue(self.summoner.differentialGainSpinBox.minimum())
        self.pidSetpointMinDoubleSpinBox.setValue(self.summoner.pidSetpointSpinBox.minimum())

        self.proportionalGainMaxDoubleSpinBox.setValue(self.summoner.proportionalGainSpinBox.maximum())
        self.integralGainMaxDoubleSpinBox.setValue(self.summoner.integralGainSpinBox.maximum())
        self.differentialGainMaxDoubleSpinBox.setValue(self.summoner.differentialGainSpinBox.maximum())
        self.pidSetpointMaxDoubleSpinBox.setValue(self.summoner.pidSetpointSpinBox.maximum())
