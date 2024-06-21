from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QStackedLayout, QHBoxLayout, QVBoxLayout, QStackedWidget

from assets import MacColoursDark
from Color import *


class SidebarView(QWidget):
    def __init__(self, color=MacColoursDark.side_bar_inactive_colour):
        super().__init__()

        ZStack = QStackedLayout()

        bgColor = Color(color)
        ZStack.addWidget(bgColor)

        self.setLayout(ZStack)

        self.setFixedSize(QSize(400, 800))
