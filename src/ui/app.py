# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPalette, QColor
from PyQt5 import QtCore, QtGui, QtWidgets

import string
from math import floor
# Some globals to avoid recomputing often
puzzleRows = list(string.ascii_uppercase[0:9])
puzzleCols = list(string.digits[1:10])

puzzleSquares = []
for row in puzzleRows:
    for col in puzzleCols:
        puzzleSquares.append(row+col)
del row, col

_tooltip        = ""
_statustip      = ""
_whatsthis      = ""
_accessibleName = ""
_fontFamily = "MS Reference Sans Serif"

# UI MainWindow
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(938, 1088)
        font = QtGui.QFont()
        font.setFamily(_fontFamily)
        font.setPointSize(12)
        MainWindow.setFont(font)
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
        self.titleLabel = QtWidgets.QLabel(self.centralWidget)
        self.titleLabel.setGeometry(QtCore.QRect(0, 0, 931, 101))
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


        self.setStartBtn = QtWidgets.QPushButton(self.centralWidget)
        self.setStartBtn.setEnabled(False)
        self.setStartBtn.setGeometry(QtCore.QRect(10, 850, 361, 41))
        self.setStartBtn.setFont(QtGui.QFont(_fontFamily, 14))
        self.setStartBtn.setToolTip(_tooltip)
        self.setStartBtn.setStatusTip(_statustip)
        self.setStartBtn.setWhatsThis(_whatsthis)
        self.setStartBtn.setAccessibleName(_accessibleName)
        self.setStartBtn.setAccessibleDescription(_accessibleName)
        self.setStartBtn.setText("SET START")
        self.setStartBtn.setShortcut("")
        self.setStartBtn.setObjectName("setStartBtn")
        self.setNumSquaresLabel = QtWidgets.QLabel(self.centralWidget)
        self.setNumSquaresLabel.setGeometry(QtCore.QRect(391, 851, 531, 38))
        font = QtGui.QFont()
        font.setFamily(_fontFamily)
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.setNumSquaresLabel.setFont(font)
        self.setNumSquaresLabel.setToolTip(_tooltip)
        self.setNumSquaresLabel.setStatusTip(_statustip)
        self.setNumSquaresLabel.setWhatsThis(_whatsthis)
        self.setNumSquaresLabel.setAccessibleName(_accessibleName)
        self.setNumSquaresLabel.setAccessibleDescription(_accessibleName)
        self.setNumSquaresLabel.setText("0 OF 17 SQUARES SET")
        self.setNumSquaresLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.setNumSquaresLabel.setObjectName("setNumSquaresLabel")
        self.solveBtn = QtWidgets.QPushButton(self.centralWidget)
        self.solveBtn.setEnabled(False)
        self.solveBtn.setGeometry(QtCore.QRect(10, 900, 911, 41))

        self.solveBtn.setFont(QtGui.QFont(_fontFamily,14))
        self.solveBtn.setToolTip(_tooltip)
        self.solveBtn.setStatusTip(_statustip)
        self.solveBtn.setWhatsThis(_whatsthis)
        self.solveBtn.setAccessibleName(_accessibleName)
        self.solveBtn.setAccessibleDescription(_accessibleName)
        self.solveBtn.setText("SOLVE")
        self.solveBtn.setShortcut("")
        self.solveBtn.setObjectName("solveBtn")
        self.puzzleFrame.raise_()
        self.titleLabel.raise_()
        self.setStartBtn.raise_()
        self.setNumSquaresLabel.raise_()
        self.solveBtn.raise_()
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 938, 22))
        font = QtGui.QFont()
        font.setFamily(_fontFamily)
        font.setPointSize(8)
        self.menuBar.setFont(font)
        self.menuBar.setAcceptDrops(False)
        self.menuBar.setToolTip(_tooltip)
        self.menuBar.setStatusTip(_statustip)
        self.menuBar.setWhatsThis(_whatsthis)
        self.menuBar.setAccessibleName(_accessibleName)
        self.menuBar.setAccessibleDescription(_accessibleName)
        self.menuBar.setObjectName("menuBar")
        self.fileMenu = QtWidgets.QMenu(self.menuBar)
        font = QtGui.QFont()
        font.setFamily(_fontFamily)
        font.setPointSize(7)
        self.fileMenu.setFont(font)
        self.fileMenu.setToolTip(_tooltip)
        self.fileMenu.setStatusTip(_statustip)
        self.fileMenu.setWhatsThis(_whatsthis)
        self.fileMenu.setAccessibleName(_accessibleName)
        self.fileMenu.setAccessibleDescription(_accessibleName)
        self.fileMenu.setTitle("FILE")
        self.fileMenu.setObjectName("fileMenu")
        self.setThemeMenu = QtWidgets.QMenu(self.menuBar)
        font = QtGui.QFont()
        font.setFamily(_fontFamily)
        font.setPointSize(7)
        self.setThemeMenu.setFont(font)
        self.setThemeMenu.setToolTip(_tooltip)
        self.setThemeMenu.setStatusTip(_statustip)
        self.setThemeMenu.setWhatsThis(_whatsthis)
        self.setThemeMenu.setAccessibleName(_accessibleName)
        self.setThemeMenu.setAccessibleDescription(_accessibleName)
        self.setThemeMenu.setTitle("THEME")
        self.setThemeMenu.setObjectName("setThemeMenu")
        MainWindow.setMenuBar(self.menuBar)
        self.importFromIniAction = QtWidgets.QAction(MainWindow)
        self.importFromIniAction.setText("IMPORT FROM INI")
        self.importFromIniAction.setIconText("IMPORT FROM INI")
        self.importFromIniAction.setToolTip("IMPORT FROM INI")
        self.importFromIniAction.setStatusTip(_statustip)
        self.importFromIniAction.setWhatsThis(_whatsthis)
        font = QtGui.QFont()
        font.setFamily(_fontFamily)
        self.importFromIniAction.setFont(font)
        self.importFromIniAction.setMenuRole(QtWidgets.QAction.ApplicationSpecificRole)
        self.importFromIniAction.setObjectName("importFromIniAction")
        self.setLightThemeAction = QtWidgets.QAction(MainWindow)
        self.setLightThemeAction.setCheckable(True)
        self.setLightThemeAction.setChecked(True)
        self.setLightThemeAction.setText("LIGHT")
        self.setLightThemeAction.setIconText("LIGHT")
        self.setLightThemeAction.setToolTip("Set Light Mode")
        self.setLightThemeAction.setStatusTip(_statustip)
        self.setLightThemeAction.setWhatsThis(_whatsthis)
        font = QtGui.QFont()
        font.setFamily(_fontFamily)
        self.setLightThemeAction.setFont(font)
        self.setLightThemeAction.setMenuRole(QtWidgets.QAction.PreferencesRole)
        self.setLightThemeAction.setShortcutVisibleInContextMenu(False)
        self.setLightThemeAction.setObjectName("setLightThemeAction")
        self.setDarkThemeAction = QtWidgets.QAction(MainWindow)
        self.setDarkThemeAction.setCheckable(True)
        self.setDarkThemeAction.setText("DARK")
        self.setDarkThemeAction.setIconText("DARK")
        self.setDarkThemeAction.setToolTip("Set Dark Mode")
        self.setDarkThemeAction.setStatusTip(_statustip)
        self.setDarkThemeAction.setWhatsThis(_whatsthis)
        font = QtGui.QFont()
        font.setFamily(_fontFamily)
        font.setPointSize(7)
        self.setDarkThemeAction.setFont(font)
        self.setDarkThemeAction.setMenuRole(QtWidgets.QAction.PreferencesRole)
        self.setDarkThemeAction.setObjectName("setDarkThemeAction")
        self.fileMenu.addAction(self.importFromIniAction)
        self.setThemeMenu.addAction(self.setLightThemeAction)
        self.setThemeMenu.addAction(self.setDarkThemeAction)
        self.menuBar.addAction(self.fileMenu.menuAction())
        self.menuBar.addAction(self.setThemeMenu.menuAction())

        self.retranslateUi(MainWindow)
        #self.A1.textChanged['QString'].connect(self.setNumSquaresLabel.setText) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        for idx in range(0,80):
            MainWindow.setTabOrder(
                self.puzzleFrame.squares[puzzleSquares[idx]],
                self.puzzleFrame.squares[puzzleSquares[idx+1]])
        
        #MainWindow.setTabOrder(self.squares['I9'], self.setStartBtn)
        #MainWindow.setTabOrder(self.setStartBtn, self.solveBtn)

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

    def eventFilter(self, source, event):
    
        if isinstance(source, PuzzleSquare) and event.type() == QtGui.QKeyEvent.KeyPress:
            sourceObjectName = source.objectName()
            rowNum = sourceObjectName[0]
            colNum = sourceObjectName[1]

            if event.key() == QtCore.Qt.Key_Up:
                newFocusCol = colNum
                newFocusRow = puzzleRows[
                    (puzzleRows.index(rowNum)-1) % len(puzzleRows)]
                
                return self._setNewFocus(sourceObjectName, newFocusRow+newFocusCol)
            elif event.key() == QtCore.Qt.Key_Down:
                newFocusCol = colNum
                newFocusRow = puzzleRows[
                    (puzzleRows.index(rowNum)+1) % len(puzzleRows) ]
                return self._setNewFocus(sourceObjectName, newFocusRow+newFocusCol)
            
            elif event.key() == QtCore.Qt.Key_Tab or event.key() == QtCore.Qt.Key_Right:
                newKey = puzzleSquares[
                    (puzzleSquares.index(sourceObjectName)+1) % len(puzzleSquares) ] 
                return self._setNewFocus(sourceObjectName, newKey)
            elif event.key() == QtCore.Qt.Key_Left:
                newKey = puzzleSquares[
                    (puzzleSquares.index(sourceObjectName)-1) % len(puzzleSquares)]
                return self._setNewFocus(sourceObjectName, newKey)
            else:
                return False
        elif isinstance(source, PuzzleSquare) and ((event.type() == QtCore.QEvent.Type.FocusIn) or (event.type() == QtCore.QEvent.Type.MouseButtonPress)):
            sourceObjectName = source.objectName()
            returnVal = self._setNewFocus(None,sourceObjectName)
            self._setFocusCursor(sourceObjectName)
            return returnVal
             
        return False
      
    def _setNewFocus(self, oldKey, newKey ):
        returnVal = False
        if oldKey in self.squares and oldKey != newKey: 
            self.squares[oldKey].clearFocus()
        elif oldKey == None:
            for key in self.squares:
                if key != newKey and self.squares[key].hasFocus():
                    
                    self.squares[key].clearFocus()
                    break
            
        if newKey in self.squares:
            #if self.squares[newKey].hasFocus() == False:
            self.squares[newKey].setFocus()
            returnVal = True
            self._setFocusCursor(newKey)
        return returnVal
    def _setFocusCursor(self,key):
        self.squares[key].setCursorPosition(0)
        self.squares[key].end(False)
        self.squares[key].home(True)

    def _setSquares(self):
        squares = {}
        for squareKey in puzzleSquares:
            squares[squareKey] = PuzzleSquare(self.gridLayoutWidget, squareKey)

            self.puzzleLayout.addWidget(
                squares[squareKey],
                3+puzzleRows.index(squareKey[0]) +
                floor(puzzleRows.index(squareKey[0])/3.),
                3+puzzleCols.index(squareKey[1]) +
                floor(puzzleCols.index(squareKey[1])/3.),
                1, 1)
            squares[squareKey].installEventFilter(self)
        self.squares = squares

    def _setHeaders(self):

        rowHeaders = {}
        for rowKey in puzzleRows:

            rowHeaders[rowKey] = PuzzleHeader(
                self.gridLayoutWidget,
                rowKey,
                'RowHeader' + rowKey)
            self.puzzleLayout.addWidget(
                rowHeaders[rowKey],
                3+puzzleRows.index(rowKey) + floor(puzzleRows.index(rowKey)/3.), 1, 1, 1)
        self.rowHeaders = rowHeaders

        colHeaders = {}
        for colKey in puzzleCols:
            colHeaders[colKey] = PuzzleHeader(
                self.gridLayoutWidget,
                colKey,
                'ColumnHeader' + colKey)
            self.puzzleLayout.addWidget(
                colHeaders[colKey],
                1, 3+puzzleCols.index(colKey) + floor(puzzleCols.index(colKey)/3.), 1, 1)
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
    _font = QtGui.QFont(_fontFamily,12)

    # Set the size policy so constant across all
    _sizePolicy = QtWidgets.QSizePolicy(
        QtWidgets.QSizePolicy.Ignored, 
        QtWidgets.QSizePolicy.Expanding)
    _sizePolicy.setVerticalStretch(0)
    _sizePolicy.setHorizontalStretch(0)
    _sizePolicy.setHeightForWidth(False)
    
    def __init__(self, parent, objectName=None):
        super(PuzzleSquare, self).__init__(parent, objectName=None)
        
        self.setObjectName(objectName)
        self.setParent(parent)

        self.setSizePolicy(self._sizePolicy)
        self.setFont(self._font)

        self.setCursor( QtGui.QCursor(QtCore.Qt.IBeamCursor))
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
        self.hasValue = False
        
    def squareTextChanged(self,newTextStr):
        _prevText = self.text()
        _newText  = newTextStr
        _newTextStr = list([val for val in _newText if val.isnumeric()])
        if not _newTextStr:
            self.setText("")
            _nextKey = self.objectName()
        else:
            self.setText(newTextStr[0])
            _nextKey = puzzleSquares[puzzleSquares.index(self.objectName())+1]
        self.parentWidget().parentWidget()._setNewFocus(self.objectName(),_nextKey)

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
    _font = QtGui.QFont(_fontFamily, 20, 75, False)

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

def getDarkPalette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, QtCore.Qt.black)
    palette.setColor(QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QPalette.Text, QtCore.Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QPalette.BrightText, QtCore.Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QtCore.Qt.black)
    return palette

        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setPalette( getDarkPalette())
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
