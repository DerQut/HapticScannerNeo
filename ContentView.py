from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QStackedLayout

from NavigationSplitView import *
from SidebarView import *
from DetailView import *


class ContentView(QMainWindow):
    def __init__(self):
        super().__init__()

        sidebarView = SidebarView(self)
        self.nsv = NavigationSplitView(sidebarView, detailView=DetailView())

        self.setCentralWidget(self.nsv)

        # Set the central widget of the Window.
        self.setFixedHeight(800)
        self.setFixedWidth(1200)
