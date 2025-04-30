
import configparser
import os
from functools import partial
from PyQt5.QtGui import QKeySequence, QFont, QGuiApplication
from PyQt5.QtWidgets import QAction, QMenu, QMenuBar, QShortcut, QFileDialog, QInputDialog, QLabel
from .uiHelpers import grabPuzzleFrame, grabWidget, getBasePath
from .uiEnums import SquareTypeEnum
import qdarktheme

_fontFamily = "Verdana"


class MenuBar(QMenuBar):
    _font = QFont(_fontFamily, 8)

    def __init__(self, theMainWindow):
        super(MenuBar, self).__init__(theMainWindow)

        self.setAcceptDrops(False)
        self.setObjectName("menuBar")
        self.setStyleSheet('font-family: Verdana; font-size: 10pt; font-weight: bold')

        self.initMenuBarComponents(theMainWindow)
        self.initMenuBarActions(theMainWindow)

        self.fileMenu.addAction(self.importFromIniAction)
        self.fileMenu.addAction(self.resetAllAction)

        self.setThemeMenu.addAction(self.setLightThemeAction)
        self.setThemeMenu.addAction(self.setDarkThemeAction)
        self.addAction(self.fileMenu.menuAction())
        self.addAction(self.setThemeMenu.menuAction())

    def initMenuBarComponents(self, theMainWindow):

        self.fileMenu = QMenu(self)
        self.fileMenu.setTitle("File")
        self.fileMenu.setObjectName("fileMenu")

        self.setThemeMenu = QMenu(self)
        self.setThemeMenu.setTitle("Theme")
        self.setThemeMenu.setObjectName("setThemeMenu")

        theMainWindow.setMenuBar(self)

    def initMenuBarActions(self, theMainWindow):

        puzzleFrame = grabPuzzleFrame()
        self.importFromIniAction = QAction(theMainWindow)
        self.importFromIniAction.setText("&IMPORT FROM INI")
        self.importFromIniAction.setIconText("IMPORT FROM INI")
        self.importFromIniAction.setToolTip("IMPORT FROM INI")
        self.importFromIniAction.setMenuRole(
            QAction.ApplicationSpecificRole)
        self.importFromIniAction.shortcut = QShortcut(
            QKeySequence("Ctrl+I"), self)
        self.importFromIniAction.setObjectName("importFromIniAction")
        self.importFromIniAction.triggered.connect(self.importIni)
        self.importFromIniAction.shortcut.activated.connect(self.importIni)

        self.resetAllAction = QAction(theMainWindow)
        self.resetAllAction.setText("&RESET ALL")
        self.resetAllAction.setIconText("RESET ALL")
        self.resetAllAction.setToolTip("RESET ALL SQUARES")
        self.resetAllAction.setMenuRole(
            QAction.ApplicationSpecificRole)
        self.resetAllAction.shortcut = QShortcut(
            QKeySequence("Ctrl+R"), self)
        self.resetAllAction.setObjectName("resetAction")

        self.resetAllAction.triggered.connect(self.resetAction)
        self.resetAllAction.shortcut.activated.connect(self.resetAction)
    
        self.setLightThemeAction = QAction(theMainWindow)
        self.setLightThemeAction.setCheckable(True)
        self.setLightThemeAction.setChecked(False)
        self.setLightThemeAction.setEnabled(False)
        self.setLightThemeAction.setText("&LIGHT")
        self.setLightThemeAction.setIconText("LIGHT")
        self.setLightThemeAction.setToolTip("Set Light Mode")
        self.setLightThemeAction.shortcut = QShortcut(
            QKeySequence("Ctrl+L"), self)
        self.setLightThemeAction.setMenuRole(QAction.PreferencesRole)
        self.setLightThemeAction.setShortcutVisibleInContextMenu(False)
        self.setLightThemeAction.setObjectName("setLightThemeAction")
        self.setLightThemeAction.triggered.connect(self.setLightMode)
        self.setLightThemeAction.shortcut.activated.connect(self.setLightMode)
        self.setLightThemeAction.triggered.connect(puzzleFrame._refresh)
        self.setLightThemeAction.shortcut.activated.connect(
            puzzleFrame._refresh)


        self.setDarkThemeAction = QAction(theMainWindow)
        self.setDarkThemeAction.setCheckable(True)
        self.setDarkThemeAction.setChecked(True)
        self.setDarkThemeAction.setText("&DARK")
        self.setDarkThemeAction.setIconText("DARK")
        self.setDarkThemeAction.shortcut = QShortcut(
            QKeySequence("Ctrl+D"), self)
        self.setDarkThemeAction.setToolTip("Set Dark Mode")
        self.setDarkThemeAction.setMenuRole(QAction.PreferencesRole)
        self.setDarkThemeAction.setObjectName("setDarkThemeAction")
        self.setDarkThemeAction.setEnabled(False)
        self.setDarkThemeAction.triggered.connect(self.setDarkMode)
        self.setDarkThemeAction.triggered.connect(puzzleFrame._refresh)
        self.setDarkThemeAction.shortcut.activated.connect(self.setDarkMode)
        self.setDarkThemeAction.shortcut.activated.connect(
            puzzleFrame._refresh)

        self.setLightThemeAction.triggered.connect(
            partial(self.uncheckTheBox, self.setDarkThemeAction))
        self.setDarkThemeAction.triggered.connect(
            partial(self.uncheckTheBox, self.setLightThemeAction))


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
                squares[squareKey.upper()]._applyFormatting()
            puzzleFrame.toggleLock()
            puzzleFrame._refresh()
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
    
    def resetAction(self):

        puzzleFrame = grabPuzzleFrame()
        squares = puzzleFrame.squares
        puzzleInfoLabel = grabWidget(QLabel, 'puzzleInfoLabel')
        displayLabel = grabWidget(QLabel, 'infoDisplayLabel')
        for square in squares.values():
            square._resetAction()

        #puzzleInfoLabel.setText('Solve')
        puzzleInfoLabel._refresh()
        puzzleFrame.toggleLock()
        displayLabel._resetAction()
        
    def setLightMode(self):
        qdarktheme.setup_theme("light")

    def setDarkMode(self):
        qdarktheme.setup_theme("dark")

    def uncheckTheBox(self, otherBox):
        otherBox.setChecked(False)

