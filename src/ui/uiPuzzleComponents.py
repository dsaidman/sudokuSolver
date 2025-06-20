import logging
import os
import sys
from functools import cached_property
from math import floor

from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)

from Puzzle import puzzle as sudokuDefs

from .uiEnums import AppStatusEnum, SquareTypeEnum, ValidityEnum
from .uiHelpers import (
    grabCurrentSquare,
    grabMainWindow,
    grabPuzzleFrame,
    grabPuzzleSquares,
    grabWidget,
)

# Until i figure out how to do this properly, path hack
sys.path.append(os.path.abspath(".."))
uiLogger = logging.getLogger("uiLogger")


class PuzzleFrame(QFrame):
    """
    A QtWidgets QFrame superclass that contains all the widgets and methods of the sudoku puzzle and its squares.

    Args:
        QtWidgets (QFrame): None, superclass of QFrame parent

    Returns:
        PuzzleFrame: An initialized widget containing the puzzle interface and and other methods
    """

    @property
    def squareCount(self) -> int:
        """
        Counts number of squares that are populated

        Returns:
            int: square count
        """
        return sum(1 for square in self.squares.values() if len(square.text()) > 0)

    @property
    def validSquareCount(self) -> int:
        """
        Counts number of squares that are populated and have values that do not violate any sudoku rules.

        Returns:
            int: square count of squares that do no violate sudoku rules
        """
        return sum(1 for square in self.squares.values() if square.isValid == ValidityEnum.Valid)

    @property
    def isValid(self) -> ValidityEnum:
        """
        Checks if the current puzzle is valid by checking all squares for validity.

        Returns:
            ValidityEnum: ValidityEnum.Valid if all squares are valid, otherwise ValidityEnum.Invalid
        """
        for square in self.squares.values():
            if square.isValid == ValidityEnum.Invalid:
                self._isValid = ValidityEnum.Invalid
                return self._isValid
        self._isValid = ValidityEnum.Valid
        return self._isValid

    def __init__(self, parent):
        """
        Main contructor of PuzzleFrame object that sets up all child widgets and graphic elements.

        Args:
            parent (QtWidget): Parent object of the puzzle frame, assumed the app MainWindow
        """
        super(PuzzleFrame, self).__init__(parent)
        self.setParent(parent)
        # self.setGeometry(QtCore.QRect(10, 130, 911, 691))

        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
        self.setLineWidth(3)
        self.setObjectName("puzzleFrame")
        self.setContentsMargins(0, 0, 0, 0)

        self.puzzleLayout = QGridLayout()
        self.puzzleLayout.setObjectName("puzzleLayout")
        self.puzzleLayout.setSpacing(1)
        self.puzzleLayout.setContentsMargins(0, 0, 0, 0)

        mainPanelLayout = grabWidget(QVBoxLayout, "mainPanelLayout")
        mainPanelLayout.addLayout(self.puzzleLayout)

        self._initSquares()
        self._initHeaders()
        self._initBorderLines()

    def asString(self) -> str:
        """
        Returns current puzzle as string arguments that can be passed into command line version of lua solver.

        Returns:
            str: string of --Key=Value pairs representing current puzzle state
        """
        argList = []
        for squareKey, squareValue in self.squares.items():
            if squareValue.squareType is SquareTypeEnum.InputLocked and len(squareValue.text()) > 0:
                argList.append("--{key}={val}".format(key=squareKey, val=squareValue.text()))
        return " ".join(argList)

    def asDict(self) -> dict:
        """
        Returns current puzzle as a python dict

        Returns:
            dict: Puzzle in dict
        """
        argList = {}
        for squareKey, squareValue in self.squares.items():
            if squareValue.squareType is SquareTypeEnum.InputLocked and len(squareValue.text()) > 0:
                argList[squareKey] = squareValue.text()
        return argList

    def onSquareChangeEvent(self):
        """
        Event handler for square change events.
        This method is called whenever a square's value changes, and it updates the UI accordingly.
        It refreshes all squares to reflect their current state and validity.

        Args:
            None
        Returns:
            None
        """
        uiLogger.debug("Square change event called")
        for puzzleSquares in self.squares.values():
            puzzleSquares._refresh()

    def toggleLock(self):
        """
        Toggles the lock state of the puzzle.
        This method checks the current validity of the puzzle and updates the square types accordingly.
        If the puzzle is valid, it locks the squares and updates the button text.
        If the puzzle is invalid or locked, it unlocks the squares and updates the button text.
        Args:
            None
        Returns:
            None
        """
        uiLogger.debug("Toggling puzzle frame lock")
        puzzleValid = grabPuzzleFrame().isValid
        solveBtn = grabWidget(QPushButton, "solveBtn")
        setBtn = grabWidget(QPushButton, "setPuzzleBtn")
        if puzzleValid == ValidityEnum.Invalid or grabMainWindow().status == AppStatusEnum.Locked:
            for square in self.squares.values():
                square.setReadOnly(False)
                square.squareType = SquareTypeEnum.InputUnlocked
                square.setReadOnly(False)
                square.setProperty("squareType", "InputUnlockedAndValid")
                self.style().polish(self)
                self.style().unpolish(self)
                self.update()

            grabMainWindow().status = AppStatusEnum.Unlocked
            solveBtn._disableMe()
            setBtn.setText("Lock")
        elif (
            grabMainWindow().status == AppStatusEnum.Unlocked and puzzleValid == ValidityEnum.Valid
        ):
            for square in self.squares.values():
                if len(square.text()) > 0 and square.squareType == SquareTypeEnum.InputUnlocked:
                    square.squareType = SquareTypeEnum.InputLocked
                    square.setReadOnly(True)
                if len(square.text()) == 0:
                    square.squareType = SquareTypeEnum.UserSet
            grabMainWindow().status = AppStatusEnum.Locked
            solveBtn._enableMe()
            setBtn.setText("Locked")
        self.onSquareChangeEvent()

    def _setNewFocus(self, oldKey, newKey) -> bool:
        """
        Sets the focus to a new square based on the old key and new key.
        This method clears the focus from the old square and sets it to the new square.
        Args:
            oldKey (str): The key of the square that currently has focus.
            newKey (str): The key of the square to which focus should be set.
        Returns:
            bool: True if the focus was successfully set to the new square, False otherwise.
        """
        uiLogger.debug(f"Setting focus to {newKey:s}")
        returnVal = False
        if oldKey in self.squares and oldKey != newKey:
            self.squares[oldKey].clearFocus()
        elif oldKey is None:
            for key in self.squares:
                if key != newKey and self.squares[key].hasFocus():
                    self.squares[key].clearFocus()
                    break

        if newKey in self.squares:
            self.squares[newKey].setFocus()
            returnVal = True
            self._setFocusCursor(newKey)

        return returnVal

    def _setFocusCursor(self, key=None) -> None:
        """
        Sets the cursor position to the beginning of the square with the given key.
        If no key is provided, it uses the current object's name as the key.
        Args:
            key (str, optional): The key of the square to set the cursor position. Defaults to None.
        Returns:
            None
        """

        if key is None:
            uiLogger.debug(f"Setting cursor to {key:s}")
            key = self.objectName()
        self.squares[key].setCursorPosition(0)

    def _initSquares(self) -> None:
        """
        Initializes the puzzle squares and adds them to the puzzle layout.
        This method creates instances of PuzzleSquare for each square defined in sudokuDefs.squares,
        sets their properties, and adds them to the puzzle layout.
        Args:
            None
        Returns:
            None
        """
        uiLogger.debug("Initializing Puzzle Squares")
        squares = {}
        for squareKey in sudokuDefs.squares:
            squares[squareKey] = PuzzleSquare(self, squareKey)

            self.puzzleLayout.addWidget(
                squares[squareKey],
                3
                + sudokuDefs.rows.index(squareKey[0])
                + floor(sudokuDefs.rows.index(squareKey[0]) / 3.0),
                3
                + sudokuDefs.columns.index(squareKey[1])
                + floor(sudokuDefs.columns.index(squareKey[1]) / 3.0),
                1,
                1,
            )
            squares[squareKey].installEventFilter(self)
        self.squares = squares

    def _initHeaders(self) -> None:
        """
        Initializes the row and column headers for the puzzle frame.
        This method creates instances of PuzzleHeader for each row and column defined in sudokuDefs,
        sets their properties, and adds them to the puzzle layout.
        Args:
            None
        Returns:
            None
        """
        uiLogger.debug("Initializing Puzzle Headers")
        rowHeaders = {}
        for rowKey in sudokuDefs.rows:
            rowHeaders[rowKey] = PuzzleHeader(self, rowKey, "RowHeader" + rowKey)
            rowHeaders[rowKey].setObjectName("RowHeader" + rowKey)
            self.puzzleLayout.addWidget(
                rowHeaders[rowKey],
                3 + sudokuDefs.rows.index(rowKey) + floor(sudokuDefs.rows.index(rowKey) / 3.0),
                1,
                1,
                1,
            )
        self.rowHeaders = rowHeaders

        colHeaders = {}
        for colKey in sudokuDefs.columns:
            colHeaders[colKey] = PuzzleHeader(self, colKey, "ColumnHeader" + colKey)
            colHeaders[colKey].setObjectName("ColumnHeader" + colKey)
            self.puzzleLayout.addWidget(
                colHeaders[colKey],
                1,
                3
                + sudokuDefs.columns.index(colKey)
                + floor(sudokuDefs.columns.index(colKey) / 3.0),
                1,
                1,
            )
        self.colHeaders = colHeaders

    def _initBorderLines(self) -> None:
        """
        Initializes the border lines for the puzzle frame.
        This method creates vertical and horizontal lines to visually separate the squares in the puzzle.
        It adds these lines to the puzzle layout at appropriate positions based on the sudoku grid structure.
        Args:
            None
        Returns:
            None
        """
        uiLogger.debug("Initializing Puzzle Border Lines")
        # LineBorders
        lineBorders = {}
        for vertLineNum in ["1", "3", "6", "9"]:
            lineBorders[vertLineNum] = PuzzleBorderLine(
                self, QFrame.Shape.VLine, "verticalLine" + vertLineNum
            )
            lineBorders[vertLineNum].setObjectName(vertLineNum)
            self.puzzleLayout.addWidget(
                lineBorders[vertLineNum],
                1,
                2 + (4 * (["1", "3", "6", "9"].index(vertLineNum))),
                13,
                1,
            )

        for horizLineNum in ["A", "C", "F", "I"]:
            lineBorders[horizLineNum] = PuzzleBorderLine(
                self, QFrame.Shape.HLine, "horizontalLine" + horizLineNum
            )
            lineBorders[horizLineNum].setObjectName(horizLineNum)
            self.puzzleLayout.addWidget(
                lineBorders[horizLineNum],
                2 + (4 * ["A", "C", "F", "I"].index(horizLineNum)),
                1,
                1,
                13,
            )

        self.lineBorders = lineBorders

    def eventFilter(self, source, event) -> bool:
        """
        Event filter for the puzzle frame to handle key presses and focus events.
        This method checks if the event is a key press or focus event and updates the focus accordingly.
        Args:
            source (QObject): The object that sent the event.
            event (QEvent): The event that occurred.
        Returns:
            bool: True if the event was handled, False otherwise.
        """

        if isinstance(source, PuzzleSquare) and event.type() == event.Type.KeyPress:
            sourceObjectName = source.objectName()
            rowNum = sourceObjectName[0]
            colNum = sourceObjectName[1]
            if event.key() == Qt.Key.Key_Up:
                newFocusCol = colNum
                newFocusRow = sudokuDefs.rows[
                    (sudokuDefs.rows.index(rowNum) - 1) % len(sudokuDefs.rows)
                ]
                return self._setNewFocus(sourceObjectName, newFocusRow + newFocusCol)
            elif event.key() == Qt.Key.Key_Down:
                newFocusCol = colNum
                newFocusRow = sudokuDefs.rows[
                    (sudokuDefs.rows.index(rowNum) + 1) % len(sudokuDefs.rows)
                ]
                return self._setNewFocus(sourceObjectName, newFocusRow + newFocusCol)
            elif event.key() == Qt.Key.Key_Tab or event.key() == Qt.Key.Key_Right:
                newKey = sudokuDefs.squares[
                    (sudokuDefs.squares.index(sourceObjectName) + 1) % len(sudokuDefs.squares)
                ]
                return self._setNewFocus(sourceObjectName, newKey)
            elif event.key() == Qt.Key.Key_Left:
                newKey = sudokuDefs.squares[
                    (sudokuDefs.squares.index(sourceObjectName) - 1) % len(sudokuDefs.squares)
                ]
                return self._setNewFocus(sourceObjectName, newKey)
            else:
                return False
        elif isinstance(source, PuzzleSquare) and (
            (event.type() == QEvent.Type.FocusIn)
            or (event.type() == QEvent.Type.MouseButtonRelease)
        ):
            if source.isEnabled():
                sourceObjectName = source.objectName()
                self._setFocusCursor(sourceObjectName)
                return False
            else:
                return False
        return False

    def resetPuzzle(self) -> None:
        """
        Resets the puzzle frame to its initial state.
        This method clears all squares, resets their types, and updates their styles.
        It also resets the puzzle frame's properties and updates the UI accordingly.
        Args:
            None
        Returns:
            None
        """
        uiLogger.debug("Performing puzzle frame reset action")
        puzzleFrame = grabPuzzleFrame()
        for squareVal in puzzleFrame.squares.values():
            squareVal._onResetAction()


class PuzzleSquare(QLineEdit):
    """A QtWidgets QLineEdit subclass that represents a single square in the sudoku puzzle.
    This class handles the square's type, neighbors, validity, and other properties.
    It also provides methods to update the square's state and appearance based on user input and puzzle rules.

    Args:
        QtWidgets (QLineEdit): None, superclass of QLineEdit parent
    Returns:
        PuzzleSquare: An initialized widget representing a single square in the sudoku puzzle.
    """

    @property
    def squareType(self):
        return self._squareType

    @squareType.setter
    def squareType(self, squareValueSetting):
        if self._squareType != squareValueSetting:
            self._squareType = squareValueSetting
        self.setStatusTip("{name}: {status}".format(name=self.name, status=self.squareType.name))

    @property
    def name(self):
        return self.objectName()

    @cached_property
    def neighborKeys(self):
        return self._neighborKeys

    @property
    def neighbors(self):
        squares = grabPuzzleSquares()
        return {squareKey: squares[squareKey] for squareKey in self.neighborKeys}

    @property
    def nextSquare(self):
        return self._nextSquare

    @property
    def lastSquare(self):
        return self._lastSquare

    @property
    def isValid(self):
        myValue = self.text()
        retVal = ValidityEnum.Valid
        if len(myValue) > 0:
            for neighborSquare in self.neighbors.values():
                if myValue in neighborSquare.text():
                    retVal = ValidityEnum.Invalid
                    break
        else:
            retVal = ValidityEnum.NoStatement

        if self._isValid != retVal:
            self._isValid = retVal
            self.setToolTip("Square {name}: {tip}".format(name=self.name, tip=retVal.name))
        self._isValid = retVal
        return self._isValid

    def __init__(self, parent, objectName=None):
        super(PuzzleSquare, self).__init__(parent, objectName=None)

        self.setObjectName(objectName)
        self.setParent(parent)
        # self.setSizePolicy(self.sizePolicy())
        self.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.setAcceptDrops(True)
        self.setInputMethodHints(Qt.InputMethodHint.ImhDigitsOnly)
        self.setInputMask("d")
        self.setText("")
        self.setMaxLength(1)
        self.setFrame(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setDragEnabled(True)
        self.setPlaceholderText("")
        self.setClearButtonEnabled(False)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self._nextSquare = sudokuDefs.nextSquare(self.name)
        self._lastSquare = sudokuDefs.lastSquare(self.name)
        self._isValid = ValidityEnum.Valid
        self._neighborKeys = sudokuDefs.neighbors(self.name)
        self._squareType = SquareTypeEnum.InputUnlocked
        self.setProperty("squareType", "InputUnlockedAndValid")

        self.setStyleSheet(
            """
            QLineEdit[squareType="InputUnlockedAndValid"]{
                color:	rgb(255,140,0);
                font-weight: bold;
                font-style: normal;
                background-color: rgb(30, 30, 30);
                border-color: rgb(255, 140, 0)}
            QLineEdit[squareType="InputUnlockedAndInvalid"] {
                color: rgb(255, 0, 0);
                font-weight: normal;
                font-style: italic}
            QLineEdit[squareType="InputLockedAndValid"]{
                color: rgb(255, 140, 0);
                font-weight: bold;
                font-style: normal;
                background-color: rgb(30, 30, 30);}
            QLineEdit[squareType="UserSetAndValid"]{
                color:	rgb(212,255,200);
                font-weight: normal;
                font-style: regular}
            QLineEdit[squareType="SolvedAndValid"] {
                color: rgba(0, 255, 0,204);
                font-weight: normal;
                font-style: regular}
            QLineEdit[isNeighbor="true"]{
                background-color: rgba(90, 3, 114, 0.3)};
            """
        )

        self.setToolTip("Square {name}: {tip}".format(name=self.name, tip=self._isValid.name))
        self.textEdited.connect(self.onChanged)
        self.textEdited.connect(grabPuzzleFrame().onSquareChangeEvent)

    def focusInEvent(self, evnt):
        currentSquare = grabCurrentSquare()
        allSquares = grabPuzzleSquares()
        grabMainWindow().uiStatusBar.showMessage(currentSquare.objectName())
        for neighborKey in currentSquare.neighborKeys:
            allSquares[neighborKey].setProperty("isNeighbor", "true")
            allSquares[neighborKey].style().polish(allSquares[neighborKey])
            allSquares[neighborKey].style().unpolish(allSquares[neighborKey])
        for nonNeighborKey in list(
            set(allSquares.keys())
            - set(currentSquare.neighborKeys)
            - set(currentSquare.objectName())
        ):
            allSquares[nonNeighborKey].setProperty("isNeighbor", "false")
            allSquares[nonNeighborKey].style().polish(allSquares[nonNeighborKey])
            allSquares[nonNeighborKey].style().unpolish(allSquares[nonNeighborKey])
        return super().focusInEvent(evnt)

    def onChanged(self, newTextStr):
        uiLogger.debug("Performing PuzzleSquare onChanged action")
        _prevText = self.text()
        _newText = newTextStr
        _newTextStr = list([val for val in _newText if val.isnumeric()])
        if not _newTextStr:
            self.setText("")
            _nextKey = self.lastSquare
        else:
            self.setText(newTextStr[0])
            _nextKey = self.nextSquare

        # Jump to next square in tab order
        grabPuzzleFrame()._setNewFocus(self.objectName(), _nextKey)

    def _onResetAction(self):
        uiLogger.debug("Performing PuzzleSquare _onResetAction action")
        self.setEnabled(True)
        self.setText("")
        self.squareType = SquareTypeEnum.InputUnlocked
        self._isValid = ValidityEnum.Valid
        self.setProperty("squareType", "InputUnlockedAndValid")
        self.style().unpolish(self)
        self.style().polish(self)

    def _refresh(self):
        # uiLogger.debug("Performing PuzzleSquare _refresh action")
        isValid = self.isValid
        if isValid == ValidityEnum.Valid and self.squareType == SquareTypeEnum.InputUnlocked:
            self.setProperty("squareType", "InputUnlockedAndValid")
        elif isValid == ValidityEnum.Invalid and self.squareType == SquareTypeEnum.InputUnlocked:
            self.setProperty("squareType", "InputUnlockedAndInvalid")
        elif isValid == ValidityEnum.Valid and self.squareType == SquareTypeEnum.InputLocked:
            self.setProperty("squareType", "InputLockedAndValid")
        elif (
            isValid == ValidityEnum.Valid or isValid == ValidityEnum.NoStatement
        ) and self.squareType == SquareTypeEnum.UserSet:
            self.setProperty("squareType", "UserSetAndValid")
        elif isValid == ValidityEnum.Valid and self.squareType == SquareTypeEnum.Solved:
            self.setProperty("squareType", "SolvedAndValid")
        self.style().unpolish(self)
        self.style().polish(self)

        self.setToolTip(
            "Square {name}: {valid} - {status}".format(
                name=self.name, valid=self._isValid.name, status=self._squareType.name
            )
        )


class PuzzleBorderLine(QFrame):
    def __init__(self, parent, frameShape, objectName=None):
        super(PuzzleBorderLine, self).__init__(parent, objectName=None)
        self.setObjectName(objectName)
        self.setParent(parent)
        self.setLineWidth(3)
        self.setFrameShape(frameShape)
        self.setFrameShadow(QFrame.Shadow.Plain)
        self.setProperty("lang", "python")
        self.setStyleSheet("""
                            QFrame[lang="luajit"] {
                                background-color: magenta;
                                border-color: magenta;
                                color: magenta;
                            }
                            QFrame[lang="lua"] {
                                background-color: forestgreen;
                                border-color: forestgreen;
                                color: forestgreen;
                            }
                            QFrame[lang="julia"] {
                                background-color: cyan;
                                border-color: cyan;
                                color: cyan;
                            }
                            QFrame[lang="python"] {
                                background-color: yellow;
                                border-color: yellow;
                                color: yellow;
                            }
                            QFrame[lang="cython"] {
                                background-color: orange;
                                border-color: orange;
                                color: orange;
                            }
                           """)


class PuzzleHeader(QLabel):
    def __init__(self, parent, text=None, objectName=None):
        super(PuzzleHeader, self).__init__(parent, text=None, objectName=None)

        headerFont = QFont()
        headerFont.setPointSize(12)
        headerFont.setBold(True)

        self.setObjectName(objectName)
        self.setParent(parent)
        self.setText("  " + text + "  ")
        self.setScaledContents(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(headerFont)
        # self.setProperty("lang","python")
        self.setStyleSheet("""
                           QLabel {
                               background-color: rgb(70,70,70);
                               border-color: rgb(70,70,70)
                               }
                            QLabel[lang="luajit"] {
                                color: magenta;
                            }
                            QLabel[lang="lua"] {
                                color: forestgreen;
                            }
                            QLabel[lang="julia"] {
                                color: cyan;
                            }
                            QLabel[lang="python"] {
                                color: yellow;
                            }
                            QLabel[lang="cython"] {
                                color: orange;
                            }
                           """)
