

# Some gui globals with default widget vals

import sys


def main():
    """
    Main function to start the Sudoku Solver application.
    Initializes the application, sets up the main window, and starts the event loop.
    This function also sets up logging for the application.
    """
    
    # Set up logging
    uiLogger = setup_logging()

    
    from PyQt6.QtWidgets import QApplication
    uiLogger.debug('Importing QApplication from PyQt6.QtWidgets')
    from ui.uiMainWindow import AppMainWindow
    
    uiLogger.info('Starting Application')
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    MainWindow = AppMainWindow()
    uiLogger.debug('AppMainWindow initialized')
    MainWindow.show()

    sys.exit(app.exec())

def setup_logging():
    """
    Set up logging configuration for the application.
    """
    import logging
    FORMAT = '%(levelname)8s %(module)25s->%(funcName)-12s %(message)-30s'
    logging.basicConfig(
        format=FORMAT,
        level=logging.INFO,
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    uiLogger = logging.getLogger('uiLogger')
    uiLogger.debug('Logging is set up')
    return uiLogger

if __name__ == "__main__":
    main()
