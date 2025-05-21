module Definitions

export rowNames, columnNames, squares, neighbors, cellRows, cellColumns, puzzle0, families

const rowNames::String = "ABCDEFGHI"
const columnNames::String = "123456789"
const squares::Vector{String} = unique([string(row, col) for row in rowNames for col in columnNames])
const cellRows::Vector{String} = ["ABC", "DEF", "GHI"]
const cellColumns::Vector{String} = ["123", "456", "789"]

_getRowNeighbors(sq)::Vector{String} = sq[1] .* collect(columnNames)
_getColumnNeighbors(sq)::Vector{String} = collect(rowNames) .* sq[2]

function _getCellNeighbors(sq::String)::Vector{String}
    _rows = cellRows[findfirst(x -> occursin(sq[1], x), cellRows)]
    _cols = cellColumns[findfirst(x -> occursin(sq[2], x), cellColumns)]
    return [r * c for r in _rows for c in _cols]
end

# All neigbhors of a
function _neighborsOf(sq::String)::Vector{String}
    return filter!(!=(sq), sort(unique(vcat(_getRowNeighbors(sq),
        _getColumnNeighbors(sq),
        _getCellNeighbors(sq)))))
end

# Get the neighbors of each square
const neighbors::Dict{String,Vector{String}} = Dict(sq => _neighborsOf(sq) for sq in squares)

# All families
begin 
    tmp = Dict{Int,Vector{String}}()
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
    const families::Dict{Int,Vector{String}} = tmp
end

puzzle0::Dict{String,String} = Dict(sq => "123456789" for sq in squares)

end