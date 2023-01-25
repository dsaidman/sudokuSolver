from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from enum import Enum, auto
from functools import cached_property

class ThemeEnum(Enum):
    Dark       = auto()
    Light      = auto()

class GuiPalette(QPalette):

    def __init__(self, theTheme=ThemeEnum.Dark):
        
        super(GuiPalette,self).__init__()
        
        self.theme = theTheme
        
        if theTheme == ThemeEnum.Dark:
            self.setColor(QPalette.Window,QColor(41, 44, 51))
            self.setColor(QPalette.WindowText, Qt.white)
            self.setColor(QPalette.Base, QColor(15, 15, 15))
            self.setColor(QPalette.AlternateBase,QColor(41, 44, 51))
            self.setColor(QPalette.ToolTipBase, Qt.white)
            self.setColor(QPalette.ToolTipText, Qt.white)
            self.setColor(QPalette.Text, Qt.white)
            self.setColor(QPalette.Button, QColor(41, 44, 51))
            self.setColor(QPalette.ButtonText, Qt.white)
            self.setColor(QPalette.BrightText, Qt.red)
            self.setColor(QPalette.Highlight,QColor(100, 100, 225))
            self.setColor(QPalette.HighlightedText, Qt.black)
          
        elif theTheme == ThemeEnum.Light:
            pass
     
