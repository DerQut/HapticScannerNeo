from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from assets import MacColoursDark
from Color import *


class DetailView(QWidget):

    def __init__(self, color=MacColoursDark.bg_colour):
        super().__init__()

        zStack = QStackedLayout()

        vStack = QVBoxLayout()
        logField = QLabel("hej")
        logField.setWordWrap(True)
        vStack.addWidget(logField)

        container = QWidget()
        container.setLayout(vStack)

        bgColor = Color(color)
        zStack.addWidget(bgColor)
        zStack.addWidget(container)
        zStack.setStackingMode(QStackedLayout.StackingMode.StackAll)

        self.setLayout(zStack)

