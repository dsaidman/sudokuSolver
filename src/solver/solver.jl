### A Pluto.jl notebook ###
# v0.20.8

using Markdown
using InteractiveUtils

# ╔═╡ 3aa97ecf-b438-427f-9ccd-a7d7e5f1d748
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

# ╔═╡ f82b8798-60d2-45e3-8880-74848c69261d
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


# ╔═╡ 7127fda9-4ade-4719-aed4-be40c469d317
isPuzzleComplete(pzl::Dict{String,String})::Bool = all([length(v) == 1 for v in values(pzl)])

# ╔═╡ 640c4df3-49e3-4fa5-a8c8-088342123b73
isFamilyCorrect(puzzle::Dict{String,String},familySquares::Vector{String})::Bool = join(sort(collect(join([puzzle[familySq] for familySq in familySquares],"")))) == "123456789"

# ╔═╡ 08adcce5-9f36-4922-a219-5cc8227447c4
isPuzzleSolved(pzl::Dict{String,String})::Bool = isPuzzleComplete(pzl) && all(map(fam -> isFamilyCorrect(pzl, fam), values(Definitions.families)))

# ╔═╡ 9fc5601d-d091-4abb-9a86-c183aab57ffc
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

# ╔═╡ d6b2d015-9ef4-43d1-be89-a38ccf96d3f3
function getNextEntryPoint(puzzle::Dict{String,String})::String

	nCounts = map(length,values(puzzle))
	maxKey  = [item.first for item in puzzle if length(item.second)==maximum(nCounts)]
	return maxKey[1]

end

# ╔═╡ 8f0ed96b-e3a4-4016-9f1f-e3a20d4ad676


# ╔═╡ 703c49b8-d51c-401e-a0b8-1982d7b2d1cc
puzzleFile = "C:\\Users\\david\\Projects\\sudokuSolver\\input\\mediumSample.ini"

# ╔═╡ bfdaf6af-1bf5-40b2-aec4-ddcb4ddcfae0
#function solveTheThing(puzzle::Dict{String,String})

	# First do an elimination pass


# ╔═╡ 757cd3a1-4715-4094-96c1-651d5aa4004b
puzzle = importPuzzle(puzzleFile)

# ╔═╡ 075a4274-5b27-466d-8226-2b68f7e5e2d2

if ~isPuzzleSolved(puzzle)
		# Make a guess
		puzzle    = eliminationPass(puzzle)
		nextEntry = getNextEntryPoint(puzzle)
		nextValues= puzzle[nextEntry]
		#for nextValue in nextValues
		nextValue = nextValues[1]
		nextPuzzleGuess = copy(puzzle)
		nextPuzzleGuess[nextEntry] = string(nextValue)
        nextPuzzleGuess = eliminationPass(nextPuzzleGuess)
	
	
end


# ╔═╡ 00000000-0000-0000-0000-000000000001
PLUTO_PROJECT_TOML_CONTENTS = """
[deps]
Memoize = "c03570c3-d221-55d1-a50c-7939bbd78826"

[compat]
Memoize = "~0.4.4"
"""

# ╔═╡ 00000000-0000-0000-0000-000000000002
PLUTO_MANIFEST_TOML_CONTENTS = """
# This file is machine-generated - editing it directly is not advised

julia_version = "1.11.5"
manifest_format = "2.0"
project_hash = "64f5358479b91887917e16ab0d9750f65a3d08e5"

[[deps.MacroTools]]
git-tree-sha1 = "1e0228a030642014fe5cfe68c2c0a818f9e3f522"
uuid = "1914dd2f-81c6-5fcd-8719-6d5c9610ff09"
version = "0.5.16"

[[deps.Memoize]]
deps = ["MacroTools"]
git-tree-sha1 = "2b1dfcba103de714d31c033b5dacc2e4a12c7caa"
uuid = "c03570c3-d221-55d1-a50c-7939bbd78826"
version = "0.4.4"
"""

# ╔═╡ Cell order:
# ╠═3aa97ecf-b438-427f-9ccd-a7d7e5f1d748
# ╠═f82b8798-60d2-45e3-8880-74848c69261d
# ╠═7127fda9-4ade-4719-aed4-be40c469d317
# ╠═640c4df3-49e3-4fa5-a8c8-088342123b73
# ╠═08adcce5-9f36-4922-a219-5cc8227447c4
# ╠═9fc5601d-d091-4abb-9a86-c183aab57ffc
# ╠═d6b2d015-9ef4-43d1-be89-a38ccf96d3f3
# ╠═8f0ed96b-e3a4-4016-9f1f-e3a20d4ad676
# ╠═703c49b8-d51c-401e-a0b8-1982d7b2d1cc
# ╠═757cd3a1-4715-4094-96c1-651d5aa4004b
# ╠═bfdaf6af-1bf5-40b2-aec4-ddcb4ddcfae0
# ╠═075a4274-5b27-466d-8226-2b68f7e5e2d2
# ╟─00000000-0000-0000-0000-000000000001
# ╟─00000000-0000-0000-0000-000000000002
