from PyQt6.QtCore import QSize, Qt, QPropertyAnimation, QRect
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QStackedLayout, QHBoxLayout, QVBoxLayout, QStackedWidget

from Color import *


class NavigationSplitView(QWidget):
    def __init__(self, sidebarView: QWidget, detailView: QWidget):
        super().__init__()

        self.isSideBarVisible = True
        self.sidebarView = sidebarView
        self.detailView = detailView

        bgColor = Color((0, 0, 0))

        container = QWidget()

        cvZStack = QStackedLayout()
        cvHStack = QHBoxLayout()

        cvHStack.addWidget(self.sidebarView)
        cvHStack.addWidget(self.detailView)

        cvHStack.setContentsMargins(0, 0, 0, 0)
        cvHStack.setSpacing(0)

        container.setLayout(cvHStack)

        cvZStack.addWidget(bgColor)
        cvZStack.addWidget(container)
        cvZStack.setStackingMode(QStackedLayout.StackingMode.StackAll)

        self.sidebarToggleButton = QPushButton("=")
        self.sidebarToggleButton.setFixedSize(QSize(32, 32))
        self.sidebarToggleButton.clicked.connect(self.toggleSidebar)
        cvZStack.addWidget(self.sidebarToggleButton)

        self.setLayout(cvZStack)

    def toggleSidebar(self):

        self.detailView.setFixedWidth(800 + 400 * self.isSideBarVisible)

        self.isSideBarVisible = not self.isSideBarVisible

        self.sidebarView.setFixedSize(QSize(self.isSideBarVisible * 400, 800))
