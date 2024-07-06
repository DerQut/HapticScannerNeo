import sys

import PyQt6
from PyQt6.QtWidgets import QApplication, QWidget

from ContentView import *


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Helvetica", 16))

    contentView = ContentView()
    contentView.show()

    contentView.setWindowTitle("HapticScannerNeo")

    app.setStyle("fusion")

    app.exec()

    return 0


if __name__ == "__main__":
    main()
