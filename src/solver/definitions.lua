
local helperFuns = require "helpers"

local definitions = {}
definitions.rowNames = {'A','B','C','D','E','F','G','H','I'}
definitions.colNames = {'1','2','3','4','5','6','7','8','9'}
definitions.allKeys  = helperFuns.cross(definitions.rowNames, definitions.colNames)

definitions.cellRows    = {
                        [1] = 'ABC',
                        [2] = 'DEF',
                        [3] = 'GHI'}
definitions.cellColumns = {
                        [1] = '123',
                        [2] = '456',
                        [3] = '789'}

definitions.difficultEnum = {
    [1] = 'TRIVIAL',
    [2] = 'EASY',
    [3] = 'SO SO',
    [4] = 'HARD',
    [5] = 'VERY HARD',
    [6] = 'EVIL',
    [7] = 'DASTURDLY EVIL'}

return definitions