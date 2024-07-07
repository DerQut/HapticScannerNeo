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

        # cvHStack.addWidget(self.sidebarView)
        cvHStack.addWidget(self.detailView)

        cvHStack.setContentsMargins(0, 0, 0, 0)
        cvHStack.setSpacing(0)

        container.setLayout(cvHStack)

        cvZStack.addWidget(bgColor)
        cvZStack.addWidget(container)
        cvZStack.setStackingMode(QStackedLayout.StackingMode.StackAll)

        toggleHStack = QHBoxLayout()
        self.toggleSpacerRight = QWidget()
        self.toggleSpacerRight.setFixedSize(800 - 25, 1)
        self.sidebarToggleButton = QPushButton("<")
        self.sidebarToggleButton.setFixedSize(25, 50)
        self.sidebarToggleButton.clicked.connect(self.toggleSidebar)

        toggleVStack = QVBoxLayout()
        toggleVStack.addWidget(self.sidebarToggleButton)
        toggleVStack.setContentsMargins(0, 0, 0, 0)
        toggleSpacerDown = QWidget()
        toggleSpacerDown.setFixedSize(1, 800-50)
        toggleVStack.addWidget(toggleSpacerDown)

        toggleHStack.addWidget(self.sidebarView)
        toggleHStack.addLayout(toggleVStack)
        toggleHStack.addWidget(self.toggleSpacerRight)
        toggleHStack.setSpacing(0)
        toggleHStack.setContentsMargins(0, 0, 0, 0)

        toggleContainer = QWidget()
        toggleContainer.setLayout(toggleHStack)

        cvZStack.addWidget(toggleContainer)

        self.setLayout(cvZStack)

        self.timer = QTimer()
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.animateSidebar)

        self.sidebarToggleButton.setStyleSheet("background-color: rgba(37,38,40,0);")

    def toggleSidebar(self):
        self.isSideBarVisible = not self.isSideBarVisible
        self.sidebarToggleButton.setText("<" if self.isSideBarVisible else ">")
        self.timer.start()

    def animateSidebar(self):
        if self.sidebarView.width() != self.isSideBarVisible * 400:
            self.sidebarView.setFixedWidth(self.sidebarView.width()-10+20*self.isSideBarVisible)
            self.toggleSpacerRight.setFixedWidth(self.toggleSpacerRight.width() + 10 - 20 * self.isSideBarVisible)
        else:
            self.timer.stop()
