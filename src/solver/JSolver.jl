
module JDefinitions
export rowNames, columnNames, squares, neighbors, cellRows, cellColumns, puzzle0, families, VectorStringT, SquareT, FamiliesT, NeighborsT, SudokuPuzzleT, squareValue0, SquareValueT

# Declare some types aliases for convenience
VectorStringT = Vector{String}
FamiliesT     = Dict{Int,VectorStringT}
NeighborsT    = Dict{String,VectorStringT}
SquareValueT  = Set{Int}
SquareT       = String
SudokuPuzzleT = Dict{SquareT,SquareValueT}


const rowNames::String          = "ABCDEFGHI"
const columnNames::String       = "123456789"
const squares::VectorStringT     = unique([string(row, col) for row in rowNames for col in columnNames])
const cellRows::VectorStringT    = ["ABC", "DEF", "GHI"]
const cellColumns::VectorStringT = ["123", "456", "789"]
squareValue0::SquareValueT = Set([1, 2, 3, 4, 5, 6, 7, 8, 9])

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
puzzle0::SudokuPuzzleT = Dict(sq => squareValue0 for sq in squares)

end

module JSolver
export solve

using ..JDefinitions



@inline function isPuzzleComplete(pzl::SudokuPuzzleT)::Bool
    all(length.(values(pzl)) .== 1)
end

@inline function isFamilyCorrect(puzzle::SudokuPuzzleT,familySquares::VectorStringT)::Bool
    reduce(union,puzzle[familySq] for familySq in familySquares) == squareValue0
end

@inline function allFamiliesValid(pzl::SudokuPuzzleT)::Bool
    all(fam -> isFamilyCorrect(pzl, fam), values(families))
end

@inline function isPuzzleSolved(pzl::SudokuPuzzleT)::Bool
    isPuzzleComplete(pzl) && allFamiliesValid(pzl)
end


# Could use StatsBase, kinda like histcounts to get how often each value appears
@inline function countAllSquareOccurances(puzzle::SudokuPuzzleT)::Dict{Int,Int}
	# Collect all values in the puzzle together
    allPuzzleValues = reduce(vcat,collect.(values(puzzle)))
    return Dict(val => count(==(val), allPuzzleValues) for val in collect(squareValue0))
    
end

function getNextEntryPoint(puzzle::SudokuPuzzleT)

	# Of all unknowns, find the unknown value that occurs most often
    unsolvedCount = countAllSquareOccurances(puzzle)

    # find most frequently unsolved number (occurs most in incomplete squares)
    mostFrequentUnsolved = findfirst(v -> v == maximum(values(unsolvedCount)), unsolvedCount)

	# get the square with fewest possiblities that contains mostFrequentlyUnresolved
	smallestMostFrequent  = [length(v) for (k,v) in puzzle if length(v) > 1 && mostFrequentUnsolved in v]
    smallestMostFrequent  = length(smallestMostFrequent) > 0 ? minimum(smallestMostFrequent) : return false
    
	# With the value that occurs most often (mostFrequentUnsolved), find the square 
	# with mostFrequentUnsolved with fewest remaining possible values (smallestMostFrequent). 
	# The selection will eliminate the most possible paths
    nextSquareChoice = squares[
        findfirst(k -> length(puzzle[k]) == smallestMostFrequent && mostFrequentUnsolved in puzzle[k], squares)
    ]
	return length(puzzle[nextSquareChoice]) <= 1 ? false : nextSquareChoice

end


function solve(puzzle::SudokuPuzzleT)
    # Make sure the puzzle is valid
    function solveTheThing(puzzle::SudokuPuzzleT)

        isPuzzleSolved(puzzle) && return puzzle

        # Make a guess
        puzzle = eliminationPass(puzzle)

        isPuzzleSolved(puzzle) && return puzzle
        !allFamiliesValid(puzzle) && return false
        isPuzzleComplete(puzzle) && return false
        nextEntry = getNextEntryPoint(puzzle)
        nextEntry == false && return false
        nextValues = sort(
            collect(puzzle[nextEntry]), 
            by=x -> count(==(x), reduce(vcat,collect.(values(puzzle)))), 
            rev=true)
        # Sort the next values by how often they occur in the puzzle, most frequent first
        # This way we try the most frequent values first, which should lead to fewer branches
        # and hopefully a faster solution
        for nextValue in nextValues
            
            nextPuzzleGuess = deepcopy(puzzle)
            !allFamiliesValid(nextPuzzleGuess) && continue
            numRecursions += 1
            nextPuzzleGuess[nextEntry] = Set(nextValue)
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
            didChange = false
            for solvedSquare in [k for (k, v) in puzzle if length(v) == 1]
                solvedValue = first(puzzle[solvedSquare])

                for nsq in neighbors[solvedSquare]
                    if solvedValue in puzzle[nsq] && length(puzzle[nsq]) > 1
                        numEliminated+=1
                        numOperations+=1
                        didChange = true
                        puzzle[nsq] = delete!(puzzle[nsq], solvedValue)
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

    soln = Dict{String,String}(k => string(first(soln[k])) for k in keys(soln))
	return Dict(
        "solution" => soln,
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
    #puzzleStr = ".15.7....4..8..75...8..9.169641.7.3..8239.5..5....4.9..2.41.8....17.39.4...92..65"

    puzzleStr = "..5...7....38.1..5..2.6..399...8...7.....5....7.2..14...........8613............3"
    puzzle = Dict( 
        squares[ix] => v == '.' ? Set([1,2,3,4,5,6,7,8,9]) :  Set(Int(v)-Int('0')) for (ix, v) in enumerate(puzzleStr)
        )
    soln = JSolver.solve(puzzle)

	print(soln["solution"])
	
end

testIt()
=#
