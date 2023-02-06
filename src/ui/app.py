# -*- coding: utf-8 -*-

import os
from functools import lru_cache
from math import floor
from appHelpers import AppStatusEnum, GuiPalette, ThemeEnum
from controlUiComponents import UiPanel
from menuUiComponents import MenuBar
from puzzleHelpers import sudokuParams as params
from puzzleUiComponents import PuzzleFrame
from PyQt5 import QtCore, QtGui, QtWidgets

# Some gui globals with default widget vals

_fontFamily = 'Segoi Ui'


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
        self.setWindowTitle("SudokuSolverApp")
        self.setDockNestingEnabled(True)
        self._status = AppStatusEnum.Unlocked
        self.resizeApp()
        self.setStyleSheet('* {font-family: Segoe Ui; font-size: 12pt}')

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
        self.titleLabel.setAutoFillBackground(True)
        self.titleLabel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.titleLabel.setText("SUDOKU SOLVER")
        self.titleLabel.setScaledContents(True)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setStyleSheet("font-family: Segoe Ui; font-size: 28pt")
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
