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
        return [row+col for row in self.rows for col in self.columns]

    @cached_property
    def rowCells(self): 
        return [ascii_uppercase[idx:(idx+3)] for idx in [0, 3, 6]]
    
    @cached_property
    def columnCells(self):
        return [digits[idx:(idx+3)] for idx in [1, 4, 7]]
    
    @lru_cache
    def nextSquare(self, currentKey):
        return self.squares[((self.squares.index(currentKey) + 1) % len(self.squares))]
    
    @lru_cache
    def lastSquare(self, currentKey):
        return self.squares[((self.squares.index(currentKey) + -1) % len(self.squares))]
    
    @lru_cache(maxsize=82, typed=False)
    def neighbors(self, squareID):
        squareRow = squareID[0]
        squareColumn = squareID[1]
        
        neighborList = []
        
        for row in self.rows:
            neighborList.append(row+squareColumn)
            
        for column in self.columns:
            neighborList.append(squareRow+column)
            
        del row, column
        
        rowCell = list([rowCell for rowCell in self.rowCells if squareRow in rowCell][0])
        columnCell = list([columnCell for columnCell in self.columnCells if squareColumn in columnCell][0])
        
        for row in rowCell:
            for column in columnCell:
                key = row+column
                if key not in neighborList:
                    neighborList.append(row+column)
        neighborList = list(set(neighborList))
        if squareID in neighborList:
            neighborList.remove(squareID)
        return sorted(neighborList)
    
    
    
    def __init__(self):
        
        self._luaSourceDir = Path(os.path.abspath( os.path.join(os.path.dirname(sys.argv[0]),'..','solver'))).resolve()

        luaImportPath = self.luaImportPath
        requirePaths = ['{s1}.{s2}'.format(s1=luaImportPath,s2=module) for module in ['helpers','solver','definitions']]
        
        self._requirePath = {}
        #self._requirePath['helpers'] = self.relPath2ImportPath(requirePaths[0])
        #self._requirePath['solver'] = self.relPath2ImportPath(requirePaths[1])
        self._requirePath['definitions'] = self.relPath2ImportPath(requirePaths[2])
        
        currentDir = str(Path('.').resolve())
        os.chdir(self._luaSourceDir)
        lua = lupa.LuaRuntime()
        _ = lua.require('table')
        self._defsModule = lua.require('definitions')
        self._defsModule = self._defsModule[0]
        self._solverModule = lua.require('solver')[0]
        os.chdir(currentDir)
        self._luaRuntime = lua
    
    @staticmethod
    def relPath2ImportPath(relPath):
        
        importPath = relPath.replace(os.sep, '.')
        return importPath[1:] if importPath[0] == '.' else importPath
        
    
    

if __name__ == "__main__":
    tmp = SudokuParams()
    print(tmp.rows)
    
