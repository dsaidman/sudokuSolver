
"""
Module of helper objects that define rules of sudoku puzzles.

Contains two helper class and preinitialized instances of those classes that can be imported
as a single instance across multiple other modules. The module contains:
    1 - Py2Lua -> class to seamlessly interface the app api with functions and variables defined in lua files
    2 - SudokuParams-> class leveraging Py2Lua to define the rules of sudoku used in the app

Returns:
    None: no return values
"""
_lang = "julia"
import os
from functools import cached_property
if _lang == "lua":
    import lupa.luajit21 as lupa
    from lupa import LuaRuntime
elif _lang == "julia":
    from juliacall import Main as jl
import logging
uiLogger = logging.getLogger('uiLogger')

class Py2Runtime:

    @property
    def runtime(self):
        return self._runtime

    @cached_property
    def defintions(self):
        return self._definitionsModule

    @cached_property
    def solver(self):
        return self._solverModule

    def __init__(self, lang=_lang):
        """Constructor method initializes runtime and modules."""
        self.lang = lang
        if lang == "lua":
            
            # Get the lua runtime from lupa. Try to use luajit if possible
            lua = LuaRuntime()
            uiLogger.info(
                f"Using {
                    lua.lua_implementation} (compiled with {
                    lupa.LUA_VERSION})")
            self._version = lupa.LUA_VERSION
            
            lua.execute("package.path = '../solver/?.lua;' .. package.path")
            lua.execute("package.cpath = '../solver/?.lua;' .. package.cpath")

            uiLogger.debug('Initializing lua runtime...')
            self._runtime = lua

            uiLogger.debug('\tImporting defintions.lua as table object...')
            
            self._definitionsModule = lua.require('src.solver.definitions')[0]

            uiLogger.debug('\tImporting solver.lua as table object...')
            self._solverModule = lua.require('src.solver.solver')[0]

            uiLogger.info('\tLua Runtime initialized')
        elif lang == "julia":
            uiLogger.info(f"Using julia {jl.VERSION}")
            self._version = jl.VERSION
            
            uiLogger.debug('Initializing julia runtime...')
            self._runtime = jl
            
            uiLogger.debug('\tImporting defintions.jl...')
            jl.include("solver\\Solver.jl")
            self._definitionsModule = jl.Solver.Definitions
            
            uiLogger.debug('\tImporting defintions.jl...')
            jl.include("solver\\Solver.jl")
            self._solverModule = jl.Solver
            
            uiLogger.info('\tJulia Runtime initialized')


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
        lua = self.runtime
        return lua.table_from(d)


# Evaluate the Py2Lua object inside the module so it can be imported
# directly without making new class instances
RuntimePy = Py2Runtime(_lang)
