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
        self.zStack = QStackedLayout()
        self.zStack.addWidget(Color(MacColoursDark.red))
        self.zStack.addWidget(QLabel("Tutaj będzie LogView()"))
        self.zStack.setStackingMode(QStackedLayout.StackingMode.StackAll)

        self.setLayout(self.zStack)
