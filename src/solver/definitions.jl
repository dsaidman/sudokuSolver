module Definitions

export rowNames, columnNames, allKeys, neighbors, cellRows, cellColumns, puzzle0

const rowNames::String             = "ABCDEFGHI"
const columnNames::String         = "123456789"
const allKeys::Vector{String}     = unique([string(row, col) for row in rowNames for col in columnNames])
const squares::Vector{String}     = allKeys
cellRows    = ["ABC", "DEF", "GHI"]
cellColumns = ["123", "456", "789"]


function _neighborsOf(sq::String)
    local _colCell = cellColumns[(first(findfirst(sq[2], columnNames))%3)+1]
    local _rowCell = cellRows[(first(findfirst(sq[1], rowNames))%3)+1]

    local _neighborCells = [string(row, col) for row in _rowCell for col in _colCell]
    local _neighborrowNames = [string(sq[1], col) for col in columnNames]
    local _neighborCols = [string(row, sq[2]) for row in rowNames]

    return filter!(!=(sq),sort(unique(vcat(_neighborCells, _neighborrowNames, _neighborCols))))

end

# Get all the neighbors for every square
const neighbors = Dict{String,Vector{String}}(sq => _neighborsOf(sq) for sq in squares)

# Default empty puzzle
puzzle0 = Dict{String,String}(sq => "123456789" for sq in squares)

end