
import configparser
import os, sys
from functools import partial

from appHelpers import (GuiPalette, SquareTypeEnum, ThemeEnum, grabPuzzleFrame,
                        grabWidget)
from PyQt5 import QtGui, QtWidgets
from pathlib import Path
_fontFamily = "Segoi Ui"


class MenuBar(QtWidgets.QMenuBar):
    _font = QtGui.QFont(_fontFamily, 8)

    def __init__(self, theMainWindow):
        super(MenuBar, self).__init__(theMainWindow)

        self.setAcceptDrops(False)
        self.setObjectName("menuBar")
        self.setStyleSheet('font-family: Segoe Ui; font-size: 10pt; font-weight: bold')

        self.initMenuBarComponents(theMainWindow)
        self.initMenuBarActions(theMainWindow)

        self.fileMenu.addAction(self.importFromIniAction)
        self.fileMenu.addAction(self.resetAllAction)

        self.setThemeMenu.addAction(self.setLightThemeAction)
        self.setThemeMenu.addAction(self.setDarkThemeAction)
        self.addAction(self.fileMenu.menuAction())
        self.addAction(self.setThemeMenu.menuAction())

    def initMenuBarComponents(self, theMainWindow):

        self.fileMenu = QtWidgets.QMenu(self)
        self.fileMenu.setTitle("FILE")
        self.fileMenu.setObjectName("fileMenu")

        self.setThemeMenu = QtWidgets.QMenu(self)
        self.setThemeMenu.setTitle("THEME")
        self.setThemeMenu.setObjectName("setThemeMenu")

        theMainWindow.setMenuBar(self)

    def initMenuBarActions(self, theMainWindow):

        puzzleFrame = grabPuzzleFrame()
        self.importFromIniAction = QtWidgets.QAction(theMainWindow)
        self.importFromIniAction.setText("&IMPORT FROM INI")
        self.importFromIniAction.setIconText("IMPORT FROM INI")
        self.importFromIniAction.setToolTip("IMPORT FROM INI")
        self.importFromIniAction.setMenuRole(
            QtWidgets.QAction.ApplicationSpecificRole)
        self.importFromIniAction.shortcut = QtWidgets.QShortcut(
            QtGui.QKeySequence("Ctrl+I"), self)
        self.importFromIniAction.setObjectName("importFromIniAction")
        self.importFromIniAction.triggered.connect(self.importIni)
        self.importFromIniAction.shortcut.activated.connect(self.importIni)

        self.resetAllAction = QtWidgets.QAction(theMainWindow)
        self.resetAllAction.setText("&RESET ALL")
        self.resetAllAction.setIconText("RESET ALL")
        self.resetAllAction.setToolTip("RESET ALL SQUARES")
        self.resetAllAction.setMenuRole(
            QtWidgets.QAction.ApplicationSpecificRole)
        self.resetAllAction.shortcut = QtWidgets.QShortcut(
            QtGui.QKeySequence("Ctrl+R"), self)
        self.resetAllAction.setObjectName("resetAction")

        self.resetAllAction.triggered.connect(self.resetAction)
        self.resetAllAction.shortcut.activated.connect(self.resetAction)
    
        self.setLightThemeAction = QtWidgets.QAction(theMainWindow)
        self.setLightThemeAction.setCheckable(True)
        self.setLightThemeAction.setChecked(False)
        self.setLightThemeAction.setEnabled(False)
        self.setLightThemeAction.setText("&LIGHT")
        self.setLightThemeAction.setIconText("LIGHT")
        self.setLightThemeAction.setToolTip("Set Light Mode")
        self.setLightThemeAction.shortcut = QtWidgets.QShortcut(
            QtGui.QKeySequence("Ctrl+L"), self)
        self.setLightThemeAction.setMenuRole(QtWidgets.QAction.PreferencesRole)
        self.setLightThemeAction.setShortcutVisibleInContextMenu(False)
        self.setLightThemeAction.setObjectName("setLightThemeAction")
        self.setLightThemeAction.triggered.connect(self.setLightMode)
        self.setLightThemeAction.shortcut.activated.connect(self.setLightMode)
        self.setLightThemeAction.triggered.connect(puzzleFrame._refresh)
        self.setLightThemeAction.shortcut.activated.connect(
            puzzleFrame._refresh)


        self.setDarkThemeAction = QtWidgets.QAction(theMainWindow)
        self.setDarkThemeAction.setCheckable(True)
        self.setDarkThemeAction.setChecked(True)
        self.setDarkThemeAction.setText("&DARK")
        self.setDarkThemeAction.setIconText("DARK")
        self.setDarkThemeAction.shortcut = QtWidgets.QShortcut(
            QtGui.QKeySequence("Ctrl+D"), self)
        self.setDarkThemeAction.setToolTip("Set Dark Mode")
        self.setDarkThemeAction.setMenuRole(QtWidgets.QAction.PreferencesRole)
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
        fname = QtWidgets.QFileDialog.getOpenFileName(
            self,
            'Load ini file',
            os.path.join(_basePath, 'input'),
            "Ini Files (*.ini *.txt)")
        if fname:
            puzzleFrame = grabPuzzleFrame()
            infoLabel = grabWidget(QtWidgets.QLabel, 'puzzleInfoLabel')
            
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
        selectedValue, isSelected = QtWidgets.QInputDialog.getItem(
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
        puzzleInfoLabel = grabWidget(QtWidgets.QLabel, 'puzzleInfoLabel')
        displayLabel = grabWidget(QtWidgets.QLabel, 'infoDisplayLabel')
        for square in squares.values():
            square._resetAction()

        #puzzleInfoLabel.setText('Solve')
        puzzleInfoLabel._refresh()
        puzzleFrame.toggleLock()
        displayLabel._refresh()
        
    def setLightMode(self):
        QtGui.QGuiApplication.setPalette(GuiPalette(ThemeEnum.Light))
        grabPuzzleFrame()._refresh()

    def setDarkMode(self):
        QtGui.QGuiApplication.setPalette(GuiPalette(ThemeEnum.Dark))
        grabPuzzleFrame()._refresh()

    def uncheckTheBox(self, otherBox):
        otherBox.setChecked(False)

def getBasePath():
    
    currentPath = Path(sys.argv[0]).resolve()
    if len(currentPath._cparts)>2:
        inputsPath = currentPath._cparts[0:-2]
        inputsPath = os.path.join(*inputsPath, 'input')
    else:
        inputsPath = currentPath._cparts[0:-1]
        inputsPath = os.path.join(*inputsPath, 'input')
        
    if not os.path.isdir(inputsPath):
        inputsPath = currentPath._cparts[0:-1]
        inputsPath = os.path.join(*inputsPath,'input')
        
    print(f'Using input location {inputsPath:s}')
    return inputsPath
   
