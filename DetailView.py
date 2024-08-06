from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from assets import MacColoursDark
from Color import *


class DetailView(QWidget):

    def __init__(self, parent, color=MacColoursDark.bg_colour):
        super().__init__(parent)

        zStack = QStackedLayout()

        vStack = QVBoxLayout()
        logField = QLabel("Welcome to HapticScannerNeo! - Marcel Chołodecki")
        logField.setWordWrap(True)
        vStack.addWidget(logField)

        container = QWidget()
        container.setLayout(vStack)

        bgColor = Color(color)
        zStack.addWidget(bgColor)
        zStack.addWidget(container)
        zStack.setStackingMode(QStackedLayout.StackingMode.StackAll)

        self.setLayout(zStack)

