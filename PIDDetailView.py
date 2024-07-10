from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from assets import MacColoursDark
from Color import *
from ServerNeo import *


class PIDDetailView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # TODO: Three numeric inputs (Kp, Ki, Kd) with ranges of 0-65535? gotta ask the doctor
        # TODO: Manual vs Online exclusive checkbox (what does it do?)
        # TODO: CE and CV readout (Cross-Entropy? or like the Error? idk and Control Variable, which is the output of the PID summator)
        # TODO Setpoint numeric input (from -10V to +10V? yes.)

        # Honestly idc I'm not touching any of that

        self.server: ServerNeo = parent.server

        self.proportionalGain = self.server.proportionalGain
        self.integralGain = self.server.integralGain
        self.differentialGain = self.server.differentialGain

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

        gainLabel = QLabel("Gain Settings")
        gainLabel.setFont(QFont("Helvetica", 20))
        vStack.addWidget(gainLabel)

        gainHStack = QHBoxLayout()

        gainLabelsVStack = QVBoxLayout()
        gainLabelsVStack.addWidget(QLabel("Proportional Gain:"))
        gainLabelsVStack.addWidget(QLabel("Integral Gain:"))
        gainLabelsVStack.addWidget(QLabel("Differential Gain:"))
        gainHStack.addLayout(gainLabelsVStack)

        gainInputVStack = QVBoxLayout()
        self.proportionalGainSpinBox = QSpinBox()
        self.proportionalGainSpinBox.setMinimum(1)
        self.proportionalGainSpinBox.setMaximum(65535)
        gainInputVStack.addWidget(self.proportionalGainSpinBox)

        self.integralGainSpinBox = QSpinBox()
        self.integralGainSpinBox.setMinimum(1)
        self.integralGainSpinBox.setMaximum(65535)
        gainInputVStack.addWidget(self.integralGainSpinBox)

        self.differentialGainSpinBox = QSpinBox()
        self.differentialGainSpinBox.setMinimum(1)
        self.differentialGainSpinBox.setMaximum(65535)
        gainInputVStack.addWidget(self.differentialGainSpinBox)
        gainHStack.addLayout(gainInputVStack)

        gainSliderVStack = QVBoxLayout()
        self.proportionalGainSlider = QSlider()
        self.proportionalGainSlider.setOrientation(Qt.Orientation.Horizontal)
        self.proportionalGainSlider.setMinimum(1)
        self.proportionalGainSlider.setMaximum(65535)
        gainSliderVStack.addWidget(self.proportionalGainSlider)

        self.integralGainSlider = QSlider()
        self.integralGainSlider.setOrientation(Qt.Orientation.Horizontal)
        self.integralGainSlider.setMinimum(1)
        self.integralGainSlider.setMaximum(65535)
        gainSliderVStack.addWidget(self.integralGainSlider)

        self.differentialGainSlider = QSlider()
        self.differentialGainSlider.setOrientation(Qt.Orientation.Horizontal)
        self.differentialGainSlider.setMinimum(1)
        self.differentialGainSlider.setMaximum(65535)
        gainSliderVStack.addWidget(self.differentialGainSlider)
        gainHStack.addLayout(gainSliderVStack)

        vStack.addLayout(gainHStack)

        self.applyGainButton = QPushButton("Apply")
        vStack.addWidget(self.applyGainButton)

        vStack.addStretch()

        self.setLayout(zStack)

        self.proportionalGainSpinBox.valueChanged.connect(self.syncValuesFromSpinBoxes)
        self.integralGainSpinBox.valueChanged.connect(self.syncValuesFromSpinBoxes)
        self.differentialGainSpinBox.valueChanged.connect(self.syncValuesFromSpinBoxes)

        self.proportionalGainSlider.valueChanged.connect(self.syncValuesFromSliders)
        self.integralGainSlider.valueChanged.connect(self.syncValuesFromSliders)
        self.differentialGainSlider.valueChanged.connect(self.syncValuesFromSliders)

        self.applyGainButton.clicked.connect(self.applyGain)

        self.hide()

    def syncValuesFromSliders(self):
        spinBoxes = [self.proportionalGainSpinBox, self.integralGainSpinBox, self.differentialGainSpinBox]
        sliders = [self.proportionalGainSlider, self.integralGainSlider, self.differentialGainSlider]

        i = 0
        while i < len(sliders):
            spinBoxes[i].setValue(sliders[i].value())
            i = i + 1

    def syncValuesFromSpinBoxes(self):
        spinBoxes = [self.proportionalGainSpinBox, self.integralGainSpinBox, self.differentialGainSpinBox]
        sliders = [self.proportionalGainSlider, self.integralGainSlider, self.differentialGainSlider]

        i = 0
        while i < len(spinBoxes):
            sliders[i].setValue(spinBoxes[i].value())
            i = i + 1

    def sendGainToServer(self):
        self.server.proportionalGain = self.proportionalGain
        self.server.integralGain = self.integralGain
        self.server.differentialGain = self.differentialGain

        print(f"Kp={self.server.proportionalGain}, Ki={self.server.integralGain}, Kd={self.server.differentialGain}")

    def applyGain(self):
        self.proportionalGain = self.proportionalGainSpinBox.value()
        self.integralGain = self.integralGainSpinBox.value()
        self.differentialGain = self.differentialGainSpinBox.value()
        self.sendGainToServer()
        pidFile = open("pid.txt", "w+")
        pidFile.write(f"""{self.proportionalGain}
{self.integralGain}
{self.differentialGain}""")
        pidFile.close()
