
local myFuns      = require("src.solver.LHelpers")
local defs        = require('src.solver.LDefinitions')

local rowNames    = defs.rowNames
local colNames    = defs.colNames
local valueList   = table.concat(defs.colNames)

local allKeys     = defs.allKeys
local squares     = defs.allKeys
local allFamilies = defs.allFamilies

local function isValidFamily( thePuzzle, theFamily )

    -- check t
    local  x = ""
    for _,squareKey in pairs( theFamily )
    do
        if #thePuzzle[squareKey] > 0
        then
            x  = x .. thePuzzle[squareKey]
        else
            return false
        end
    end

    for sqVal = 1, 9
    do
        if not string.find( x, tostring(sqVal) ) then
            return false
        end
    end
    return true
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


local function allFamiliesValid(thePuzzle)
    for _, theFamily in ipairs( allFamilies )
    do
        if  isValidFamily( thePuzzle, theFamily ) == false
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

    if not isPuzzleComplete(thePuzzle)
    then
        return false
    end

    return allFamiliesValid(thePuzzle)
end


local function initEmptyPuzzle()
    local emptyPuzzle = {}
    local gridKeys = myFuns.cross(rowNames, colNames)
    for _,gridKey in pairs(gridKeys) do
         emptyPuzzle[gridKey] = valueList
    end
    return emptyPuzzle
end

--local previousKey
local function getNextEntryPoint(thePuzzle)
    local occuranceCount    = myFuns.countOccurances(thePuzzle)
    local maxOccuranceValue = tostring(select(2,myFuns.max(occuranceCount)))
    local filteredPuzzle = {}
    for theGridKey, theGridValue in pairs(thePuzzle) do
        if string.find(theGridValue, maxOccuranceValue) and #theGridValue > 1 then
           filteredPuzzle[theGridKey]=thePuzzle[theGridKey]
        end
    end

    local minAvailable   = 10000
    for _,value in pairs(filteredPuzzle)
    do
        minAvailable = math.min(minAvailable, #value)
    end
    local entryPointKey
    for sqKey, sqVal in pairs(filteredPuzzle)
    do
        if #sqVal == minAvailable
        then
            entryPointKey = sqKey
            break
        end
    end

    if thePuzzle[entryPointKey] == nil or #thePuzzle[entryPointKey] <= 1 then
        return nil, nil
    else
        local orderedGuesses = myFuns.string2Table(thePuzzle[entryPointKey])
        table.sort(orderedGuesses, function (v1, v2) return occuranceCount[v1] > occuranceCount[v2] end)

        return entryPointKey, orderedGuesses
    end
end

local solver = {}
function solver.importPuzzle(startingValues)
    local startingPuzzle = initEmptyPuzzle()
    for gridID, gridValue in pairs(startingValues)
    do
        startingPuzzle[gridID] = tostring(gridValue)
    end
    return startingPuzzle
end

function solver.solve(startingValues)

    local result = {        ['solution'] = {},
        ['duration_ms']    = 0.0,
        ['bestSinglePass'] = 0,
        ['numOperations']  = 0,
        ['numRecursions']  = 0}
    local function eliminationPass(thePuzzle)

        local thisSinglePass = 0
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
                            thisSinglePass = thisSinglePass+1
                            didChange = true
                            thePuzzle[neighborKey] = neighborVals:gsub(gridValues,'')
                        end
                    end
                end
            end
        end
        result.bestSinglePass = math.max(thisSinglePass, result.bestSinglePass)
        return thePuzzle
    end
    local function solveTheThing(thePuzzle)

        thePuzzle = eliminationPass(thePuzzle)
        if (isPuzzleComplete(thePuzzle)==true)
        then
            return isPuzzleSolved(thePuzzle)==true and thePuzzle or -1
        else
            local nextPuzzleGuess
            local entryPoint, nextGuesses = getNextEntryPoint(thePuzzle)
            if entryPoint == nil then return -1 end
            for _,nextGuess in ipairs(nextGuesses)
            do
                nextPuzzleGuess = myFuns.copyTable(thePuzzle)
                nextPuzzleGuess[entryPoint] = nextGuess
                if allFamiliesValid(nextPuzzleGuess) then
                    result.numRecursions = result.numRecursions+1
                    nextPuzzleGuess = solveTheThing(myFuns.copyTable(nextPuzzleGuess))
                    if nextPuzzleGuess and (isPuzzleSolved(nextPuzzleGuess)==true)
                    then
                        return nextPuzzleGuess
                    end
                end
            end
            return -1 -- if it gets here, didnt find the soln
        end
    end

    local myPuzzle = solver.importPuzzle(startingValues)
    local startTime = os.clock()
    local theSolution = solveTheThing( myPuzzle )
    result.duration_ms = (os.clock()-startTime)*1000
    result.solution    = theSolution

    return result
end

function solver.puzzleString2puzzle(puzzleStr)

    local pzlVals   = myFuns.string2Table(puzzleStr)
    local puzzle = {}
    for ix, sqKey in ipairs(defs.allKeys)
    do
        if pzlVals[ix] == "."
        then
            puzzle[sqKey] = "123456789"
        else
            puzzle[sqKey] = pzlVals[ix]
        end
    end
    return puzzle
end

function solver.testIt()
   -- local puzzleStr = ".15.7....4..8..75...8..9.169641.7.3..8239.5..5....4.9..2.41.8....17.39.4...92..65"
  --  local puzzleStr = "32.9.......52.7.....958...2.87..5.4.......6...3....7.86......17.....24...7.4...2."
    local puzzleStr = ".......7..1.9.4..8..9........5..17....3..96..1...67..9........4.82.46...3...8...."
    local puzzle    = solver.puzzleString2puzzle(puzzleStr)
    local result = solver.solve(puzzle)
    for k,v in pairs(result.solution) do print(k, v) end

end

return solver
