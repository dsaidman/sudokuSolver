from string import ascii_uppercase, digits
from functools import cached_property, lru_cache
import os, sys
import lupa
from lupa import LuaRuntime
from pathlib import Path


class SudokuParams:
    
    @property
    def luaSourcePath(self):
        return str(self._luaSourceDir.relative_to(Path('.').resolve()))
    
    @property
    def luaImportPath(self):
        return self.relPath2ImportPath(self.luaSourcePath)
    
    @cached_property
    def luaSourceDir(self):
        return str(self._luaSourceDir)
    
    @cached_property
    def rows(self):
        #return list(ascii_uppercase[0:9])
        return list(self._defsModule.rowNames.values())


    @cached_property
    def columns(self):
        #return list(digits[1:10])
        return list(self._defsModule.colNames.values())

    @cached_property
    def squares(self): 
        # return [row+col for row in self.rows for col in self.columns]
        return list(self._defsModule.allKeys.values())


    @lru_cache
    def nextSquare(self, currentKey):
        return self.squares[((self.squares.index(currentKey) + 1) % len(self.squares))]
    
    @lru_cache
    def lastSquare(self, currentKey):
        return self.squares[((self.squares.index(currentKey) + -1) % len(self.squares))]
    
    @lru_cache(maxsize=82, typed=False)
    def neighbors(self, squareID):
        
        return list(self._defsModule['getNeighbors'](squareID))

    def __init__(self):
        
        self._luaSourceDir = Path(os.path.abspath( os.path.join(os.path.dirname(sys.argv[0]),'..','solver'))).resolve()

        luaImportPath = self.luaImportPath

        currentDir = str(Path('.').resolve())
        os.chdir(self._luaSourceDir)
        lua = lupa.LuaRuntime()
        self._lua = lua
        self._defsModule = lua.require('definitions')[0]
        self._solverModule = lua.require('solver')[0]
        os.chdir(currentDir)
    
    @staticmethod
    def relPath2ImportPath(relPath):
        
        importPath = relPath.replace(os.sep, '.')
        return importPath[1:] if importPath[0] == '.' else importPath
        