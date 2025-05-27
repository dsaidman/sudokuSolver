
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
    return sorted(list((set(_getRowNeighbors(sq)) | set(_getColumnNeighbors(sq)) | set(_getCellNeighbors(sq))) -set(sq)))

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


def isPuzzleComplete(pzl):
    return all([len(v) == 1 for v in pzl.values()])

def isFamilyCorrect(pzl,familySquares):
    return sorted( "".join([pzl[familySq] for familySq in familySquares])) == "123456789"

def isPuzzleSolved(pzl):
    return isPuzzleComplete(pzl) and all(map(lambda fam: isFamilyCorrect(pzl, fam), families))


def _getNextEntryPoint(pzl):

	# Of all unknowns, find the unknown value that occurs most often
    pzlStr               = pzl.values()
    unsolvedCount        = [pzlStr.count(val) for val in "123456789"]
    mostFrequentUnsolved = unsolvedCount.index( max(unsolvedCount) ) [0]

	# With the value that occurs most often (mostFrequentUnsolved), find the square 
	# with mostFrequentUnsolved with fewest remaining possible values. 
	# The selection will eliminate the most possible paths
    nextSquareChoices   = { k : len(v) for k, v in pzl.items() if mostFrequentUnsolved in v and len(v)>1}
    nextSquareChoiceKey = nextSquareChoices.index( min(nextSquareChoices) )[0]
    return nextSquareChoiceKey

def _eliminationPass(pzl):
    
    
	didChange = True
	while didChange and not isPuzzleComplete(pzl):
		solvedSquares = [k for k,v in pzl.items() if len(v)==1]
		didChange = False
		for solvedSquare in solvedSquares:
			solvedValue     = pzl[solvedSquare]
			solvedNeighbors = [nsq for nsq in neighbors[solvedSquare] if nsq is not solvedSquare]
            # Remove solvedValue from all neighbors 
			for nsq in solvedNeighbors:
				if len(pzl[nsq])>1 and solvedValue in pzl[nsq]:
					didChange = True
					pzl[nsq] = pzl[nsq].replace(solvedValue,"")
	# Dont return a copy in this case, change in place
	return pzl

def _solveTheThing(puzzle):

	if not isPuzzleSolved(puzzle):
		# Make a guess
		puzzle    = _eliminationPass(puzzle)
		if isPuzzleSolved(puzzle):
			return puzzle
		elif isPuzzleComplete(puzzle) and  not isPuzzleSolved(puzzle):
			return False
		else:
			nextEntry = _getNextEntryPoint(puzzle)
			nextValues= puzzle[nextEntry]
			for nextValue in nextValues:
				nextPuzzleGuess = puzzle.copy()
				nextPuzzleGuess[nextEntry] = nextValue
				nextPuzzleGuess = _solveTheThing(nextPuzzleGuess)
				
				if nextPuzzleGuess is False:
					continue
				elif isPuzzleSolved(nextPuzzleGuess):
					return nextPuzzleGuess
			return False
	else:
		return puzzle

def solve(puzzle):
    """
    Solve the given sudoku puzzle using a backtracking algorithm.
    
    Args:
        puzzle (dict): A dictionary representing the sudoku puzzle, where keys are square IDs and values are possible values.
    
    Returns:
        dict: The solved puzzle or False if no solution exists.
    """
    return _solveTheThing(puzzle)
