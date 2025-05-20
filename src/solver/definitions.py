from functools import cached_property, lru_cache
import logging
from solver.py2runtime import _lang
if _lang == "python":
    from string import ascii_uppercase 
    from string import digits
else:
    from solver.py2runtime import RuntimePy as rt
uiLogger = logging.getLogger('uiLogger')

class definitions:
    """
    A class with properties and methods that collectively define the rules of a lua puzzle.

    SudokuParams behaves as in interface the definitions.lua lua module imported in
    LuaPy to utilize the lightweight and very fast cached variables and methods in
    a familiar python container

    Returns:
        object: SudokuParams object with cached methods and properties that define the rules of sudoku
    """

    @cached_property
    def rows(self):
        """
        Returns the rows letters of the puzzle as a list of strings.

        Returns:
            list: capital let`ters A to I
        """
        if self.lang == "lua":
            return sorted(list(rt.defintions.rowNames.values()))
        elif self.lang == "julia":
            return sorted(list(rt.defintions.rowNames)) 
        elif self.lang == "python":
            return sorted(list(ascii_uppercase[0:9]))

    @cached_property
    def columns(self):
        """
        Returns the column numbers of the puzzle as a list of strings.

        Returns:
            list: capital letters A to I
        """
        # return list(digits[1:10])
        if self.lang == "lua":
            return sorted(list(rt.defintions.colNames.values()))
        elif self.lang == "julia":
            return sorted(list(rt.defintions.columnNames)) 
        elif self.lang == "python":
            return list(digits[1:])


    @cached_property
    def squares(self):
        """
        Returns list of all square tile keys A1-I9 - 81 total.

        Returns:
            list: cached list of keys
        """
        if self.lang == "lua":
            return sorted(
                list(
                    rt.defintions.allKeys.values()),
                    reverse=False)
        elif self.lang == "julia":
            return sorted(
                list(
                    rt.defintions.squares),
                    reverse=False)
        elif self.lang == "python":
            return sorted(list([row+col for row in self.rows for col in self.columns]))

    def nextSquare(self, currentKey):
        """
        Returns next square in list of square keys A1->I9.

        Args:
            currentKey (str): A square tile ID

        Returns:
            str: The key of the next tile in order A1->I9. For example, nextSquare('A2') returns A3. nextSquare('I9') returns A1
        """
        return self.squares[(
            (self.squares.index(currentKey) + 1) % len(self.squares))]

    def lastSquare(self, currentKey):
        """
        Returns previous square in list of square keys A1->I9.

        Args:
            currentKey (str): A square tile ID A1->I9

        Returns:
            str: The key of the previous tile in order A1->I9. For example, nextSquare('A2') returns A1. nextSquare('A1') returns I9
        """
        return self.squares[(
            (self.squares.index(currentKey) + -1) % len(self.squares))]

    @lru_cache(maxsize=82)
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
        if self.lang == "lua":
            return list(rt.defintions['getNeighbors'](squareID))
        elif self.lang == "julia":
            return list(rt.defintions.neighbors[squareID])
        elif self.lang == "python":
            print("not yet implimented")
            return
            
    
    def __init__(self,lang=_lang):
        self.lang = lang
        uiLogger.info("Using %s runtime", self.lang)
        


# Return the pre-cached SudokuParams instance to be shared across modules
sudokuDefs = definitions(_lang)
