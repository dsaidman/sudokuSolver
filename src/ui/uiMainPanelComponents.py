import logging

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QMainWindow, QVBoxLayout

from Puzzle import puzzle as sudokuDefs
from .uiControlComponents import UiPanel
from .uiPuzzleComponents import PuzzleFrame

uiLogger = logging.getLogger("uiLogger")


class UiMainPanel(QFrame):
    def __init__(self, parent):
        super(UiMainPanel, self).__init__(parent)

        uiLogger.debug("Entered UiMainPanel")
        self.setObjectName("uiMainPanel")
        self.setParent(parent)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
        self.setContentsMargins(3, 3, 3, 3)
        self.setLineWidth(1)
        self.setupUi()

    def setupUi(self):
        # Master Layout
        uiLogger.debug("Setting UiMainPanel main layout")
        self.mainPanelLayout = QVBoxLayout()
        self.mainPanelLayout.setObjectName("mainPanelLayout")
        self.setLayout(self.mainPanelLayout)

        self.uiTitleFrame = UiTitleFrame(self)
        self.puzzleFrame = PuzzleFrame(self)
        self.uiFrame = UiPanel(self)

        # make master layout widget for nestthig the layouts
        self.mainPanelLayout.setContentsMargins(0, 0, 0, 0)

        self.mainPanelLayout.addStretch()

        uiLogger.debug("Inserting uiTitleFrame Widget into UiMainPanel")
        self.mainPanelLayout.insertWidget(0, self.uiTitleFrame)

        uiLogger.debug("Inserting PuzzleFrame into UiMainPanel")
        self.mainPanelLayout.insertWidget(1, self.puzzleFrame)

        uiLogger.debug("Inserting UiControlFrame into UiMainPanel")
        self.mainPanelLayout.insertWidget(2, self.uiFrame)

        self.mainPanelLayout.addStretch()

    def orderTabs(self):
        uiLogger.debug("Ordering puzzle frame tabs")
        for idx in range(len(sudokuDefs.squares) - 1):
            QMainWindow.setTabOrder(
                self.puzzleFrame.squares[sudokuDefs.squares[idx]],
                self.puzzleFrame.squares[sudokuDefs.squares[idx + 1]],
            )
        QMainWindow.setTabOrder(
            self.puzzleFrame.squares[sudokuDefs.squares[-1]],
            self.puzzleFrame.squares[sudokuDefs.squares[0]],
        )


class UiTitleFrame(QFrame):
    def __init__(self, parent):
        super(UiTitleFrame, self).__init__(parent)

        self.setObjectName("uiTitleFrame")
        self.setParent(parent)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)

        self.setContentsMargins(0, 0, 0, 0)

        self.titleFrameLayout = QHBoxLayout()
        self.titleFrameLayout.setObjectName("uiTitleFrameLayout")
        self.titleFrameLayout.setParent(self)
        self.titleFrameLayout.setSpacing(0)
        self.titleFrameLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.titleFrameLayout)

        self.titleLabel = QLabel(self)
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setParent(self)
        # self.titleLabel.setAutoFillBackground(True)
        self.titleLabel.setText("Sudoku Solver")
        self.titleLabel.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.titleLabel.setStyleSheet("""
                                      QLabel#titleLabel {
                                          background-color: rgb(100,100,100);
                                          font-weight: bold;
                                          font-size: 14px;
                                          }
                                        """)
        self.setContentsMargins(0, 0, 0, 0)
        self.titleFrameLayout.addWidget(self.titleLabel)
