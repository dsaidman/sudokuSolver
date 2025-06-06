
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
    _rows = cellRows[findfirst(x -> occursin(sq[1], x), cellRows)]
    _cols = cellColumns[findfirst(x -> occursin(sq[2], x), cellColumns)]
    return [r * c for r in _rows for c in _cols]
end

# All neigbhors of a
function _neighborsOf(sq::SquareT)::VectorStringT
    return filter(!=(sq), sort(unique(vcat(_getRowNeighbors(sq),
        _getColumnNeighbors(sq),
        _getCellNeighbors(sq)))))
end

# Get the neighbors of each square
const neighbors::NeighborsT = Dict(sq => _neighborsOf(sq) for sq in squares)

# All families
function _getFamilies()::FamiliesT
	# Create a dictionary of families, where the key is the family number

    tmp = Dict()
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
puzzle0::SudokuPuzzleT = Dict(sq => "123456789" for sq in squares)

end

module JSolver
export solve

using ..JDefinitions
using ProfileView

	
@inline function isPuzzleComplete(pzl::SudokuPuzzleT)::Bool
    all(v -> length(v) == 1, values(pzl))
end

@inline function isFamilyCorrect(puzzle::SudokuPuzzleT,familySquares::VectorStringT)::Bool
    Set(join([puzzle[familySq] for familySq in familySquares])) == Set("123456789")
end

@inline function isPuzzleSolved(pzl::SudokuPuzzleT)::Bool
    isPuzzleComplete(pzl) && all(fam -> isFamilyCorrect(pzl, fam), values(families))
end



# Could use StatsBase, kinda like histcounts to get how often each value appears
@inline function countOccurances(puzzle::SudokuPuzzleT)::Dict{Char,Int}
	# Collect all values in the puzzle together
        return Dict(val => count(==(val), join(values(puzzle))) for val in "123456789")
end

function getNextEntryPoint(puzzle::SudokuPuzzleT)

	# Of all unknowns, find the unknown value that occurs most often
	unsolvedCount             = countOccurances(puzzle)

    # find most frequently unsolved number (occurs most in incomplete squares)
    mostFrequentUnsolved = findfirst(v -> v == maximum(values(unsolvedCount)), unsolvedCount)

	# get the square with fewest possiblities that contains mostFrequentlyUnresolved
	smallestMostFrequent  = [length(v) for (k,v) in puzzle if length(v) > 1 && occursin(mostFrequentUnsolved, v)]
    if isempty(smallestMostFrequent)
		return false   
	else
        smallestMostFrequent = minimum(smallestMostFrequent) # Return if no choices
	end

	# With the value that occurs most often (mostFrequentUnsolved), find the square 
	# with mostFrequentUnsolved with fewest remaining possible values (smallestMostFrequent). 
	# The selection will eliminate the most possible paths
    nextSquareChoice = squares[
		findfirst(k -> length(puzzle[k]) == smallestMostFrequent && occursin(mostFrequentUnsolved, puzzle[k]), squares)
		]
	return length(puzzle[nextSquareChoice]) <= 1 ? false : nextSquareChoice

end



function solve(puzzle::SudokuPuzzleT)::Dict{String,Any}
    # Make sure the puzzle is valid

    function solveTheThing(puzzle::SudokuPuzzleT)

        isPuzzleSolved(puzzle) && return puzzle

        # Make a guess
        puzzle = eliminationPass(puzzle)

        isPuzzleSolved(puzzle) && return puzzle
        isPuzzleComplete(puzzle) && return false
        nextEntry = getNextEntryPoint(puzzle)
        nextEntry == false && return false
        
        nextValues = join(
                sort!(collect(puzzle[nextEntry]), by=x -> count(==(x), join(values(puzzle))), rev=true)
			)
        # Sort the next values by how often they occur in the puzzle, most frequent first
        # This way we try the most frequent values first, which should lead to fewer branches
        # and hopefully a faster solution
        for nextValue in nextValues
            numRecursions += 1
            nextPuzzleGuess = copy(puzzle)
            nextPuzzleGuess[nextEntry] = string(nextValue)
            nextPuzzleGuess = solveTheThing(nextPuzzleGuess)

            nextPuzzleGuess == false && continue
            isPuzzleSolved(nextPuzzleGuess) && return nextPuzzleGuess
        end
        return false
    end

    # Is there a way to make this more julia-like? Probably
    function eliminationPass(puzzle::SudokuPuzzleT)::SudokuPuzzleT
        numEliminated = 0
        didChange = true
        while didChange == true && ~isPuzzleComplete(puzzle)
            solvedSquares = [k for (k, v) in puzzle if length(v) == 1]
            didChange = false
            for solvedSquare in solvedSquares
                solvedValue = puzzle[solvedSquare]

                for nsq in neighbors[solvedSquare]
                    if length(puzzle[nsq]) > 1 && occursin(solvedValue, puzzle[nsq])
                        numEliminated+=1
                        numOperations+=1
                        didChange = true
                        puzzle[nsq] = replace(puzzle[nsq], solvedValue => "")
                    end
                end
            end
        end
        bestSinglePass = max(bestSinglePass, numEliminated)
        # Dont return a copy in this case, change in place
        return puzzle
    end

    numRecursions::Int  = 0
	numOperations::Int  = 0
    bestSinglePass = 0

	elapsedTime = @elapsed soln = solveTheThing(puzzle)

	return Dict(
		"solution"=>soln,
		"numRecursions"=>numRecursions,
		"numOperations"=>numOperations,
        "bestSinglePass"=>bestSinglePass,
		"duration_ms"=>elapsedTime*1000.0)
end
end

#=
using ..JDefinitions
using ..JSolver
@inline function testIt()
    puzzleStr = ".......7..1.9.4..8..9........5..17....3..96..1...67..9........4.82.46...3...8...."
    puzzle = Dict(squares[ix] => replace(string(v), "." => "123456789") for (ix, v) in enumerate(puzzleStr))
    soln = JSolver.solve(puzzle)
	print("Hello")
	
end

testIt()
=#
