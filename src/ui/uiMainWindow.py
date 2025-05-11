
from PyQt6.QtWidgets import QWidget, QMainWindow, QSizePolicy, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, QMetaObject
from PyQt6.QtGui import QIcon, QPixmap, QGuiApplication
from .uiMainPanelComponents import UiMainPanel
from .uiStatusBarComponents import PuzzleInfoLabel
from .uiMenuComponents import MenuBar
from .uiHelpers import grabWidget, grabPuzzleFrame
from .uiEnums import AppStatusEnum
from functools import lru_cache
from math import floor
import inspect, os


class AppMainWindow(QMainWindow):

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, statusVal):
        self._status = statusVal
        return statusVal

    def __init__(self):
        super(AppMainWindow, self).__init__()

        self.setObjectName("MainWindow")
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.setWindowTitle("SudokuSolverApp")

        filename = inspect.getframeinfo(inspect.currentframe()).filename
        path     = os.path.dirname(os.path.abspath(filename))
        iconpath = os.path.join(os.path.dirname(os.path.dirname(path)),'res','icon.ico')

        appIcon = QIcon()
        appIcon.addPixmap(QPixmap(iconpath), QIcon.Mode.Normal, QIcon.State.Off)
        self.setWindowIcon(appIcon)
        self._status = AppStatusEnum.Unlocked

        self.centralWidget = QWidget()
        self.centralWidget.setObjectName("centralWidget")
        self.setCentralWidget(self.centralWidget)

        self.masterAppLayout = QHBoxLayout()
        self.masterAppLayout.setObjectName('masterAppLayout')
        self.centralWidget.setLayout( self.masterAppLayout)

        self.setStyleSheet("QWidget {font-family: 'Segoe ui';}");

        '''
        theSizePolicy = QSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding)
        theSizePolicy.setVerticalStretch(0)
        theSizePolicy.setHorizontalStretch(0)
        theSizePolicy.setHeightForWidth(False)
        self.setSizePolicy(theSizePolicy)
        '''

    def setupUi(self):

        self.uiMainPanel = UiMainPanel(self)
        self.masterAppLayout.addWidget(self.uiMainPanel)

        self.uiStatusBar = self.statusBar()
        self.uiStatusBar.setObjectName('uiStatusBar')
        self.uiStatusBar.showMessage('Starting Up')
        self.uiStatusBar.puzzleInfoLabel = PuzzleInfoLabel(self.uiStatusBar)
        self.uiStatusBar.addPermanentWidget(self.uiStatusBar.puzzleInfoLabel)

        
        self.menuBar = MenuBar(self)

        QMetaObject.connectSlotsByName(self)

    def _resetMainWindow(self):
        self.uiStatusBar.puzzleInfoLabel.reset()
        self.uiMainPanel.puzzleFrame.resetPuzzle()
        grabWidget(QLabel, 'infoDisplayLabel')._resetAction()
        grabWidget(QPushButton, 'setPuzzleBtn')._disableMe()
        

    def _updateWindow(self):
        self.uiStatusBar.puzzleInfoLabel.update()
        grabPuzzleFrame().onSquareChangeEvent()
        

    
    def resizeApp(self):

        _height, _width = getScreenSize()

        self.resize(
            int(floor(float(_height)/6)),
            floor(int(float(_width)/12)))

@lru_cache(typed=False)
def getScreenSize():
    cp = QGuiApplication.primaryScreen().availableGeometry().size()
    return cp.height(), cp.width()