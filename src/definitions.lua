
local myFuns = require "src.helpers"

local definitions = {}

definitions.rowNames = {'A','B','C','D','E','F','G','H','I'}
definitions.colNames = {'1','2','3','4','5','6','7','8','9'}
definitions.allKeys  = myFuns.cross(definitions.rowNames, definitions.colNames)

definitions.cellRows    = {
                        [1] = 'ABC',
                        [2] = 'DEF',
                        [3] = 'GHI'}
definitions.cellColumns = {
                        [1] = '123',
                        [2] = '456',
                        [3] = '789'}

definitions.difficultyEnum = {
    [1] = 'TRIVIAL',
    [2] = 'EASY',
    [3] = 'SO SO',
    [4] = 'HARD',
    [5] = 'VERY HARD',
    [6] = 'EVIL',
    [7] = 'DASTURDLY EVIL'}

local getRow = myFuns.getRow
local getCol = myFuns.getCol


local theRowNeighbors = {}
function definitions.getRowNeighbors(theGridID)

    if theRowNeighbors[theGridID] == nil
    then
        local theNeighbors = {}
        local theRow = getRow(theGridID)
        for _,theCol in pairs(definitions.colNames) do
            table.insert(theNeighbors, theRow .. tostring(theCol))
        end
        theRowNeighbors[theGridID] = theNeighbors
        return theRowNeighbors[theGridID]
    else
        return theRowNeighbors[theGridID]
    end
end

local theColumnNeighbors = {}
function definitions.getColumnNeighbors(theGridID)

    if theColumnNeighbors[theGridID] == nil
    then

        local theNeighbors = {}
        local theCol = getCol(theGridID)
        for _,theRow in ipairs(definitions.rowNames) do
            table.insert(theNeighbors, theRow .. tostring(theCol))
        end
        theColumnNeighbors[theGridID] = theNeighbors
        return theColumnNeighbors[theGridID]
    else

        return theColumnNeighbors[theGridID]
    end
end

local theCellNeighbors = {} -- put outside so can cache the result
function definitions.getCellNeighbors(theGridID)

    if theCellNeighbors[theGridID] == nil
    then
        local rowGroupIdx    = myFuns.findStringMember(
            getRow(theGridID),
            definitions.cellRows)
        local columnGroupIdx = myFuns.findStringMember(
            getCol(theGridID),
            definitions.cellColumns)
        theCellNeighbors[theGridID] = myFuns.cross( 
            myFuns.string2Table(definitions.cellRows[rowGroupIdx]),
            myFuns.string2Table(definitions.cellColumns[columnGroupIdx]) )
        return theCellNeighbors[theGridID]
    else
        return theCellNeighbors[theGridID]
    end
end

local allSquareNeighbors = {}
function definitions.getNeighbors(gridKey)
    if allSquareNeighbors[gridKey] == nil
    then
        local allSquares = myFuns.joinTables(
            definitions.getRowNeighbors(gridKey),
            definitions.getColumnNeighbors(gridKey),
            definitions.getCellNeighbors(gridKey))
        allSquares[gridKey] = nil
        allSquareNeighbors[gridKey] = allSquares
        return allSquareNeighbors[gridKey]
    else
        return allSquareNeighbors[gridKey]
    end
end

local function getAllPuzzleFamilies()
    local theFamilies = {}
    -- be sure only do this once and not waste the effort

    -- the row families
    for _,rowName in pairs(definitions.rowNames)
    do
        table.insert(theFamilies, definitions.getRowNeighbors(rowName .. '1') )
    end

        -- the column families
    for _,colNumber in pairs(definitions.colNames)
    do
        table.insert(theFamilies, definitions.getColumnNeighbors('A' .. tostring(colNumber)) )
    end

        -- the cell families. the same getRow and getCol will work here to grab one of each cell

    for iRow = 1,3 do
        for iCol = 1,3 do
            table.insert(
                theFamilies,
                definitions.getCellNeighbors( tostring(getRow(definitions.cellRows[iRow])) .. tostring(getCol(definitions.cellColumns[iCol]))))
        end
    end

    return theFamilies
end
definitions.allFamilies = getAllPuzzleFamilies()

return definitions