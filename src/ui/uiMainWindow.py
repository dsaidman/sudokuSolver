from functools import lru_cache
from math import floor
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QWidget, QGridLayout, QFrame, QApplication, QMainWindow
from PyQt6.QtCore import Qt, QMetaObject
from PyQt6.QtGui import QGuiApplication
from .uiEnums import AppStatusEnum
from .uiPuzzleComponents import PuzzleFrame
from .uiControlComponents import UiPanel
from pySolver.py2lua import luaPy as sudokuDefs
from .uiMenuComponents import MenuBar

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
        self.setDockNestingEnabled(True)
        self._status = AppStatusEnum.Unlocked
        self.resizeApp()

        self.centralWidget = QWidget(parent=self)
        self.centralWidget.setObjectName("centralWidget")

        # Master Layout
        masterLayout = QVBoxLayout()
        masterLayout.setParent(self.centralWidget)
        masterLayout.setObjectName('masterLayout')

        self.centralWidget.setLayout(masterLayout)
        anotherLayout = QGridLayout()
        anotherLayout.setSpacing(0)
        anotherLayout.setContentsMargins(0, 0, 0, 0)
        masterLayout.addLayout(anotherLayout)

        # Title Label
        self.titleLabel = QLabel(self.centralWidget)
        self.titleLabel.setAutoFillBackground(True)
        self.titleLabel.setFrameShadow(QFrame.Shadow.Plain)
        self.titleLabel.setText("Sudoku Solver")
        self.titleLabel.setScaledContents(True)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setStyleSheet("font-size: 14pt; font-weight: bold")
        anotherLayout.addWidget(self.titleLabel, 0, 0,
                                alignment=Qt.AlignmentFlag.AlignVCenter)
        self.puzzleFrame = PuzzleFrame(self.centralWidget)
        self.uiFrame = UiPanel(self.centralWidget)
        # make master layout widget for nestthig the layouts
        anotherLayout.addWidget(self.titleLabel, 0, 0,
                                alignment=Qt.AlignmentFlag.AlignVCenter)
        masterLayout.addWidget(self.puzzleFrame,
                               alignment=Qt.AlignmentFlag.AlignVCenter)
        masterLayout.addWidget(self.uiFrame,
                               alignment=Qt.AlignmentFlag.AlignVCenter)
        self.uiFrame.raise_()
        self.puzzleFrame.raise_()
        self.titleLabel.raise_()
        self.setCentralWidget(self.centralWidget)
        self.menuBar = MenuBar(self)
        w = self.windowHandle()
        self.retranslateUi(self)
        QMetaObject.connectSlotsByName(self)

    def resizeApp(self):
        
        _height, _weight = getScreenSize()
        
        self.resize(
            int(floor(float(_height)/3)),
            floor(int(float(_weight)/4)))

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