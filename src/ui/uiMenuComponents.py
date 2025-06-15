import logging
import os

from PyQt6.QtGui import QAction, QKeySequence, QShortcut, QCursor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMenu,
    QMenuBar,
    QPushButton,
    QDialog,
    QSlider,
    QHBoxLayout,
    QLineEdit
)

from Puzzle import puzzle as sudokuDefs

from .uiEnums import SquareTypeEnum
from .uiHelpers import (
    getBasePath,
    grabMainWindow,
    grabPuzzleFrame,
    grabPuzzleSquares,
    grabWidget,
)

uiLogger = logging.getLogger("uiLogger")


class MenuBar(QMenuBar):
    def __init__(self, theMainWindow):
        super(MenuBar, self).__init__(theMainWindow)

        self.setAcceptDrops(False)
        self.setObjectName("menuBar")

        self.initMenuBarComponents(theMainWindow)
        self.initMenuBarActions(theMainWindow)
        self.fileMenu.addAction(self.importFromIniAction)
        self.fileMenu.addAction(self.resetAllAction)
        self.addAction(self.fileMenu.menuAction())

    def initMenuBarComponents(self, theMainWindow):
        self.fileMenu = QMenu(self)
        self.fileMenu.setTitle("File")
        self.fileMenu.setObjectName("fileMenu")
        theMainWindow.setMenuBar(self)

    def initMenuBarActions(self, theMainWindow):
        # puzzleFrame = grabPuzzleFrame()
        self.importFromIniAction = QAction(theMainWindow)
        self.importFromIniAction.setText("&Import")
        self.importFromIniAction.setIconText("Import")
        self.importFromIniAction.setToolTip("Import")
        self.importFromIniAction.setMenuRole(QAction.MenuRole.ApplicationSpecificRole)
        self.importFromIniAction.shortcut = QShortcut(QKeySequence("Ctrl+I"), self)
        self.importFromIniAction.setObjectName("importFromIniAction")
        self.importFromIniAction.triggered.connect(self.importPuzzleBtnPushed)
        self.importFromIniAction.shortcut.activated.connect(self.importPuzzleBtnPushed)

        self.resetAllAction = QAction(theMainWindow)
        self.resetAllAction.setText("&Reset")
        self.resetAllAction.setIconText("&Reset")
        self.resetAllAction.setToolTip("Reset Squares")
        self.resetAllAction.setMenuRole(QAction.MenuRole.ApplicationSpecificRole)
        self.resetAllAction.shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        self.resetAllAction.setObjectName("resetAction")
        self.resetAllAction.triggered.connect(grabMainWindow()._resetMainWindow)
        self.resetAllAction.shortcut.activated.connect(grabMainWindow()._resetMainWindow)
    
    def importPuzzleBtnPushed(self):
        PuzzleSelectDlg(self)
        
    def _importPuzzle(self, id) -> None | str:
        _id = str(id)
        from csv import DictReader

        _basePath = getBasePath()
        puzzleFile = os.path.normpath(
            os.path.join(_basePath, "..", "..", "resources", "puzzles.csv")
        )

        if not os.path.isfile(puzzleFile):
            uiLogger.error("Puzzle file %s not found", puzzleFile)
            return None

        grabMainWindow()._resetMainWindow()

        inputPuzzle = None
        try:
            with open(puzzleFile, "r") as puzzleCsv:
                puzzleReader = DictReader(puzzleCsv)
                for row in puzzleReader:
                    if row["ID"] == _id:
                        inputPuzzle = row
                        break
        except OSError:
            uiLogger.error("Failed to open %s", puzzleFile)
            return None

        if inputPuzzle:
            uiLogger.debug("Puzzle ID %s found", _id)
        else:
            uiLogger.error("Puzzle ID %s not found. Returning", _id)
            return None

        uiLogger.info(
            f"Importing Puzzle {_id:s} with difficulty score {float(inputPuzzle['Score']) / 8.5 * 10.0:.1} out of 10"
        )
        inputPuzzle = inputPuzzle["Puzzle"]
        self._setUiPuzzle(inputPuzzle)
        return inputPuzzle

    def _importAllPuzzles(self):
        _id = range(16402)
        from csv import DictReader

        _basePath = getBasePath()
        puzzleFile = os.path.normpath(
            os.path.join(_basePath, "..", "..", "resources", "puzzles.csv")
        )

        if not os.path.isfile(puzzleFile):
            uiLogger.error("Puzzle file %s not found", puzzleFile)
            return None

        grabMainWindow()._resetMainWindow()
        uiLogger.info("Importing 16403 puzzles...")
        inputPuzzle = []
        try:
            with open(puzzleFile, "r") as puzzleCsv:
                puzzleReader = DictReader(puzzleCsv)
                for row in puzzleReader:
                    inputPuzzle.append(row["Puzzle"])
        except OSError:
            uiLogger.error("Failed to open %s", puzzleFile)
            return None

        uiLogger.info("Puzzles imported")
        return inputPuzzle

    def _setUiPuzzle(self, dotPuzzle) -> None:
        squares = grabPuzzleSquares()

        squareKeys = sudokuDefs.squares

        for idx, val in enumerate(dotPuzzle):
            sq = squares[squareKeys[idx]]
            if val == ".":
                sq.squareType = SquareTypeEnum.InputUnlocked
                sq.setProperty("squareType", "UserSetAndValid")
            else:
                sq.setText(val)
                sq.squareType = SquareTypeEnum.InputLocked
                sq.setProperty(
                    "squareType", "InputLockedAndValid"
                )  # We'll assume for now input puzzles are are valid
            sq._refresh()
        grabMainWindow()._updateWindow()
        grabPuzzleFrame().toggleLock()
        grabWidget(QPushButton, "setPuzzleBtn")._enableMe()

    def uncheckTheBox(self, otherBox):
        otherBox.setChecked(False)

    @staticmethod
    def puzzleToDict(dotPuzzle) -> dict[str, str]:
        squareKeys = sudokuDefs.squares
        pzlOut = dict.fromkeys(squareKeys, "123456789")
        return {pzlOut[squareKeys[idx]]: val for idx, val in enumerate(dotPuzzle) if val != "."}


class PuzzleSelectDlg(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Puzzle")
        #self.setGeometry(100, 100, 300, 200)

        self.leftbtn = QPushButton(">", self)
        self.leftbtn.setContentsMargins(0,0,0,0)
        self.leftbtn.setFlat(True)
        self.leftbtn.clicked.connect(self._addOne)
        self.leftbtn.setFixedWidth(20)

        
        self.rightbtn = QPushButton("<", self)
        self.rightbtn.setContentsMargins(0, 0, 0, 0)
        self.rightbtn.setFlat(True)
        self.rightbtn.setFixedWidth(20)
        self.rightbtn.clicked.connect(self._loseOne)
        
        self.leftpagebtn = QPushButton(">>>", self)
        self.leftpagebtn.setContentsMargins(0, 0, 0, 0)
        self.leftpagebtn.setFlat(True)
        self.leftpagebtn.clicked.connect(self._addOneT)
        self.leftpagebtn.setFixedWidth(20)

        self.rightpagebtn = QPushButton("<<<", self)
        self.rightpagebtn.setContentsMargins(0, 0, 0, 0)
        self.rightpagebtn.setFlat(True)
        self.rightpagebtn.setFixedWidth(20)
        self.rightpagebtn.clicked.connect(self._loseOneT)
        
        self.sliderbar = QSlider(Qt.Orientation.Horizontal,self)
        self.sliderbar.setContentsMargins(0, 0, 0, 0)
        self.sliderbar.setFixedWidth(400)
        
        self.sliderbar.setMinimum(0)
        self.sliderbar.setMaximum(16401)
        self.sliderbar.setSingleStep(1)
        self.sliderbar.setPageStep(1000)
        self.sliderbar.setValue(16401)
        self.sliderbar.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.sliderbar.valueChanged.connect(self.update)
        
        self.selectionlabel = QLineEdit(str(self.sliderbar.value()),self)
        self.selectionlabel.setContentsMargins(0, 0, 0, 0)
        self.selectionlabel.textChanged.connect(self.update)
        self.selectionlabel.setInputMethodHints(Qt.InputMethodHint.ImhDigitsOnly)
        self.selectionlabel.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        
        self.okButton = QPushButton("OK", self)
        self.okButton.setContentsMargins(0, 0, 0, 0)
        self.okButton.setFlat(True)
        self.okButton.setFixedWidth(20)
        self.okButton.clicked.connect( lambda state: grabWidget(QMenuBar,"menuBar")._importPuzzle( self.sliderbar.value() ))
        self.okButton.clicked.connect(self.close)
        
        
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.rightpagebtn)
        self.layout.addWidget(self.rightbtn)
        self.layout.addWidget(self.sliderbar)
        self.layout.addWidget(self.leftbtn)
        self.layout.addWidget(self.leftpagebtn)
        self.layout.addWidget(self.selectionlabel)
        self.layout.addWidget(self.okButton)

        self.setLayout(self.layout)
        self.show()
        
    def update(self,value):
        
        self.sliderbar.setValue(int(value))
        self.selectionlabel.setText(str(self.sliderbar.value()))

    def _addOne(self):
        self.sliderbar.setValue(min(self.sliderbar.value() + 1,16402))
    def _loseOne(self):
        self.sliderbar.setValue(max(self.sliderbar.value() - 1,0))
    def _addOneT(self):
            self.sliderbar.setValue(min(self.sliderbar.value() + 1000,16402))
    def _loseOneT(self):
            self.sliderbar.setValue(max(self.sliderbar.value() - 1000,0))