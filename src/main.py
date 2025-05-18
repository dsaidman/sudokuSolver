

# Some gui globals with default widget vals
from PyQt6.QtWidgets import QApplication
from ui.uiMainWindow import AppMainWindow
import sys
import logging
uiLogger = logging.getLogger('uiLogger')

def main():
    FORMAT = '%(levelname)8s %(module)25s->%(funcName)-12s %(message)-30s'
    logging.basicConfig(
        format=FORMAT,
        level=logging.DEBUG)
    uiLogger.info('Starting Application')
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    uiLogger.debug('Setting main window')
    MainWindow = AppMainWindow()
    MainWindow.setupUi()
    MainWindow.resizeApp()

    uiLogger.debug('Showing main window')
    MainWindow.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
