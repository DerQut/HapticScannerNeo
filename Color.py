from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QStackedLayout, QHBoxLayout, QVBoxLayout, QStackedWidget


class Color(QWidget):
    def __init__(self, color: tuple):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color[0], color[1], color[2]))
        self.setPalette(palette)


class Divider(Color):
    def __init__(self, color: tuple):
        super().__init__(color)
        self.setFixedHeight(1)
