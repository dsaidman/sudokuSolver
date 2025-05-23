local argparse = require("src.argparse")
local myFuns    = require("src.helpers")


local rowNames = {'A','B','C','D','E','F','G','H','I'}
local colNames = {'1','2','3','4','5','6','7','8','9'}
local puzzleKeys = myFuns.cross(rowNames, colNames)

local inputHandler = {}

local keyParser = argparse()
    :name "sudokuPuzzleparser"
    :description "lua argument parser to connect with the solver graphic interface"
    :epilog "not finished yet"

for _,key in ipairs(puzzleKeys) do
        keyParser:option('--' .. key)
            :count '0-1'
            :convert(tostring)
            :args(1)
            :default(nil)
            :description(string.format('Initial puzzle value for row %s and column %s',string.sub(key,1,1),string.sub(key,2,2)))
end

--[[ local optParser = argparse()
optParser:option("-f --file",'Path to a file with input arguments',nil)
    :count '0-1'
    :args(1)
    :convert(tostring)

optParser:flag('--verbose', 'Set verbosity as on')
    :action("store_true")
    :default(false)

optParser:flag('-v --version', 'Print version info')
    :action("store_true")
    :default(false)

optParser:flag('-p --print', 'Print puzzle formed from inputs')
    :action("store_true")
    :default(false) ]]


function inputHandler.parse()
    return keyParser:parse()
end

return inputHandler





