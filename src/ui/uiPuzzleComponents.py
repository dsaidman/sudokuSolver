
from solver.definitions import sudokuDefs
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtWidgets import QFrame, QGridLayout, QVBoxLayout, QPushButton, QLabel, QSizePolicy, QLineEdit
from .uiEnums import ValidityEnum, SquareTypeEnum, AppStatusEnum
from .uiHelpers import grabWidget, grabPuzzleFrame, grabMainWindow, grabPuzzleSquares, grabCurrentSquare
import sys, os
from math import floor
from functools import cached_property

# Until i figure out how to do this properly, path hack
sys.path.append(os.path.abspath('..'))


class PuzzleFrame(QFrame):
    """
    A QtWidgets QFrame superclass that contains all the widgets and methods of the sudoku puzzle and its squares.

    Args:
        QtWidgets (QFrame): None, superclass of QFrame parent

    Returns:
        PuzzleFrame: An initialized widget containing the puzzle interface and and other methods
    """

    @property
    def squareCount(self):
        """
        Counts number of squares that are populated

        Returns:
            int: square count
        """
        cnt = 0
        for square in self.squares.values():
            cnt = cnt + 1 if len(square.text()) > 0 else cnt
        return cnt

    @property
    def validSquareCount(self):
        """
        Counts number of squares that are populated and have values that do not violate any sudoku rules.

        Returns:
            int: square count of squares that do no violate sudoku rules
        """
        cnt = 0
        for square in self.squares.values():
            if len(square.text()) > 0 and square.isValid == ValidityEnum.Valid:
                cnt = cnt + 1
        return cnt

    @property
    def isValid(self):
        """
        Returns whether the current state of the sudoku puzzle violates any sudoku rules.

        Returns:
            ValidityEnum: Enumeration of square is valid
        """
        for square in self.squares.values():

            if square.isValid == ValidityEnum.Invalid:
                self._isValid = ValidityEnum.Invalid
                return self._isValid
        self._isValid = ValidityEnum.Valid
        return self._isValid

    def __init__(self, parent):
        """
        Main contructor of PuzzleFrame object that sets up all child widgets and graphic elements.

        Args:
            parent (QtWidget): Parent object of the puzzle frame, assumed the app MainWindow
        """
        super(PuzzleFrame, self).__init__(parent)
        self.setParent(parent)
        # self.setGeometry(QtCore.QRect(10, 130, 911, 691))

        self.setAutoFillBackground(True)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Plain)
        self.setLineWidth(3)
        self.setObjectName("puzzleFrame")
        
        self.setSizePolicy(
            QSizePolicy(
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.MinimumExpanding)
        )

        self.puzzleLayout = QGridLayout()
        self.puzzleLayout.setObjectName("puzzleLayout")
        self.puzzleLayout.setSpacing(1)
        self.puzzleLayout.setContentsMargins(0, 0, 0, 0)

        mainPanelLayout = grabWidget(QVBoxLayout, 'mainPanelLayout')
        mainPanelLayout.addLayout(self.puzzleLayout)

        self._initSquares()
        self._initHeaders()
        self._initBorderLines()

    def asString(self):
        """
        Returns current puzzle as string arguments that can be passed into command line version of lua solver.

        Returns:
            str: string of --Key=Value pairs representing current puzzle state
        """
        argList = []
        for squareKey, squareValue in self.squares.items():
            if squareValue.squareType is SquareTypeEnum.InputLocked and len(squareValue.text()) > 0:

                argList.append(
                    '--{key}={val}'.format(key=squareKey, val=squareValue.text()))
        return ' '.join(argList)

    def asDict(self):
        """
        Returns current puzzle as a python dict

        Returns:
            dict: Puzzle in dict
        """
        argList = {}
        for squareKey, squareValue in self.squares.items():
            if squareValue.squareType is SquareTypeEnum.InputLocked and len(squareValue.text()) > 0:
                argList[squareKey] = squareValue.text()
        return argList

    def onSquareChangeEvent(self):
        for puzzleSquares in self.squares.values():
            puzzleSquares._refresh()

    def toggleLock(self):
        puzzleValid = grabPuzzleFrame().isValid
        solveBtn = grabWidget(QPushButton, 'solveBtn')
        setBtn = grabWidget(QPushButton, 'setPuzzleBtn')
        if puzzleValid == ValidityEnum.Invalid or grabMainWindow().status == AppStatusEnum.Locked:
            for square in self.squares.values():
                square.setReadOnly(False)
                square.squareType = SquareTypeEnum.InputUnlocked
                square.setReadOnly(False)
                square.setProperty('squareType','InputUnlockedAndValid')
                self.style().polish(self)
                self.style().unpolish(self)
                self.update()
                      
            grabMainWindow().status = AppStatusEnum.Unlocked
            solveBtn._disableMe()
            setBtn.setText("Lock")
        elif grabMainWindow().status == AppStatusEnum.Unlocked and puzzleValid == ValidityEnum.Valid:
            for square in self.squares.values():
                if len(square.text()) > 0 and square.squareType == SquareTypeEnum.InputUnlocked:
                    square.squareType = SquareTypeEnum.InputLocked
                    square.setReadOnly(True)
                if len(square.text()) == 0:
                    square.squareType = SquareTypeEnum.UserSet
            grabMainWindow().status = AppStatusEnum.Locked
            solveBtn._enableMe()
            setBtn.setText("Locked")
        self.onSquareChangeEvent()

    def _setNewFocus(self, oldKey, newKey):

        returnVal = False
        if oldKey in self.squares and oldKey != newKey:
            self.squares[oldKey].clearFocus()
        elif oldKey == None:
            for key in self.squares:
                if key != newKey and self.squares[key].hasFocus():

                    self.squares[key].clearFocus()
                    break

        if newKey in self.squares:
            self.squares[newKey].setFocus()
            returnVal = True
            self._setFocusCursor(newKey)

        return returnVal

    def _setFocusCursor(self, key=None):
        if key == None:
            key = self.objectName()
        self.squares[key].setCursorPosition(0)

    def _initSquares(self):
        squares = {}
        for squareKey in sudokuDefs.squares:
            squares[squareKey] = PuzzleSquare(self, squareKey)

            self.puzzleLayout.addWidget(
                squares[squareKey],
                3+sudokuDefs.rows.index(squareKey[0]) +
                floor(sudokuDefs.rows.index(squareKey[0])/3.),
                3+sudokuDefs.columns.index(squareKey[1]) +
                floor(sudokuDefs.columns.index(squareKey[1])/3.),
                1, 1)
            squares[squareKey].installEventFilter(self)
        self.squares = squares

    def _initHeaders(self):

        rowHeaders = {}
        for rowKey in sudokuDefs.rows:

            rowHeaders[rowKey] = PuzzleHeader(
                self, rowKey,
                'RowHeader' + rowKey)
            self.puzzleLayout.addWidget(
                rowHeaders[rowKey],
                3+sudokuDefs.rows.index(rowKey) + floor(sudokuDefs.rows.index(rowKey)/3.), 1, 1, 1)
        self.rowHeaders = rowHeaders

        colHeaders = {}
        for colKey in sudokuDefs.columns:
            colHeaders[colKey] = PuzzleHeader(
                self, colKey,
                'ColumnHeader' + colKey)
            self.puzzleLayout.addWidget(
                colHeaders[colKey],
                1, 3+sudokuDefs.columns.index(colKey) + floor(sudokuDefs.columns.index(colKey)/3.), 1, 1)
        self.colHeaders = colHeaders

    def _initBorderLines(self):
        # LineBorders
        lineBorders = {}
        for vertLineNum in ['1', '3', '6', '9']:
            lineBorders[vertLineNum] = PuzzleBorderLine(
                self,
                QFrame.Shape.VLine,
                'verticalLine'+vertLineNum)

            self.puzzleLayout.addWidget(
                lineBorders[vertLineNum],
                1, 2+(4*(['1', '3', '6', '9'].index(vertLineNum))), 13, 1)

        for horizLineNum in ['A', 'C', 'F', 'I']:
            lineBorders[horizLineNum] = PuzzleBorderLine(
                self,
                QFrame.Shape.HLine,
                'horizontalLine'+horizLineNum)
            self.puzzleLayout.addWidget(
                lineBorders[horizLineNum],
                2+(4*['A', 'C', 'F', 'I'].index(horizLineNum)), 1, 1, 13)

        self.lineBorders = lineBorders

    def eventFilter(self, source, event):
        if isinstance(source, PuzzleSquare) and event.type() == event.Type.KeyPress:
            sourceObjectName = source.objectName()
            rowNum = sourceObjectName[0]
            colNum = sourceObjectName[1]
            if event.key() == Qt.Key.Key_Up:
                newFocusCol = colNum
                newFocusRow = sudokuDefs.rows[
                    (sudokuDefs.rows.index(rowNum)-1) % len(sudokuDefs.rows)]
                return self._setNewFocus(sourceObjectName, newFocusRow+newFocusCol)
            elif event.key() == Qt.Key.Key_Down:
                newFocusCol = colNum
                newFocusRow = sudokuDefs.rows[
                    (sudokuDefs.rows.index(rowNum)+1) % len(sudokuDefs.rows)]
                return self._setNewFocus(sourceObjectName, newFocusRow+newFocusCol)
            elif event.key() == Qt.Key.Key_Tab or event.key() == Qt.Key.Key_Right:
                newKey = sudokuDefs.squares[
                    (sudokuDefs.squares.index(sourceObjectName)+1) % len(sudokuDefs.squares)]
                return self._setNewFocus(sourceObjectName, newKey)
            elif event.key() == Qt.Key.Key_Left:
                newKey = sudokuDefs.squares[
                    (sudokuDefs.squares.index(sourceObjectName)-1) % len(sudokuDefs.squares)]
                return self._setNewFocus(sourceObjectName, newKey)
            else:
                return False
        elif isinstance(source, PuzzleSquare) and ((event.type() == QEvent.Type.FocusIn)
                                                   or (event.type() == QEvent.Type.MouseButtonRelease)):

            if source.isEnabled() == True:
                sourceObjectName = source.objectName()
                returnVal = self._setNewFocus(None, sourceObjectName)
                self._setFocusCursor(sourceObjectName)
                return False
            else:
                return False
        return False
    
    def resetPuzzle(self):
        puzzleFrame = grabPuzzleFrame()
        for squareVal in puzzleFrame.squares.values():
            squareVal._onResetAction()
        
class PuzzleSquare(QLineEdit):

    @cached_property
    def _sizePolicy(self):
        # Set the size policy so constant across all
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHorizontalStretch(0)

        sizePolicy.setHeightForWidth(False)
        return sizePolicy

    @property
    def squareType(self):
        return self._squareType

    @squareType.setter
    def squareType(self, squareValueSetting):
        if self._squareType != squareValueSetting:
            self._squareType = squareValueSetting
        self.setStatusTip('{name}: {status}'.format(
            name=self.name, status=self.squareType.name))

    @property
    def name(self):
        return self.objectName()

    @cached_property
    def neighborKeys(self):
        return self._neighborKeys

    @property
    def neighbors(self):

        squares = grabPuzzleSquares()
        outArg = {}
        for squareKey in self.neighborKeys:
            outArg[squareKey] = squares[squareKey]
        return outArg

    @property
    def nextSquare(self):
        return self._nextSquare

    @property
    def lastSquare(self):
        return self._lastSquare

    @property
    def isValid(self):
        myValue = self.text()
        retVal = ValidityEnum.Valid
        if len(myValue) > 0:
            for neighborSquare in self.neighbors.values():
                if myValue in neighborSquare.text():
                    retVal = ValidityEnum.Invalid
                    break
        else:
            retVal = ValidityEnum.NoStatement

        if self._isValid != retVal:
            self._isValid = retVal
            self.setToolTip('Square {name}: {tip}'.format(
                name=self.name, tip=retVal.name))
        self._isValid = retVal
        return self._isValid

    def __init__(self, parent, objectName=None):
        super(PuzzleSquare, self).__init__(parent, objectName=None)

        self.setObjectName(objectName)
        self.setParent(parent)
        self.setSizePolicy(self.sizePolicy())
        self.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.setAcceptDrops(True)
        self.setInputMethodHints(Qt.InputMethodHint.ImhDigitsOnly)
        self.setInputMask("d")
        self.setText("")
        self.setMaxLength(1)
        self.setFrame(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setDragEnabled(True)
        self.setPlaceholderText("")
        self.setClearButtonEnabled(False)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        self._nextSquare = sudokuDefs.nextSquare(self.name)
        self._lastSquare = sudokuDefs.lastSquare(self.name)
        self._isValid = ValidityEnum.Valid
        self._neighborKeys = sudokuDefs.neighbors(self.name)
        self._squareType = SquareTypeEnum.InputUnlocked
        self.setProperty('squareType','InputUnlockedAndValid')

        self.setStyleSheet(
            """
            QLineEdit[squareType="InputUnlockedAndValid"]{
                color:	rgb(255,140,0);
                font-weight: bold;
                font-style: normal;
                background-color: rgb(30, 30, 30);
                border-color: rgb(255, 140, 0)}
            QLineEdit[squareType="InputUnlockedAndInvalid"] {
                color: rgb(255, 0, 0);
                font-weight: normal;
                font-style: italic}
            QLineEdit[squareType="InputLockedAndValid"]{
                color: rgb(255, 140, 0);
                font-weight: bold;
                font-style: normal;
                background-color: rgb(30, 30, 30);}
            QLineEdit[squareType="UserSetAndValid"]{
                color:	rgb(212,255,200);
                font-weight: normal;
                font-style: regular}
            QLineEdit[squareType="SolvedAndValid"] {
                color: rgba(0, 255, 0,204);
                font-weight: normal;
                font-style: regular}
            QLineEdit[isNeighbor="true"]{
                background-color: rgba(90, 3, 114, 0.3)};
            """
        )

        self.setToolTip('Square {name}: {tip}'.format(
            name=self.name, tip=self._isValid.name))
        self.textEdited.connect(self.onChanged)
        self.textEdited.connect(grabPuzzleFrame().onSquareChangeEvent)

    def focusInEvent(self, evnt):
        currentSquare = grabCurrentSquare()
        allSquares    = grabPuzzleSquares()
        grabMainWindow().uiStatusBar.showMessage(currentSquare.objectName())
        for neighborKey in currentSquare.neighborKeys:
            allSquares[neighborKey].setProperty("isNeighbor","true")
            allSquares[neighborKey].style().polish(allSquares[neighborKey])
            allSquares[neighborKey].style().unpolish(allSquares[neighborKey])
        for nonNeighborKey in list(set(allSquares.keys())-set(currentSquare.neighborKeys)-set(currentSquare.objectName())):
            allSquares[nonNeighborKey].setProperty("isNeighbor","false")
            allSquares[nonNeighborKey].style().polish(allSquares[nonNeighborKey])
            allSquares[nonNeighborKey].style().unpolish(allSquares[nonNeighborKey])
        return super().focusInEvent(evnt)

    def onChanged(self, newTextStr):
        _prevText = self.text()
        _newText = newTextStr
        _newTextStr = list([val for val in _newText if val.isnumeric()])
        if not _newTextStr:
            self.setText("")
            _nextKey = self.lastSquare
        else:
            self.setText(newTextStr[0])
            _nextKey = self.nextSquare

        # Jump to next square in tab order
        grabPuzzleFrame()._setNewFocus(self.objectName(), _nextKey)

    def _onResetAction(self):
        self.setEnabled(True)
        self.setText('')
        self.squareType = SquareTypeEnum.InputUnlocked
        self._isValid = ValidityEnum.Valid
        self.setProperty('squareType',"InputUnlockedAndValid")
        self.style().unpolish(self)
        self.style().polish(self)

    def _refresh(self):
        isValid = self.isValid
        if isValid == ValidityEnum.Valid and self.squareType == SquareTypeEnum.InputUnlocked:
            self.setProperty('squareType',"InputUnlockedAndValid")
            '''
            self.setStyleSheet("QLineEdit {"
                               "color:	rgb(255,140,0);"
                               "font-weight: bold;"
                               "font-style: regular;}")
                               '''
        elif isValid == ValidityEnum.Invalid and self.squareType == SquareTypeEnum.InputUnlocked:
            self.setProperty('squareType',"InputUnlockedAndInvalid")
            '''
            self.setStyleSheet("QLineEdit {"
                               "color:	rgb(255,0,0);"
                               "font-style: italic;}")
            '''
        elif isValid == ValidityEnum.Valid and self.squareType == SquareTypeEnum.InputLocked:
            self.setProperty('squareType',"InputLockedAndValid")
            '''
            self.setStyleSheet("QLineEdit {"
                               "color:	rgb(255,140,0);"
                               "font-weight: bold;"
                               "font-style: normal;"
                               "background-color: rgb(30,30,30);"
                               "border-color: rgb(255,140,0);}")
            '''
        elif (isValid == ValidityEnum.Valid or isValid == ValidityEnum.NoStatement) and self.squareType == SquareTypeEnum.UserSet:
            self.setProperty('squareType',"UserSetAndValid")
            '''
            self.setStyleSheet("QLineEdit {"
                               "color:	rgb(212,255,200);"
                               "font-weight: normal;"
                               "font-style: regular;}")
            '''
        elif isValid == ValidityEnum.Valid and self.squareType == SquareTypeEnum.Solved:
            self.setProperty('squareType',"SolvedAndValid")
            '''
            self.setStyleSheet("QLineEdit {"
                               "color:	rgba(0,255,0,204);"
                               "font-weight: normal;"
                               "font-style: regular;}")
            '''
        self.style().unpolish(self)
        self.style().polish(self)
        
        self.setToolTip('Square {name}: {valid} - {status}'.format(
            name=self.name, valid=self._isValid.name, status=self._squareType.name))


class PuzzleBorderLine(QFrame):
    def __init__(self, parent, frameShape, objectName=None):
        super(PuzzleBorderLine, self).__init__(parent, objectName=None)
        self.setObjectName(objectName)
        self.setParent(parent)
        self.setLineWidth(3)
        self.setFrameShape(frameShape)


class PuzzleHeader(QLabel):
    def __init__(self, parent, text=None, objectName=None):
        super(PuzzleHeader, self).__init__(parent, text=None,  objectName=None)

        headerFont = QFont()
        headerFont.setPointSize(12)
        headerFont.setBold(True)

        self.setObjectName(objectName)
        self.setParent(parent)
        self.setText('  ' + text + '  ')
        self.setScaledContents(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(headerFont)
        self.setStyleSheet("QLabel {" 
            "background-color: rgb(70,70,70);" \
            "border-color: rgb(70,70,70)}")

