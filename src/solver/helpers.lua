local helperFuns = {}

function helperFuns.min(inTable)
    local minVal = math.huge
    local minKey
    for key, value in pairs(inTable)
    do
        if value < minVal
        then
            minVal = value
            minKey = key
        end
    end
    return minVal, minKey

end

function helperFuns.max(inTable)
    local maxVal = -math.huge
    local maxKey
    for key, value in pairs(inTable)
    do
        if value > maxVal
        then
            maxVal = value
            maxKey = key
        end
    end
    return maxVal, maxKey

end

function helperFuns.string2Table(inString)
    local outArg = {}
    for ii = 1, #inString
    do
        outArg[#outArg+1] = inString:sub(ii,ii)
    end
    return outArg
end

function helperFuns.joinTables(...)
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

function helperFuns.copyTable(origTable)
    local newTable = {}
    for key, val in pairs(origTable)
    do
        newTable[key] = val
    end
    return newTable
end

function helperFuns.asIndexedTable(inTable)
    local outArg = {}
    for _,gridVal in pairs(inTable)
    do
        outArg[#outArg+1] = gridVal
    end
    return outArg
end

function helperFuns.count(base, pattern)
    return select(2, string.gsub(base, pattern, ""))
end

function helperFuns.countOccurances(inTable)

    -- convert to indexed so can table.concat
    local valsList = table.concat(helperFuns.asIndexedTable(inTable),'')

    local occuranceCount = {}
    for ii = 1, 9
    do

        local count = helperFuns.count(valsList, tostring(ii))

        occuranceCount[tostring(ii)] = count
    end
    return occuranceCount
end

function helperFuns.cross(inArg1, inArg2)
    local outArg = {}
    for _,arg1 in pairs(inArg1) do
        for _,arg2 in pairs(inArg2) do
            outArg[#outArg+1] = arg1 .. arg2
        end
    end
    return outArg
end

function helperFuns.findStringMember(theStr, theMembers)
    for idx,groupMembers in pairs(theMembers)
    do
        if string.find(groupMembers, theStr)  then
            return idx
        end
    end
    return nil
end

function helperFuns.cprint(msg, color)
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

function helperFuns.subsref(inArg, referenceKeys)
    local outArg = {}
    for _, key in ipairs(referenceKeys)
    do
        outArg[key] = inArg[key]
    end
    return outArg
end


return helperFuns