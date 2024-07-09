from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from assets import MacColoursDark
from Color import *


class PIDDetailView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # TODO: Three numeric inputs (Kp, Ki, Kd) with ranges of 0-65535? gotta ask the doctor
        # TODO: Manual vs Online exclusive checkbox (what does it do?)
        # TODO: CE and CV readout (Cross-Entropy? or like the Error? idk and Control Variable, which is the output of the PID summator)
        # TODO Setpoint numeric input (from -10V to +10V?)

        vStack = QVBoxLayout()
        vStack.setContentsMargins(0, 0, 0, 0)
        vStack.setSpacing(0)
        self.setLayout(vStack)

        vStack.addWidget(Color(MacColoursDark.green))

        self.hide()
