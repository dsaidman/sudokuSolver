
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

# Could use StatsBase, kinda like histcounts to get how often each value appears
function countOccurances(puzzle::Dict{String,String})::Dict{Char,Int}
	# Collect all values in the puzzle together
	allPuzzleVals::String = join(values(puzzle),"")
	occurances = Dict{Char,Int}()
	for val::Char in "123456789"
		occurances[val] = count(==(val), allPuzzleVals)
	end
	return occurances
end

findFirstDictKey(inDict::Dict, matchedValue::Int) = first([k for (k,v) in inDict if v==matchedValue])

function getNextEntryPoint(puzzle::Dict{String,String})::String

	# Of all unknowns, find the unknown value that occurs most often
	unsolvedCount::Dict{Char,Int}   = countOccurances(puzzle)
    mostFrequentUnsolved::Char      = findFirstDictKey(unsolvedCount, maximum(values(unsolvedCount)))

	# With the value that occurs most often (mostFrequentUnsolved), find the square 
	# with mostFrequentUnsolved with fewest remaining possible values. 
	# The selection will eliminate the most possible paths
    nextSquareChoices::Dict{String,Int} = Dict{String,Int}(k => length(v) for (k, v) in puzzle if (occursin(mostFrequentUnsolved, v) && length(v)>1))
	nextSquareChoiceKey = findFirstDictKey(nextSquareChoices, minimum(values(nextSquareChoices)))
	return nextSquareChoiceKey

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
