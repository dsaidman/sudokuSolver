

from PyQt6.QtWidgets import QVBoxLayout, QLabel, QFrame, QMainWindow, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from .uiPuzzleComponents import PuzzleFrame
from .uiControlComponents import UiPanel
from solver.py2lua import luaPy as sudokuDefs
import logging
uiLogger = logging.getLogger('uiLogger')

class UiMainPanel(QFrame):

    def __init__(self, parent):
        super(UiMainPanel, self).__init__(parent)

        uiLogger.debug('Entered UiMainPanel')
        self.setObjectName('uiMainPanel')
        self.setParent(parent)
        self.setupUi()

    def setupUi(self):

        # Master Layout
        uiLogger.debug('Setting UiMainPanel main layout')
        self.mainPanelLayout = QVBoxLayout()
        self.mainPanelLayout.setParent(self)
        self.mainPanelLayout.setObjectName('mainPanelLayout')
        self.setLayout(self.mainPanelLayout)


        self.uiTitleFrame = UiTitleFrame(self)
        self.puzzleFrame = PuzzleFrame(self)
        self.uiFrame = UiPanel(self)

        # make master layout widget for nestthig the layouts
        uiLogger.debug('Inserting uiTitleFrame Widget into UiMainPanel')
        self.mainPanelLayout.insertWidget(0, self.uiTitleFrame)

        uiLogger.debug('Inserting PuzzleFrame into UiMainPanel')
        self.mainPanelLayout.insertWidget(1, self.puzzleFrame)

        uiLogger.debug('Inserting UiControlFrame into UiMainPanel')
        self.mainPanelLayout.insertWidget(2, self.uiFrame)

        self.uiTitleFrame.raise_()
        self.uiFrame.raise_()
        self.puzzleFrame.raise_()

    def orderTabs(self):

        uiLogger.debug('Ordering puzzle frame tabs')
        for idx in range(len(sudokuDefs.squares) - 1):
            QMainWindow.setTabOrder(
                self.puzzleFrame.squares[sudokuDefs.squares[idx]],
                self.puzzleFrame.squares[sudokuDefs.squares[idx + 1]])
        QMainWindow.setTabOrder(
            self.puzzleFrame.squares[sudokuDefs.squares[-1]],
            self.puzzleFrame.squares[sudokuDefs.squares[0]])


class UiTitleFrame(QFrame):
    def __init__(self, parent):
        super(UiTitleFrame, self).__init__(parent)

        self.setObjectName("uiTitleFrame")
        self.setParent(parent)
        self.setFrameShadow(QFrame.Shadow.Plain)
        self.setContentsMargins(0, 0, 0, 0)

        self.titleFrameLayout = QHBoxLayout()
        self.titleFrameLayout.setObjectName('uiTitleFrameLayout')
        self.titleFrameLayout.setParent(self)
        self.setLayout(self.titleFrameLayout)

        self.titleLabel = QLabel(self)
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setParent(self)
        self.titleLabel.setAutoFillBackground(True)
        self.titleLabel.setFrameShadow(QFrame.Shadow.Plain)
        self.titleLabel.setText("Sudoku Solver")
        self.titleLabel.setScaledContents(True)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setStyleSheet("background-color: rgb(100,100,100);")
        self.setContentsMargins(0, 0, 0, 0)

        titleFont = QFont()
        titleFont.setBold(True)
        titleFont.setPointSize(14)
        self.titleLabel.setFont(titleFont)
        self.titleFrameLayout.addWidget(self.titleLabel, stretch=1)
