from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *

import assets
from assets import MacColoursDark
from Color import *


class LogView(QWidget):
    def __init__(self):
        super().__init__()
        self.vStack = QVBoxLayout()

        self.vStack.setContentsMargins(0, 0, 0, 0)
        self.vStack.setSpacing(0)
        self.vStack.addWidget(Color(MacColoursDark.red))

        self.setLayout(self.vStack)
