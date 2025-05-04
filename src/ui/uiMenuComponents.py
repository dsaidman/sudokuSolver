
import configparser
import os, sys
from PyQt6.QtGui import QKeySequence, QAction, QShortcut
from PyQt6.QtWidgets import QMenu, QMenuBar, QFileDialog, QInputDialog, QLabel, QPushButton
from .uiHelpers import grabPuzzleFrame, grabWidget, getBasePath, grabMainWindow
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

        #puzzleFrame = grabPuzzleFrame()
        self.importFromIniAction = QAction(theMainWindow)
        self.importFromIniAction.setText("&Import")
        self.importFromIniAction.setIconText("Import")
        self.importFromIniAction.setToolTip("Import")
        self.importFromIniAction.setMenuRole(
            QAction.MenuRole.ApplicationSpecificRole)
        self.importFromIniAction.shortcut = QShortcut(
            QKeySequence("Ctrl+I"), self)
        self.importFromIniAction.setObjectName("importFromIniAction")
        self.importFromIniAction.triggered.connect(self.importIni)
        self.importFromIniAction.shortcut.activated.connect(self.importIni)

        self.resetAllAction = QAction(theMainWindow)
        self.resetAllAction.setText("&Reset")
        self.resetAllAction.setIconText("Reset")
        self.resetAllAction.setToolTip("Reset Squares")
        self.resetAllAction.setMenuRole(
            QAction.MenuRole.ApplicationSpecificRole)
        self.resetAllAction.shortcut = QShortcut(
            QKeySequence("Ctrl+R"), self)
        self.resetAllAction.setObjectName("resetAction")

        for square in grabPuzzleFrame().squares.values():
            self.resetAllAction.triggered.connect(square._resetAction)
            self.resetAllAction.shortcut.activated.connect(square._resetAction)

        self.resetAllAction.triggered.connect(grabWidget(QLabel, 'puzzleInfoLabel')._refresh)
        self.resetAllAction.shortcut.activated.connect(grabWidget(QLabel, 'puzzleInfoLabel')._refresh)

        self.resetAllAction.triggered.connect(grabWidget(QLabel, 'infoDisplayLabel')._resetAction)
        self.resetAllAction.shortcut.activated.connect(grabWidget(QLabel, 'infoDisplayLabel')._resetAction)  

        self.resetAllAction.triggered.connect(grabWidget(QPushButton, 'setPuzzleBtn')._disableMe)
        self.resetAllAction.shortcut.activated.connect(grabWidget(QPushButton, 'setPuzzleBtn')._disableMe)

        self.resetAllAction.triggered.connect(grabMainWindow().resizeApp)
        self.resetAllAction.shortcut.activated.connect(grabMainWindow().resizeApp)

    def importIni(self):
        
        _basePath = getBasePath()
        fname = QFileDialog.getOpenFileName(
            self,
            'Load ini file',
            os.path.join(_basePath, 'input'),
            "Ini Files (*.ini *.txt)")
        if fname:
            puzzleFrame = grabPuzzleFrame()
            infoLabel = grabWidget(QLabel, 'puzzleInfoLabel')
            
            squares = puzzleFrame.squares
            puzzleIni = configparser.ConfigParser()
            puzzleIni.read(fname)
            puzzleNames = list(puzzleIni._sections.keys())
            if len(puzzleNames) == 0:
                return
            puzzleName = self._choosePuzzle(puzzleNames)
            if not puzzleName:
                return

            puzzleIni._sections[puzzleName]
            for squareVal in puzzleFrame.squares.values():
                squareVal._resetAction()
            for squareKey, squareVal in puzzleIni._sections[puzzleName].items():
                squares[squareKey.upper()].setText(squareVal)
                squares[squareKey.upper()].squareType = SquareTypeEnum.InputUnlocked
                squares[squareKey.upper()]._refresh()
            puzzleFrame.toggleLock()
            puzzleFrame.puzzleContentChangedFcn()
            infoLabel._refresh()
    
    def _choosePuzzle(self,puzzleNames):
        if not puzzleNames:
            return False
        selectedValue, isSelected = QInputDialog.getItem(
            self, 
            'Import Puzzle', 
            'Select Puzzle to Import:', 
            puzzleNames)
        
        if isSelected:
             return selectedValue
        else:
             return False
    

    def uncheckTheBox(self, otherBox):
        otherBox.setChecked(False)

