import logging
import os

from PyQt6.QtGui import QAction, QKeySequence, QShortcut
from PyQt6.QtWidgets import QInputDialog, QMenu, QMenuBar, QPushButton

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
        self.importFromIniAction.triggered.connect(self._importPuzzle)
        self.importFromIniAction.shortcut.activated.connect(self._importPuzzle)

        self.resetAllAction = QAction(theMainWindow)
        self.resetAllAction.setText("&Reset")
        self.resetAllAction.setIconText("&Reset")
        self.resetAllAction.setToolTip("Reset Squares")
        self.resetAllAction.setMenuRole(QAction.MenuRole.ApplicationSpecificRole)
        self.resetAllAction.shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        self.resetAllAction.setObjectName("resetAction")
        self.resetAllAction.triggered.connect(grabMainWindow()._resetMainWindow)
        self.resetAllAction.shortcut.activated.connect(grabMainWindow()._resetMainWindow)

    """def importPuzzle1(self):
        import configparser
        _basePath = getBasePath()
        fname = os.path.normpath(os.path.join(_basePath, "..", "..", "resources", "samples.ini"))
        if fname:
            grabMainWindow()._resetMainWindow()

            puzzleIni = configparser.ConfigParser()
            puzzleIni.read(fname)
            puzzleNames = list(puzzleIni._sections.keys())

            if len(puzzleNames) == 0:
                return
            puzzleName = self._choosePuzzle(puzzleNames)
            if not puzzleName:
                return
            squares = grabPuzzleSquares()

            for squareKey, squareVal in puzzleIni._sections[puzzleName].items():
                squares[squareKey.upper()].setText(squareVal)
                squares[squareKey.upper()].squareType = SquareTypeEnum.InputUnlocked
                squares[squareKey.upper()]._refresh()

            grabMainWindow()._updateWindow()
            grabPuzzleFrame().toggleLock()
            grabWidget(QPushButton, "setPuzzleBtn")._enableMe()
            """

    def _importPuzzle(self) -> None | str:
        _id = "16401"
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
            f"Importing Puzzle {_id:s} with difficulty score {float(inputPuzzle['Score']) / 8.5 * 10.0} out of 10"
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

    def _choosePuzzle(self, puzzleNames):
        if not puzzleNames:
            return False
        selectedValue, isSelected = QInputDialog.getItem(
            self, "Import Puzzle", "Select Puzzle to Import:", puzzleNames
        )

        if isSelected:
            return selectedValue
        else:
            return False

    def uncheckTheBox(self, otherBox):
        otherBox.setChecked(False)

    @staticmethod
    def puzzleToDict(dotPuzzle) -> dict[str, str]:
        squareKeys = sudokuDefs.squares
        pzlOut = dict.fromkeys(squareKeys, "123456789")
        return {pzlOut[squareKeys[idx]]: val for idx, val in enumerate(dotPuzzle) if val != "."}
