---@diagnostic disable: trailing-space
-- sudoku solver in lua, at least an attempt of one

local myFuns      = require("src.solver.LHelpers")
local defs        = require('src.solver.LDefinitions')

local rowNames    = defs.rowNames
local colNames    = defs.colNames
local valueList   = table.concat(defs.colNames)

local result = {        ['solution'] = {},
                        ['duration_ms']    = 0.0,
                        ['bestSinglePass'] = 0,
                        ['numOperations']  = 0,
                        ['numRecursions']  = 0}

local allKeys     = defs.allKeys
local squares     = defs.allKeys
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
        -- print(gridID .. ' = ' .. gridValue)
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

--[[ local function getDifficulty()
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
                        result.numOperations = result.numOperations+1
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
            result.numRecursions = result.numRecursions+1
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
    result.bestSinglePass = 0
    result.numOperations  = 0
    result.numRecursions  = 0
    result.solution       = false

    local startTime = os.clock()
    local theSolution = solveTheThing( myPuzzle )
    result['duration_ms'] = (os.clock()-startTime)*1000
    result['solution'] = theSolution

    return result
end

return solver
