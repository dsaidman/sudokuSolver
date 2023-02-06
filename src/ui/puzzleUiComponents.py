from functools import cached_property
from math import floor

from appHelpers import (AppStatusEnum, SquareTypeEnum, ThemeEnum, ValidityEnum,
                        grabAppInstance, grabMainWindow, grabPuzzleFrame,
                        grabPuzzleSquares, grabUiFrame, grabWidget)
from puzzleHelpers import sudokuParams as params
from PyQt5 import QtCore, QtGui, QtWidgets
_fontFamily = "Segoi Ui"

class PuzzleFrame(QtWidgets.QFrame):

    
    @property
    def squareCount(self):
        cnt = 0
        for square in self.squares.values():
            cnt = cnt + 1 if len(square.text()) > 0 else cnt
        return cnt

    @property
    def validSquareCount(self):
        cnt = 0
        for square in self.squares.values():
            if len(square.text()) > 0 and square.isValid == ValidityEnum.Valid:
                cnt = cnt + 1
        return cnt

    @property
    def isValid(self):
        for square in self.squares.values():

            if square.isValid == ValidityEnum.Invalid:
                self._isValid = ValidityEnum.Invalid
                return self._isValid
        self._isValid = ValidityEnum.Valid
        return self._isValid
    
    def __init__(self, parent):
        super(PuzzleFrame, self).__init__(parent)
        self.setParent(parent)
        # self.setGeometry(QtCore.QRect(10, 130, 911, 691))

        self.setAutoFillBackground(False)
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setLineWidth(3)
        self.setObjectName("puzzleFrame")

        self.puzzleLayout = QtWidgets.QGridLayout()
        self.puzzleLayout.setObjectName("puzzleLayout")
        self.puzzleLayout.setSpacing(0)
        self.puzzleLayout.setContentsMargins(0, 0, 0, 0)

        masterLayout = grabWidget(QtWidgets.QVBoxLayout, 'masterLayout')
        masterLayout.addLayout(self.puzzleLayout)

        self._initSquares()
        self._initHeaders()
        self._initBorderLines()
        
    def asString(self):
        argList = []
        for squareKey, squareValue in self.squares.items():
            if squareValue.squareType is SquareTypeEnum.InputLocked and len(squareValue.text()) > 0:

                argList.append(
                    '--{key}={val}'.format(key=squareKey, val=squareValue.text()))
        return ' '.join(argList)
    
    def asDict(self):
        argList = {}
        for squareKey, squareValue in self.squares.items():
            if squareValue.squareType is SquareTypeEnum.InputLocked and len(squareValue.text()) > 0:
                argList[squareKey] = squareValue.text()
        return argList
        
    
    def _refresh(self):
        self._applyFormatting()

    def _applyFormatting(self):
        for puzzleSquares in self.squares.values():
            puzzleSquares._applyFormatting()
        
    def toggleLock(self):
        puzzleValid = grabPuzzleFrame().isValid
        solveBtn = grabWidget(QtWidgets.QPushButton, 'solveBtn')
        setBtn = grabWidget(QtWidgets.QPushButton, 'setPuzzleBtn')
        if puzzleValid == ValidityEnum.Invalid or grabMainWindow().status == AppStatusEnum.Locked:
            for square in self.squares.values():
                square.setReadOnly(False)
                if square.squareType == SquareTypeEnum.InputLocked:
                    square.squareType = SquareTypeEnum.InputUnlocked
                    square.setReadOnly(False)
            grabMainWindow().status = AppStatusEnum.Unlocked
            solveBtn._disableMe()
            setBtn.setText("LOCK PUZZLE")
        elif grabMainWindow().status == AppStatusEnum.Unlocked and puzzleValid == ValidityEnum.Valid:
            for square in self.squares.values():
                if len(square.text()) > 0 and square.squareType == SquareTypeEnum.InputUnlocked:
                    square.squareType = SquareTypeEnum.InputLocked
                    square.setReadOnly(True)
                if len(square.text()) == 0:
                    square.squareType = SquareTypeEnum.UserSet
            grabMainWindow().status = AppStatusEnum.Locked
            solveBtn._enableMe()
            setBtn.setText("LOCKED")
        self._refresh()
        
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
        self.squares[key].end(False)
        self.squares[key].home(True)

    def _initSquares(self):
        squares = {}
        for squareKey in params.squares:
            squares[squareKey] = PuzzleSquare(self, squareKey)

            self.puzzleLayout.addWidget(
                squares[squareKey],
                3+params.rows.index(squareKey[0]) +
                floor(params.rows.index(squareKey[0])/3.),
                3+params.columns.index(squareKey[1]) +
                floor(params.columns.index(squareKey[1])/3.),
                1, 1)
            squares[squareKey].installEventFilter(self)
        self.squares = squares

    def _initHeaders(self):

        rowHeaders = {}
        for rowKey in params.rows:

            rowHeaders[rowKey] = PuzzleHeader(
                self, rowKey,
                'RowHeader' + rowKey)
            self.puzzleLayout.addWidget(
                rowHeaders[rowKey],
                3+params.rows.index(rowKey) + floor(params.rows.index(rowKey)/3.), 1, 1, 1)
        self.rowHeaders = rowHeaders

        colHeaders = {}
        for colKey in params.columns:
            colHeaders[colKey] = PuzzleHeader(
                self, colKey,
                'ColumnHeader' + colKey)
            self.puzzleLayout.addWidget(
                colHeaders[colKey],
                1, 3+params.columns.index(colKey) + floor(params.columns.index(colKey)/3.), 1, 1)
        self.colHeaders = colHeaders

    def _initBorderLines(self):
        # LineBorders
        lineBorders = {}
        for vertLineNum in ['1', '3', '6', '9']:
            lineBorders[vertLineNum] = PuzzleBorderLine(
                self,
                QtWidgets.QFrame.VLine,
                'verticalLine'+vertLineNum)

            self.puzzleLayout.addWidget(
                lineBorders[vertLineNum],
                1, 2+(4*(['1', '3', '6', '9'].index(vertLineNum))), 13, 1)

        for horizLineNum in ['A', 'C', 'F', 'I']:
            lineBorders[horizLineNum] = PuzzleBorderLine(
                self,
                QtWidgets.QFrame.HLine,
                'horizontalLine'+horizLineNum)
            self.puzzleLayout.addWidget(
                lineBorders[horizLineNum],
                2+(4*['A', 'C', 'F', 'I'].index(horizLineNum)), 1, 1, 13)

        lineBorders['horizontalLine0'] = PuzzleBorderLine(
            self,
            QtWidgets.QFrame.HLine,
            'horizontalLine0')
        self.puzzleLayout.addWidget(
            lineBorders['horizontalLine0'], 0, 3, 1, 11)

        lineBorders['verticalLine0'] = PuzzleBorderLine(
            self,
            QtWidgets.QFrame.VLine,
            'verticalLine0')
        self.puzzleLayout.addWidget(
            lineBorders['verticalLine0'], 3, 0, 11, 1)
        self.lineBorders = lineBorders

    def eventFilter(self, source, event):

        if isinstance(source, PuzzleSquare) and event.type() == QtGui.QKeyEvent.KeyPress:
            sourceObjectName = source.objectName()
            rowNum = sourceObjectName[0]
            colNum = sourceObjectName[1]

            if event.key() == QtCore.Qt.Key_Up:
                newFocusCol = colNum
                newFocusRow = params.rows[
                    (params.rows.index(rowNum)-1) % len(params.rows)]

                return self._setNewFocus(sourceObjectName, newFocusRow+newFocusCol)
            elif event.key() == QtCore.Qt.Key_Down:
                newFocusCol = colNum
                newFocusRow = params.rows[
                    (params.rows.index(rowNum)+1) % len(params.rows)]
                return self._setNewFocus(sourceObjectName, newFocusRow+newFocusCol)

            elif event.key() == QtCore.Qt.Key_Tab or event.key() == QtCore.Qt.Key_Right:
                newKey = params.squares[
                    (params.squares.index(sourceObjectName)+1) % len(params.squares)]
                return self._setNewFocus(sourceObjectName, newKey)
            elif event.key() == QtCore.Qt.Key_Left:
                newKey = params.squares[
                    (params.squares.index(sourceObjectName)-1) % len(params.squares)]
                return self._setNewFocus(sourceObjectName, newKey)
            else:
                return False
        elif isinstance(source, PuzzleSquare) and ((event.type() == QtCore.QEvent.Type.FocusIn) or (event.type() == QtCore.QEvent.Type.MouseButtonRelease)):
           
            if source.isEnabled() == True:
                sourceObjectName = source.objectName()
                returnVal = self._setNewFocus(None, sourceObjectName)
                self._setFocusCursor(sourceObjectName)
                return returnVal
            else:
                return False
        return False
    
class PuzzleSquare(QtWidgets.QLineEdit):
    
    @cached_property
    def _sizePolicy(self):
        # Set the size policy so constant across all
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Ignored,
            QtWidgets.QSizePolicy.Expanding)
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

        self.setSizePolicy(self._sizePolicy)

        self.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.setAcceptDrops(True)

        self.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.setInputMask("D")
        self.setText("")
        self.setMaxLength(1)
        self.setFrame(True)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setDragEnabled(True)
        self.setPlaceholderText("")
        self.setClearButtonEnabled(False)

        self._nextSquare = params.nextSquare(self.name)
        self._lastSquare = params.lastSquare(self.name)
        self._isValid = ValidityEnum.Valid
        self._theme = ThemeEnum.Dark
        self._neighborKeys = params.neighbors(self.name)
        self._squareType = SquareTypeEnum.InputUnlocked
        self.setToolTip('Square {name}: {tip}'.format(
            name=self.name, tip=self._isValid.name))
        self.textEdited.connect(self._onTextChange)
        self.textEdited.connect(grabPuzzleFrame()._refresh)

    def _onTextChange(self, newTextStr):
        _prevText = self.text()
        _newText = newTextStr
        _newTextStr = list([val for val in _newText if val.isnumeric()])
        if not _newTextStr:
            self.setText("")
            _nextKey = self.lastSquare

        else:
            self.setText(newTextStr[0])
            _nextKey = self.nextSquare
        grabPuzzleFrame()._setNewFocus(self.objectName(),_nextKey)
        #theNextSquare = grabWidget(QtWidgets.QLineEdit, _nextKey)
        
        
    def _resetAction(self):
        self.setEnabled(True)
        self.setText('') 
        self.squareType = SquareTypeEnum.InputUnlocked
        self._isValid = ValidityEnum.Valid
        self._applyFormatting()


    def _applyFormatting(self):
        isValid = self._isValid
        
        if isValid == ValidityEnum.Valid and self.squareType == SquareTypeEnum.InputUnlocked:
            self.setStyleSheet("QLineEdit {"
                               "color:	rgb(255,140,0);"
                               "font-weight: bold;"
                               "font-size: 14pt;"
                               "font-style: regular;}")
        elif isValid == ValidityEnum.Invalid and self.squareType == SquareTypeEnum.InputUnlocked:
            self.setStyleSheet("QLineEdit {"
                               "color:	rgb(255,0,0);"
                               "font-weight: bold;"
                               "font-size: 14pt;"
                               "font-style: italic;}")
        elif isValid == ValidityEnum.Valid and self.squareType == SquareTypeEnum.InputLocked:
            self.setStyleSheet("QLineEdit {"
                               "color:	rgb(255,140,0);"
                               "font-weight: bold;"
                               "font-size: 14pt;"
                               "font-style: normal;"
                               "background-color: rgb(30,30,30);"
                               "border-color: rgb(255,140,0);}")
        elif (isValid == ValidityEnum.Valid or isValid == ValidityEnum.NoStatement) and self.squareType == SquareTypeEnum.UserSet:
            self.setStyleSheet("QLineEdit {"
                               "color:	rgb(212,255,200);"
                               "font-weight: normal;"
                               "font-size: 12pt;"
                               "font-style: regular;}")
        elif isValid == ValidityEnum.Valid and self.squareType == SquareTypeEnum.Solved:
            self.setStyleSheet("QLineEdit {"
                               "color:	rgb(0,255,0);"
                               "font-weight: normal;"
                               "font-size: 12pt;"
                               "font-style: regular;}")
        self.setToolTip('Square {name}: {valid} - {status}'.format(
            name=self.name, valid=self._isValid.name, status=self._squareType.name))


class PuzzleBorderLine(QtWidgets.QFrame):
    def __init__(self, parent, frameShape, objectName=None):
        super(PuzzleBorderLine, self).__init__(parent, objectName=None)
        self.setObjectName(objectName)
        self.setParent(parent)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setLineWidth(1)
        self.setFrameShape(frameShape)

class PuzzleHeader(QtWidgets.QLabel):
    def __init__(self, parent, text=None, objectName=None):
        super(PuzzleHeader, self).__init__(parent, text=None,  objectName=None)

        self.setObjectName(objectName)
        self.setParent(parent)
        self.setText(text)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setStyleSheet("font-family: Segoe Ui; font-weight: bold; font-size: 14pt")
