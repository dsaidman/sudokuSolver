from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QPushButton, QVBoxLayout, QLabel

from Puzzle import puzzle
from py2runtime import RuntimePy as rt

from .uiHelpers import grabMainWindow, grabWidget


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
        self.setFixedWidth(75)  # Adjust width as needed
        self.setContentsMargins(0, 0, 0, 0)
        # Example layout and styling
        layout = QVBoxLayout(self)
        layout.setObjectName("uiSidebarLayout")
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignRight)
        layout.setSpacing(3)
        self.setLayout(layout)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)

        self.setLineWidth(1)
        self.setStyleSheet("""
                            QPushButton {
                               padding: 5px;
                               font-weight: bold;
                            }
                            QPushButton:disabled {
                               color: gray;
                            }
                            QPushButton[selected="true"] {
                                border: 1px solid gray;
                                font-style: italic;
                            }
                            QPushButton#luajitBtn {
                               color: magenta;
                            }
                            QPushButton#luaBtn {
                               color: forestgreen;
                            }
                            QPushButton#juliaBtn {
                                color: cyan;
                            }
                            QPushButton#pythonBtn {
                                color: yellow;
                            }
                            QPushButton#cythonBtn {
                                color: orange;
                            }
                           """)

        self.initUi()

    def initUi(self):
        # Initialize sidebar components here
        # For example, you can add buttons, labels, etc.

        self.luajitBtn = UiSidebarButton("LuaJit", self)
        self.luajitBtn.setObjectName("luajitBtn")
        self.luajitBtn.setEnabled(True)
        self.luajitBtn.setProperty("selected", False)
        self.luajitBtn.setToolTip("Using lupa")

        self.luaBtn = UiSidebarButton("Lua", self)
        self.luaBtn.setObjectName("luaBtn")
        self.luaBtn.setEnabled(True)
        self.luaBtn.setProperty("selected", False)
        self.luaBtn.setToolTip("Using lupa")

        self.juliaBtn = UiSidebarButton("julia", self)
        self.juliaBtn.setObjectName("juliaBtn")
        self.juliaBtn.setEnabled(True)
        self.juliaBtn.setProperty("selected", False)
        self.juliaBtn.setToolTip("Using juliaCall")

        self.pythonBtn = UiSidebarButton("python", self)
        self.pythonBtn.setObjectName("pythonBtn")
        self.pythonBtn.setEnabled(True)
        self.pythonBtn.setProperty("selected", True)
        self.pythonBtn.setToolTip("Python sovler not yet implemented")

        layout = self.layout()
        layout.addStretch()
        layout.addWidget(self.luajitBtn)
        layout.addWidget(self.luaBtn)
        layout.addWidget(self.juliaBtn)
        layout.addWidget(self.pythonBtn)
        layout.addStretch()

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
        self.setContentsMargins(0, 0, 0, 0)

    def onButtonClicked(self, button):
        """
        Set the selected button in the sidebar.
        :param button: The button to be selected.
        """

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
