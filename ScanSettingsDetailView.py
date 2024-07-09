from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from assets import MacColoursDark
from Color import *


class ScanSettingsDetailView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        vStack = QVBoxLayout()
        vStack.setContentsMargins(0, 0, 0, 0)
        vStack.setSpacing(0)
        self.setLayout(vStack)

        vStack.addWidget(Color(MacColoursDark.purple))
