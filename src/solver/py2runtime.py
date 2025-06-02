"""
Module of helper objects that define rules of sudoku puzzles.

Contains two helper class and preinitialized instances of those classes that can be imported
as a single instance across multiple other modules. The module contains:
    1 - Py2Lua -> class to seamlessly interface the app api with functions and variables defined in lua files
    2 - SudokuParams-> class leveraging Py2Lua to define the rules of sudoku used in the app

Returns:
    None: no return values
"""

import os, sys
import logging

uiLogger = logging.getLogger("uiLogger")


class Py2Runtime:
    @property
    def runtime(self):
        return self._runtime[self.lang]

    @property
    def defintions(self):
        return self._definitionsModule[self.lang]

    @property
    def solver(self):
        return self._solverModule[self.lang]

    def __init__(self, lang=None):
        """Constructor method initializes runtime and modules."""
        self.lang = lang
        self._runtime = {}
        self._definitionsModule = {}
        self._solverModule = {}
        self._version = {}

    def getLang(self):
        return self.lang

    def setLang(self, lang):
        """
        Set the runtime language.

        Args:
            lang (str): The language to set the runtime to. Can be "lua" or "julia".
        """
        if lang.lower() not in ["luajit", "lua", "julia", "python"]:
            raise ValueError(
                f"Invalid language: {lang}. Must be 'luajit','lua', or 'julia'."
            )
        self.lang = lang.lower()
        uiLogger.info(f"Using {self.lang} runtime")

        if self.lang == "luajit" and self.lang not in self._runtime:
            import lupa.luajit21 as lupa
            from lupa import LuaRuntime

            # Get the lua runtime from lupa. Try to use luajit if possible
            lua = LuaRuntime()
            uiLogger.info(
                f"Using {lua.lua_implementation} (compiled with {lupa.LUA_VERSION})"
            )
            self._version["luajit"] = lupa.LUA_VERSION

            lua.execute("package.path = '../solver/?.lua;' .. package.path")
            lua.execute("package.cpath = '../solver/?.lua;' .. package.cpath")

            uiLogger.debug("Initializing lua runtime...")
            self._runtime["luajit"] = lua

            uiLogger.debug("\tImporting defintions.lua as table object...")

            self._definitionsModule["luajit"] = lua.require("src.solver.definitions")[0]

            uiLogger.debug("\tImporting solver.lua as table object...")
            self._solverModule["luajit"] = lua.require("src.solver.solver")[0]

            uiLogger.info("\tLuaJit Runtime initialized")
        elif self.lang == "lua" and self.lang not in self._runtime:
            import lupa.lua54 as lupa
            from lupa import LuaRuntime

            # Get the lua runtime from lupa. Try to use luajit if possible
            lua = LuaRuntime()
            uiLogger.info(
                f"Using {lua.lua_implementation} (compiled with {lupa.LUA_VERSION})"
            )
            self._version["lua"] = lupa.LUA_VERSION

            lua.execute("package.path = '../solver/?.lua;' .. package.path")
            lua.execute("package.cpath = '../solver/?.lua;' .. package.cpath")

            uiLogger.debug("Initializing lua runtime...")
            self._runtime["lua"] = lua

            uiLogger.debug("\tImporting defintions.lua as table object...")

            self._definitionsModule["lua"] = lua.require("src.solver.definitions")[0]

            uiLogger.debug("\tImporting solver.lua as table object...")
            self._solverModule["lua"] = lua.require("src.solver.solver")[0]

            uiLogger.info("\tLua Runtime initialized")
        elif lang == "julia" and self.lang not in self._runtime:
            from juliacall import Main as jl

            uiLogger.info(f"Using julia {jl.VERSION}")
            self._version["julia"] = jl.VERSION

            uiLogger.debug("Initializing julia runtime...")
            self._runtime["julia"] = jl

            uiLogger.debug("\tImporting defintions.jl...")

            jl.include("src\\solver\\Solver.jl")

            self._definitionsModule["julia"] = jl.JDefinitions

            uiLogger.debug("\tImporting defintions.jl...")
            self._solverModule["julia"] = jl.JSolver

            uiLogger.info("\tJulia Runtime initialized")
        elif lang == "python" and self.lang not in self._runtime:
            import solver.solver as pySolver

            # uiLogger.info(f"Using python {jl.VERSION}")
            self._version["python"] = sys.version

            self._runtime["python"] = []

            self._definitionsModule["python"] = pySolver

            self._solverModule["python"] = pySolver.solve

    @staticmethod
    def relPath2ImportPath(relPath):
        importPath = relPath.replace(os.sep, ".")
        return importPath[1:] if importPath[0] == "." else importPath

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
RuntimePy = Py2Runtime()
