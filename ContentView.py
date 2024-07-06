from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QStackedLayout

from NavigationSplitView import *
from SidebarView import *
from DetailView import *


class ContentView(QMainWindow):
    def __init__(self):
        super().__init__()

        nv = NavigationSplitView(sidebarView=SidebarView(), detailView=DetailView())

        self.setCentralWidget(nv)

        # Set the central widget of the Window.
        self.setFixedHeight(800)
        self.setFixedWidth(1200)
