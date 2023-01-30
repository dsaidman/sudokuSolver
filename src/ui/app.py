# -*- coding: utf-8 -*-

from enum import Enum, auto
from functools import cached_property, partial, lru_cache
from math import floor
from string import ascii_uppercase, digits

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor, QPalette

from puzzleHelpers import SudokuParams
from appHelpers import AppStatusEnum, SquareTypeEnum, ValidityEnum, GuiPalette, ThemeEnum
import os
import configparser
from glob import glob
from re import search as re_search
from subprocess import run as sp_run

# Some gui globals with default widget vals
_tooltip = ""
_statustip = ""
_whatsthis = ""
_accessibleName = ""
_fontFamily = 'Segoi U'
_guiHeightPixels = 1100
_guiWidthPixels = 950
_basepath = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..','..'))
params = SudokuParams()

# UI MainWindow


class AppMainWindow(QtWidgets.QMainWindow):
    

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
        self.setWindowModality(QtCore.Qt.NonModal)
        #self.resize(_guiWidthPixels, _guiHeightPixels)
        self.setFont(QtGui.QFont("Segoi Ui", 12))
        self.setWindowTitle("SudokuSolverApp")
        self.setDockNestingEnabled(True)
        self._status = AppStatusEnum.Unlocked
        self.resizeApp()

        self.centralWidget = QtWidgets.QWidget(parent=self)
        self.centralWidget.setObjectName("centralWidget")

        # Master Layout
        masterLayout = QtWidgets.QVBoxLayout()
        masterLayout.setParent(self.centralWidget)
        masterLayout.setObjectName('masterLayout')

        self.centralWidget.setLayout(masterLayout)
        anotherLayout = QtWidgets.QGridLayout()
        anotherLayout.setSpacing(0)
        anotherLayout.setContentsMargins(0, 0, 0, 0)
        masterLayout.addLayout(anotherLayout)

        # Title Label
        self.titleLabel = QtWidgets.QLabel(self.centralWidget)
        # self.titleLabel.setGeometry(QtCore.QRect(0, 0, _guiWidthPixels, 100))
        self.titleLabel.setFont(QtGui.QFont(
            _fontFamily, 40, 50, False))
        self.titleLabel.setAutoFillBackground(True)
        self.titleLabel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.titleLabel.setText("SUDOKU SOLVER")
        self.titleLabel.setScaledContents(True)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        anotherLayout.addWidget(self.titleLabel, 0, 0,
                                alignment=QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.puzzleFrame = PuzzleFrame(self.centralWidget)
        self.uiFrame = UiPanel(self.centralWidget)

        # make master layout widget for nestthig the layouts
        anotherLayout.addWidget(self.titleLabel, 0, 0,
                                alignment=QtCore.Qt.AlignmentFlag.AlignVCenter)
        masterLayout.addWidget(self.puzzleFrame,
                               alignment=QtCore.Qt.AlignmentFlag.AlignVCenter)
        masterLayout.addWidget(self.uiFrame,
                               alignment=QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.uiFrame.raise_()
        # self.puzzleInfoLabel.raise_()
        # self.solvePuzzleBtn.raise_()
        self.puzzleFrame.raise_()
        self.titleLabel.raise_()
        #

        self.setCentralWidget(self.centralWidget)

        self.menuBar = MenuBar(self)
        w = self.windowHandle()
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    @property
    def screenSize(self):
        appDesktop = QtWidgets.QApplication.desktop()

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
        for idx in range(len(params.squares)-1):
            MainWindow.setTabOrder(
                self.puzzleFrame.squares[params.squares[idx]],
                self.puzzleFrame.squares[params.squares[idx+1]])
        MainWindow.setTabOrder(
            self.puzzleFrame.squares[params.squares[-1]],
            self.puzzleFrame.squares[params.squares[0]])

    def retranslateUi(self, MainWindow):
        pass


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

    @property
    def asArgString(self):
        argList = []
        for squareKey, squareValue in self.squares.items():
            if squareValue.squareType is SquareTypeEnum.InputLocked and len(squareValue.text())>0:
                
                argList.append('--{key}={val}'.format(key=squareKey,val=squareValue.text()))
        return ' '.join(argList)
    
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

    def refresh(self):
        for square in self.squares.values():
            square._applyFormatting()

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
            grabMainWindow().status = AppStatusEnum.Locked
            solveBtn._enableMe()
            setBtn.setText("LOCKED")
        self.refresh()

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

    def _setFocusCursor(self, key):
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
        elif isinstance(source, PuzzleSquare) and ((event.type() == QtCore.QEvent.Type.FocusIn) or (event.type() == QtCore.QEvent.Type.MouseButtonPress)):
            sourceObjectName = source.objectName()
            returnVal = self._setNewFocus(None, sourceObjectName)
            self._setFocusCursor(sourceObjectName)
            return returnVal

        return False

    
class PuzzleSquare(QtWidgets.QLineEdit):

    @cached_property
    def _font(self):
        return QtGui.QFont(_fontFamily, 12)

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

        return retVal

    def __init__(self, parent, objectName=None):
        super(PuzzleSquare, self).__init__(parent, objectName=None)

        self.setObjectName(objectName)
        self.setParent(parent)

        self.setSizePolicy(self._sizePolicy)
        self.setFont(self._font)

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
        self.textChanged.connect(self._onTextChange)
        self.textChanged.connect(grabPuzzleFrame().refresh)
        #self.textEdited.connect(self._setSolution)

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
            self.clearFocus()
        self.clearFocus()
        grabWidget(QtWidgets.QLineEdit, _nextKey).setFocus()

    def _applyFormatting(self):
        isValid = self.isValid
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
        elif isValid == ValidityEnum.Valid and self.squareType == SquareTypeEnum.UserSet:
            self.setStyleSheet("QLineEdit {"
                               "color:	rgb(212,212,200);"
                               "font-weight: normal;"
                               "font-size: 12pt;"
                               "font-style: regular;}")
        elif isValid == ValidityEnum.Valid and self.squareType == SquareTypeEnum.Solved:
            self.setStyleSheet("QLineEdit {"
                               "color:	green;"
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
        self.setLineWidth(3)
        self.setFrameShape(frameShape)


class PuzzleHeader(QtWidgets.QLabel):

    # Set the font so constant across all
    @cached_property
    def _font(self):
        return QtGui.QFont(_fontFamily, 20, 75, False)

    def __init__(self, parent, text=None, objectName=None):
        super(PuzzleHeader, self).__init__(parent, text=None,  objectName=None)

        self.setObjectName(objectName)
        self.setParent(parent)
        self.setFont(self._font)
        self.setToolTip(_tooltip)
        self.setStatusTip(_statustip)
        self.setWhatsThis(_whatsthis)
        self.setAccessibleName(_accessibleName)
        self.setAccessibleDescription(_accessibleName)
        self.setText(text)
        self.setAlignment(QtCore.Qt.AlignCenter)


class PuzzleInfoLabel(QtWidgets.QLabel):

    def __init__(self, parent, objectName="puzzleInfoLabel"):
        super(PuzzleInfoLabel, self).__init__(
            parent, objectName="puzzleInfoLabel")

        self.setParent(parent)
        self.setObjectName(objectName)

        puzzleLabelFont = QtGui.QFont(_fontFamily, 14)
        puzzleLabelFont.setBold(False)
        puzzleLabelFont.setItalic(False)
        puzzleLabelFont.setWeight(75)

        # self.setGeometry(QtCore.QRect(391, 851, 531, 38))  # Change this
        self.setText("0 OF 17 SQUARES SET")
        self.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)

        # Connect the puzzle squares to update text when changed. Cant do before because this class didnt exist yet

        for theSquare in grabPuzzleSquares().values():
            theSquare.textChanged.connect(self.refresh)

    def refresh(self):

        puzzleFrame = grabWidget(QtWidgets.QFrame, 'puzzleFrame')
        numFilledSquares = puzzleFrame.validSquareCount
        theText = str(numFilledSquares) + " OF 17 SQUARES SET"
        puzzleIsValid = puzzleFrame.isValid

        setPuzzleBtn = grabWidget(QtWidgets.QPushButton, 'setPuzzleBtn')

        if puzzleIsValid == ValidityEnum.Invalid:
            self.setStyleSheet(
                "QLabel{ color: rgb(255, 0, 0); font-style: italic;font-weight: regular;font-size: 18pt;}")
            setPuzzleBtn._disableMe()
        elif numFilledSquares >= 17 and puzzleIsValid == ValidityEnum.Valid:
            self.setStyleSheet(
                "QLabel{ color: rgb(255, 140, 0); font-style: regular;font-weight: bold;font-size: 18pt;}")
            theText = theText + ': READY'
            setPuzzleBtn._enableMe()
        elif numFilledSquares < 17 or puzzleIsValid == ValidityEnum.Valid:
            self.setStyleSheet(
                "QLabel{ color: rgb(212,212,200); font-style: normal;font-weight: regular;font-size: 18pt;}")
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
            "QPushButton {color: rgb(212,212,200);""font-weight: bold;}")
        self.setToolTip(
            'Push button to lock the puzzle to be solved')

    def _disableMe(self):
        self.setStyleSheet("QPushButton { color: grey;font-weight: regular;}")
        self.setToolTip(
            'The puzzle can be solved once the minimum number of squares required for a unique solution have been entered')
        self.setEnabled(False)


class SolvePuzzleButton(QtWidgets.QPushButton):
    def __init__(self, parent, objectName='solvePuzzleButton'):
        super(SolvePuzzleButton, self).__init__(
            parent, objectName='solvePuzzleButton')

        self.setParent(parent)
        # self.setGeometry(QtCore.QRect(10, 900, 911, 41))
        self.setFont(QtGui.QFont(_fontFamily, 14))
        self.setText("SOLVE")
        self.setShortcut("")
        self.setObjectName("solveBtn")
        self._disableMe()
        self.clicked.connect(self.solveIt)

    def _enableMe(self):
        self.setEnabled(True)
        self.setStyleSheet("color: green;"
                           "font-weight: bold;")

    def _disableMe(self):
        self.setStyleSheet("color: grey;"
                           "font-weight: regular;")
        self.setEnabled(False)

    def solveIt(self):
        print('Entered solvePuzzle method of solvePuzzleButton!')
        puzzleFrame = grabPuzzleFrame()
        if puzzleFrame.isValid is not ValidityEnum.Valid:
            print('\tPuzzle not valid condition, returning')
            return False
        else:
            argStr = puzzleFrame.asArgString
            currentPath = os.getcwd()
            newRoot = os.path.join(_basepath, 'src', 'solver')
            os.chdir(newRoot)
            _includes = [file for file in glob('*.lua') if file.endswith('lua')]
            includesArg = [' -l {file}'.format(file=luaFile) for luaFile in _includes]
            includesArg = ' '.join(includesArg)
            
            cmd = '{exe} {script} {args}'.format(
                exe='/usr/bin/luajit',
                script='solver.lua',
                # includes=includesArg,
                args=argStr)

            result = sp_run([cmd], capture_output=True, shell=True)
            os.chdir(currentPath)
            self.setSolution(str(result.stdout))
            self.setText('SOLVED')
            self.setEnabled(False)
            infoLabel = grabWidget(QtWidgets.QLabel, 'puzzleInfoLabel')
            infoLabel.setText('81 of 81 SQUARES SET: SOLVED')
            puzzleFrame.refresh()

            
    def setSolution(self, resultStr):
        puzzleSquares = grabPuzzleSquares()
        for puzzleKey in params.squares:
            if puzzleSquares[puzzleKey].squareType is not SquareTypeEnum.InputLocked:
                puzzleSquares[puzzleKey].squareType = SquareTypeEnum.Solved
                txt = str(
                    re_search('({k})=([1-9])'.format(k=puzzleKey), str(resultStr)).group(2))
                
                puzzleSquares[puzzleKey].setText(txt)
            puzzleSquares[puzzleKey].setEnabled(False)
        
            
            
        
class UiPanel(QtWidgets.QFrame):
    def __init__(self, parent, objectName='UIPanel'):
        super(UiPanel, self).__init__(parent, objectName='UIPanel')

        self.setParent(parent)
        self.setObjectName(objectName)

        self.setupUiPanel()

    def setupUiPanel(self):
        self.solvePuzzleBtn = SolvePuzzleButton(parent=self)
        self.puzzleInfoLabel = PuzzleInfoLabel(parent=self)
        self.setPuzzleBtn = SetPuzzleBtn(parent=self)

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
                                0, 1, 4, QtCore.Qt.AlignmentFlag.AlignVCenter)


class MenuBar(QtWidgets.QMenuBar):
    _font = QtGui.QFont(_fontFamily, 8)

    def __init__(self, theMainWindow):
        super(MenuBar, self).__init__(theMainWindow)

        # self.setGeometry(QtCore.QRect(0, 0, 938, 22))

        self.setFont(self._font)
        self.setAcceptDrops(False)
        self.setObjectName("menuBar")

        self.initMenuBarComponents(theMainWindow)
        self.initMenuBarActions(theMainWindow)

        self.fileMenu.addAction(self.importFromIniAction)
        self.setThemeMenu.addAction(self.setLightThemeAction)
        self.setThemeMenu.addAction(self.setDarkThemeAction)
        self.addAction(self.fileMenu.menuAction())
        self.addAction(self.setThemeMenu.menuAction())

        ''' # Connect the theme changed to update the properties
        for square in grabPuzzleSquares().values():
            self.setLightThemeAction.triggered.connect(
                partial(square.themeChanged, ThemeEnum.Light))
            self.setDarkThemeAction.triggered.connect(
                partial(square.themeChanged, ThemeEnum.Dark)) '''

    def initMenuBarComponents(self, theMainWindow):

        self.fileMenu = QtWidgets.QMenu(self)
        self.fileMenu.setFont(self._font)
        self.fileMenu.setToolTip(_tooltip)
        self.fileMenu.setStatusTip(_statustip)
        self.fileMenu.setWhatsThis(_whatsthis)
        self.fileMenu.setAccessibleName(_accessibleName)
        self.fileMenu.setAccessibleDescription(_accessibleName)
        self.fileMenu.setTitle("FILE")
        self.fileMenu.setObjectName("fileMenu")

        self.setThemeMenu = QtWidgets.QMenu(self)
        self.setThemeMenu.setFont(self._font)
        self.setThemeMenu.setToolTip(_tooltip)
        self.setThemeMenu.setStatusTip(_statustip)
        self.setThemeMenu.setWhatsThis(_whatsthis)
        self.setThemeMenu.setAccessibleName(_accessibleName)
        self.setThemeMenu.setAccessibleDescription(_accessibleName)
        self.setThemeMenu.setTitle("THEME")
        self.setThemeMenu.setObjectName("setThemeMenu")

        theMainWindow.setMenuBar(self)

    def initMenuBarActions(self, theMainWindow):

        self.importFromIniAction = QtWidgets.QAction(theMainWindow)
        self.importFromIniAction.setText("&IMPORT FROM INI")
        self.importFromIniAction.setIconText("IMPORT FROM INI")
        self.importFromIniAction.setToolTip("IMPORT FROM INI")
        self.importFromIniAction.setStatusTip(_statustip)
        self.importFromIniAction.setWhatsThis(_whatsthis)
        self.importFromIniAction.setFont(self._font)
        self.importFromIniAction.setMenuRole(
            QtWidgets.QAction.ApplicationSpecificRole)
        self.importFromIniAction.shortcut = QtWidgets.QShortcut(
            QtGui.QKeySequence("Ctrl+I"), self)
        self.importFromIniAction.setObjectName("importFromIniAction")
        self.importFromIniAction.triggered.connect(self.importIni)
        self.importFromIniAction.shortcut.activated.connect(self.importIni)

        puzzleFrame = grabPuzzleFrame()

        self.setLightThemeAction = QtWidgets.QAction(theMainWindow)
        self.setLightThemeAction.setCheckable(True)
        self.setLightThemeAction.setChecked(False)
        self.setLightThemeAction.setText("&LIGHT")
        self.setLightThemeAction.setIconText("LIGHT")
        self.setLightThemeAction.setToolTip("Set Light Mode")
        self.setLightThemeAction.setStatusTip(_statustip)
        self.setLightThemeAction.setWhatsThis(_whatsthis)
        self.setLightThemeAction.setFont(self._font)
        self.setLightThemeAction.shortcut = QtWidgets.QShortcut(
            QtGui.QKeySequence("Ctrl+L"), self)
        self.setLightThemeAction.setMenuRole(QtWidgets.QAction.PreferencesRole)
        self.setLightThemeAction.setShortcutVisibleInContextMenu(False)
        self.setLightThemeAction.setObjectName("setLightThemeAction")
        self.setLightThemeAction.triggered.connect(self.setLightMode)
        self.setLightThemeAction.triggered.connect(puzzleFrame.refresh)
        self.setLightThemeAction.shortcut.activated.connect(self.setLightMode)
        self.setLightThemeAction.shortcut.activated.connect(
            puzzleFrame.refresh)

        self.setDarkThemeAction = QtWidgets.QAction(theMainWindow)
        self.setDarkThemeAction.setCheckable(True)
        self.setDarkThemeAction.setChecked(True)
        self.setDarkThemeAction.setText("&DARK")
        self.setDarkThemeAction.setIconText("DARK")
        self.setDarkThemeAction.shortcut = QtWidgets.QShortcut(
            QtGui.QKeySequence("Ctrl+D"), self)
        self.setDarkThemeAction.setToolTip("Set Dark Mode")
        self.setDarkThemeAction.setStatusTip(_statustip)
        self.setDarkThemeAction.setWhatsThis(_whatsthis)
        self.setDarkThemeAction.setFont(self._font)
        self.setDarkThemeAction.setMenuRole(QtWidgets.QAction.PreferencesRole)
        self.setDarkThemeAction.setObjectName("setDarkThemeAction")
        self.setDarkThemeAction.triggered.connect(self.setDarkMode)
        self.setDarkThemeAction.triggered.connect(puzzleFrame.refresh)
        self.setDarkThemeAction.shortcut.activated.connect(self.setDarkMode)
        self.setDarkThemeAction.shortcut.activated.connect(
            puzzleFrame.refresh)

        self.setLightThemeAction.triggered.connect(
            partial(self.uncheckTheBox, self.setDarkThemeAction))
        self.setDarkThemeAction.triggered.connect(
            partial(self.uncheckTheBox, self.setLightThemeAction))

    def importIni(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Load ini file', os.getcwd(), "Ini file (*.ini)")
        if fname:
            squares = grabPuzzleSquares()
            puzzleIni = configparser.ConfigParser()
            puzzleIni.read(fname)
            puzzleName = list(puzzleIni._sections.keys())[-1]
            puzzleIni._sections[puzzleName]
            for squareKey, squareVal in puzzleIni._sections[puzzleName].items():
                squares[squareKey.upper()].setText(squareVal)
                squares[squareKey.upper()].squareType = SquareTypeEnum.InputUnlocked
            grabPuzzleFrame().toggleLock()
            # squares[squareKey]._applyFormatting()

    def setLightMode(self):
        QtGui.QGuiApplication.setPalette(GuiPalette(ThemeEnum.Light))

    def setDarkMode(self):
        QtGui.QGuiApplication.setPalette(GuiPalette(ThemeEnum.Dark))

    def uncheckTheBox(self, otherBox):
        otherBox.setChecked(False)


def grabWidget(widgetType, widgetName):
    centralWidget = grabMainWindow().centralWidget
    return centralWidget.findChildren(widgetType, widgetName)[0]


def grabAppInstance():
    return QtWidgets.QApplication([])


@lru_cache(typed=False)
def grabMainWindow():
    return [widget for widget in QtWidgets.QApplication.topLevelWidgets() if isinstance(widget, QtWidgets.QMainWindow)][0]


def grabPuzzleFrame():
    return grabWidget(QtWidgets.QFrame, 'puzzleFrame')


def grabUiFrame():
    return grabWidget(QtWidgets.QFrame, 'UIPanel')


def grabPuzzleSquares():
    return grabPuzzleFrame().squares


def getAppStatus():
    return grabMainWindow().status


def changeQtLineEditProp(widget, prop, newVal):
    widget.setProperty(prop, newVal)
    widget.style().unpolish(widget)
    widget.style().polish(widget)
    widget.update()


@lru_cache(typed=False)
def getScreenSize():
    appDesktop = QtWidgets.QApplication.desktop()

    screenRect = appDesktop.screenGeometry()
    height = screenRect.height()
    width = screenRect.width()
    return height, width

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setPalette(GuiPalette(ThemeEnum.Dark))

    MainWindow = AppMainWindow()
    MainWindow.setupUi()
    MainWindow.show()
    sys.exit(app.exec_())
