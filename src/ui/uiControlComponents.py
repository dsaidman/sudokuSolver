
from time import perf_counter as tictoc
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QGridLayout, QVBoxLayout, QFrame, QPushButton
from .uiHelpers import grabPuzzleFrame, grabWidget, grabStatusBar
from .uiEnums import ValidityEnum, SquareTypeEnum
from solver.definitions import sudokuDefs
from solver.py2runtime import RuntimePy as rt


class UiPanel(QFrame):
    def __init__(self, parent, objectName='UiPanel'):
        super(UiPanel, self).__init__(parent, objectName='UiPanel')

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
            """)
        
        self.setupUiPanel()

    def setupUiPanel(self):
        self.solvePuzzleBtn = SolvePuzzleButton(parent=self)
        self.setPuzzleBtn = SetPuzzleBtn(parent=self)
        self.infoDisplayLabel = InfoDisplayLabel(parent=self)

        uiFrameLayout = QGridLayout()
        uiFrameLayout.setObjectName('uiFrameLayout')
        uiFrameLayout.setSpacing(3)
        uiFrameLayout.setContentsMargins(0, 0, 0, 0)

        mainPanelLayout = grabWidget(QVBoxLayout, 'mainPanelLayout')

        mainPanelLayout.addLayout(uiFrameLayout)
        uiFrameLayout.addWidget(self.setPuzzleBtn, 0, 0,
                                1, 1, Qt.AlignmentFlag.AlignVCenter)
        uiFrameLayout.addWidget(self.solvePuzzleBtn, 0, 1,
                                1, 1, Qt.AlignmentFlag.AlignVCenter)
        uiFrameLayout.addWidget(
            self.infoDisplayLabel,
            1,
            0,
            1,
            2,
            Qt.AlignmentFlag.AlignVCenter)

    def _setCompleted(self):

        self.setPuzzleBtn._disableMe()
        self.setPuzzleBtn.setProperty("completed", True)
        self.setPuzzleBtn.setToolTip("Puzzle is complete! Nothing to do here")
        
        self.solvePuzzleBtn._disableMe()
        self.solvePuzzleBtn.setProperty("completed", True)
        self.solvePuzzleBtn.setText('SOLVED')


        grabPuzzleFrame().onSquareChangeEvent()
        grabStatusBar().statusWidget.puzzleInfoLabel.setText('81 of 81 SQUARES SET: SOLVED')
        grabStatusBar().statusWidget.puzzleInfoLabel.update()

class InfoDisplayLabel(QLabel):
    def __init__(self, parent, objectName="infoDisplayLabel"):
        super(InfoDisplayLabel, self).__init__(
            parent, objectName="infoDisplayLabel")

        self.setParent(parent)
        self.setObjectName(objectName)
        self.setText("")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setEnabled(False)

    def _resetAction(self):
        self.setText("")
        self.setStyleSheet("")


class SetPuzzleBtn(QPushButton):
    def __init__(self, parent, objectName='setPuzzleBtn'):
        super(SetPuzzleBtn, self).__init__(
            parent, objectName='setPuzzleBtn')

        self.setParent(parent)
        self.setObjectName(objectName)
        self.setText("Lock")
        #self.setFlat(True)
        self.clicked.connect(grabPuzzleFrame().toggleLock)
        self._disableMe()
        self.setProperty('completed', False)

    def _enableMe(self):
        self.setEnabled(True)
        self.setProperty('completed', False)
        if self.text() == "Lock":
            self.setToolTip(
                'Puzzle is valid, click to lock the puzzle when ready')
        else:
             self.setToolTip(
                'Im locked and puzzle is set. Press solve to solve the puzzle')
        self.style().polish(self)
        self.style().unpolish(self)

    def _disableMe(self):
        self.setToolTip(
            'The puzzle can be solved once the minimum number of squares required for a unique solution have been entered')
        self.setProperty('completed', False)
        self.setDisabled(True)
        self.style().polish(self)
        self.style().unpolish(self)

    def _completeMe(self):
        self.setToolTip('Puzzle is completed, nothing to do here')
        self.setText('DONE')
        self.setProperty('completed', True)
        self.setDisabled(True)


class SolvePuzzleButton(QPushButton):
    def __init__(self, parent, objectName='solveBtn'):
        super(SolvePuzzleButton, self).__init__(
            parent, objectName='solveBtn')

        self.setParent(parent)
        self.setText("Solve")
        self.setShortcut("")
        self.setObjectName("solveBtn")
        self.setProperty("completed", False)
        #self.setFlat(True)
        self._disableMe()
        self.clicked.connect(self.solveIt)
        self.clicked.connect(self._disableMe)

    def _enableMe(self):
        self.setEnabled(True)
        self.setProperty("completed", False)
        self.setToolTip('Im valid, defined, and ready to go')
        self.style().polish(self)
        self.style().unpolish(self)

    def _disableMe(self):
        self.setDisabled(True)
        self.setProperty("completed", False)
        self.setText("Solve")
        self.setToolTip(
            'Im disabled the puzzle isnt ready to solve yet')
        self.style().polish(self)
        self.style().unpolish(self)

    def solveIt(self):
        print('Entered solvePuzzle method of solvePuzzleButton!')
        puzzleFrame = grabPuzzleFrame()
        if puzzleFrame.isValid is not ValidityEnum.Valid:
            print('\tPuzzle not valid condition, returning')
            self.setProperty("completed", False)
            return False
        else:
            if rt.lang == "luajit" or rt.lang == "lua":
                
                puzzleArg = rt.dict2Table(puzzleFrame.asDict())
                solveFun = rt.solver['solve']
            elif rt.lang == "julia":
                #puzzleArg = rt.runtime.convert( 
                #                                      rt.runtime.Dict[rt.runtime.String,rt.runtime.String], 
                #                                      puzzleFrame.asDict()) # Ensure typed correctly
                puzzleArg = rt.runtime.copy(rt.defintions.puzzle0)
                for k,v in  puzzleFrame.asDict().items():
                    puzzleArg[k] = v
                solveFun  = rt.solver.solveTheThing

            # Everything is ready to call
            tStart = tictoc()
            result = solveFun(puzzleArg)
            tDuration_ms = (tictoc() - tStart) * 1000
            print(f"Elapsed time: {tDuration_ms:.2f} milliseconds")

            theSolution = {}
            for squareKey, squareValue in result.items():
                theSolution[squareKey] = squareValue

            self.setSolution(theSolution)
            uiPanel = grabWidget(QFrame, 'UiPanel')
            uiPanel._setCompleted()

            if rt.lang == "luajit" or rt.lang == "lua":
                runtimeInfo = dict(result['info'])
                difficultyEnum = runtimeInfo['difficulty']
                numRecursions = runtimeInfo['numRecursions']
                numOperations = runtimeInfo['numOperations']
            else:
                difficultyEnum = "UNSET"
                numRecursions  = "UNSET"
                numOperations  = "UNSET"
                
            displayLabel = grabWidget(QLabel, 'infoDisplayLabel')

            displayText = f'Completed in {
                tDuration_ms:.2f} milliseconds - Difficulty: {
                difficultyEnum:s}\n{numRecursions} Recursions - {numOperations} Operations'
            displayLabel.setText(displayText)
            displayLabel.setStyleSheet(
                """
                font-size: 12px; 
                font-weight: bold; 
                color: rgb(0, 255, 0);
                background-color: rgba(0, 0, 0, 0.5);
                """)
                
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
