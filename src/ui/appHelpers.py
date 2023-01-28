from enum import Enum, auto, unique
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt


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

theStyleSheet = '''


'''