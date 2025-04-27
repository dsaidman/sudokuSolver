---@diagnostic disable: trailing-space
-- sudoku solver in lua, at least an attempt of one

local myFuns      = require("src.helpers")
local defs        = require('src.definitions')

local rowNames    = defs.rowNames
local colNames    = defs.colNames
local valueList   = table.concat(defs.colNames)

local solverInfo = {
                        ['numOperations'] = 0,
                        ['numRecursions'] = 0}

local difficultEnum = defs.difficultyEnum

local allKeys     = defs.allKeys
local allFamilies = defs.allFamilies

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
    local gridKeys = myFuns.cross(rowNames, colNames)
    for _,gridKey in pairs(gridKeys) do
         emptyPuzzle[gridKey] = valueList
    end
    return emptyPuzzle
end

local function importPuzzle(startingValues)
    local startingPuzzle = initEmptyPuzzle()
    for gridID, gridValue in pairs(startingValues)
    do
        print(gridID .. ' = ' .. gridValue)
        startingPuzzle[gridID] = tostring(gridValue)
    end
    return startingPuzzle
end

--local previousKey
local function getNextEntryPoint(thePuzzle)
    local occuranceCount    = myFuns.countOccurances(thePuzzle)

    local maxOccuranceValue = tostring(select(2,myFuns.max(occuranceCount)))
    local filteredPuzzle = {}
    for theGridKey, theGridValue in pairs(thePuzzle) do
        if string.find(theGridValue, maxOccuranceValue) then
           filteredPuzzle[theGridKey]=thePuzzle[theGridKey]
        end
    end

    local maxAvailable   = 0
    for _,value in pairs(thePuzzle)
    do
        maxAvailable = math.max(maxAvailable, #value)
    end

    local possibleKeys = {}
    for numPossibilities = 2, maxAvailable
    do
        local continueFlag = true
        for theGridKey, theGridValue in pairs(filteredPuzzle) do

            if string.find(theGridValue, maxOccuranceValue) and (#theGridValue == numPossibilities) --and (theGridKey~=previousKey)
            then

                continueFlag = false
                table.insert(possibleKeys, theGridKey)
            end
        end
        if continueFlag == false then break end
    end

    local sumOccurances = {}
    for _, gridKey in ipairs(possibleKeys) do
        sumOccurances[gridKey] = 0
        local possibleVals = myFuns.string2Table(filteredPuzzle[gridKey])
        for _,possibleVal in ipairs(possibleVals) do
             sumOccurances[gridKey] =  sumOccurances[gridKey] + occuranceCount[possibleVal]
        end
    end

    local entryPointKey = select(2,myFuns.max(sumOccurances))
    --previousKey = entryPointKey
    if thePuzzle[entryPointKey] == nil then
        return nil, nil
    else
        local orderedGuesses = myFuns.string2Table(thePuzzle[entryPointKey])
        table.sort(orderedGuesses, function (v1, v2) return occuranceCount[v1] > occuranceCount[v2] end)

        return entryPointKey, orderedGuesses
    end
end

local function getDifficulty()
    if solverInfo.numRecursions == 0 then
        return difficultEnum[1]
    elseif solverInfo.numRecursions < 5 then
        return difficultEnum[2]
    elseif solverInfo.numRecursions < 25 then
        return difficultEnum[3]
    elseif solverInfo.numRecursions < 50 then
        return difficultEnum[4]
    elseif solverInfo.numRecursions < 100 then
        return difficultEnum[5]
    elseif solverInfo.numRecursions < 400 then
        return difficultEnum[6]
    else
        return difficultEnum[7]
    end
end

local function puzzle2String( sudokuPuzzle )
    local argOut = ''
    for key, val in pairs(sudokuPuzzle)
    do
        argOut = argOut .. key .. '=' .. val .. '\n'
    end
    return argOut
end

--[[ local function printPuzzle( sudokuPuzzle )

    -- print row headers
    local msg = '\n' .. string.format('%5s',' ')
    for colIdx,_ in ipairs(colNames)
    do
        if ((colIdx % 3) == 1)
        then
            msg = msg .. string.format('%3s',' ')
        end
        msg = msg .. myFuns.cprint(string.format('%10s',tostring(colIdx)),'orange')
    end
    msg = msg .. '\n'

    -- print the rest of the puzzle
    for rowIdx,rowName in ipairs(rowNames) do
        if ((rowIdx % 3) == 1)
        then
            msg = msg .. string.format('%7s',' ') .. string.rep('-',98) .. '\n'
        end
        msg = msg .. myFuns.cprint(rowName .. ' -> ','orange')
        for _,colName in ipairs(colNames) do
            if ((colName % 3) == 1)
            then
                msg = msg .. ' | '
            end
            local gridKey = rowName .. tostring(colName)
            if importedValues[gridKey] == nil

            then
                msg = msg .. string.format('%10s',sudokuPuzzle[gridKey])
            else
                msg = msg .. myFuns.cprint(string.format('%10s',sudokuPuzzle[gridKey]),'red')
            end
        end
        msg = msg .. '\n'
    end
     if isPuzzleComplete(sudokuPuzzle) then
        msg = msg .. myFuns.cprint('Number of Operations: ','green') .. tostring(solverInfo.numOperations) .. '\n'
        msg = msg .. myFuns.cprint('Number of Recursions: ','green') .. tostring(solverInfo.numRecursions) .. '\n'
        msg = msg .. myFuns.cprint('Difficult Level: ', 'green') .. getDifficulty() .. '\n'
    end
    if solverInfo['runTime_seconds'] ~= nil then
        msg = msg .. myFuns.cprint('Elapsed Time: ','green') .. string.format('%.8f seconds', solverInfo.runTime_seconds) .. '\n'
    end

    local isValid = isPuzzleSolved(sudokuPuzzle)
    if isValid == true
    then
        msg = msg .. myFuns.cprint('Solution is valid','green') .. '\n'
    else
        msg = msg .. myFuns.cprint('Solution is invalid','red') .. '\n'
    end

    print(msg)
end ]]

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
                allNeighbors = defs.getNeighbors(gridID)
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
        local entryPoint, nextGuesses = getNextEntryPoint(thePuzzle)

        if entryPoint == nil then
            return -1
        end
        for _,nextGuess in ipairs(nextGuesses)
        do
            --print(string.format('Entry: %s - Value -%s',entryPoint, nextGuess ))
            --printPuzzle(thePuzzle)
            solverInfo.numRecursions = solverInfo.numRecursions+1
            nextPuzzleGuess = myFuns.copyTable(thePuzzle)
            nextPuzzleGuess[entryPoint] = nextGuess
            nextPuzzleGuess = solveTheThing(myFuns.copyTable(nextPuzzleGuess))
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


---local function doTheThing(inFilePath)
---    local myPuzzle = importPuzzle(inFilePath)
---    printPuzzle(myPuzzle)
---   print(myFuns.cprint('Running...','red'))
---    local startTime = os.clock()
---    local theSolution = solveTheThing( myPuzzle )
---    solverInfo['runTime_seconds'] = os.clock()-startTime
---    printPuzzle(theSolution)
---    return theSolution
---end
local solver = {}
function solver.solve(myStartingVals)

    local myPuzzle = importPuzzle(myStartingVals)
    --printPuzzle(myPuzzle)
    print(myFuns.cprint('Running...','red'))
    local startTime = os.clock()
    local theSolution = solveTheThing( myPuzzle )
    solverInfo['runTime_seconds'] = os.clock()-startTime
    solverInfo['difficulty'] = getDifficulty()
    --printPuzzle(theSolution)
    --print( puzzle2String(theSolution) )
    theSolution['info'] = solverInfo
    return theSolution
end

return solver
