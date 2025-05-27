

rowNames    = "ABCDEFGHI"
columnNames = "123456789"
squares     = [row+col for row in rowNames for col in columnNames]
cellRows    = ["ABC", "DEF", "GHI"]
cellColumns = ["123", "456", "789"]

def _getRowNeighbors(sq):
    return [sq[0] + col for col in columnNames]

def _getColumnNeighbors(sq):
    return [row + sq[1] for row in rowNames]

def _getCellNeighbors(sq):
    _rows = cellRows[  [idx for idx, s in enumerate(cellRows) if sq[0] in s][0] ]
    _cols = cellColumns[  [idx for idx, s in enumerate(cellColumns) if sq[1] in s][0] ]
    return [r + c for r in _rows for c in _cols]


# All neigbhors of a
def _neighborsOf(sq):
    return list((set(_getRowNeighbors(sq)) | set(_getColumnNeighbors(sq)) | set(_getCellNeighbors(sq))) -set(sq)).sort()

neighbors = {sq : _neighborsOf(sq) for sq in squares}


# All families
_families = list()
for rowName in rowNames:
    _families.append( _getRowNeighbors(rowName+columnNames[1])) 

for colName in columnNames:
    _families.append( _getColumnNeighbors(rowNames[1] + colName)) 

for cellRow in cellRows:
    for cellCol in cellColumns:
        _families.append( _getCellNeighbors(cellRow[1]+cellCol[1]))
families = _families.copy()

puzzle0 = {sq : "123456789" for sq in squares}
