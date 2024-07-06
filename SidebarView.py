from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *

import assets
from assets import MacColoursDark
from Color import *


class SidebarView(QWidget):
    def __init__(self, color=MacColoursDark.side_bar_inactive_colour):
        super().__init__()

        zStack = QStackedLayout()
        vStack = QVBoxLayout()
        vContainer = QWidget()
        vContainer.setLayout(vStack)

        mainLabel = QLabel("HapticScannerNeo")
        mainLabel.setFont(QFont("Helvetica", 28))
        vStack.addWidget(mainLabel)

        vStack.addWidget(Divider(assets.MacColoursDark.gray))

        spacer = QWidget()
        spacer.setFixedSize(1, 640)
        vStack.addWidget(spacer)

        bgColor = Color(color)
        zStack.addWidget(bgColor)
        zStack.addWidget(vContainer)
        zStack.setStackingMode(QStackedLayout.StackingMode.StackAll)

        vStack.setSpacing(0)
        self.setLayout(zStack)

        self.setFixedSize(QSize(400, 800))
