import configparser
import os
from PyQt6.QtGui import QKeySequence, QAction, QShortcut
from PyQt6.QtWidgets import QMenu, QMenuBar, QInputDialog, QPushButton
from .uiHelpers import (
    grabPuzzleSquares,
    grabPuzzleFrame,
    grabWidget,
    getBasePath,
    grabMainWindow,
)
from .uiEnums import SquareTypeEnum


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
        self.importFromIniAction.triggered.connect(self.importPuzzle)
        self.importFromIniAction.shortcut.activated.connect(self.importPuzzle)

        self.resetAllAction = QAction(theMainWindow)
        self.resetAllAction.setText("&Reset")
        self.resetAllAction.setIconText("&Reset")
        self.resetAllAction.setToolTip("Reset Squares")
        self.resetAllAction.setMenuRole(QAction.MenuRole.ApplicationSpecificRole)
        self.resetAllAction.shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        self.resetAllAction.setObjectName("resetAction")
        self.resetAllAction.triggered.connect(grabMainWindow()._resetMainWindow)
        self.resetAllAction.shortcut.activated.connect(
            grabMainWindow()._resetMainWindow
        )

    def importPuzzle(self):
        _basePath = getBasePath()
        fname = os.path.normpath(
            os.path.join(_basePath, "..", "..", "resources", "samples.ini")
        )
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
            puzzleIni._sections[puzzleName]
            for squareKey, squareVal in puzzleIni._sections[puzzleName].items():
                squares[squareKey.upper()].setText(squareVal)
                squares[squareKey.upper()].squareType = SquareTypeEnum.InputUnlocked
                squares[squareKey.upper()]._refresh()

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
