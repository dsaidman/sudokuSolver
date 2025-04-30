

# Some gui globals with default widget vals
from PyQt5.QtWidgets import QApplication
from ui.uiMainWindow import AppMainWindow
import qdarktheme, sys
_fontFamily = 'Verdana'


if __name__ == "__main__":

    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    

    qdarktheme.setup_theme("auto")
    app.setStyle('Fusion')
    MainWindow = AppMainWindow()
    MainWindow.setupUi()
    MainWindow.show()
    
    sys.exit(app.exec_())
