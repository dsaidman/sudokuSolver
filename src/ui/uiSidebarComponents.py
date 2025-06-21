import inspect
import logging
import os
from random import randint

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QIcon
from PyQt6.QtWidgets import (
    QDialog,
    QFrame,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSlider,
    QVBoxLayout,
)

from Puzzle import puzzle
from Puzzle import puzzle as sudokuDefs
from py2runtime import RuntimePy as rt

from .uiEnums import SquareTypeEnum
from .uiHelpers import (
    grabMainWindow,
    grabPuzzleFrame,
    grabPuzzleSquares,
    grabWidget,
)
from .uiPuzzleFile import puzzleInput

uiLogger = logging.getLogger("uiLogger")
__all__ = ["UiSidebar"]


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
        # self.setFixedWidth(75)  # Adjust width as needed
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
        iconpath = os.path.join(os.path.dirname(os.path.dirname(path)), "resources", "icons")
        puzzlePath = os.path.join(os.path.dirname(os.path.dirname(path)), "resources", "icons")

        self.importBtn = UiSidebarButton("Import", self)
        self.importBtn.setObjectName("importBtn")
        self.importBtn.setEnabled(True)
        self.importBtn.setIcon(QIcon(os.path.join(iconpath, "importIcon.ico")))
        self.importBtn.setToolTip(f"Import a puzzle from {puzzlePath:s}")
        self.importBtn.clicked.connect(PuzzleSelectDlg)

        self.resetBtn = UiSidebarButton("Reset", self)
        self.resetBtn.setObjectName("resetBtn")
        self.resetBtn.setEnabled(True)
        self.resetBtn.setIcon(QIcon(os.path.join(iconpath, "resetIcon.ico")))
        self.resetBtn.setToolTip("Reset to blank puzzle")
        self.resetBtn.clicked.connect(grabMainWindow()._resetMainWindow)

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
        layout.addWidget(self.importBtn)
        layout.addWidget(self.resetBtn)
        layout.addStretch(3)
        layout.addWidget(self.luajitBtn)
        layout.addWidget(self.luaBtn)
        layout.addWidget(self.juliaBtn)
        layout.addWidget(self.pythonBtn)
        layout.addWidget(self.cythonBtn)
        layout.addWidget(self.jsBtn)
        # layout.addStretch()

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
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

    def onButtonClicked(self, button):
        """
        Handles the button click event in the sidebar.
        Updates the selected state of all buttons, updates the UI styling for various elements,
        and sets the current language for the puzzle solver.

        Args:
            button: The button that was clicked

        Effects:
            - Updates selected state of all sidebar buttons
            - Updates border frame language properties
            - Updates puzzle display label language property
            - Sets puzzle and runtime language
            - Updates main window runtime language
            - Updates status bar language label
        """
        uiLogger.debug(f"Button clicked: {self.text()}")
        parent = self.parent()
        for btn in [parent.luajitBtn, parent.luaBtn, parent.juliaBtn, parent.pythonBtn]:
            btn.setProperty("selected", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        for btnName in ["1", "3", "6", "9", "A", "C", "F", "I"]:
            borderFrame = grabWidget(QFrame, btnName)
            borderFrame.setProperty("lang", self.text().lower())
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
        pzlDisplayLabel = grabWidget(QLabel, "infoDisplayLabel")
        pzlDisplayLabel.setProperty("lang", self.text().lower())
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


class PuzzleSelectDlg(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Select Puzzle")
        self.setObjectName("PuzzleSelectDlg")
        self.setContentsMargins(0, 0, 0, 0)
        self.initUi()

    def initUi(self):
        self.leftbtn = QPushButton(">", self)
        self.leftbtn.setContentsMargins(0, 0, 0, 0)
        self.leftbtn.setFlat(True)
        self.leftbtn.clicked.connect(self._addOne)
        self.leftbtn.setFixedWidth(20)

        self.rightbtn = QPushButton("<", self)
        self.rightbtn.setContentsMargins(0, 0, 0, 0)
        self.rightbtn.setFlat(True)
        self.rightbtn.setFixedWidth(20)
        self.rightbtn.clicked.connect(self._loseOne)

        self.leftpagebtn = QPushButton(">>>", self)
        self.leftpagebtn.setContentsMargins(0, 0, 0, 0)
        self.leftpagebtn.setFlat(True)
        self.leftpagebtn.clicked.connect(self._addOneT)
        self.leftpagebtn.setFixedWidth(20)

        self.rightpagebtn = QPushButton("<<<", self)
        self.rightpagebtn.setContentsMargins(0, 0, 0, 0)
        self.rightpagebtn.setFlat(True)
        self.rightpagebtn.setFixedWidth(20)
        self.rightpagebtn.clicked.connect(self._loseOneT)

        self.sliderbar = QSlider(Qt.Orientation.Horizontal, self)
        self.sliderbar.setContentsMargins(0, 0, 0, 0)
        self.sliderbar.setFixedWidth(400)
        self.sliderbar.setTickInterval(500)
        self.sliderbar.setMinimum(puzzleInput.minID)
        self.sliderbar.setMaximum(puzzleInput.maxID)
        self.sliderbar.setSingleStep(1)
        self.sliderbar.setPageStep(1000)
        self.sliderbar.setValue(randint(puzzleInput.minID, puzzleInput.maxID))
        self.sliderbar.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.sliderbar.valueChanged.connect(self.update)

        self.selectionlabel = QLineEdit(str(self.sliderbar.value()), self)
        self.selectionlabel.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
        )
        self.selectionlabel.setContentsMargins(0, 0, 0, 0)
        self.selectionlabel.textChanged.connect(self.update)
        self.selectionlabel.setInputMethodHints(Qt.InputMethodHint.ImhDigitsOnly)
        self.selectionlabel.setCursor(QCursor(Qt.CursorShape.IBeamCursor))

        self.okButton = QPushButton("OK", self)
        self.okButton.setContentsMargins(0, 0, 0, 0)
        self.okButton.setFlat(True)
        self.okButton.setFixedWidth(20)
        self.okButton.clicked.connect(
            lambda state: _setUiPuzzle(puzzleInput.puzzles[self.sliderbar.value()])
        )
        self.okButton.clicked.connect(self.close)
        self.okButton.clicked.connect(grabPuzzleFrame().toggleLock)
        self.okButton.clicked.connect(grabWidget(QPushButton, "setPuzzleBtn")._enableMe)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.rightpagebtn, 0, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.rightbtn, 0, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.sliderbar, 0, 2, 4, 1, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.leftbtn, 0, 7, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.leftpagebtn, 0, 8, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.selectionlabel, 0, 2, 4, 1, Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.okButton, 1, 2, 4, 1, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)
        self.show()

    def update(self, value):
        uiLogger.debug(f"Slider value changed to {value}")
        self.sliderbar.setValue(int(value))
        self.selectionlabel.setText(str(self.sliderbar.value()))

    def _addOne(self):
        self.sliderbar.setValue(min(self.sliderbar.value() + 1, 16402))

    def _loseOne(self):
        self.sliderbar.setValue(max(self.sliderbar.value() - 1, 0))

    def _addOneT(self):
        self.sliderbar.setValue(min(self.sliderbar.value() + 1000, 16402))

    def _loseOneT(self):
        self.sliderbar.setValue(max(self.sliderbar.value() - 1000, 0))


def _setUiPuzzle(dotPuzzle) -> None:
    squares = grabPuzzleSquares()

    squareKeys = sudokuDefs.squares

    for idx, val in enumerate(dotPuzzle):
        sq = squares[squareKeys[idx]]
        if val == ".":
            sq.squareType = SquareTypeEnum.InputUnlocked
            sq.setProperty("squareType", "UserSetAndValid")
        else:
            sq.setText(val)
            sq.squareType = SquareTypeEnum.InputLocked
            sq.setProperty(
                "squareType", "InputLockedAndValid"
            )  # We'll assume for now input puzzles are are valid
        sq._refresh()
    grabMainWindow()._updateWindow()
    grabPuzzleFrame().toggleLock()
    grabWidget(QPushButton, "setPuzzleBtn")._enableMe()
