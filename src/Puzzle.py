import logging
from enum import Enum
from functools import cache, cached_property

from py2runtime import RuntimePy as rt

uiLogger = logging.getLogger("uiLogger")


class SudokuPuzzle(object):
    def __init__(self, lang: str = "python", value="." * 81):
        self._lang = lang
        rt.lang = lang
        self.value = value
        self.solution = None

    @property
    def runtimes(self) -> list[str]:
        return self._lang

    @property
    def value(self) -> dict[str, str]:
        return self._value

    @value.setter
    def value(self, inPuzzle) -> None:
        ptype = type(inPuzzle)

        pzl = {sq: [1, 2, 3, 4, 5, 6, 7, 8, 9] for sq in self.squares}

        if ptype is dict:
            for sqKey, sqValue in inPuzzle.items():
                pzl[sqKey] = [int(sqValue)]
        elif ptype is str and len(inPuzzle) == 81:
            for idx, val in enumerate(inPuzzle):
                if val != ".":
                    pzl[self.squares[idx]] = [int(val)]
        self._value = pzl

    @property
    def runtime(self) -> str:
        return self._lang

    @runtime.setter
    def runtime(self, lang: str) -> None:
        if lang.lower() not in ["luajit", "lua", "julia", "python"]:
            raise ValueError(
                "Invalid language specified. Choose from 'luajit','lua', 'julia', or 'python'."
            )
        self.lang = lang
        rt.lang = lang

    @cached_property
    def rows(self):
        """
        Returns the rows letters of the puzzle as a list of strings.

        Returns:
            list: capital let`ters A to I
        """
        if self.runtime == "luajit" or self.runtime == "lua":
            return sorted(list(rt.definitions.rowNames.values()))
        elif self.runtime == "julia":
            return sorted(list(rt.definitions.rowNames))
        elif self.runtime == "python":
            return sorted(rt.definitions.rowNames)

    @cached_property
    def columns(self):
        """
        Returns the column numbers of the puzzle as a list of strings.

        Returns:
            list: capital letters A to I
        """
        if self.runtime == "luajit" or self.runtime == "lua":
            return sorted(list(rt.definitions.colNames.values()))
        elif self.runtime == "julia":
            return sorted(list(rt.definitions.columnNames))
        elif self.runtime == "python":
            return sorted(rt.definitions.columnNames)

    @cached_property
    def squares(self) -> list[str]:
        """
        Returns list of all square tile keys A1-I9 - 81 total.

        Returns:
            list: cached list of keys
        """
        if self.runtime == "luajit" or self.runtime == "lua":
            return sorted(list(rt.definitions.allKeys.values()), reverse=False)
        elif self.runtime == "julia":
            return sorted(list(rt.definitions.squares), reverse=False)
        elif self.runtime == "python":
            return sorted(rt.definitions.squares)

    @cache
    def nextSquare(self, currentKey: str) -> str:
        """
        Returns next square in list of square keys A1->I9.

        Args:
            currentKey (str): A square tile ID

        Returns:
            str: The key of the next tile in order A1->I9. For example, nextSquare('A2') returns A3. nextSquare('I9') returns A1
        """
        return self.squares[((self.squares.index(currentKey) + 1) % len(self.squares))]

    @cache
    def lastSquare(self, currentKey: str) -> str:
        """
        Returns previous square in list of square keys A1->I9.

        Args:
            currentKey (str): A square tile ID A1->I9

        Returns:
            str: The key of the previous tile in order A1->I9. For example, nextSquare('A2') returns A1. nextSquare('A1') returns I9
        """
        return self.squares[((self.squares.index(currentKey) + -1) % len(self.squares))]

    @cache
    def neighbors(self, squareID: str) -> list[str]:
        """
        Returns list of squareID that cannot share the same value.

        The cached helper function returns a list of square tile IDs that cannot share the same value as the input tile.
        A neighbor is definited as another square tile in the same row, column, or cell.
        The function returns a unique list containing all the squares tiles sharing the same row, column or cell.
        The function is performed in the getNeighbors() function of definitions.lua.

        Args:
            squareID (str): A square tile ID A1->I9

        Returns:
            list: Unique list of strings of squares that cannot share same value
        """
        if self.runtime == "luajit":
            return list(rt.definitions["getNeighbors"](squareID))
        elif self.runtime == "julia":
            return list(rt.definitions.neighbors[squareID])
        elif self.runtime == "python":
            return rt.definitions.neighbors[squareID]

    def solve(self) -> dict[str, str]:
        puzzleArg = self.value

        self.lang = rt.lang
        if rt.lang == "luajit" or rt.lang == "lua":
            puzzleArg = {
                k: "".join([str(x) for x in puzzleArg[k]]) for k in puzzleArg.keys()
            }  # temporary
            puzzleArg = rt.dict2Table(puzzleArg)
            solveFun = rt.solver["solve"]
        elif rt.lang == "julia":
            puzzleArg = rt.runtime.copy(rt.definitions.puzzle0)
            for k, v in self.value.items():
                puzzleArg[k] = v
            solveFun = rt.solver.solve
        elif rt.lang == "python":
            solveFun = rt.solver
            # Everything is ready to call

        result = solveFun(puzzleArg)

        if self._lang != "python":  # Convert lua table to a dict
            result = dict(result)
            result["solution"] = dict(result["solution"])

        if type(result) is dict and "numRecursions" in result:
            result["difficultyLevel"] = getDifficulty(result["numRecursions"])

        self.solution = dict(result["solution"])

        return result

    def clear(self):
        self.value = "." * 81
        self.solution = None


class DifficultyLevel(Enum):
    TRIVIAL = 0
    EASY = 1
    MEH = 2
    HARD = 3
    VERYHARD = 4
    EVIL = 5
    DASTURDLY_EVIL = 6


def getDifficulty(numRecursions: int) -> Enum:
    if numRecursions == 0:
        retVal = DifficultyLevel.TRIVIAL
    elif numRecursions < 5:
        retVal = DifficultyLevel.EASY
    elif numRecursions < 25:
        retVal = DifficultyLevel.MEH
    elif numRecursions < 50:
        retVal = DifficultyLevel.HARD
    elif numRecursions < 100:
        retVal = DifficultyLevel.VERYHARD
    elif numRecursions < 400:
        retVal = DifficultyLevel.EVIL
    else:
        retVal = DifficultyLevel.DASTURDLY_EVIL

    return retVal.name


puzzle = SudokuPuzzle()
