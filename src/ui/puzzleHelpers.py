# from string import ascii_uppercase, digits
import os
import sys
from functools import cached_property, lru_cache
from pathlib import Path

try:
    import lupa.luajit20 as lupa
except ImportError:
    try:
        import lupa.lua54 as lupa
    except ImportError:
        try:
            import lupa.lua53 as lupa
        except ImportError:
            import lupa

from lupa import LuaRuntime


class LuaPy(object):

    @property
    def lua(self):
        return self._lua

    @cached_property
    def defintions(self):
        return self._luaDefinitionsModule
    
    @cached_property
    def sovler(self):
        return self._luaSolverModule

    @property
    def luaSourcePath(self):
        return str(self._luaSourceDir.relative_to(Path('.').resolve()))

    @property
    def luaImportPath(self):
        return self.relPath2ImportPath(self.luaSourcePath)

    @cached_property
    def luaSourceDir(self):
        return str(self._luaSourceDir)

    def __init__(self):

        print(
            f"Using {lupa.LuaRuntime().lua_implementation} (compiled with {lupa.LUA_VERSION})")
        self._version = lupa.LUA_VERSION
        self._luaSourceDir = Path(os.path.abspath(os.path.join(
            os.path.dirname(sys.argv[0]), '..', 'solver'))).resolve()

        # luaImportPath = self.luaImportPath

        currentDir = str(Path('.').resolve())

        os.chdir(self._luaSourceDir)

        lua = lupa.LuaRuntime()
        
        lua.execute(
            "package.path = package.path .. ';{relpath}/?.lua;{relpath}/?/init.lua'".format(relpath=self.luaSourcePath))
        self._lua = lua
        self._luaDefinitionsModule = lua.require('definitions')[0]
        self._luaSolverModule = lua.require('solver')[0]
        
        os.chdir(currentDir)

    @staticmethod
    def relPath2ImportPath(relPath):

        importPath = relPath.replace(os.sep, '.')
        return importPath[1:] if importPath[0] == '.' else importPath

    def dict2Table(self, d):
        lua = self._lua
        
        tableFun = lua.eval(
            'function(d) local t = {} for key, value in python.iterex(d.items()) do t[key] = value end return t end')
        return tableFun(lupa.as_attrgetter(d))


luaPy = LuaPy()

class SudokuParams:

    @cached_property
    def rows(self):
        # return list(ascii_uppercase[0:9])
        return list(luaPy.defintions.rowNames.values())

    @cached_property
    def columns(self):
        # return list(digits[1:10])
        return list(luaPy.defintions.colNames.values())

    @cached_property
    def squares(self):
        # return [row+col for row in self.rows for col in self.columns]
        return list(luaPy.defintions.allKeys.values())

    @lru_cache(maxsize=82, typed=False)
    def nextSquare(self, currentKey):
        return self.squares[((self.squares.index(currentKey) + 1) % len(self.squares))]

    @lru_cache(maxsize = 82, typed = False)
    def lastSquare(self, currentKey):
        return self.squares[((self.squares.index(currentKey) + -1) % len(self.squares))]

    @lru_cache(maxsize=82, typed=False)
    def neighbors(self, squareID):

        return list(luaPy.defintions['getNeighbors'](squareID))

sudokuParams = SudokuParams()

