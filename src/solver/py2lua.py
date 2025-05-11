
"""
Module of helper objects that define rules of sudoku puzzles.

Contains two helper class and preinitialized instances of those classes that can be imported
as a single instance across multiple other modules. The module contains:
    1 - Py2Lua -> class to seamlessly interface the app api with functions and variables defined in lua files
    2 - SudokuParams-> class leveraging Py2Lua to define the rules of sudoku used in the app

Returns:
    None: no return values
"""

import os
from functools import cached_property
import lupa.luajit21 as lupa
from lupa import LuaRuntime


class Py2Lua:
    """
    Create lua runtime instance with lua modules that evaluate sudoku rules and sudoku solving processes.

    Py2Lua creates a lua runtime in lupa. The lua runtime calls 'require' on the definitions.lua file
    and solver.lua to import their functions and values into python as tables. The module tables are
    initialized on formation and cached in order to prevent formation of redundant lua runtimes or
    imported modules.

    Returns:
        obj : Py2Lua object
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
    def solver(self):
        """
        Returns ./solver.lua as a lupa table.

        Uses lupa 'require' on solver.lua to import the lua file as module that can executed in python.
        The property is cached to keep multiple modules from becoming initialized.
        The table only contains a single function called solve(), which accepts a sudoku puzzle represented
        as a lua table.

        Returns:
            table : lua table object containing functions and variables that define sudoku puzzles
        """
        return self._luaSolverModule[0]

    def __init__(self):
        """Constructor method initializes lua runtime and modules."""
        print(
            f"Using {
                LuaRuntime().lua_implementation} (compiled with {
                lupa.LUA_VERSION})")
        self._version = lupa.LUA_VERSION

        # Get the lua runtime from lupa. Try to use luajit if possible
        lua = LuaRuntime()
        lua.execute("package.path = '../solver/?.lua;' .. package.path")
        lua.execute("package.cpath = '../solver/?.lua;' .. package.cpath")

        print('Initializing lua runtime...')
        self._lua = lua

        print('\tImporting defintions.lua as table object...')
        self._luaDefinitionsModule = lua.require('src.solver.definitions')

        print('\tImporting solver.lua as table object...')
        self._luaSolverModule = lua.require('src.solver.solver')

        print('\tPy2Lua initialized')

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
        # tableFun = lua.eval(
        #    'function(d) ' \
        #    'local t = {}'
        #    'for key, value in python.iterex(d.items()) ' \
        #    'do t[key] = value ' \
        #    'end ' \
        #    'return t ' \
        #    'end')
        # return tableFun(lupa.as_attrgetter(d))
        return lua.table_from(d)


# Evaluate the Py2Lua object inside the module so it can be imported
# directly without making new class instances
luaPy = Py2Lua()
