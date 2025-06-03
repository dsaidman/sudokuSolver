from functools import cached_property

from solver.py2runtime import RuntimePy as rt

class SudokuPuzzle:
    def __init__(self, lang = None, pzlStr:str="."*81):
        self._lang    = None
        self.value    = pzlStr

    @property
    def runtimes(self) -> list[str]:
        return self._lang

    @property
    def value(self) -> dict[str,str]:
        return self._value

    @value.setter
    def value(self,pzlStr:str) -> None:
        self._value = {sqKey : sqValue if sqValue !="." else "123456789" for sqKey, sqValue in enumerate(pzlStr) }

    @property
    def runtime(self)  -> str:
        return self._lang
    
    @runtime.setter
    def runtime(self,lang : str) -> None:
        
        if lang.lower() not in ["luajit", "lua", "julia", "python"]:
            raise ValueError(
                "Invalid language specified. Choose from 'luajit','lua', 'julia', or 'python'."
            )
        self._lang = lang
        rt.lang    = lang

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
    def squares(self):
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

    @cached_property
    def nextSquare(self, currentKey):
        """
        Returns next square in list of square keys A1->I9.

        Args:
            currentKey (str): A square tile ID

        Returns:
            str: The key of the next tile in order A1->I9. For example, nextSquare('A2') returns A3. nextSquare('I9') returns A1
        """
        return self.squares[((self.squares.index(currentKey) + 1) % len(self.squares))]

    @cached_property
    def lastSquare(self, currentKey):
        """
        Returns previous square in list of square keys A1->I9.

        Args:
            currentKey (str): A square tile ID A1->I9

        Returns:
            str: The key of the previous tile in order A1->I9. For example, nextSquare('A2') returns A1. nextSquare('A1') returns I9
        """
        return self.squares[((self.squares.index(currentKey) + -1) % len(self.squares))]

    @cached_property
    def neighbors(self, squareID):
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

puzzle = SudokuPuzzle()