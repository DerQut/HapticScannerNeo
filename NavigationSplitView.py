from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *

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

        self.timer = QTimer()
        self.timer.setInterval(4)
        self.timer.timeout.connect(self.animateSidebar)

    def toggleSidebar(self):
        self.isSideBarVisible = not self.isSideBarVisible
        self.timer.start()

    def animateSidebar(self):
        if self.sidebarView.width() != self.isSideBarVisible * 400:
            self.sidebarView.setFixedWidth(self.sidebarView.width()-10+20*self.isSideBarVisible)
        else:
            self.timer.stop()
