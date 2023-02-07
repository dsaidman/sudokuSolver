
"""
Module of helper objects that define rules of sudoku puzzles.

Contains two helper class and preinitialized instances of those classes that can be imported
as a single instance across multiple other modules. The module contains:
    1 - LuaPy -> class to seamlessly interface the app api with functions and variables defined in lua files
    2 - SudokuParams-> class leveraging LuaPy to define the rules of sudoku used in the app

Returns:
    None: no return values
"""

import os
import sys
from functools import cached_property, lru_cache
from pathlib import Path, PurePath
import lupa
from lupa import LuaRuntime


class LuaPy:
    """
    Create lua runtime instance with lua modules that evaluate sudoku rules and sudoku solving processes.
    
    LuaPy creates a lua runtime in lupa. The lua runtime calls 'require' on the definitions.lua file
    and solver.lua to import their functions and values into python as tables. The module tables are
    initialized on formation and cached in order to prevent formation of redundant lua runtimes or
    imported modules.
    
    Returns:
        obj : LuaPy object
    """
    
    @property
    def lua(self):
        """
        Returns base lua runtime to be executed in the app.

        Returns:
            lupa.luaRuntime : lua runtime object
        """
        return self._lua

    @cached_property
    def defintions(self):
        """
        Returns ./definitions.lua as a lupa table.
        
        Uses lupa 'require' on definitions.lua to import the lua file as module that can executed in python.
        The property is cached to keep multiple modules from becoming initialized.
        The module contains functions that defines the squares of the puzzles, has cached functions that determine
        the neighbors of a square, as well as other lightweight and cached methods

        Returns:
            table : lua table object containing functions and variables that define sudoku puzzles
        """        
        return self._luaDefinitionsModule

    @cached_property
    def sovler(self):
        """
        Returns ./solver.lua as a lupa table.

        Uses lupa 'require' on solver.lua to import the lua file as module that can executed in python.
        The property is cached to keep multiple modules from becoming initialized.
        The table only contains a single function called solve(), which accepts a sudoku puzzle represented
        as a lua table.

        Returns:
            table : lua table object containing functions and variables that define sudoku puzzles
        """
        return self._luaSolverModule

    def __init__(self):
        """Constructor method initializes lua runtime and modules."""
        print(
            f"Using {lupa.LuaRuntime().lua_implementation} (compiled with {lupa.LUA_VERSION})")
        self._version = lupa.LUA_VERSION

        # Get the lua runtime from lupa. Try to use luajit if possible
        lua = lupa.LuaRuntime()

        print('Initializing lua runtime...')
        self._lua = lua
        
        print('\tImporting defintions.lua as table object...')
        self._luaDefinitionsModule = lua.require('definitions')[0]
        
        print('\tImporting solver.lua as table object...')
        self._luaSolverModule = lua.require('solver')[0]
        
        print('\tLuaPy initialized')

    @staticmethod
    def relPath2ImportPath(relPath):

        importPath = relPath.replace(os.sep, '.')
        return importPath[1:] if importPath[0] == '.' else importPath

    def dict2Table(self, d):
        """
        Convert a python dictionary into a lua table.
        
        Class function (method?) that converts a python dict object into lua table object.
        The table object can be passed into the lua runtime as an input.

        Args:
            d (dict): python dictionary

        Returns:
            table: a lua table that can be used as an input to lua module functions
        """        
        # Get the lua runtime
        lua = self._lua

        # Evaluate a function that can iterate over a python key so it can be put into a table
        tableFun = lua.eval(
            'function(d) local t = {} for key, value in python.iterex(d.items()) do t[key] = value end return t end')
        return tableFun(lupa.as_attrgetter(d))

# Evaluate the luaPy object inside the module so it can be imported directly without making new class instances
luaPy = LuaPy()


class SudokuParams:
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
            list: capital letters A to I 
        """        
        return sorted(list(luaPy.defintions.rowNames.values()))

    @cached_property
    def columns(self):
        """
        Returns the column numbers of the puzzle as a list of strings.

        Returns:
            list: capital letters A to I 
        """
        # return list(digits[1:10])
        return sorted(list(luaPy.defintions.colNames.values()))

    @cached_property
    def squares(self):
        """
        Returns list of all square tile keys A1-I9 - 81 total.

        Returns:
            list: cached list of keys
        """        
        return sorted(list(luaPy.defintions.allKeys.values()), reverse=False)

    def nextSquare(self, currentKey):
        """
        Returns next square in list of square keys A1->I9.

        Args:
            currentKey (str): A square tile ID

        Returns:
            str: The key of the next tile in order A1->I9. For example, nextSquare('A2') returns A3. nextSquare('I9') returns A1
        """        
        return self.squares[((self.squares.index(currentKey) + 1) % len(self.squares))]

    def lastSquare(self, currentKey):
        """
        Returns previous square in list of square keys A1->I9.

        Args:
            currentKey (str): A square tile ID A1->I9

        Returns:
            str: The key of the previous tile in order A1->I9. For example, nextSquare('A2') returns A1. nextSquare('A1') returns I9
        """
        return self.squares[((self.squares.index(currentKey) + -1) % len(self.squares))]

    @lru_cache(maxsize=82, typed=False)
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
        return list(luaPy.defintions['getNeighbors'](squareID))

# Return the pre-cached SudokuParams instance to be shared across modules
sudokuParams = SudokuParams()
