module Definitions
	
export rowNames, columnNames, squares, neighbors, cellRows, cellColumns, puzzle0, families

const rowNames::String = "ABCDEFGHI"
const columnNames::String = "123456789"
const squares::Vector{String} = unique([string(row, col) for row in rowNames for col in columnNames])
const cellRows::Vector{String} = ["ABC", "DEF", "GHI"]
const cellColumns::Vector{String} = ["123", "456", "789"]

_getRowNeighbors(sq)::Vector{String}    = sq[1] .* collect(columnNames)
_getColumnNeighbors(sq)::Vector{String} = collect(rowNames) .* sq[2]

function _getCellNeighbors(sq::String)::Vector{String}
	_rows = cellRows[findfirst(x -> occursin(sq[1], x), cellRows)]
	_cols = cellColumns[findfirst(x -> occursin(sq[2], x), cellColumns)]
	return [r*c for r in _rows for c in _cols]
end

# All neigbhors of a
function _neighborsOf(sq::String)::Vector{String}
    return filter!(!=(sq), sort(unique(vcat(_getRowNeighbors(sq) ,
									 _getColumnNeighbors(sq) ,
									 _getCellNeighbors(sq) ))))
end

# Get the neighbors of each square
const neighbors::Dict{String,Vector{String}} = Dict(sq => _neighborsOf(sq) for sq in squares)
	
# All families
begin
	tmp = Dict{Int,Vector{String}}()
	for rowName in rowNames
		tmp[length(tmp)+1] = _getRowNeighbors( string(rowName, columnNames[1] ) )
	end
	for colName in columnNames
		tmp[length(tmp)+1] = _getColumnNeighbors( string(rowNames[1], colName) )
	end
	for cellRow in cellRows
		for cellCol in cellColumns
			tmp[length(tmp)+1] = _getCellNeighbors( string(cellRow[1],cellCol[1]) )
		end
	end
	const families::Dict{Int,Vector{String}} = tmp
	tmp=nothing
end

puzzle0::Dict{String,String} = Dict(sq => "123456789" for sq in squares)

end

function importPuzzle(filePath::String)::Dict{String,String}
	puzzle = copy(Definitions.puzzle0)
	open(filePath, "r") do file
		for line in eachline(file)
			line = filter(x -> !isspace(x), line)
			puzzle[line[1:2]] = string(last(line))
		end
	end
	return puzzle
end

isPuzzleComplete(pzl::Dict{String,String})::Bool = all([length(v) == 1 for v in values(pzl)])

isFamilyCorrect(puzzle::Dict{String,String},familySquares::Vector{String})::Bool = join(sort(collect(join([puzzle[familySq] for familySq in familySquares],"")))) == "123456789"

isPuzzleSolved(pzl::Dict{String,String})::Bool = isPuzzleComplete(pzl) && all(map(fam -> isFamilyCorrect(pzl, fam), values(Definitions.families)))

# Is there a way to make this more julia-like? Probably
function eliminationPass(puzzle::Dict{String,String})::Dict{String,String}
	didChange::Bool = true
	while didChange == true && ~isPuzzleComplete(puzzle)
		solvedSquares::Vector{String} = [k for (k,v) in puzzle if length(v)==1]
		didChange = false
		for solvedSquare in solvedSquares
			solvedValue = puzzle[solvedSquare]
			solvedNeighbors::Vector{String} = filter(!=(solvedSquare), Definitions.neighbors[solvedSquare])
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

function getNextEntryPoint(puzzle::Dict{String,String})::String

	nCounts = map(length,values(puzzle))
	maxKey  = [item.first for item in puzzle if length(item.second)==maximum(nCounts)]
	return maxKey[1]

end

function solveTheThing(puzzle::Dict{String,Vector{String}})

	if ~isPuzzleSolved(puzzle)
		# Make a guess
		puzzle    = eliminationPass(puzzle)
		nextEntry = getNextEntryPoint(puzzle)
		nextValues= puzzle[nextEntry]
		for nextValue in nextValues
			nextValue = nextValues[1]
			nextPuzzleGuess = copy(puzzle)
			nextPuzzleGuess[nextEntry] = string(nextValue)
			nextPuzzleGuess = eliminationPass(nextPuzzleGuess)
		end

	end
end

puzzleFile = "C:\\Users\\david\\Projects\\sudokuSolver\\input\\mediumSample.ini"
puzzle = importPuzzle(puzzleFile)