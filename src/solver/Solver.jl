module Solver

include("Definitions.jl")

export isPuzzleComplete, isPuzzleSolved, isFamilyCorrect, solveTheThing

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
	minCounts = minimum(nCounts[nCounts .> 1])
    maxKey = [item.first for item in puzzle if length(item.second) == minCounts]
	return maxKey[1]

end

function solveTheThing(puzzle::Dict{String,String})

	if ~isPuzzleSolved(puzzle)
		# Make a guess
		puzzle    = eliminationPass(puzzle)
		if isPuzzleSolved(puzzle)
			return puzzle
		elseif isPuzzleComplete(puzzle) && ~isPuzzleSolved(puzzle)
			return false
		else
			nextEntry = getNextEntryPoint(puzzle)
			nextValues= puzzle[nextEntry]
			for nextValue in nextValues
				nextPuzzleGuess = copy(puzzle)
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

end


function importPuzzle(filePath::String)::Dict{String,String}
    puzzle = copy(Solver.Definitions.puzzle0)
    open(filePath, "r") do file
        for line in eachline(file)
            line = filter(x -> !isspace(x), line)
            puzzle[line[1:2]] = string(last(line))
        end
    end
    return puzzle
end



puzzleFile = "C:\\Users\\david\\Projects\\sudokuSolver\\input\\hardSample.ini"
puzzle = importPuzzle(puzzleFile)

using Profile
@profile Solver.solveTheThing(copy(puzzle))
Profile.print()

