
from time import perf_counter as tictoc
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QGridLayout, QVBoxLayout, QFrame, QPushButton
from .uiHelpers import grabPuzzleFrame, grabWidget, grabStatusBar
from .uiEnums import ValidityEnum, SquareTypeEnum
from pySolver.definitions import sudokuDefs
from pySolver.py2lua import luaPy

class UiPanel(QFrame):
    def __init__(self, parent, objectName='UiPanel'):
        super(UiPanel, self).__init__(parent, objectName='UiPanel')

        self.setParent(parent)
        self.setObjectName(objectName)
        self.setupUiPanel()

    def setupUiPanel(self):
        self.solvePuzzleBtn = SolvePuzzleButton(parent=self)
        self.setPuzzleBtn = SetPuzzleBtn(parent=self)
        self.infoDisplayLabel = InfoDisplayLabel(parent=self)

        uiFrameLayout = QGridLayout()
        uiFrameLayout.setObjectName('uiFrameLayout')
        uiFrameLayout.setSpacing(0)
        uiFrameLayout.setContentsMargins(0, 0, 0, 0)

        mainPanelLayout = grabWidget(QVBoxLayout, 'mainPanelLayout')

        mainPanelLayout.addLayout(uiFrameLayout)

        uiFrameLayout.addWidget(self.setPuzzleBtn, 0, 0,
                                1, 1, Qt.AlignmentFlag.AlignVCenter)
        uiFrameLayout.addWidget(self.solvePuzzleBtn, 0, 1,
                                1, 1, Qt.AlignmentFlag.AlignVCenter)
        uiFrameLayout.addWidget(self.infoDisplayLabel, 1, 0, 1, 2, Qt.AlignmentFlag.AlignVCenter)

    def _setCompleted(self):

        self.setPuzzleBtn._disableMe()
        self.setPuzzleBtn.setEnabled(False)

        grabPuzzleFrame().onSquareChangeEvent()
        grabStatusBar().puzzleInfoLabel.setText('81 of 81 SQUARES SET: SOLVED')
        grabStatusBar().puzzleInfoLabel.update()

        self.solvePuzzleBtn._disableMe()
        self.solvePuzzleBtn.setEnabled(False)
        self.solvePuzzleBtn.setText('SOLVED')


class InfoDisplayLabel(QLabel):
    def __init__(self, parent, objectName="infoDisplayLabel"):
        super(InfoDisplayLabel, self).__init__(
            parent, objectName="infoDisplayLabel")

        self.setParent(parent)
        self.setObjectName(objectName)
        self.setText("")
        self.setStyleSheet("font-size: 14px;")
        self.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)
        self.setEnabled(False)

    def _resetAction(self):
        self.setText("")

class SetPuzzleBtn(QPushButton):
    def __init__(self, parent, objectName='setPuzzleBtn'):
        super(SetPuzzleBtn, self).__init__(
            parent, objectName='setPuzzleBtn')

        self.setParent(parent)
        self.setObjectName(objectName)
        self.setText("Lock")
        self.setShortcut("")
        self.clicked.connect(grabPuzzleFrame().toggleLock)
        self._disableMe()
        btnFont = QFont()
        self.setFont(btnFont)

    def _enableMe(self):
        self.setEnabled(False)
        self.setEnabled(True)

        self.setStyleSheet(
            "QPushButton {color : rgb(255,140,0); font-weight: bold;}")
        self.setToolTip(
            'Push button to lock the puzzle to be solved')

    def _disableMe(self):
        self.setStyleSheet(
            "QPushButton { color: rgb(140,140,140);}")
        self.setToolTip(
            'The puzzle can be solved once the minimum number of squares required for a unique solution have been entered')
        self.setEnabled(False)
        self.setDisabled(True)

    def _completeMe(self):
        self.setStyleSheet(
            "QPushButton { color: rgb(0,255,0); font-weight: bold;}")
        self.setToolTip('Puzzle is completed, nothing to do here')
        self.setText('DONE')
        self.setEnabled(False)
        self.setDisabled(True)


class SolvePuzzleButton(QPushButton):
    def __init__(self, parent, objectName='solveBtn'):
        super(SolvePuzzleButton, self).__init__(
            parent, objectName='solveBtn')

        self.setParent(parent)
        self.setText("Solve")
        self.setShortcut("")
        self.setObjectName("solveBtn")
        self._disableMe()
        btnFont = QFont()
        self.setFont(btnFont)
        self.clicked.connect(self.solveIt)
        self.clicked.connect(self._disableMe)

    def _enableMe(self):
        self.setDisabled(False)
        self.setEnabled(True)
        self.setStyleSheet(
            "QPushButton {color: rgb(0,255,0); font-weight: bold;}")
        self.setToolTip('Im enabled and ready to go')

    def _disableMe(self):
        self.setEnabled(False)
        self.setDisabled(True)
        self.setStyleSheet(
            "QPushButton {color:  rgb(140,140,140); font-weight: regular;}")
        self.setText("Solve")
        self.setToolTip(
            'Im disabled because couldnt lock the puzzle that was given')

    def solveIt(self):
        print('Entered solvePuzzle method of solvePuzzleButton!')
        puzzleFrame = grabPuzzleFrame()
        if puzzleFrame.isValid is not ValidityEnum.Valid:
            print('\tPuzzle not valid condition, returning')
            return False
        else:
            puzzleArg = luaPy.dict2Table(puzzleFrame.asDict())
            solveFun = luaPy.solver['solve']

            # Everything is ready to call
            tStart = tictoc()
            result = solveFun(puzzleArg)
            tDuration_ms = (tictoc()-tStart)*1000
            print(f"Elapsed time: {tDuration_ms:.2f} milliseconds")

            runtimeInfo = dict(result['info'])
            theSolution = {}
            for squareKey, squareValue in result.items():
                theSolution[squareKey] = squareValue

            self.setSolution(theSolution)
            uiPanel = grabWidget(QFrame, 'UiPanel')
            uiPanel._setCompleted()

            difficultyEnum = runtimeInfo['difficulty']
            numRecursions = runtimeInfo['numRecursions']
            numOperations = runtimeInfo['numOperations']
            displayLabel = grabWidget(QLabel, 'infoDisplayLabel')

            displayText = f'Completed in {tDuration_ms:.2f} milliseconds - Difficulty: {difficultyEnum:s}\n{numRecursions} Recursions - {numOperations} Operations'
            displayLabel.setText(displayText)
            self._disableMe()
            uiPanel.setPuzzleBtn._disableMe()

    def setSolution(self, theSolutionDict):
        puzzleFrame = grabPuzzleFrame()
        puzzleSquares = puzzleFrame.squares
        allComplete = True
        for puzzleKey in sudokuDefs.squares:
            if puzzleSquares[puzzleKey].squareType is SquareTypeEnum.UserSet:
                puzzleSquares[puzzleKey].squareType = SquareTypeEnum.Solved
                puzzleSquares[puzzleKey].setText(theSolutionDict[puzzleKey])
            # else:
            #    allComplete = False
            puzzleSquares[puzzleKey].setEnabled(False)
        # if allComplete:
        for squareValue in puzzleSquares.values():
            squareValue.setEnabled(False)
            squareValue.isValid
        puzzleFrame.onSquareChangeEvent()
