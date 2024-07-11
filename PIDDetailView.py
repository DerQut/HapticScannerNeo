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

        self.proportionalGain = self.server.proportionalGain
        self.integralGain = self.server.integralGain
        self.differentialGain = self.server.differentialGain

        self.proportionalGainLowerBound = self.server.proportionalGainLowerBound
        self.integralGainLowerBound = self.server.integralGainLowerBound
        self.differentialGainLowerBound = self.server.differentialGainLowerBound

        self.proportionalGainUpperBound = self.server.proportionalGainUpperBound
        self.integralGainUpperBound = self.server.integralGainUpperBound
        self.differentialGainUpperBound = self.server.differentialGainUpperBound

        self.isPIDOnline = self.server.isPIDOnline
        self.pidSetpoint = self.server.pidSetpoint

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
        self.proportionalGainSpinBox.setMinimum(self.proportionalGainLowerBound)
        self.proportionalGainSpinBox.setMaximum(self.proportionalGainUpperBound)
        self.proportionalGainSpinBox.setSingleStep(0.1)
        gainInputVStack.addWidget(self.proportionalGainSpinBox)

        self.integralGainSpinBox = QDoubleSpinBox()
        self.integralGainSpinBox.setMinimum(self.integralGainLowerBound)
        self.integralGainSpinBox.setMaximum(self.integralGainUpperBound)
        self.integralGainSpinBox.setSingleStep(0.1)
        gainInputVStack.addWidget(self.integralGainSpinBox)

        self.differentialGainSpinBox = QDoubleSpinBox()
        self.differentialGainSpinBox.setMinimum(self.differentialGainLowerBound)
        self.differentialGainSpinBox.setMaximum(self.differentialGainUpperBound)
        self.differentialGainSpinBox.setSingleStep(0.1)
        gainInputVStack.addWidget(self.differentialGainSpinBox)

        self.pidSetpointSpinBox = QDoubleSpinBox()
        self.pidSetpointSpinBox.setMinimum(-10.0)
        self.pidSetpointSpinBox.setMaximum(10.0)
        self.pidSetpointSpinBox.setSingleStep(0.1)
        gainInputVStack.addWidget(self.pidSetpointSpinBox)
        gainHStack.addLayout(gainInputVStack)

        gainSliderVStack = QVBoxLayout()
        self.proportionalGainSlider = QSlider()
        self.proportionalGainSlider.setOrientation(Qt.Orientation.Horizontal)
        self.proportionalGainSlider.setMinimum(0)
        self.proportionalGainSlider.setMaximum(65535)
        gainSliderVStack.addWidget(self.proportionalGainSlider)

        self.integralGainSlider = QSlider()
        self.integralGainSlider.setOrientation(Qt.Orientation.Horizontal)
        self.integralGainSlider.setMinimum(0)
        self.integralGainSlider.setMaximum(65535)
        gainSliderVStack.addWidget(self.integralGainSlider)

        self.differentialGainSlider = QSlider()
        self.differentialGainSlider.setOrientation(Qt.Orientation.Horizontal)
        self.differentialGainSlider.setMinimum(0)
        self.differentialGainSlider.setMaximum(65535)
        gainSliderVStack.addWidget(self.differentialGainSlider)

        self.pidSetpointSlider = QSlider()
        self.pidSetpointSlider.setOrientation(Qt.Orientation.Horizontal)
        self.pidSetpointSlider.setMinimum(0)
        self.pidSetpointSlider.setMaximum(65535)
        gainSliderVStack.addWidget(self.pidSetpointSlider)
        gainHStack.addLayout(gainSliderVStack)

        vStack.addLayout(gainHStack)

        autoHStack = QHBoxLayout()
        autoHStack.addWidget(QLabel("Automatic PID Setup:"))
        self.isPIDOnlineCheckBox = QCheckBox()
        self.isPIDOnlineCheckBox.setChecked(self.isPIDOnline)
        autoHStack.addStretch()
        autoHStack.addWidget(self.isPIDOnlineCheckBox)

        vStack.addLayout(autoHStack)

        self.applyGainButton = QPushButton("Apply")
        vStack.addWidget(self.applyGainButton)

        vStack.addStretch()

        self.setLayout(zStack)

        self.proportionalGainSpinBox.valueChanged.connect(self.syncValuesFromSpinBoxes)
        self.integralGainSpinBox.valueChanged.connect(self.syncValuesFromSpinBoxes)
        self.differentialGainSpinBox.valueChanged.connect(self.syncValuesFromSpinBoxes)
        self.pidSetpointSpinBox.valueChanged.connect(self.syncValuesFromSpinBoxes)

        self.proportionalGainSlider.valueChanged.connect(self.syncValuesFromSliders)
        self.integralGainSlider.valueChanged.connect(self.syncValuesFromSliders)
        self.differentialGainSlider.valueChanged.connect(self.syncValuesFromSliders)
        self.pidSetpointSlider.valueChanged.connect(self.syncValuesFromSliders)

        self.applyGainButton.clicked.connect(self.applyGain)

        self.proportionalGainSlider.setValue(self.proportionalGain)
        self.integralGainSlider.setValue(self.integralGain)
        self.differentialGainSlider.setValue(self.differentialGain)
        self.pidSetpointSpinBox.setValue(self.pidSetpoint)

        self.isPIDOnlineCheckBox.clicked.connect(self.isPIDOnlineToggle)

        self.syncValuesFromSliders()
        self.hide()

    def syncValuesFromSliders(self):
        self.proportionalGain = self.proportionalGainSlider.value()
        self.integralGain = self.integralGainSlider.value()
        self.differentialGain = self.differentialGainSlider.value()

        self.proportionalGainSpinBox.setValue(self.proportionalGainLowerBound + self.proportionalGain * (self.proportionalGainUpperBound - self.proportionalGainLowerBound) / 65535)
        self.integralGainSpinBox.setValue(self.integralGainLowerBound + self.integralGain * (self.integralGainUpperBound - self.integralGainLowerBound) / 65535)
        self.differentialGainSpinBox.setValue(self.differentialGainLowerBound + self.differentialGain * (self.differentialGainUpperBound - self.differentialGainLowerBound) / 65535)
        self.pidSetpointSpinBox.setValue(-10 + self.pidSetpointSlider.value() * (10 + 10) / 65535)

        self.pidSetpoint = self.pidSetpointSpinBox.value()

    def syncValuesFromSpinBoxes(self):
        self.proportionalGainSlider.setValue(int(65535 * (self.proportionalGainSpinBox.value()-self.proportionalGainLowerBound) / (self.proportionalGainUpperBound - self.proportionalGainLowerBound)))
        self.integralGainSlider.setValue(int(65535 * (self.integralGainSpinBox.value()-self.integralGainLowerBound) / (self.integralGainUpperBound - self.integralGainLowerBound)))
        self.differentialGainSlider.setValue(int(65535 * (self.differentialGainSpinBox.value()-self.differentialGainLowerBound) / (self.differentialGainUpperBound - self.differentialGainLowerBound)))

        self.pidSetpointSlider.setValue(int(65535 * (self.pidSetpointSpinBox.value()+10) / (10 + 10)))

        self.proportionalGain = self.proportionalGainSlider.value()
        self.integralGain = self.integralGainSlider.value()
        self.differentialGain = self.differentialGainSlider.value()
        self.pidSetpoint = self.pidSetpointSpinBox.value()


    def sendGainToServer(self):
        self.server.proportionalGain = self.proportionalGain
        self.server.integralGain = self.integralGain
        self.server.differentialGain = self.differentialGain
        self.server.pidSetpoint = self.pidSetpoint
        self.server.isPIDOnline = self.isPIDOnline

        logFileAppend(self.server.logFile, f"New PID settings applied: Kp: {self.proportionalGain}, Ki: {self.integralGain}, Kd: {self.differentialGain}, pidSetpoint: {self.pidSetpoint}, isPIDOnline: {self.isPIDOnline}")

    def applyGain(self):
        self.sendGainToServer()
        pidFile = open("pid.txt", "w+")
        pidFile.write(f"""# PID GAINS
{self.proportionalGain}
{self.integralGain}
{self.differentialGain}
# PID LOWER BOUNDARIES
{self.proportionalGainLowerBound}
{self.integralGainLowerBound}
{self.differentialGainLowerBound}
#PID UPPER BOUNDARIES
{self.proportionalGainUpperBound}
{self.integralGainUpperBound}
{self.differentialGainUpperBound}
# PID SETPOINT
{self.pidSetpoint}
# PID ONLINE
{int(self.isPIDOnline)}""")
        pidFile.close()

    def isPIDOnlineToggle(self):
        self.isPIDOnline = self.isPIDOnlineCheckBox.isChecked()
        print(self.isPIDOnline)
