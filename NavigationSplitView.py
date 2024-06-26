from PyQt6.QtCore import QSize, Qt
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

        cvZtack = QStackedLayout()
        cvHStack = QHBoxLayout()

        cvHStack.addWidget(sidebarView)
        cvHStack.addWidget(detailView)

        cvHStack.setContentsMargins(0, 0, 0, 0)
        cvHStack.setSpacing(0)

        container.setLayout(cvHStack)

        cvZtack.addWidget(bgColor)
        cvZtack.addWidget(container)
        cvZtack.setStackingMode(QStackedLayout.StackingMode.StackAll)

        self.sidebarToggleButton = QPushButton("D")
        self.sidebarToggleButton.setFixedSize(QSize(72, 72))
        self.sidebarToggleButton.clicked.connect(self.toggleSidebar)
        cvZtack.addWidget(self.sidebarToggleButton)

        self.setLayout(cvZtack)

    def toggleSidebar(self):
        self.isSideBarVisible = not self.isSideBarVisible
        self.sidebarView.setFixedSize(QSize(self.isSideBarVisible * 400, 800))
        #self.detailView.setFixedWidth(800 + 400*self.isSideBarVisible)
