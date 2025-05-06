from functools import lru_cache
from math import floor
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QWidget, QFrame, QMainWindow, QSizePolicy, QStyle, QStatusBar
from PyQt6.QtCore import Qt, QMetaObject, QSize
from PyQt6.QtGui import QGuiApplication, QFont, QIcon, QPixmap
from .uiEnums import AppStatusEnum
from .uiPuzzleComponents import PuzzleFrame
from .uiControlComponents import UiPanel
from pySolver.py2lua import luaPy as sudokuDefs
from .uiMenuComponents import MenuBar
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

    def setupUi(self):

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


        theSizePolicy = QSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding)
        theSizePolicy.setVerticalStretch(0)
        theSizePolicy.setHorizontalStretch(0)
        theSizePolicy.setHeightForWidth(False)
        self.setSizePolicy(theSizePolicy)

        # Master Layout
        masterLayout = QVBoxLayout()
        masterLayout.setParent(self.centralWidget)
        masterLayout.setObjectName('masterLayout')
        self.centralWidget.setLayout(masterLayout)

        # Title Label
        self.titleLabel = QLabel()
        self.titleLabel.setParent(self.centralWidget)
        self.titleLabel.setAutoFillBackground(True)
        self.titleLabel.setFrameShadow(QFrame.Shadow.Raised)
        self.titleLabel.setText("Sudoku Solver")
        self.titleLabel.setScaledContents(True)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setStyleSheet("background-color: rgb(100,100,100);")
        self.setContentsMargins(0, 0, 0, 0)

        titleFont = QFont()
        titleFont.setBold(True)
        titleFont.setPointSize(14)
        titleFont.setFamily("Lucida Console")
        self.titleLabel.setFont(titleFont)

        self.puzzleFrame = PuzzleFrame(self.centralWidget)
        self.uiFrame = UiPanel(self.centralWidget)

        # make master layout widget for nestthig the layouts
        masterLayout.insertWidget(0, self.titleLabel)
        masterLayout.insertWidget(1, self.puzzleFrame)
        masterLayout.insertWidget(2, self.uiFrame)

        self.titleLabel.raise_()
        self.uiFrame.raise_()
        self.puzzleFrame.raise_()

        self.setCentralWidget(self.centralWidget)
        self.menuBar = MenuBar(self)

        self.uiStatusBar = self.statusBar()
        self.uiStatusBar.showMessage('A1')

        w = self.windowHandle()
        self.retranslateUi(self)
        QMetaObject.connectSlotsByName(self)

    def resizeApp(self):

        _height, _width = getScreenSize()

        self.resize(
            int(floor(float(_height)/6)),
            floor(int(float(_width)/12)))

    def orderTabs(self):
        for idx in range(len(sudokuDefs.squares)-1):
            QMainWindow.setTabOrder(
                self.puzzleFrame.squares[sudokuDefs.squares[idx]],
                self.puzzleFrame.squares[sudokuDefs.squares[idx+1]])
        QMainWindow.setTabOrder(
            self.puzzleFrame.squares[sudokuDefs.squares[-1]],
            self.puzzleFrame.squares[sudokuDefs.squares[0]])

    def retranslateUi(self, MainWindow):
        pass


@lru_cache(typed=False)
def getScreenSize():
    cp = QGuiApplication.primaryScreen().availableGeometry().size()
    return cp.height(), cp.width()
