# -*- coding: utf-8 -*-

from enum import Enum, auto
from functools import cached_property, partial
from math import floor
from string import ascii_uppercase, digits

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor, QPalette

from puzzleHelpers import SudokuParams
from styleUi import GuiPalette, ThemeEnum

# Some gui globals with default widget vals
_tooltip = ""
_statustip = ""
_whatsthis = ""
_accessibleName = ""
_fontFamily = "MS Reference Sans Serif"
_guiHeightPixels = 1100
_guiWidthPixels = 950

params = SudokuParams()


class PuzzleStausEnum(Enum):
    NotReady = auto()
    Locking = auto()
    Ready = auto()
    Solving = auto()
    Solved = auto()

# UI MainWindow


class AppMainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(_guiWidthPixels, _guiHeightPixels)
        MainWindow.setFont(QtGui.QFont(_fontFamily, 12))
        MainWindow.setWindowTitle("SudokuSolverApp")
        MainWindow.setToolTip(_tooltip)
        MainWindow.setStatusTip(_statustip)
        MainWindow.setWhatsThis(_whatsthis)
        MainWindow.setAccessibleName(_accessibleName)
        MainWindow.setAccessibleDescription(_accessibleName)
        MainWindow.setDockNestingEnabled(True)

        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setToolTip(_tooltip)
        self.centralWidget.setStatusTip(_statustip)
        self.centralWidget.setWhatsThis(_whatsthis)
        self.centralWidget.setAccessibleName(_accessibleName)
        self.centralWidget.setAccessibleDescription(_accessibleName)
        self.centralWidget.setObjectName("centralWidget")

        self.centralWidget.puzzleStatus = PuzzleStausEnum.NotReady

        self.titleLabel = QtWidgets.QLabel(self.centralWidget)
        self.titleLabel.setGeometry(QtCore.QRect(0, 0, _guiWidthPixels, 100))
        self.titleLabel.setFont(QtGui.QFont(
            _fontFamily, 40, 50, False))
        self.titleLabel.setToolTip(_tooltip)
        self.titleLabel.setStatusTip(_statustip)
        self.titleLabel.setWhatsThis(_whatsthis)
        self.titleLabel.setAccessibleName(_accessibleName)
        self.titleLabel.setAccessibleDescription(_accessibleName)
        self.titleLabel.setAutoFillBackground(True)
        self.titleLabel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.titleLabel.setText("Sudoku Solver")
        self.titleLabel.setScaledContents(True)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")

        self.puzzleFrame = PuzzleFrame(self.centralWidget)
        self.uiFrame = UiPanel(self.centralWidget)

        # self.titleLabel.raise_()
        self.uiFrame.raise_()
        # self.puzzleInfoLabel.raise_()
        # self.solvePuzzleBtn.raise_()
        self.puzzleFrame.raise_()

        MainWindow.setCentralWidget(self.centralWidget)

        self.menuBar = MenuBar(MainWindow)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        for idx in range(0, 80):
            MainWindow.setTabOrder(
                self.puzzleFrame.squares[params.squares[idx]],
                self.puzzleFrame.squares[params.squares[idx+1]])

    def retranslateUi(self, MainWindow):
        pass


class PuzzleFrame(QtWidgets.QFrame):
    def __init__(self, parent):
        super(PuzzleFrame, self).__init__(parent)
        self.setParent(parent)
        self.setGeometry(QtCore.QRect(10, 130, 911, 691))
        self.setToolTip(_tooltip)
        self.setStatusTip(_statustip)
        self.setWhatsThis(_whatsthis)
        self.setAccessibleName(_accessibleName)
        self.setAccessibleDescription(_accessibleName)
        self.setAutoFillBackground(False)
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setLineWidth(3)
        self.setObjectName("puzzleFrame")

        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 911, 691))
        self.gridLayoutWidget.setToolTip(_tooltip)
        self.gridLayoutWidget.setStatusTip(_statustip)
        self.gridLayoutWidget.setWhatsThis(_whatsthis)
        self.gridLayoutWidget.setAccessibleName(_accessibleName)
        self.gridLayoutWidget.setAccessibleDescription(_accessibleName)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")

        self.puzzleLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.puzzleLayout.setContentsMargins(0, 0, 0, 0)
        self.puzzleLayout.setSpacing(0)
        self.puzzleLayout.setObjectName("puzzleLayout")

        self._setSquares()
        self._setHeaders()
        self._setBorderLines()

        self.puzzleStatus = PuzzleStausEnum.NotReady

    def setFilledSqure(self):
        cnt = 0
        for squareKey in params.squares:
            cnt = cnt+1 if self.squares[squareKey].getText() else cnt

    def getNumFilledSquares(self):
        cnt = 0
        for squareKey in params.squares:
            cnt = cnt+1 if str.isdigit(self.squares[squareKey].text()) else cnt
        return cnt

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
    
    def check(self):
        
        for squareKey in params.squares:
            squareValue = self.squares[squareKey].text()
            isValid = True
            if len(squareValue)>0:
                
                neighbors = params.neighbors(squareKey)
                for neighbor in neighbors:
                    if squareValue in self.squares[neighbor].text():
                        isValid = False
                        self.squares[squareKey].setStyleSheet(
                            "color: rgb(255,0,0); font-weight: bold;")
                        self.squares[neighbor].setStyleSheet(
                            "color: rgb(255,0,0); font-weight: bold;")
            if isValid == True:
                self.squares[squareKey].setStyleSheet(
                    "color: rgb(255,140,0);font-weight: bold;")
    
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
            # if self.squares[newKey].hasFocus() == False:
            self.squares[newKey].setFocus()
            returnVal = True
            self._setFocusCursor(newKey)
            ''' neighbors = params.neighbors(newKey)
            for squareKey in params.squares:
                if squareKey in neighbors:
                    self.squares[squareKey].setStyleSheet(
                        "background-color: grey")
                else:
                    self.squares[squareKey].setStyleSheet(
                        "background-color: black") '''
        return returnVal

    def _setFocusCursor(self, key):
        self.squares[key].setCursorPosition(0)
        self.squares[key].end(False)
        self.squares[key].home(True)

    def _setSquares(self):
        squares = {}
        for squareKey in params.squares:
            squares[squareKey] = PuzzleSquare(self.gridLayoutWidget, squareKey)

            self.puzzleLayout.addWidget(
                squares[squareKey],
                3+params.rows.index(squareKey[0]) +
                floor(params.rows.index(squareKey[0])/3.),
                3+params.columns.index(squareKey[1]) +
                floor(params.columns.index(squareKey[1])/3.),
                1, 1)
            squares[squareKey].installEventFilter(self)
        self.squares = squares

    def _setHeaders(self):

        rowHeaders = {}
        for rowKey in params.rows:

            rowHeaders[rowKey] = PuzzleHeader(
                self.gridLayoutWidget,
                rowKey,
                'RowHeader' + rowKey)
            self.puzzleLayout.addWidget(
                rowHeaders[rowKey],
                3+params.rows.index(rowKey) + floor(params.rows.index(rowKey)/3.), 1, 1, 1)
        self.rowHeaders = rowHeaders

        colHeaders = {}
        for colKey in params.columns:
            colHeaders[colKey] = PuzzleHeader(
                self.gridLayoutWidget,
                colKey,
                'ColumnHeader' + colKey)
            self.puzzleLayout.addWidget(
                colHeaders[colKey],
                1, 3+params.columns.index(colKey) + floor(params.columns.index(colKey)/3.), 1, 1)
        self.colHeaders = colHeaders

    def _setBorderLines(self):
        # LineBorders
        lineBorders = {}
        for vertLineNum in ['1', '3', '6', '9']:
            lineBorders[vertLineNum] = PuzzleBorderLine(
                self.gridLayoutWidget,
                QtWidgets.QFrame.VLine,
                'verticalLine'+vertLineNum)

            self.puzzleLayout.addWidget(
                lineBorders[vertLineNum],
                1, 2+(4*(['1', '3', '6', '9'].index(vertLineNum))), 13, 1)

        for horizLineNum in ['A', 'C', 'F', 'I']:
            lineBorders[horizLineNum] = PuzzleBorderLine(
                self.gridLayoutWidget,
                QtWidgets.QFrame.HLine,
                'horizontalLine'+horizLineNum)
            self.puzzleLayout.addWidget(
                lineBorders[horizLineNum],
                2+(4*['A', 'C', 'F', 'I'].index(horizLineNum)), 1, 1, 13)

        lineBorders['horizontalLine0'] = PuzzleBorderLine(
            self.gridLayoutWidget,
            QtWidgets.QFrame.HLine,
            'horizontalLine0')
        self.puzzleLayout.addWidget(
            lineBorders['horizontalLine0'], 0, 3, 1, 11)

        lineBorders['verticalLine0'] = PuzzleBorderLine(
            self.gridLayoutWidget,
            QtWidgets.QFrame.VLine,
            'verticalLine0')
        self.puzzleLayout.addWidget(
            lineBorders['verticalLine0'], 3, 0, 11, 1)
        self.lineBorders = lineBorders


class PuzzleSquare(QtWidgets.QLineEdit):

    # Set the font so constant across all
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

    def __init__(self, parent, objectName=None):
        super(PuzzleSquare, self).__init__(parent, objectName=None)

        self.setObjectName(objectName)
        self.setParent(parent)

        self.setSizePolicy(self._sizePolicy)
        self.setFont(self._font)

        self.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.setAcceptDrops(True)
        self.setToolTip('Select Position ' + objectName)
        self.setStatusTip(objectName + ' Selected')
        self.setWhatsThis(_whatsthis)
        self.setAccessibleName(_accessibleName)
        self.setAccessibleDescription(_accessibleName)
        self.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.setInputMask("D")
        self.setText("")
        self.setMaxLength(1)
        self.setFrame(True)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setDragEnabled(True)
        self.setPlaceholderText("")
        self.setClearButtonEnabled(False)

        self.textChanged.connect(self.squareTextChanged)
        self.textChanged.connect(self.parent().parent().check)

    def squareTextChanged(self, newTextStr):

        if self.parentWidget().parentWidget().puzzleStatus == PuzzleStausEnum.NotReady:
            self.setStyleSheet(
                "color: rgb(255,140,0);font-weight: bold;")

        elif self.parentWidget().parentWidget().puzzleStatus == PuzzleStausEnum.Ready:

            self.setStyleSheet(
                "color: rgb(219,226,233); font-weight: normal;")
        _prevText = self.text()
        _newText = newTextStr
        _newTextStr = list([val for val in _newText if val.isnumeric()])
        if not _newTextStr:
            self.setText("")
            _nextKey = self.objectName()
        else:
            self.setText(newTextStr[0])
            _nextKey=params.squares[((params.squares.index(self.objectName())+1) % len(params.squares))]
        self.parentWidget().parentWidget()._setNewFocus(self.objectName(), _nextKey)

class PuzzleBorderLine(QtWidgets.QFrame):
    def __init__(self, parent, frameShape, objectName=None):
        super(PuzzleBorderLine, self).__init__(parent, objectName=None)
        self.setObjectName(objectName)
        self.setParent(parent)
        self.setToolTip(_tooltip)
        self.setStatusTip(_statustip)
        self.setWhatsThis(_whatsthis)
        self.setAccessibleName(_accessibleName)
        self.setAccessibleDescription(_accessibleName)
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

    _italic = True
    _pointSize = 14
    _bold = True
    _weight = 75

    def __init__(self, parent, objectName="puzzleInfoLabel"):
        super(PuzzleInfoLabel, self).__init__(
            parent, objectName="puzzleInfoLabel")

        self.setParent(parent)
        self.setObjectName(objectName)

        puzzleLabelFont = QtGui.QFont(_fontFamily, self._pointSize)
        puzzleLabelFont.setBold(self._bold)
        puzzleLabelFont.setItalic(self._italic)
        puzzleLabelFont.setWeight(self._weight)

        self.setGeometry(QtCore.QRect(391, 851, 531, 38))  # Change this

        self.setFont(puzzleLabelFont)
        self.setToolTip(_tooltip)
        self.setStatusTip(_statustip)
        self.setWhatsThis(_whatsthis)
        self.setAccessibleName(_accessibleName)
        self.setAccessibleDescription(_accessibleName)
        self.setText("0 OF 17 SQUARES SET")
        self.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)

        # Connect the puzzle squares to update text when changed. Cant do before because this class didnt exist yet
        squares = self.parent().parent().findChildren(
            QtWidgets.QFrame, 'puzzleFrame')[0].squares

        for theSquare in squares.values():
            theSquare.textChanged.connect(self.refresh)

    def refresh(self):

        puzzleFrame = self.parent().parent().findChildren(
            QtWidgets.QFrame, 'puzzleFrame')[0]
        numFilledSquares = puzzleFrame.getNumFilledSquares()

        self.setText(str(numFilledSquares) + " OF 17 SQUARES SET")

        setBtn = self.parent().findChild(QtWidgets.QPushButton, 'setPuzzleButton')

        if numFilledSquares >= 17 and setBtn.isEnabled() is False:
            setBtn.setEnabled(True)
            self.setStyleSheet("color: rgb(0,255,0);font-weight: bold;")
        elif numFilledSquares < 17 and setBtn.isEnabled() is True:
            setBtn.setEnabled(False)


class SetPuzzleButton(QtWidgets.QPushButton):
    def __init__(self, parent, objectName='setPuzzleButton'):
        super(SetPuzzleButton, self).__init__(
            parent, objectName='setPuzzleButton')

        self.setParent(parent)
        self.setObjectName(objectName)
        self.setEnabled(False)
        self.setGeometry(QtCore.QRect(10, 850, 361, 41))
        self.setFont(QtGui.QFont(_fontFamily, 14))
        self.setToolTip(
            'The puzzle can be solved once the minimum number of squares required for a unique solution have been entered')
        self.setStatusTip(_statustip)
        self.setWhatsThis(_whatsthis)
        self.setAccessibleName(_accessibleName)
        self.setAccessibleDescription(_accessibleName)
        self.setText("SET START")
        self.setShortcut("")

        self.clicked.connect(self.parent().setSolvePuzzleBtnStatus)


class SolvePuzzleButton(QtWidgets.QPushButton):
    def __init__(self, parent, objectName='solvePuzzleButton'):
        super(SolvePuzzleButton, self).__init__(
            parent, objectName='solvePuzzleButton')

        self.setParent(parent)
        self.setObjectName(objectName)
        self.setEnabled(False)
        self.setGeometry(QtCore.QRect(10, 900, 911, 41))

        self.setFont(QtGui.QFont(_fontFamily, 14))
        self.setToolTip(_tooltip)
        self.setStatusTip(_statustip)
        self.setWhatsThis(_whatsthis)
        self.setAccessibleName(_accessibleName)
        self.setAccessibleDescription(_accessibleName)
        self.setText("SOLVE")
        self.setShortcut("")
        self.setObjectName("solveBtn")

        self.clicked.connect(self.solvePuzzle)

    def solvePuzzle(self):
        pass


class UiPanel(QtWidgets.QFrame):
    def __init__(self, parent, objectName='UIPanel'):
        super(UiPanel, self).__init__(parent, objectName='UIPanel')

        self.setParent(parent)
        self.setObjectName(objectName)

        self.setupUiPanel()

    def setupUiPanel(self):

        self.puzzleInfoLabel = PuzzleInfoLabel(parent=self)
        self.setPuzzleBtn = SetPuzzleButton(parent=self)
        self.solvePuzzleBtn = SolvePuzzleButton(parent=self)

    def setSolvePuzzleBtnStatus(self):
        self.solvePuzzleBtn.setEnabled(True)


class MenuBar(QtWidgets.QMenuBar):
    _font = QtGui.QFont(_fontFamily, 8)

    def __init__(self, theMainWindow):
        super(MenuBar, self).__init__(theMainWindow)

        self.setGeometry(QtCore.QRect(0, 0, 938, 22))

        self.setFont(self._font)
        self.setAcceptDrops(False)
        self.setToolTip(_tooltip)
        self.setStatusTip(_statustip)
        self.setWhatsThis(_whatsthis)
        self.setAccessibleName(_accessibleName)
        self.setAccessibleDescription(_accessibleName)
        self.setObjectName("menuBar")

        self.initMenuBarComponents(theMainWindow)
        self.initMenuBarActions(theMainWindow)

        self.fileMenu.addAction(self.importFromIniAction)
        self.setThemeMenu.addAction(self.setLightThemeAction)
        self.setThemeMenu.addAction(self.setDarkThemeAction)
        self.addAction(self.fileMenu.menuAction())
        self.addAction(self.setThemeMenu.menuAction())

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
        self.importFromIniAction.setText("IMPORT FROM INI")
        self.importFromIniAction.setIconText("IMPORT FROM INI")
        self.importFromIniAction.setToolTip("IMPORT FROM INI")
        self.importFromIniAction.setStatusTip(_statustip)
        self.importFromIniAction.setWhatsThis(_whatsthis)
        self.importFromIniAction.setFont(self._font)
        self.importFromIniAction.setMenuRole(
            QtWidgets.QAction.ApplicationSpecificRole)
        self.importFromIniAction.setObjectName("importFromIniAction")

        self.setLightThemeAction = QtWidgets.QAction(theMainWindow)
        self.setLightThemeAction.setCheckable(True)
        self.setLightThemeAction.setChecked(False)
        self.setLightThemeAction.setText("LIGHT")
        self.setLightThemeAction.setIconText("LIGHT")
        self.setLightThemeAction.setToolTip("Set Light Mode")
        self.setLightThemeAction.setStatusTip(_statustip)
        self.setLightThemeAction.setWhatsThis(_whatsthis)
        self.setLightThemeAction.setFont(self._font)
        self.setLightThemeAction.setMenuRole(QtWidgets.QAction.PreferencesRole)
        self.setLightThemeAction.setShortcutVisibleInContextMenu(False)
        self.setLightThemeAction.setObjectName("setLightThemeAction")
        self.setLightThemeAction.triggered.connect(self.setLightMode)

        self.setDarkThemeAction = QtWidgets.QAction(theMainWindow)
        self.setDarkThemeAction.setCheckable(True)
        self.setDarkThemeAction.setChecked(True)
        self.setDarkThemeAction.setText("DARK")
        self.setDarkThemeAction.setIconText("DARK")
        self.setDarkThemeAction.setToolTip("Set Dark Mode")
        self.setDarkThemeAction.setStatusTip(_statustip)
        self.setDarkThemeAction.setWhatsThis(_whatsthis)
        self.setDarkThemeAction.setFont(self._font)
        self.setDarkThemeAction.setMenuRole(QtWidgets.QAction.PreferencesRole)
        self.setDarkThemeAction.setObjectName("setDarkThemeAction")
        self.setDarkThemeAction.triggered.connect(self.setDarkMode)

        self.setLightThemeAction.triggered.connect(
            partial(self.uncheckTheBox, self.setDarkThemeAction))
        self.setDarkThemeAction.triggered.connect(
            partial(self.uncheckTheBox, self.setLightThemeAction))

    def setLightMode(self):
        
        QtGui.QGuiApplication.setPalette(GuiPalette(ThemeEnum.Light))
        self.parent().findChild(QtWidgets.QFrame,'puzzleFrame').check()
    def setDarkMode(self):
        QtGui.QGuiApplication.setPalette(GuiPalette(ThemeEnum.Dark))
        self.parent().findChild(QtWidgets.QFrame, 'puzzleFrame').check()
    def uncheckTheBox(self, otherBox):
        otherBox.setChecked(False)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setPalette(GuiPalette(ThemeEnum.Dark))
    MainWindow = QtWidgets.QMainWindow()
    ui = AppMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
