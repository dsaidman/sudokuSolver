from enum import Enum, auto
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from functools import lru_cache

class AppStatusEnum(Enum):
    NotReady = auto()
    Ready = auto()
    Locked = auto()
    Unlocked = auto()
    Solving = auto()
    Solved = auto()

class SquareTypeEnum(Enum):
    Unset = -1
    InputUnlocked = auto()
    InputLocked = auto()
    UserSet = auto()
    Solved = auto()

class ValidityEnum(Enum):
    NoStatement = -1
    Valid = auto()
    Invalid = auto()

class ThemeEnum(Enum):
    Dark = auto()
    Light = auto()

class GuiPalette(QPalette):

    def __init__(self, theTheme=ThemeEnum.Dark):

        super(GuiPalette, self).__init__()

        self.theme = theTheme

        if theTheme == ThemeEnum.Dark:
            self.setColor(QPalette.Window, QColor(30, 30, 30))
            self.setColor(QPalette.WindowText, Qt.white)
            self.setColor(QPalette.Base, QColor(50, 50, 51))
            self.setColor(QPalette.AlternateBase, QColor(41, 44, 51))
            self.setColor(QPalette.ToolTipBase, Qt.white)
            self.setColor(QPalette.ToolTipText, Qt.white)
            self.setColor(QPalette.Text, Qt.white)
            self.setColor(QPalette.Button, QColor(41, 44, 51))
            self.setColor(QPalette.ButtonText, Qt.white)
            self.setColor(QPalette.BrightText, Qt.red)
            self.setColor(QPalette.Highlight, QColor(100, 100, 225))
            self.setColor(QPalette.HighlightedText, Qt.black)

        elif theTheme == ThemeEnum.Light:
            pass


def grabWidget(widgetType, widgetName):
    centralWidget = grabMainWindow().centralWidget
    return centralWidget.findChildren(widgetType, widgetName)[0]


def grabAppInstance():
    return QtWidgets.QApplication([])


@lru_cache(typed=False)
def grabMainWindow():
    return [widget for widget in QtWidgets.QApplication.topLevelWidgets() if isinstance(widget, QtWidgets.QMainWindow)][0]


def grabPuzzleFrame():
    return grabWidget(QtWidgets.QFrame, 'puzzleFrame')


def grabUiFrame():
    return grabWidget(QtWidgets.QFrame, 'UIPanel')


def grabPuzzleSquares():
    return grabPuzzleFrame().squares


def getAppStatus():
    return grabMainWindow().status

def changeQtLineEditProp(widget, prop, newVal):
    widget.setProperty(prop, newVal)
    widget.style().unpolish(widget)
    widget.style().polish(widget)
    widget.update()
