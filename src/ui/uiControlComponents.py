import logging
import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QFrame, QGridLayout, QLabel, QPushButton, QVBoxLayout

from Puzzle import SudokuPuzzle as Puzzle
from Puzzle import puzzle as sudokuDefs
from py2runtime import RuntimePy as rt

from .uiEnums import SquareTypeEnum, ValidityEnum
from .uiHelpers import getBasePath, grabPuzzleFrame, grabStatusBar, grabWidget

uiLogger = logging.getLogger("uiLogger")
iconPath = os.path.normpath(os.path.join(getBasePath(), "..", "..", "resources", "icons"))


class UiPanel(QFrame):
    def __init__(self, parent, objectName="UiPanel"):
        super(UiPanel, self).__init__(parent, objectName="UiPanel")

        self.setParent(parent)
        self.setObjectName(objectName)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLineWidth(1)

        self.setStyleSheet(
            """
            QFrame {
                border: none;
                margin: 0;
                padding: 0;
            }
            QPushButton {
                border: none;
                border-radius: 5px;
                font-size: 16px;
                }
            QPushButton:disabled {
                color: rgb(140,140,140);
                font-weight: regular;
                }
            QPushButton:enabled {
                color: yellow;
                font-weight: bold;
                }
            QPushButton[completed="true"] {
                color: rgb(0,255,0);
                font-weight: bold;
                }
            """
        )

        self.setupUiPanel()

    def setupUiPanel(self):
        self.solvePuzzleBtn = SolvePuzzleButton(parent=self)
        self.setPuzzleBtn = SetPuzzleBtn(parent=self)
        self.infoDisplayLabel = InfoDisplayLabel(parent=self)

        uiFrameLayout = QGridLayout()
        uiFrameLayout.setObjectName("uiFrameLayout")
        uiFrameLayout.setSpacing(3)
        uiFrameLayout.setContentsMargins(0, 0, 0, 0)

        mainPanelLayout = grabWidget(QVBoxLayout, "mainPanelLayout")

        mainPanelLayout.addLayout(uiFrameLayout)
        uiFrameLayout.addWidget(self.setPuzzleBtn, 0, 0, 1, 1, Qt.AlignmentFlag.AlignVCenter)
        uiFrameLayout.addWidget(self.solvePuzzleBtn, 0, 1, 1, 1, Qt.AlignmentFlag.AlignVCenter)
        uiFrameLayout.addWidget(self.infoDisplayLabel, 1, 0, 1, 2, Qt.AlignmentFlag.AlignVCenter)

    def _setCompleted(self):
        uiLogger.debug("Setting UiPanel Puzzle completed")
        self.setPuzzleBtn._disableMe()
        self.setPuzzleBtn.setProperty("completed", True)
        self.setPuzzleBtn.setToolTip("Puzzle is complete! Nothing to do here")

        self.solvePuzzleBtn._disableMe()
        self.solvePuzzleBtn.setProperty("completed", True)
        self.solvePuzzleBtn.setText("SOLVED")

        grabPuzzleFrame().onSquareChangeEvent()
        grabStatusBar().statusWidget.puzzleInfoLabel.setText("81 of 81 SQUARES SET: SOLVED")
        grabStatusBar().statusWidget.puzzleInfoLabel.update()


class InfoDisplayLabel(QLabel):
    def __init__(self, parent, objectName="infoDisplayLabel"):
        super(InfoDisplayLabel, self).__init__(parent, objectName="infoDisplayLabel")

        self.setParent(parent)
        self.setObjectName(objectName)
        self.setToolTip(self.objectName())
        self.setText("")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setEnabled(False)
        self.setVisible(False)
        self.setProperty("lang", "python")
        self.setStyleSheet("""
                           QLabel{
                                font-size: 14px;
                                font-weight: bold;
                                background-color: rgba(0, 0, 0, 0.5);
                                border: none;
                           }
                            QLabel[lang="luajit"] {
                                color: magenta;
                            }
                            QLabel[lang="lua"] {
                                color: forestgreen;
                            }
                            QLabel[lang="julia"] {
                                color: cyan;
                            }
                            QLabel[lang="python"] {
                                color: yellow;
                            }
                            QLabel[lang="cython"] {
                                color: orange;
                            }
                           """)

    def _resetAction(self):
        uiLogger.debug("Setting InfoDisplayLabel reset action")
        self.setText("")
        self.setVisible(False)
        # self.setStyleSheet("")


class SetPuzzleBtn(QPushButton):
    def __init__(self, parent, objectName="setPuzzleBtn"):
        super(SetPuzzleBtn, self).__init__(parent, objectName="setPuzzleBtn")

        self.setParent(parent)
        self.setObjectName(objectName)
        self.setToolTip(self.objectName())
        self.setText("Lock")
        # self.setFlat(True)
        self.clicked.connect(grabPuzzleFrame().toggleLock)
        self._disableMe()
        self.setProperty("completed", False)

    def _enableMe(self):
        uiLogger.debug("Performing SetPuzzleBtn _enableMe action")
        self.setEnabled(True)
        self.setProperty("completed", False)
        if self.text() == "Lock":
            self.setToolTip("Puzzle is valid, click to lock the puzzle when ready")
        else:
            self.setToolTip("Im locked and puzzle is set. Press solve to solve the puzzle")

        self.style().polish(self)
        self.style().unpolish(self)

    def _disableMe(self):
        uiLogger.debug("Performing SetPuzzleBtn _disableMe action")
        self.setToolTip(
            "The puzzle can be solved once the minimum number of squares required for a unique solution have been entered"
        )
        self.setProperty("completed", False)
        self.setDisabled(True)
        self.style().polish(self)
        self.style().unpolish(self)

    def _completeMe(self):
        uiLogger.debug("Performing SetPuzzleBtn _completeMe action")
        self.setToolTip("Puzzle is completed, nothing to do here")
        self.setText("DONE")
        self.setProperty("completed", True)
        self.setDisabled(True)


class SolvePuzzleButton(QPushButton):
    def __init__(self, parent, objectName="solveBtn"):
        super(SolvePuzzleButton, self).__init__(parent, objectName="solveBtn")

        self.setParent(parent)
        self.setText("Solve")
        self.setIcon(QIcon(os.path.join(iconPath, "runIcon.ico")))
        self.setShortcut("")
        self.setObjectName("solveBtn")
        self.setToolTip(self.objectName())
        self.setProperty("completed", False)
        # self.setFlat(True)
        self._disableMe()
        self.clicked.connect(self.solveIt)
        self.clicked.connect(self._disableMe)

    def _enableMe(self):
        uiLogger.debug("Performing SolvePuzzleButton _enableMe action")
        self.setEnabled(True)
        self.setProperty("completed", False)
        self.setToolTip("Im valid, defined, and ready to go")
        self.style().polish(self)
        self.style().unpolish(self)

    def _disableMe(self):
        uiLogger.debug("Performing SolvePuzzleButton _disableMe action")
        self.setDisabled(True)
        self.setProperty("completed", False)
        self.setText("Solve")
        self.setToolTip("Im disabled the puzzle isnt ready to solve yet")
        self.style().polish(self)
        self.style().unpolish(self)

    def solveIt(self):
        uiLogger.info("Entered solvePuzzle method of solvePuzzleButton!")
        puzzleFrame = grabPuzzleFrame()
        if puzzleFrame.isValid is not ValidityEnum.Valid:
            print("\tPuzzle not valid condition, returning")
            self.setProperty("completed", False)
            return False
        else:
            thePzlDict = puzzleFrame.asDict()
            thePzl = Puzzle(lang=rt.lang, value=thePzlDict)
            uiLogger.info("Puzzle successfully imported")
            # uiLogger.debug(f"thePzlDict: {thePzlDict:s}")
            # compilate run
            uiLogger.info("Evaluating puzzle: untimed compile step")
            thePzl.solve()
            uiLogger.info("Compile step complete.  Evaluating puzzle for timed run")
            # timed run

            uiLogger.debug("Resetting puzzle")
            thePzl.value = thePzlDict
            uiLogger.debug("Puzzle reset")
            result = thePzl.solve()
            uiLogger.info("Puzzle solved. Collecting result")

            solution = result["solution"]
            tDuration_ms = result["duration_ms"]
            numRecursions = result["numRecursions"]
            numOperations = result["numOperations"]

            difficultyLevel = result["difficultyLevel"]
            # bestSinglePass = result["bestSinglePass"]

            self.setSolution(solution)

            uiPanel = grabWidget(QFrame, "UiPanel")
            uiPanel._setCompleted()

            displayLabel = grabWidget(QLabel, "infoDisplayLabel")

            displayText = f"Completed in {tDuration_ms:.2f} milliseconds - Difficulty: {
                difficultyLevel:s
            }\n{numRecursions} Recursions - {numOperations} Operations"
            uiLogger.info(displayText)
            displayLabel.setText(displayText)
            uiLogger.debug("Showing displayLabel result")
            displayLabel.setVisible(True)
            self._disableMe()
            uiPanel.setPuzzleBtn._disableMe()

    def setSolution(self, theSolutionDict):
        uiLogger.debug("Setting puzzle solution")
        puzzleFrame = grabPuzzleFrame()
        puzzleSquares = puzzleFrame.squares
        for puzzleKey in sudokuDefs.squares:
            if puzzleSquares[puzzleKey].squareType is SquareTypeEnum.UserSet:
                puzzleSquares[puzzleKey].squareType = SquareTypeEnum.Solved
                puzzleSquares[puzzleKey].setText(theSolutionDict[puzzleKey])
            puzzleSquares[puzzleKey].setEnabled(False)
        # if allComplete:
        for squareValue in puzzleSquares.values():
            squareValue.setEnabled(False)
        puzzleFrame.onSquareChangeEvent()
