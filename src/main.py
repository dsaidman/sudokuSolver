

# Some gui globals with default widget vals
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from ui.uiMainWindow import AppMainWindow
import sys


if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    MainWindow = AppMainWindow()
    MainWindow.setupUi()
    MainWindow.resizeApp()
    MainWindow.show()

    sys.exit(app.exec())
