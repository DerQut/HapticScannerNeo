from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QStackedLayout

from NavigationSplitView import *
from SidebarView import *
from DetailView import *

from ServerNeo import *


class ContentView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.server = ServerNeo()

        self.sidebarView = SidebarView(self)
        self.detailView = DetailView(self)
        self.nsv = NavigationSplitView(self, self.sidebarView, self.detailView)

        self.setCentralWidget(self.nsv)

        # Set the central widget of the Window.
        self.setFixedHeight(800)
        self.setFixedWidth(1200)
