import os
import inspect
import logging
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QFrame, QPushButton, QVBoxLayout, QLabel, QSizePolicy

from Puzzle import puzzle
from py2runtime import RuntimePy as rt

from .uiHelpers import grabMainWindow, grabWidget
uiLogger = logging.getLogger("uiLogger")

class UiSidebar(QFrame):
    """
    Sidebar component for the Sudoku Solver application.
    This class creates a sidebar with buttons for different solver options.
    """

    def __init__(self, parent=None):
        """
        Initializes the sidebar with a specified parent widget.
        :param parent: The parent widget for the sidebar.
        """

        super().__init__(parent)
        # Set up the sidebar properties
        self.setParent(parent)
        self.setObjectName("UiSidebar")
        #self.setFixedWidth(75)  # Adjust width as needed
        self.setContentsMargins(0, 0, 0, 0)
        
        # Example layout and styling
        layout = QVBoxLayout(self)
        layout.setObjectName("uiSidebarLayout")
        layout.setAlignment(Qt.AlignmentFlag.AlignAbsolute)
        self.setLayout(layout)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
        self.setLineWidth(1)
        self.setStyleSheet("""
                            QFrame {
                                padding: 0;
                                margin: 0;
                            }                      
                            QPushButton {
                               font-weight: bold;
                               text-align: left;
                               padding: 2px 2px;
                               margin: 0;
                            }
                            QPushButton:disabled {
                               color: gray;
                            }
                            QPushButton[selected="true"] {
                                font-style: italic;
                            }
                            QPushButton#luajitBtn {
                               color: magenta;
                            }
                            QPushButton#luajitBtn[selected="true"] {
                                border: 2px solid magenta;
                            }
                            QPushButton#luaBtn {
                               color: forestgreen;
                            }
                            QPushButton#luaBtn[selected="true"] {
                                border: 2px solid forestgreen;
                            }
                            QPushButton#juliaBtn {
                                color: cyan;
                            }
                            QPushButton#juliaBtn[selected="true"] {
                                border: 2px solid cyan;
                            }
                            QPushButton#pythonBtn {
                                color: yellow;
                            }
                            QPushButton#pythonBtn[selected="true"] {
                                border: 2px solid yellow;
                            }
                            QPushButton#cythonBtn {
                                color: rgb(169,169,169);
                            }
                            QPushButton#cythonBtn[selected="true"] {
                                border: 2px solid orange;
                            }
                            QPushButton#javascriptBtn {
                                color: rgb(169,169,169);
                            }
                            QPushButton#javascriptBtn[selected="true"] {
                                border: 2px solid rgb(169,169,169);
                            }
                           """)

        self.initUi()

    def initUi(self):
        # Initialize sidebar components here
        # For example, you can add buttons, labels, etc.

        filename = inspect.getframeinfo(inspect.currentframe()).filename
        path = os.path.dirname(os.path.abspath(filename))
        iconpath = os.path.join(os.path.dirname(os.path.dirname(path)), "resources","icons")

        self.luajitBtn = UiSidebarButton("LuaJit", self)
        self.luajitBtn.setObjectName("luajitBtn")
        self.luajitBtn.setEnabled(True)
        self.luajitBtn.setProperty("selected", False)
        self.luajitBtn.setToolTip("Using lupa")
        self.luajitBtn.setIcon(QIcon(os.path.join(iconpath, "luaLogo.ico")))
        
        
        self.luaBtn = UiSidebarButton("Lua", self)
        self.luaBtn.setObjectName("luaBtn")
        self.luaBtn.setEnabled(True)
        self.luaBtn.setProperty("selected", False)
        self.luaBtn.setToolTip("Using lupa solver//LSolver.lua")
        self.luaBtn.setIcon(QIcon(os.path.join(iconpath, "luaLogo.ico")))

        self.juliaBtn = UiSidebarButton("julia", self)
        self.juliaBtn.setObjectName("juliaBtn")
        self.juliaBtn.setEnabled(True)
        self.juliaBtn.setProperty("selected", False)
        self.juliaBtn.setToolTip("Using juliaCall solver//JSolver.jl")
        self.juliaBtn.setIcon(QIcon(os.path.join(iconpath, "juliaLogo.ico")))

        self.pythonBtn = UiSidebarButton("python", self)
        self.pythonBtn.setObjectName("pythonBtn")
        self.pythonBtn.setEnabled(True)
        self.pythonBtn.setProperty("selected", True)
        self.pythonBtn.setToolTip("solver//pySolver.py")
        self.pythonBtn.setIcon(QIcon(os.path.join(iconpath, "pythonLogo.ico")))
        
        self.cythonBtn = UiSidebarButton("cython", self)
        self.cythonBtn.setObjectName("cythonBtn")
        self.cythonBtn.setEnabled(False)
        self.cythonBtn.setProperty("selected", False)
        self.cythonBtn.setToolTip("cython sovler not yet implemented")
        self.cythonBtn.setIcon(QIcon(os.path.join(iconpath, "cythonLogo.ico")))
        
        self.jsBtn = UiSidebarButton("javascript", self)
        self.jsBtn.setObjectName("javascriptBtn")
        self.jsBtn.setEnabled(False)
        self.jsBtn.setProperty("selected", False)
        self.jsBtn.setToolTip("Javascript sovler not yet implemented")
        self.jsBtn.setIcon(QIcon(os.path.join(iconpath, "js.ico")))

        layout = self.layout()
        layout.addStretch(3)
        layout.addWidget(self.luajitBtn)
        layout.addWidget(self.luaBtn)
        layout.addWidget(self.juliaBtn)
        layout.addWidget(self.pythonBtn)
        layout.addWidget(self.cythonBtn)
        layout.addWidget(self.jsBtn)
        #layout.addStretch()

        for btn in [self.luajitBtn, self.luaBtn, self.juliaBtn, self.pythonBtn]:
            btn.clicked.connect(btn.onButtonClicked)


class UiSidebarButton(QPushButton):
    """
    Custom button class for the sidebar.
    This class can be extended to add more functionality to the sidebar buttons.
    """

    def __init__(self, text=None, parent=None):
        super().__init__(text, parent)
        self.setFlat(True)
        self.setText(text)
        self.setParent(parent)
        self.setToolTip(self.objectName())
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Preferred,
                           QSizePolicy.Policy.Expanding)
        

    def onButtonClicked(self, button):
        """
        Set the selected button in the sidebar.
        :param button: The button to be selected.
        """
        uiLogger.debug(f"Button clicked: {self.text()}")
        parent = self.parent()
        for btn in [parent.luajitBtn, parent.luaBtn, parent.juliaBtn, parent.pythonBtn]:
            btn.setProperty("selected", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        for btnName in ["1", "3", "6", "9","A","C","F","I"]:
            borderFrame = grabWidget(QFrame, btnName)
            borderFrame.setProperty("lang",self.text().lower())
            borderFrame.style().unpolish(borderFrame)
            borderFrame.style().polish(borderFrame)
        """
        for headerName in ["A","B","C","D","E","F","G","H","I"]:
            headerObj = grabWidget(QLabel, "RowHeader" + headerName)
            headerObj.setProperty("lang", self.text().lower())
            headerObj.style().unpolish(headerObj)
            headerObj.style().polish(headerObj)
        for headerName in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            headerObj = grabWidget(QLabel, "ColumnHeader" + headerName)
            headerObj.setProperty("lang", self.text().lower())
            headerObj.style().unpolish(headerObj)
            headerObj.style().polish(headerObj)
        """
        pzlDisplayLabel = grabWidget(QLabel,"infoDisplayLabel")
        pzlDisplayLabel.setProperty("lang",self.text().lower())
        pzlDisplayLabel.style().unpolish(pzlDisplayLabel)
        pzlDisplayLabel.style().polish(pzlDisplayLabel)
            
        puzzle.lang = self.text()
        rt.lang = self.text()

        self.setProperty("selected", True)
        self.style().unpolish(self)
        self.style().polish(self)

        grabMainWindow().runtimeLang = self.text()
        languageLabel = grabMainWindow().uiStatusBar.statusWidget.languageLabel
        languageLabel.setText(f"{self.text()}       ")
        languageLabel.setStyleSheet(
            "QLabel#languageLabel { color:"
            + self.palette().color(self.foregroundRole()).name()
            + "; font-weight: bold; } "
        )
