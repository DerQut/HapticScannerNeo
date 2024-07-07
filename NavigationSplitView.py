from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *

import assets
from Color import *


class NavigationSplitView(QWidget):
    def __init__(self, sidebarView: QWidget, detailView: QWidget):
        super().__init__()

        self.isSideBarVisible = True
        self.sidebarView = sidebarView
        self.detailView = detailView

        container = QWidget()

        self.cvHStack = QHBoxLayout()

        self.cvHStack.setContentsMargins(0, 0, 0, 0)
        self.cvHStack.setSpacing(0)

        self.sidebarToggleButton = QPushButton("◀")
        self.sidebarToggleButton.setFixedSize(25, 50)
        self.sidebarToggleButton.clicked.connect(self.toggleSidebar)

        toggleVStack = QVBoxLayout()
        toggleVStack.addWidget(self.sidebarToggleButton)
        toggleVStack.setContentsMargins(0, 0, 0, 0)
        toggleSpacerDown = Color(assets.MacColoursDark.bg_colour)
        toggleSpacerDown.setFixedHeight(800-50)
        toggleVStack.addWidget(toggleSpacerDown)

        self.cvHStack.addWidget(self.sidebarView)
        self.cvHStack.addLayout(toggleVStack)

        self.cvHStack.addWidget(self.detailView)

        self.setLayout(self.cvHStack)

        self.timer = QTimer()
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.animateSidebar)

        self.sidebarToggleButton.setStyleSheet("background-color: rgba(37,38,40,0);")

    def toggleSidebar(self):
        self.isSideBarVisible = not self.isSideBarVisible
        self.sidebarToggleButton.setText("◀" if self.isSideBarVisible else "▶")
        self.timer.start()

    def animateSidebar(self):
        if self.sidebarView.width() != self.isSideBarVisible * 400:
            self.sidebarView.setFixedWidth(self.sidebarView.width()-10+20*self.isSideBarVisible)
        else:
            self.timer.stop()

    def changeDetailView(self, newDetailView: QWidget):
        self.cvHStack.removeWidget(self.detailView)
        self.detailView = newDetailView
        self.cvHStack.addWidget(self.detailView)
        print(newDetailView)
