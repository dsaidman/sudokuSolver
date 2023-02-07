
from time import perf_counter as tictoc

from appHelpers import (ValidityEnum, SquareTypeEnum, grabPuzzleFrame, grabPuzzleSquares,
                        grabWidget)
from puzzleHelpers import luaPy
from puzzleHelpers import sudokuParams as params
from PyQt5 import QtCore, QtGui, QtWidgets
_fontFamily = "Segoi Ui"

class UiPanel(QtWidgets.QFrame):
    def __init__(self, parent, objectName='UiPanel'):
        super(UiPanel, self).__init__(parent, objectName='UiPanel')

        self.setParent(parent)
        self.setObjectName(objectName)

        self.setupUiPanel()

    def setupUiPanel(self):
        self.solvePuzzleBtn = SolvePuzzleButton(parent=self)
        self.puzzleInfoLabel = PuzzleInfoLabel(parent=self)
        self.setPuzzleBtn = SetPuzzleBtn(parent=self)
        self.infoDisplayLabel = InfoDisplayLabel(parent=self)
        
        uiFrameLayout = QtWidgets.QGridLayout()
        uiFrameLayout.setObjectName('uiFrameLayout')
        uiFrameLayout.setSpacing(0)
        uiFrameLayout.setContentsMargins(0, 0, 0, 0)

        masterLayout = grabWidget(QtWidgets.QVBoxLayout, 'masterLayout')

        masterLayout.addLayout(uiFrameLayout)

        uiFrameLayout.addWidget(self.puzzleInfoLabel, 0,
                                1, 1, 3, QtCore.Qt.AlignmentFlag.AlignRight)
        uiFrameLayout.addWidget(self.setPuzzleBtn, 0, 0,
                                1, 1, QtCore.Qt.AlignmentFlag.AlignVCenter)
        uiFrameLayout.addWidget(self.solvePuzzleBtn, 1,
                                0, 1, 1, QtCore.Qt.AlignmentFlag.AlignVCenter)
        uiFrameLayout.addWidget(self.infoDisplayLabel, 1,
                                1, 1, 3, QtCore.Qt.AlignmentFlag.AlignVCenter)
    def _setCompleted(self):
        
        self.setPuzzleBtn._disableMe()
        self.setPuzzleBtn.setEnabled(False)
        
        grabPuzzleFrame()._refresh()
        #self.setEnabled(False)
        self.puzzleInfoLabel.setText('81 of 81 SQUARES SET: SOLVED')
        self.puzzleInfoLabel._refresh()
        
        self.solvePuzzleBtn._disableMe()
        self.solvePuzzleBtn.setEnabled(False)
        self.solvePuzzleBtn.setText('SOLVED')

class InfoDisplayLabel(QtWidgets.QLabel):
    def __init__(self, parent, objectName="infoDisplayLabel"):
        super(InfoDisplayLabel, self).__init__(
            parent, objectName="infoDisplayLabel")
        
        self.setParent(parent)
        self.setObjectName(objectName)
        self.setText("")
        self.setStyleSheet("font-family: Segoe Ui; font-size: 14px;")
        self.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.setEnabled(False)

    def _resetAction(self):
        self.setText("")
class PuzzleInfoLabel(QtWidgets.QLabel):
    
    def __init__(self, parent, objectName="puzzleInfoLabel"):
        super(PuzzleInfoLabel, self).__init__(
            parent, objectName="puzzleInfoLabel")

        self.setParent(parent)
        self.setObjectName(objectName)

        puzzleLabelFont = QtGui.QFont(_fontFamily, 14)
        puzzleLabelFont.setBold(False)
        puzzleLabelFont.setItalic(False)

        # self.setGeometry(QtCore.QRect(391, 851, 531, 38))  # Change this
        self.setText("0 OF 17 SQUARES SET")
        self.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)

        # Connect the puzzle squares to update text when changed. Cant do before because this class didnt exist yet

        for theSquare in grabPuzzleSquares().values():
            theSquare.textEdited.connect(self._refresh)

    def _refresh(self):

        puzzleFrame = grabWidget(QtWidgets.QFrame, 'puzzleFrame')
        numFilledSquares = puzzleFrame.validSquareCount
        theText = str(numFilledSquares) + " OF 17 SQUARES SET"
        puzzleIsValid = puzzleFrame.isValid

        setPuzzleBtn = grabWidget(QtWidgets.QPushButton, 'setPuzzleBtn')

        if puzzleIsValid == ValidityEnum.Invalid:
            self.setStyleSheet(
                "QLabel{ color: rgb(255, 0, 0); font-style: italic;font-weight: regular;font-size: 14pt;}")
            setPuzzleBtn._disableMe()
        elif numFilledSquares >= 17 and numFilledSquares < 81 and puzzleIsValid == ValidityEnum.Valid:
            self.setStyleSheet(
                "QLabel{ color: rgb(255, 140, 0); font-style: regular;font-weight: bold;font-size: 14pt;}")
            theText = theText + ': READY'
            setPuzzleBtn._enableMe()
        elif numFilledSquares == 81 and puzzleIsValid == ValidityEnum.Valid:
            self.setStyleSheet(
                "QLabel{ color: rgb(0, 255, 0); font-style: regular;font-weight: bold;font-size: 14pt;}")
            theText = theText + ': COMPLETE'
            setPuzzleBtn._enableMe()
        elif numFilledSquares < 17 or puzzleIsValid == ValidityEnum.Valid:
            self.setStyleSheet(
                "QLabel{ color: rgb(212,212,200); font-style: normal;font-weight: regular;font-size: 14pt;}")
            setPuzzleBtn._disableMe()
        self.setText(theText)


class SetPuzzleBtn(QtWidgets.QPushButton):
    def __init__(self, parent, objectName='setPuzzleBtn'):
        super(SetPuzzleBtn, self).__init__(
            parent, objectName='setPuzzleBtn')

        self.setParent(parent)
        self.setObjectName(objectName)
        # self.setGeometry(QtCore.QRect(10, 850, 361, 41))
        self.setFont(QtGui.QFont(_fontFamily, 14))

        self.setText("LOCK PUZZLE")
        self.setShortcut("")

        self.clicked.connect(grabPuzzleFrame().toggleLock)
        self._disableMe()

    def _enableMe(self):
        self.setEnabled(True)
        self.setStyleSheet(
            "QPushButton {color : rgb(255,140,0); font-weight: bold;}")
        self.setToolTip(
            'Push button to lock the puzzle to be solved')

    def _disableMe(self):
        self.setStyleSheet(
            "QPushButton { color: white; font-weight : bold;}")
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


class SolvePuzzleButton(QtWidgets.QPushButton):
    def __init__(self, parent, objectName='solveBtn'):
        super(SolvePuzzleButton, self).__init__(
            parent, objectName='solveBtn')

        self.setParent(parent)
        self.setFont(QtGui.QFont(_fontFamily, 14))
        self.setText("SOLVE")
        self.setShortcut("")
        self.setObjectName("solveBtn")
        self._disableMe()
        self.clicked.connect(self.solveIt)
        self.clicked.connect(self._disableMe)

    def _enableMe(self):
        self.setEnabled(True)
        self.setStyleSheet(
            "QPushButton {color: rgb(0,255,0); font-weight: bold;}")
        self.setToolTip('Im enabled and ready to go')

    def _disableMe(self):
        self.setStyleSheet(
            "QPushButton {color:  white; font-weight: regular;}")
        self.setEnabled(False)
        self.setDisabled(True)
        self.setToolTip('Im disabled because couldnt lock the puzzle that was given')

    def solveIt(self):
        print('Entered solvePuzzle method of solvePuzzleButton!')
        puzzleFrame = grabPuzzleFrame()
        if puzzleFrame.isValid is not ValidityEnum.Valid:
            print('\tPuzzle not valid condition, returning')
            return False
        else:
            puzzleArg = luaPy.dict2Table(puzzleFrame.asDict())
            solveFun = luaPy.sovler['solve']
            
            # Everything is ready to call
            tStart = tictoc()
            result = solveFun( puzzleArg )
            tDuration_ms = (tictoc()-tStart)*1000
            print(f"Elapsed time: {tDuration_ms:.2f} milliseconds")
            
            runtimeInfo = dict(result['info'])
            theSolution = {}
            for squareKey, squareValue in result.items():
                theSolution[squareKey] = squareValue

            self.setSolution(theSolution)
            uiPanel = grabWidget(QtWidgets.QFrame, 'UiPanel')
            uiPanel._setCompleted()
            
            difficultyEnum = runtimeInfo['difficulty']
            numRecursions = runtimeInfo['numRecursions']
            numOperations = runtimeInfo['numOperations']
            displayLabel = grabWidget(QtWidgets.QLabel, 'infoDisplayLabel')
            
            displayText = f'Completed in {tDuration_ms:.2f} seconds - Difficulty: {difficultyEnum:s}\n{numRecursions} Recursions - {numOperations} Operations'
            displayLabel.setText(displayText)
            self._disableMe()
            uiPanel.setPuzzleBtn._disableMe()
            
    def setSolution(self, theSolutionDict):
        puzzleFrame = grabPuzzleFrame()
        puzzleSquares = puzzleFrame.squares
        allComplete = True
        for puzzleKey in params.squares:
            if puzzleSquares[puzzleKey].squareType is SquareTypeEnum.UserSet:
                puzzleSquares[puzzleKey].squareType = SquareTypeEnum.Solved
                puzzleSquares[puzzleKey].setText(theSolutionDict[puzzleKey])
            #else:
            #    allComplete = False
            puzzleSquares[puzzleKey].setEnabled(False)
        #if allComplete:
        for squareValue in puzzleSquares.values():
            squareValue.setEnabled(False)
            squareValue.isValid
        puzzleFrame._refresh()
                