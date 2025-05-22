from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt


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
        layout.setObjectName('uiSidebarLayout')
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
                               color: green;
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
        self.luaBtn.setEnabled(False)
        self.luaBtn.setProperty("selected", False)
        self.luaBtn.setToolTip("Using lupa")
        
        self.juliaBtn  = UiSidebarButton("julia", self)
        self.juliaBtn.setObjectName("juliaBtn")
        self.juliaBtn.setEnabled(True) 
        self.juliaBtn.setProperty("selected", True)
        self.juliaBtn.setToolTip("Using juliaCall")
        
        self.pythonBtn = UiSidebarButton("python", self)
        self.pythonBtn.setObjectName("pythonBtn")
        self.pythonBtn.setEnabled(False)
        self.pythonBtn.setProperty("selected", False)
        self.pythonBtn.setToolTip("Python sovler not yet implemented")
        
        self.cythonBtn = UiSidebarButton("cython", self)
        self.cythonBtn.setObjectName("cythonBtn")
        self.cythonBtn.setEnabled(False)
        self.cythonBtn.setProperty("selected", False)
        self.cythonBtn.setToolTip("cython sovler not yet implemented")
        
        layout = self.layout()
        layout.addStretch()
        layout.addWidget(self.luajitBtn)
        layout.addWidget(self.luaBtn)
        layout.addWidget(self.juliaBtn)
        layout.addWidget(self.pythonBtn)
        layout.addWidget(self.cythonBtn)
        layout.addStretch()
        
        for btn in [self.luajitBtn, self.luaBtn, self.juliaBtn, self.pythonBtn, self.cythonBtn]:
            btn.clicked.connect(btn.onButtonClicked)
        
class UiSidebarButton(QPushButton):
    """
    Custom button class for the sidebar.
    This class can be extended to add more functionality to the sidebar buttons.
    """
    def __init__(self, text=None,parent=None):
        super().__init__(text,parent)
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
        for btn in [parent.luajitBtn, parent.luaBtn, parent.juliaBtn, parent.pythonBtn, parent.cythonBtn]:
            btn.setProperty("selected", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        self.setProperty("selected", True)
        self.style().unpolish(self)
        self.style().polish(self)

