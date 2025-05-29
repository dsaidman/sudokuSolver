
from PyQt6.QtWidgets import QWidget, QMainWindow, QSizePolicy, QLabel, QPushButton, QHBoxLayout, QSplitter
from PyQt6.QtCore import Qt, QMetaObject
from PyQt6.QtGui import QIcon, QPixmap, QGuiApplication
from .uiMainPanelComponents import UiMainPanel
from .uiSidebarComponents import UiSidebar
from .uiStatusBarComponents import PuzzleInfoLabel
from .uiMenuComponents import MenuBar
from solver.py2runtime import RuntimePy as rt
from solver.definitions import sudokuDefs as defs
from .uiHelpers import grabWidget, grabPuzzleFrame, grabMainWindow
from .uiEnums import AppStatusEnum
from functools import lru_cache
from math import floor
import inspect
import logging
import os
__all__ = ['AppMainWindow']
uiLogger = logging.getLogger('uiLogger')


class AppMainWindow(QMainWindow):

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, statusVal):
        self._status = statusVal
        return statusVal

    def __init__(self, lang="python"):
        """Constructor method initializes the main window and its components."""
        uiLogger.debug('Initializing AppMainWindow')
        super(AppMainWindow, self).__init__()

        self.runtimeLang = lang
        rt.setLang(self.runtimeLang)
        defs.setLang(self.runtimeLang)
        uiLogger.debug('Entered AppMainWindow')
        self.setObjectName("MainWindow")
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.setWindowTitle("SudokuSolverApp")

        uiLogger.debug('Setting app icon')
        filename = inspect.getframeinfo(inspect.currentframe()).filename
        path = os.path.dirname(os.path.abspath(filename))
        iconpath = os.path.join(
            os.path.dirname(
                os.path.dirname(path)),
            'res',
            'icon.ico')

        appIcon = QIcon()
        appIcon.addPixmap(
            QPixmap(iconpath),
            QIcon.Mode.Normal,
            QIcon.State.Off)
        self.setWindowIcon(appIcon)
        self._status = AppStatusEnum.Unlocked

        uiLogger.debug('Setting Central Widget')
        self.centralWidget = QWidget()
        self.centralWidget.setObjectName("centralWidget")
        self.setCentralWidget(self.centralWidget)

        self.layout = QHBoxLayout(self.centralWidget)
        self.layout.setObjectName('mainWindowLayout')
        # self.centralWidget.setLayout(self.splitter)
        self.setStyleSheet("* {font-family: 'Consolas';}")

    def setupUi(self):

        uiLogger.debug('Entered AppMainWindow setup')
        self.uiSidebarPanel = UiSidebar(self)
        self.uiMainPanel = UiMainPanel(self)

        self.splitter = QSplitter()
        self.splitter.setObjectName('masterSplitter')
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter.setChildrenCollapsible(True)
        self.splitter.setHandleWidth(8)

        self.splitter.addWidget(self.uiSidebarPanel)
        self.splitter.addWidget(self.uiMainPanel)

        self.layout.addWidget(self.splitter)
        self.layout.setStretch(0, 1)
        self.layout.setSpacing(0)

        self.uiStatusBar = self.statusBar()
        self.uiStatusBar.setObjectName('uiStatusBar')
        self.uiStatusBar.showMessage('Starting Up')

        self.uiStatusBar.statusWidget = QWidget(self.uiStatusBar)
        self.uiStatusBar.statusWidget.setObjectName('statusWidget')
        statusWidgetLayout = QHBoxLayout(self.uiStatusBar.statusWidget)
        statusWidgetLayout.setObjectName('statusWidgetLayout')
        statusWidgetLayout.setContentsMargins(0, 0, 0, 0)
        statusWidgetLayout.setSpacing(0)

        self.uiStatusBar.statusWidget.languageLabel = QLabel(
            self.uiStatusBar.statusWidget)
        self.uiStatusBar.statusWidget.languageLabel.setObjectName(
            'languageLabel')
        self.uiStatusBar.statusWidget.languageLabel.setText(
            f'{grabMainWindow().runtimeLang}')
        self.uiStatusBar.statusWidget.languageLabel.setStyleSheet("""
                                                                    color: yellow;
                                                                    font-weight: bold;
                                                                  """)
        self.uiStatusBar.statusWidget.puzzleInfoLabel = PuzzleInfoLabel(
            self.uiStatusBar.statusWidget)

        statusWidgetLayout.addStretch()
        statusWidgetLayout.addWidget(
            self.uiStatusBar.statusWidget.languageLabel)
        statusWidgetLayout.addStretch()
        statusWidgetLayout.addWidget(
            self.uiStatusBar.statusWidget.puzzleInfoLabel)
        statusWidgetLayout.addStretch()

        self.uiStatusBar.addPermanentWidget(self.uiStatusBar.statusWidget)
        self.menuBar = MenuBar(self)

        QMetaObject.connectSlotsByName(self)
        self.uiStatusBar.showMessage('Ready')

    def _resetMainWindow(self):
        self.uiStatusBar.statusWidget.puzzleInfoLabel.reset()
        self.uiMainPanel.puzzleFrame.resetPuzzle()
        grabWidget(QLabel, 'infoDisplayLabel')._resetAction()
        grabWidget(QPushButton, 'setPuzzleBtn')._disableMe()

    def _updateWindow(self):
        self.uiStatusBar.statusWidget.puzzleInfoLabel.update()
        grabPuzzleFrame().onSquareChangeEvent()

    def resizeApp(self):

        _height, _width = getScreenSize()

        self.resize(
            int(floor(float(_height) / 6)),
            floor(int(float(_width) / 12)))


@lru_cache(typed=False)
def getScreenSize():
    cp = QGuiApplication.primaryScreen().availableGeometry().size()
    return cp.height(), cp.width()
