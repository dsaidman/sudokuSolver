import logging

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QGridLayout, QLabel, QPushButton, QVBoxLayout

from Puzzle import SudokuPuzzle as Puzzle
from Puzzle import puzzle as sudokuDefs
from py2runtime import RuntimePy as rt

from .uiEnums import SquareTypeEnum, ValidityEnum
from .uiHelpers import grabPuzzleFrame, grabStatusBar, grabWidget

uiLogger = logging.getLogger("uiLogger")


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
            QPushButton {
                border: 1px solid purple;
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
        self.setText("")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setEnabled(False)
        self.setVisible(False)
        self.setProperty("lang","python")
        self.setStyleSheet("""
                           QLabel{
                                font-size: 14px;
                                font-weight: bold;
                                background-color: rgba(0, 0, 0, 0.5);
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
        self.setText("")
        self.setVisible(False)
        #self.setStyleSheet("")


class SetPuzzleBtn(QPushButton):
    def __init__(self, parent, objectName="setPuzzleBtn"):
        super(SetPuzzleBtn, self).__init__(parent, objectName="setPuzzleBtn")

        self.setParent(parent)
        self.setObjectName(objectName)
        self.setText("Lock")
        # self.setFlat(True)
        self.clicked.connect(grabPuzzleFrame().toggleLock)
        self._disableMe()
        self.setProperty("completed", False)

    def _enableMe(self):
        self.setEnabled(True)
        self.setProperty("completed", False)
        if self.text() == "Lock":
            self.setToolTip("Puzzle is valid, click to lock the puzzle when ready")
        else:
            self.setToolTip("Im locked and puzzle is set. Press solve to solve the puzzle")

        self.style().polish(self)
        self.style().unpolish(self)

    def _disableMe(self):
        self.setToolTip(
            "The puzzle can be solved once the minimum number of squares required for a unique solution have been entered"
        )
        self.setProperty("completed", False)
        self.setDisabled(True)
        self.style().polish(self)
        self.style().unpolish(self)

    def _completeMe(self):
        self.setToolTip("Puzzle is completed, nothing to do here")
        self.setText("DONE")
        self.setProperty("completed", True)
        self.setDisabled(True)


class SolvePuzzleButton(QPushButton):
    def __init__(self, parent, objectName="solveBtn"):
        super(SolvePuzzleButton, self).__init__(parent, objectName="solveBtn")

        self.setParent(parent)
        self.setText("Solve")
        self.setShortcut("")
        self.setObjectName("solveBtn")
        self.setProperty("completed", False)
        # self.setFlat(True)
        self._disableMe()
        self.clicked.connect(self.solveIt)
        self.clicked.connect(self._disableMe)

    def _enableMe(self):
        self.setEnabled(True)
        self.setProperty("completed", False)
        self.setToolTip("Im valid, defined, and ready to go")
        self.style().polish(self)
        self.style().unpolish(self)

    def _disableMe(self):
        self.setDisabled(True)
        self.setProperty("completed", False)
        self.setText("Solve")
        self.setToolTip("Im disabled the puzzle isnt ready to solve yet")
        self.style().polish(self)
        self.style().unpolish(self)

    def solveIt(self):
        print("Entered solvePuzzle method of solvePuzzleButton!")
        puzzleFrame = grabPuzzleFrame()
        if puzzleFrame.isValid is not ValidityEnum.Valid:
            print("\tPuzzle not valid condition, returning")
            self.setProperty("completed", False)
            return False
        else:
            thePzlDict = puzzleFrame.asDict()
            thePzl = Puzzle(lang=rt.lang, value=thePzlDict)
            # compilate run
            thePzl.solve()

            # timed run
            thePzl.value = thePzlDict

            result = thePzl.solve()

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
            displayLabel.setText(displayText)
            displayLabel.setVisible(True)
            self._disableMe()
            uiPanel.setPuzzleBtn._disableMe()

    def setSolution(self, theSolutionDict):
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
