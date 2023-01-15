# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import string
from math import floor

puzzleRows = list(string.ascii_uppercase[0:9])
puzzleCols = list(string.digits[1:10])

puzzleSquares = []
for row in puzzleRows:
    for col in puzzleCols:
        puzzleSquares.append(row+col)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(938, 1088)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(12)
        MainWindow.setFont(font)
        MainWindow.setWindowTitle("SudokuSolverApp")
        MainWindow.setToolTip("")
        MainWindow.setStatusTip("")
        MainWindow.setWhatsThis("")
        MainWindow.setAccessibleName("")
        MainWindow.setAccessibleDescription("")
        MainWindow.setDockNestingEnabled(True)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setToolTip("")
        self.centralWidget.setStatusTip("")
        self.centralWidget.setWhatsThis("")
        self.centralWidget.setAccessibleName("")
        self.centralWidget.setAccessibleDescription("")
        self.centralWidget.setObjectName("centralWidget")
        self.titleLabel = QtWidgets.QLabel(self.centralWidget)
        self.titleLabel.setGeometry(QtCore.QRect(0, 0, 931, 101))
        font = QtGui.QFont(
            "MS Reference Sans Serif",40,50,False)
        self.titleLabel.setFont(font)
        self.titleLabel.setToolTip("")
        self.titleLabel.setStatusTip("")
        self.titleLabel.setWhatsThis("")
        self.titleLabel.setAccessibleName("")
        self.titleLabel.setAccessibleDescription("")
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
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(14)
        self.setStartBtn.setFont(font)
        self.setStartBtn.setToolTip("")
        self.setStartBtn.setStatusTip("")
        self.setStartBtn.setWhatsThis("")
        self.setStartBtn.setAccessibleName("")
        self.setStartBtn.setAccessibleDescription("")
        self.setStartBtn.setText("SET START")
        self.setStartBtn.setShortcut("")
        self.setStartBtn.setObjectName("setStartBtn")
        self.setNumSquaresLabel = QtWidgets.QLabel(self.centralWidget)
        self.setNumSquaresLabel.setGeometry(QtCore.QRect(391, 851, 531, 38))
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.setNumSquaresLabel.setFont(font)
        self.setNumSquaresLabel.setToolTip("")
        self.setNumSquaresLabel.setStatusTip("")
        self.setNumSquaresLabel.setWhatsThis("")
        self.setNumSquaresLabel.setAccessibleName("")
        self.setNumSquaresLabel.setAccessibleDescription("")
        self.setNumSquaresLabel.setText("0 OF 17 SQUARES SET")
        self.setNumSquaresLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.setNumSquaresLabel.setObjectName("setNumSquaresLabel")
        self.solveBtn = QtWidgets.QPushButton(self.centralWidget)
        self.solveBtn.setEnabled(False)
        self.solveBtn.setGeometry(QtCore.QRect(10, 900, 911, 41))
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(14)
        self.solveBtn.setFont(font)
        self.solveBtn.setToolTip("")
        self.solveBtn.setStatusTip("")
        self.solveBtn.setWhatsThis("")
        self.solveBtn.setAccessibleName("")
        self.solveBtn.setAccessibleDescription("")
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
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(8)
        self.menuBar.setFont(font)
        self.menuBar.setAcceptDrops(False)
        self.menuBar.setToolTip("")
        self.menuBar.setStatusTip("")
        self.menuBar.setWhatsThis("")
        self.menuBar.setAccessibleName("")
        self.menuBar.setAccessibleDescription("")
        self.menuBar.setObjectName("menuBar")
        self.fileMenu = QtWidgets.QMenu(self.menuBar)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(7)
        self.fileMenu.setFont(font)
        self.fileMenu.setToolTip("")
        self.fileMenu.setStatusTip("")
        self.fileMenu.setWhatsThis("")
        self.fileMenu.setAccessibleName("")
        self.fileMenu.setAccessibleDescription("")
        self.fileMenu.setTitle("FILE")
        self.fileMenu.setObjectName("fileMenu")
        self.setThemeMenu = QtWidgets.QMenu(self.menuBar)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(7)
        self.setThemeMenu.setFont(font)
        self.setThemeMenu.setToolTip("")
        self.setThemeMenu.setStatusTip("")
        self.setThemeMenu.setWhatsThis("")
        self.setThemeMenu.setAccessibleName("")
        self.setThemeMenu.setAccessibleDescription("")
        self.setThemeMenu.setTitle("THEME")
        self.setThemeMenu.setObjectName("setThemeMenu")
        MainWindow.setMenuBar(self.menuBar)
        self.importFromIniAction = QtWidgets.QAction(MainWindow)
        self.importFromIniAction.setText("IMPORT FROM INI")
        self.importFromIniAction.setIconText("IMPORT FROM INI")
        self.importFromIniAction.setToolTip("IMPORT FROM INI")
        self.importFromIniAction.setStatusTip("")
        self.importFromIniAction.setWhatsThis("")
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        self.importFromIniAction.setFont(font)
        self.importFromIniAction.setMenuRole(QtWidgets.QAction.ApplicationSpecificRole)
        self.importFromIniAction.setObjectName("importFromIniAction")
        self.setLightThemeAction = QtWidgets.QAction(MainWindow)
        self.setLightThemeAction.setCheckable(True)
        self.setLightThemeAction.setChecked(True)
        self.setLightThemeAction.setText("LIGHT")
        self.setLightThemeAction.setIconText("LIGHT")
        self.setLightThemeAction.setToolTip("Set Light Mode")
        self.setLightThemeAction.setStatusTip("")
        self.setLightThemeAction.setWhatsThis("")
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        self.setLightThemeAction.setFont(font)
        self.setLightThemeAction.setMenuRole(QtWidgets.QAction.PreferencesRole)
        self.setLightThemeAction.setShortcutVisibleInContextMenu(False)
        self.setLightThemeAction.setObjectName("setLightThemeAction")
        self.setDarkThemeAction = QtWidgets.QAction(MainWindow)
        self.setDarkThemeAction.setCheckable(True)
        self.setDarkThemeAction.setText("DARK")
        self.setDarkThemeAction.setIconText("DARK")
        self.setDarkThemeAction.setToolTip("Set Dark Mode")
        self.setDarkThemeAction.setStatusTip("")
        self.setDarkThemeAction.setWhatsThis("")
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
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
        self.setToolTip("")
        self.setStatusTip("")
        self.setWhatsThis("")
        self.setAccessibleName("")
        self.setAccessibleDescription("")
        self.setAutoFillBackground(False)
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setLineWidth(3)
        self.setObjectName("puzzleFrame")

        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 911, 691))
        self.gridLayoutWidget.setToolTip("")
        self.gridLayoutWidget.setStatusTip("")
        self.gridLayoutWidget.setWhatsThis("")
        self.gridLayoutWidget.setAccessibleName("")
        self.gridLayoutWidget.setAccessibleDescription("")
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")

        self.puzzleLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.puzzleLayout.setContentsMargins(0, 0, 0, 0)
        self.puzzleLayout.setSpacing(0)
        self.puzzleLayout.setObjectName("puzzleLayout")
    
        self.setSquares()
        self.setHeaders()
        self.setBorderLines()

    def setSquares(self):
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
        self.squares = squares

    def setHeaders(self):

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

    def setBorderLines(self):
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
    _font = QtGui.QFont("MS Reference Sans Serif",12)

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
        self.setToolTip("")
        self.setStatusTip("")
        self.setWhatsThis("")
        self.setAccessibleName("")
        self.setAccessibleDescription("")
        self.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.setInputMask("0")
        self.setText("")
        self.setMaxLength(1)
        self.setFrame(True)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setDragEnabled(True)
        self.setPlaceholderText("")
        self.setClearButtonEnabled(False)

class PuzzleBorderLine(QtWidgets.QFrame):
    def __init__(self, parent, frameShape, objectName=None):
        super(PuzzleBorderLine, self).__init__(parent, objectName=None)
        self.setObjectName(objectName)
        self.setParent(parent)
        self.setToolTip("")
        self.setStatusTip("")
        self.setWhatsThis("")
        self.setAccessibleName("")
        self.setAccessibleDescription("")
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setLineWidth(3)
        self.setFrameShape(frameShape)

class PuzzleHeader(QtWidgets.QLabel):

    # Set the font so constant across all
    _font = QtGui.QFont("MS Reference Sans Serif", 20, 75, False)

    def __init__(self, parent, text=None, objectName=None):
        super(PuzzleHeader, self).__init__(parent, text=None,  objectName=None)

        self.setObjectName(objectName)
        self.setParent(parent)
        self.setFont(self._font)
        self.setToolTip("")
        self.setStatusTip("")
        self.setWhatsThis("")
        self.setAccessibleName("")
        self.setAccessibleDescription("")
        self.setText(text)
        self.setAlignment(QtCore.Qt.AlignCenter)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
