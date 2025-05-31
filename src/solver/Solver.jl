
module JDefinitions

export rowNames, columnNames, squares, neighbors, cellRows, cellColumns, puzzle0, families, VectorStringT, SquareT, FamiliesT, NeighborsT, SudokuPuzzleT

# Declare some types aliases for convenience
VectorStringT = Vector{String}
SquareT       = String
FamiliesT     = Dict{Int,VectorStringT}
NeighborsT    = Dict{String,VectorStringT}
SudokuPuzzleT = Dict{String,String}

const rowNames::String          = "ABCDEFGHI"
const columnNames::String       = "123456789"
const squares::VectorStringT     = unique([string(row, col) for row in rowNames for col in columnNames])
const cellRows::VectorStringT    = ["ABC", "DEF", "GHI"]
const cellColumns::VectorStringT = ["123", "456", "789"]

_getRowNeighbors(sq)::VectorStringT    = sq[1] .* collect(columnNames)
_getColumnNeighbors(sq)::VectorStringT = collect(rowNames) .* sq[2]

function _getCellNeighbors(sq::SquareT)::VectorStringT
    _rows::String = cellRows[findfirst(x -> occursin(sq[1], x), cellRows)]
    _cols::String = cellColumns[findfirst(x -> occursin(sq[2], x), cellColumns)]
    return [r * c for r in _rows for c in _cols]
end

# All neigbhors of a
function _neighborsOf(sq::SquareT)::VectorStringT
    return filter!(!=(sq), sort(unique(vcat(_getRowNeighbors(sq),
        _getColumnNeighbors(sq),
        _getCellNeighbors(sq)))))
end

# Get the neighbors of each square
const neighbors::NeighborsT = Dict(sq => _neighborsOf(sq) for sq::SquareT in squares)

# All families
function _getFamilies()::FamiliesT
	# Create a dictionary of families, where the key is the family number

    tmp::FamiliesT = FamiliesT()
    for rowName in rowNames
        tmp[length(tmp)+1] = _getRowNeighbors(string(rowName, columnNames[1]))
    end
    for colName in columnNames
        tmp[length(tmp)+1] = _getColumnNeighbors(string(rowNames[1], colName))
    end
    for cellRow in cellRows
        for cellCol in cellColumns
            tmp[length(tmp)+1] = _getCellNeighbors(string(cellRow[1], cellCol[1]))
        end
    end
    return tmp
end

const families::FamiliesT = _getFamilies()
puzzle0::SudokuPuzzleT = Dict(sq => "123456789" for sq::SquareT in squares)

end

module JSolver

export solve, importPuzzle

using ..JDefinitions
	
isPuzzleComplete(pzl::SudokuPuzzleT)::Bool = all([length(v) == 1 for v in values(pzl)])

isFamilyCorrect(puzzle::SudokuPuzzleT,familySquares::VectorStringT)::Bool = join(sort(collect(join([puzzle[familySq] for familySq in familySquares],"")))) == "123456789"

isPuzzleSolved(pzl::SudokuPuzzleT)::Bool = isPuzzleComplete(pzl) && all(map(fam -> isFamilyCorrect(pzl, fam), values(families)))

# Is there a way to make this more julia-like? Probably
function eliminationPass(puzzle::SudokuPuzzleT)::SudokuPuzzleT
	didChange::Bool = true
	while didChange == true && ~isPuzzleComplete(puzzle)
		solvedSquares::VectorStringT = [k for (k::String,v::String) in puzzle if length(v)==1]
		didChange = false
		for solvedSquare::String in solvedSquares
			solvedValue::String = puzzle[solvedSquare]
			solvedNeighbors::VectorStringT = filter(!=(solvedSquare), neighbors[solvedSquare])
			for nsq in solvedNeighbors
				if length(puzzle[nsq])>1 && occursin(solvedValue,puzzle[nsq])
					didChange = true
					puzzle[nsq] = replace(puzzle[nsq], solvedValue=>"")
				end
			end
		end
	end
	# Dont return a copy in this case, change in place
	return puzzle
end

# Could use StatsBase, kinda like histcounts to get how often each value appears
function countOccurances(puzzle::SudokuPuzzleT)::Dict{Char,Int}
	# Collect all values in the puzzle together
	allPuzzleVals::String = join(values(puzzle),"")
	occurances = Dict{Char,Int}()
	for val::Char in "123456789"
		occurances[val] = count(==(val), allPuzzleVals)
	end
	return occurances
end

findFirstDictKey(inDict::Dict, matchedValue::Int) = first([k for (k,v) in inDict if v==matchedValue])

function getNextEntryPoint(puzzle::SudokuPuzzleT)::Union{String,Bool}

	# Of all unknowns, find the unknown value that occurs most often
	unsolvedCount::Dict{Char,Int}   = countOccurances(puzzle)
    mostFrequentUnsolved::Char      = findFirstDictKey(unsolvedCount, maximum(values(unsolvedCount)))

	# With the value that occurs most often (mostFrequentUnsolved), find the square 
	# with mostFrequentUnsolved with fewest remaining possible values. 
	# The selection will eliminate the most possible paths
    nextSquareChoices::Dict{String,Int} = Dict{String,Int}(k => length(v) for (k, v) in puzzle if (occursin(mostFrequentUnsolved, v) && length(v)>1))
	if isempty(nextSquareChoices)
		return false
	end
	nextSquareChoiceKey = findFirstDictKey(nextSquareChoices, minimum(values(nextSquareChoices)))
	return nextSquareChoiceKey

end

function solveTheThing(puzzle::SudokuPuzzleT)::Union{SudokuPuzzleT,Bool}

	if ~isPuzzleSolved(puzzle)
		# Make a guess
		puzzle    = eliminationPass(puzzle)
		if isPuzzleSolved(puzzle)
			return puzzle
		elseif isPuzzleComplete(puzzle) && ~isPuzzleSolved(puzzle)
			return false
		else
			nextEntry::Union{String,Bool} = getNextEntryPoint(puzzle)
			if nextEntry == false
				return false
			end
			allPuzzleVals = join(values(puzzle))
			
			nextValues::String = join(sort(collect(puzzle[nextEntry]), by = x->count(==(x), allPuzzleVals ), rev = true))
			# Sort the next values by how often they occur in the puzzle, most frequent first
			# This way we try the most frequent values first, which should lead to fewer branches
			# and hopefully a faster solution
			for nextValue::Char in nextValues
				nextPuzzleGuess::Union{SudokuPuzzleT,Bool} = copy(puzzle)
				nextPuzzleGuess[nextEntry] = string(nextValue)
				nextPuzzleGuess = solveTheThing(nextPuzzleGuess)
				
				if typeof(nextPuzzleGuess) == Bool && !nextPuzzleGuess 
					continue
				elseif isPuzzleSolved(nextPuzzleGuess)
					return nextPuzzleGuess
				end
			end
			return false
		end
	
	else
		return puzzle
	end
end

function solve(puzzle::SudokuPuzzleT)::Union{SudokuPuzzleT,Bool}
	# Make sure the puzzle is valid
	if !isPuzzleComplete(puzzle) && !isPuzzleSolved(puzzle)
		return solveTheThing(puzzle)
	elseif isPuzzleSolved(puzzle)
		return puzzle
	else
		return false
	end
end

end

function importPuzzle(filePath::String)::SudokuPuzzleT
    puzzle = copy(Solver.Definitions.puzzle0)
    open(filePath, "r") do file
        for line in eachline(file)
            line = filter(x -> !isspace(x), line)
            puzzle[line[1:2]] = string(last(line))
        end
    end
    return puzzle
end
