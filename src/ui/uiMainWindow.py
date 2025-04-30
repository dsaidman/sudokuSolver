from functools import lru_cache
from math import floor
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QGridLayout, QFrame, QApplication, QMainWindow
from PyQt5.QtCore import Qt, QMetaObject
from .uiEnums import AppStatusEnum
from .uiMenuComponents import MenuBar
from .uiPuzzleComponents import PuzzleFrame, UiPanel
from src.pySolver.py2lua import luaPy as sudokuDefs

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
        self.setWindowModality(Qt.NonModal)
        self.setWindowTitle("SudokuSolverApp")
        self.setDockNestingEnabled(True)
        self._status = AppStatusEnum.Unlocked
        self.resizeApp()
        self.setStyleSheet('* {font-family: Segoe Ui; font-size: 12pt}')

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
        self.titleLabel.setFrameShadow(QFrame.Plain)
        self.titleLabel.setText("SUDOKU SOLVER")
        self.titleLabel.setScaledContents(True)
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setStyleSheet("font-family: Segoe Ui; font-size: 28pt; font-weight: bold")
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

    @property
    def screenSize(self):
        appDesktop = QApplication.desktop()

        screenRect = appDesktop.screenGeometry()
        self._heightPx = screenRect.height()
        self._widthPx = screenRect.width()
        return self._heightPx, self._widthPx

    def resizeApp(self):
        
        heightPx, widthPx = self.screenSize
        
        self.resize(
            int(floor(self._heightPx/2)),
            floor(int(self._widthPx/4)))

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
    appDesktop = QApplication.desktop()

    screenRect = appDesktop.screenGeometry()
    height = screenRect.height()
    width = screenRect.width()
    return height, width




def changeQtLineEditProp(widget, prop, newVal):
    widget.setProperty(prop, newVal)
    widget.style().unpolish(widget)
    widget.style().polish(widget)
    widget.update()