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

        # TODO: CE and CV readout (Cross-Entropy? or like the Error? idk and Control Variable, which is the output of the PID summator)

        # Honestly idc I'm not touching any of that

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
        gainInputVStack.addWidget(self.proportionalGainSpinBox)

        self.integralGainSpinBox = QDoubleSpinBox()
        self.integralGainSpinBox.setMinimum(self.server.integralGainLowerBound)
        self.integralGainSpinBox.setMaximum(self.server.integralGainUpperBound)
        self.integralGainSpinBox.setSingleStep(0.1)
        gainInputVStack.addWidget(self.integralGainSpinBox)

        self.differentialGainSpinBox = QDoubleSpinBox()
        self.differentialGainSpinBox.setMinimum(self.server.differentialGainLowerBound)
        self.differentialGainSpinBox.setMaximum(self.server.differentialGainUpperBound)
        self.differentialGainSpinBox.setSingleStep(0.1)
        gainInputVStack.addWidget(self.differentialGainSpinBox)

        self.pidSetpointSpinBox = QDoubleSpinBox()
        self.pidSetpointSpinBox.setMinimum(self.server.pidSetpointLowerBound)
        self.pidSetpointSpinBox.setMaximum(self.server.pidSetpointUpperBound)
        self.pidSetpointSpinBox.setSingleStep(0.1)
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
        autoHStack.addWidget(QLabel("Automatic PID Setup:"))
        self.isPIDOnlineCheckBox = QCheckBox()
        autoHStack.addStretch()
        autoHStack.addWidget(self.isPIDOnlineCheckBox)

        vStack.addLayout(autoHStack)

        self.applyGainButton = QPushButton("Apply")
        vStack.addWidget(self.applyGainButton)

        vStack.addStretch()

        self.setLayout(zStack)

        self.proportionalGainSlider.valueChanged.connect(self.syncValuesFromSliders)
        self.integralGainSlider.valueChanged.connect(self.syncValuesFromSliders)
        self.differentialGainSlider.valueChanged.connect(self.syncValuesFromSliders)
        self.pidSetpointSlider.valueChanged.connect(self.syncValuesFromSliders)

        self.applyGainButton.clicked.connect(self.applyGain)

        self.syncValuesFromSliders()
        self.hide()

    def syncValuesFromSliders(self):
        self.proportionalGainSpinBox.setValue(self.server.proportionalGainLowerBound + (self.server.proportionalGainUpperBound - self.server.proportionalGainLowerBound) * self.proportionalGainSlider.value() / 65535)
        self.integralGainSpinBox.setValue(self.server.integralGainLowerBound + (self.server.integralGainUpperBound - self.server.integralGainLowerBound) * self.integralGainSlider.value() / 65535)
        self.differentialGainSpinBox.setValue(self.server.differentialGainLowerBound + (self.server.differentialGainUpperBound - self.server.differentialGainLowerBound) * self.differentialGainSlider.value() / 65535)
        self.pidSetpointSpinBox.setValue(self.server.pidSetpointLowerBound + (self.server.pidSetpointUpperBound - self.server.pidSetpointLowerBound) * self.pidSetpointSlider.value() / 65535)

        self.proportionalGainSpinBox.valueChanged.connect(self.syncValuesFromSpinBoxes)
        self.integralGainSpinBox.valueChanged.connect(self.syncValuesFromSpinBoxes)
        self.differentialGainSpinBox.valueChanged.connect(self.syncValuesFromSpinBoxes)
        self.pidSetpointSpinBox.valueChanged.connect(self.syncValuesFromSpinBoxes)

    def syncValuesFromSpinBoxes(self):
        self.proportionalGainSlider.setValue(int(65535 * (self.proportionalGainSpinBox.value()-self.server.proportionalGainLowerBound) / (self.server.proportionalGainUpperBound - self.server.proportionalGainLowerBound)))
        self.integralGainSlider.setValue(int(65535 * (self.integralGainSpinBox.value()-self.server.integralGainLowerBound) / (self.server.integralGainUpperBound - self.server.integralGainLowerBound)))
        self.differentialGainSlider.setValue(int(65535 * (self.differentialGainSpinBox.value()-self.server.differentialGainLowerBound) / (self.server.differentialGainUpperBound - self.server.differentialGainLowerBound)))
        self.pidSetpointSlider.setValue(int(65535 * (self.pidSetpointSpinBox.value()-self.server.pidSetpointLowerBound) / (self.server.pidSetpointUpperBound - self.server.pidSetpointLowerBound)))

    def sendGainToServer(self):
        self.server.proportionalGain = self.proportionalGainSlider.value()
        self.server.integralGain = self.integralGainSlider.value()
        self.server.differentialGain = self.differentialGainSlider.value()
        self.server.pidSetpoint = self.pidSetpointSlider.value()
        self.server.isPIDOnline = self.isPIDOnlineCheckBox.isChecked()

        logFileAppend(self.server.logFile, f"New PID settings applied: Kp: {self.server.proportionalGain}, Ki: {self.server.integralGain}, Kd: {self.server.differentialGain}, pidSetpoint: {self.server.pidSetpoint}, isPIDOnline: {self.server.isPIDOnline}")

    def applyGain(self):

        self.sendGainToServer()
        self.server.writePIDXML()
