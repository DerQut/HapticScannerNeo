from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *

import assets
from Color import *
from DetailView import DetailView
from LogView import LogView

from SidebarView import SidebarView


class NavigationSplitView(QWidget):
    def __init__(self, parent, sidebarView, detailView):
        super().__init__(parent)

        self.isSideBarVisible = True
        self.isLogViewVisible = True
        self.sidebarView = sidebarView
        self.detailView = detailView
        self.logView = LogView()
        self.logView.setFixedHeight(100)

        self.cvHStack = QHBoxLayout()

        self.cvHStack.setContentsMargins(0, 0, 0, 0)
        self.cvHStack.setSpacing(0)

        self.sidebarToggleButton = QPushButton("◀")
        self.sidebarToggleButton.setFixedSize(25, 50)
        self.sidebarToggleButton.clicked.connect(self.toggleSidebar)

        sidebarToggleVStack = QVBoxLayout()
        sidebarToggleVStack.addWidget(self.sidebarToggleButton)
        sidebarToggleVStack.setContentsMargins(0, 0, 0, 0)
        sidebarToggleSpacerDown = Color(assets.MacColoursDark.bg_colour)
        sidebarToggleSpacerDown.setFixedHeight(800 - 50)
        sidebarToggleVStack.addWidget(sidebarToggleSpacerDown)

        self.cvHStack.addWidget(self.sidebarView)
        self.cvHStack.addLayout(sidebarToggleVStack)

        self.dvVStack = QVBoxLayout()
        self.dvVStack.setContentsMargins(0, 0, 0, 0)
        self.dvVStack.setSpacing(0)
        self.dvVStack.addWidget(self.detailView)

        self.logToggleButton = QPushButton("▼")
        self.logToggleButton.setFixedSize(50, 25)
        self.logToggleButton.clicked.connect(self.toggleLog)

        logToggleHStack = QHBoxLayout()
        logToggleHStack.setContentsMargins(0, 0, 0, 0)
        logToggleHStack.setSpacing(0)
        self.logToggleSpacerLeft = Color(assets.MacColoursDark.bg_colour)
        self.logToggleSpacerLeft.setFixedWidth(800-50)
        logToggleHStack.addWidget(self.logToggleSpacerLeft)
        logToggleHStack.addWidget(self.logToggleButton)
        self.dvVStack.addLayout(logToggleHStack)
        self.dvVStack.addWidget(self.logView)

        self.cvHStack.addLayout(self.dvVStack)

        self.setLayout(self.cvHStack)

        self.sidebarTimer = QTimer()
        self.sidebarTimer.setInterval(1)
        self.sidebarTimer.timeout.connect(self.animateSidebar)

        self.logTimer = QTimer()
        self.logTimer.setInterval(1)
        self.logTimer.timeout.connect(self.animateLog)

        self.sidebarToggleButton.setStyleSheet("background-color: rgba(37,38,40,0);")
        self.logToggleButton.setStyleSheet("background-color: rgba(37,38,40,0);")

        #######

    def toggleSidebar(self):
        self.isSideBarVisible = not self.isSideBarVisible
        self.sidebarToggleButton.setText("◀" if self.isSideBarVisible else "▶")
        self.sidebarTimer.start()

    def toggleLog(self):
        self.isLogViewVisible = not self.isLogViewVisible
        self.logToggleButton.setText("▼" if self.isLogViewVisible else "▲")
        self.logTimer.start()

    def animateSidebar(self):
        if self.sidebarView.width() != self.isSideBarVisible * 400:
            self.sidebarView.setFixedWidth(self.sidebarView.width()-10+20*self.isSideBarVisible)
            self.logToggleSpacerLeft.setFixedWidth(self.logToggleSpacerLeft.width()+10-20*self.isSideBarVisible)
        else:
            self.sidebarTimer.stop()

    def animateLog(self):
        if self.logView.height() != self.isLogViewVisible * 100:
            self.logView.setFixedHeight(self.logView.height()-5+10*self.isLogViewVisible)
        else:
            self.logTimer.stop()

    def changeDetailView(self, newDetailView: QWidget):
        self.dvVStack.replaceWidget(self.detailView, newDetailView)
        self.detailView = newDetailView
