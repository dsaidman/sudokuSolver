---@diagnostic disable: trailing-space
-- sudoku solver in lua, at least an attempt of one
package.path = package.path .. ';/usr/local/share/lua/5.1/?.lua'
local iniReader   = require "inifile"
local rowNames    = {'A', 'B', 'C','D','E','F','G','H','I'}
local colNames    =  {1,2,3,4,5,6,7,8,9}
local valueList   =  '123456789'
local cellRows    = {
                        [1] = 'ABC',
                        [2] = 'DEF',
                        [3] = 'GHI'}
local cellColumns = {
                        [1] = '123',
                        [2] = '456',
                        [3] = '789'}
local solverInfo = {
                        ['numOperations'] = 0,
                        ['numRecursions'] = 0}

local difficultEnum = {
    [1] = 'TRIVIAL',
    [2] = 'EASY',
    [3] = 'SO SO',
    [4] = 'HARD',
    [5] = 'VERY HARD',
    [6] = 'DASTURDLY EVIL'
}
local function string2Table(inString)
    local outArg = {}
    for ii = 1, #inString
    do
        outArg[ii] = inString:sub(ii,ii)
    end
    return outArg
end

local function catTables(...)
    local outArg = {}
    local inArgs = {...}
    for _,nextTable in ipairs(inArgs)
    do
        for _,v in pairs(nextTable)
        do
            outArg[v]=v
        end
    end
    return outArg

end

local function cross(inArg1, inArg2)
    local outArg = {}
    local n = 0
    for _,arg1 in pairs(inArg1) do
        for _,arg2 in pairs(inArg2) do
            n = n+1
            outArg[n] = arg1 .. arg2
        end
    end
    return outArg
end

local allKeys = cross(rowNames, colNames)

local function getRow(theGridID) return string.sub(theGridID,1,1) end

local function getCol(theGridID) return string.sub(theGridID,2,2) end

local function findStringMember(theStr, theMembers)
    for idx,groupMembers in pairs(theMembers)
    do
        if string.find(groupMembers, theStr)  then
            return idx
        end
    end
    return nil
end

local function importFromFile(filePath) return iniReader.parse(filePath).HARD end

local function cprint(msg, color)
    local val
    if color == 'red' then
        val = 31
    elseif color == 'green' then
        val = 32
    elseif color == 'orange' then
        val = 33
    elseif color == 'blue' then
        val = 34
    end

    return string.format("\27[%dm%s\27[0m", val, msg)
end

local function getRowNeighbors(theGridID)
    local theNeighbors = {}
    local theRow = getRow(theGridID)
    for _,theCol in pairs(colNames) do
        table.insert(theNeighbors, theRow .. tostring(theCol))
    end
    return theNeighbors

end

local function getColumnNeighbors(theGridID)
    local theNeighbors = {}
    local theCol = getCol(theGridID)
    for _,theRow in ipairs(rowNames) do
        table.insert(theNeighbors, theRow .. tostring(theCol))
    end
    return theNeighbors
end

local function getCellNeighbors(theGridID)

    local rowGroupIdx    = findStringMember(
        getRow(theGridID),
        cellRows)
    local columnGroupIdx = findStringMember(
        getCol(theGridID),
        cellColumns)
    return cross( string2Table(cellRows[rowGroupIdx]),  string2Table(cellColumns[columnGroupIdx]) )
end

local function getAllPuzzleFamilies()
    -- be sure only do this once and not waste the effort

    local theFamilies = {}

    -- the row families
    for _,rowName in pairs(rowNames)
    do
        table.insert(theFamilies, getRowNeighbors(rowName .. '1') )
    end

    -- the column families
    for _,colNumber in pairs(colNames)
    do
        table.insert(theFamilies, getColumnNeighbors('A' .. tostring(colNumber)) )
    end

    -- the cell families. the same getRow and getCol will work here to grab one of each cell

    for iRow = 1,3 do
        for iCol = 1,3 do
            table.insert(
                theFamilies,
                getCellNeighbors( tostring(getRow(cellRows[iRow])) .. tostring(getCol(cellColumns[iCol]))))
        end
    end
    return theFamilies
end

local allFamilies = getAllPuzzleFamilies()

local function getSquareNeighbors(gridKey)
    local allSquares = catTables(
        getRowNeighbors(gridKey),
        getColumnNeighbors(gridKey),
        getCellNeighbors(gridKey))
    allSquares[gridKey] = nil

    return allSquares
end

local function isValidFamily( thePuzzle, theFamily )

    --Check and see if all squares have only a single option left
    for _,squareKey in pairs( theFamily )
    do
        if #thePuzzle[squareKey] > 1
        then
            return false
        end
    end

    --If single option in all squares, make sure values are unique 1-9
    local familyCheckVals = valueList -- copy of possible values

    for _,squareKey in pairs( theFamily )
    do
        familyCheckVals = familyCheckVals:gsub(thePuzzle[squareKey],'')
    end

    -- If value list is empty, then family passed
    return (familyCheckVals:len() == 0)
end

local function isPuzzleComplete(thePuzzle)

    if thePuzzle == -1 or thePuzzle == nil
    then
        return true
    end
    for _,theGridID in pairs(allKeys)
    do
        if #thePuzzle[theGridID] > 1
        then
            return false
        end
    end
    return true
end

local function isPuzzleSolved(thePuzzle)

    -- Now check all the families and make sure those are all valid
    if thePuzzle == -1
    then
        return false
    end

    for _, theFamily in ipairs( allFamilies )
    do
        if  isValidFamily( thePuzzle, theFamily ) == false
        then
            return false
        end
    end
    return true

end

local function initEmptyPuzzle()
    local emptyPuzzle = {}
    local gridKeys = cross(rowNames, colNames)
    for _,gridKey in pairs(gridKeys) do
         emptyPuzzle[gridKey] = valueList
    end
    return emptyPuzzle
end

local function importPuzzle(fileName)
    local startingPuzzle = initEmptyPuzzle()
    local importedValues = importFromFile(fileName)

    for gridID, gridValue in pairs(importedValues)
    do
        startingPuzzle[gridID] = tostring(gridValue)
    end

    return startingPuzzle

end

local function getNextEntryPoint(thePuzzle)
    local minKey
    local minVal = 99
    for gridKey,gridVal in pairs(thePuzzle)
    do
        if #gridVal < minVal and #gridVal > 1
        then
            minKey = gridKey
            minVal =  #gridVal
            if minVal == 2 then
                return minKey
            end
        end
    end
    return minKey
end

local function getDifficulty()
    if solverInfo.numRecursions == 0 then
        return difficultEnum[1]
    elseif solverInfo.numRecursions == 1 then
        return difficultEnum[2]
    elseif solverInfo.numRecursions > 3 then
        return difficultEnum[3]
    elseif solverInfo.numRecursions > 10 then
        return difficultEnum[4]
    elseif solverInfo.numRecursions > 20 then
        return difficultEnum[5]
    elseif solverInfo.numRecursions > 50 then
        return difficultEnum[6]
    end
end

local function copyTable(origTable)
    local newTable = {}
    for key, val in pairs(origTable)
    do
        newTable[key] = val
    end
    return newTable
end

local function printPuzzle( sudokuPuzzle )

    -- print row headers
    local msg = '\n' .. string.format('%5s',' ')
    for colIdx,_ in ipairs(colNames)
    do
        if ((colIdx % 3) == 1)
        then
            msg = msg .. string.format('%3s',' ')
        end
        msg = msg .. cprint(string.format('%10s',tostring(colIdx)),'orange')
    end
    msg = msg .. '\n'

    -- print the rest of the puzzle
    for rowIdx,rowName in ipairs(rowNames) do
        if ((rowIdx % 3) == 1)
        then
            msg = msg .. string.format('%7s',' ') .. string.rep('-',44) .. '\n'
        end
        msg = msg .. cprint(rowName .. ' -> ','orange')
        for _,colName in ipairs(colNames) do
            if ((colName % 3) == 1)
            then
                msg = msg .. ' | '
            end
            msg = msg .. string.format('%10s',sudokuPuzzle[rowName .. tostring(colName)])
        end
        msg = msg .. '\n'
    end
    msg = msg .. cprint('Number of Operations: ','green') .. tostring(solverInfo.numOperations) .. '\n'
    msg = msg .. cprint('Number of Recursions: ','green') .. tostring(solverInfo.numRecursions) .. '\n'
    --msg = msg .. cprint('Difficult Level: ', 'green') .. getDifficulty() .. '\n'
    --msg = msg .. cprint('Elapsed Time: ','green') .. string.format('%.8f seconds', solverInfo.runTime_seconds) .. '\n'

    local isValid = isPuzzleSolved(sudokuPuzzle)
    if isValid == true
    then
        msg = msg .. cprint('Solution is valid','green') .. '\n'
    else
        msg = msg .. cprint('Solution is invalid','red') .. '\n'
    end

    print(msg)
end

local function solveTheThing(thePuzzle)

    local allNeighbors, neighborVals
    local didChange = true

    while (didChange==true) and (isPuzzleComplete(thePuzzle)==false)
    do
        didChange = false
        for gridID,gridValues in pairs(thePuzzle)
        do

            if #gridValues == 1
            then
                allNeighbors = getSquareNeighbors(gridID)
                for neighborKey in pairs(allNeighbors)
                do
                    neighborVals = thePuzzle[neighborKey]
                    if #neighborVals > 1 and neighborVals:find(gridValues)
                    then
                        solverInfo.numOperations = solverInfo.numOperations+1
                        didChange = true
                        thePuzzle[neighborKey] = neighborVals:gsub(gridValues,'')
                    end
                end
            end
        end
    end

    if (isPuzzleComplete(thePuzzle)==true)
    then

        if (isPuzzleSolved(thePuzzle)==true)
        then
            return thePuzzle
        else
            return -1
        end
    else
        local nextPuzzleGuess
        local entryPoint = getNextEntryPoint(thePuzzle)
        local nextGuesses = string2Table( thePuzzle[entryPoint] )
        for _,nextGuess in ipairs(nextGuesses)
        do
            print(string.format('Entry: %s - Value -%s',entryPoint, nextGuess ))
            printPuzzle(thePuzzle)
            solverInfo.numRecursions = solverInfo.numRecursions+1
            nextPuzzleGuess = copyTable(thePuzzle)
            nextPuzzleGuess[entryPoint] = nextGuess
            nextPuzzleGuess = solveTheThing(copyTable(nextPuzzleGuess))
            if isPuzzleComplete(nextPuzzleGuess) == true then
                if (isPuzzleSolved(nextPuzzleGuess)==true)
                then
                    return nextPuzzleGuess
                end
            --else
                -- do next iter
            end
        end

        return -1 -- if it gets here, didnt find the soln
    end
end

local function doTheThing(inFilePath)
    local myPuzzle = importPuzzle(inFilePath)

    local startTime = os.clock()
    local theSolution = solveTheThing( myPuzzle )
    solverInfo['runTime_seconds'] = os.clock()-startTime
    printPuzzle(theSolution)
    return theSolution
end

local luaFile = '/home/dsaidman/projects/sudoku/samples.ini'
doTheThing(luaFile)


