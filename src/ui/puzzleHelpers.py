from string import ascii_uppercase, digits
from functools import cached_property, lru_cache


class SudokuParams:

    @cached_property
    def rows(self):
        return list(ascii_uppercase[0:9])

    @cached_property
    def columns(self):
        return list(digits[1:10])

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
    
    

#if __name__ == "__main__":
#    return PuzzleDefinition()