
package.path = package.path .. ';/usr/local/share/lua/5.3/?.lua;/usr/local/share/lua/5.3/?/init.lua;/usr/local/lib/lua/5.3/?.lua;/usr/local/lib/lua/5.3/?/init.lua;/usr/share/lua/5.3/?.lua;/usr/share/lua/5.3/?/init.lua;./?.lua;./?/init.lua'
package.cpath = package.cpath .. ';/usr/local/lib/lua/5.3/?.so;/usr/lib/x86_64-linux-gnu/lua/5.3/?.so;/usr/lib/lua/5.3/?.so;/usr/local/lib/lua/5.3/loadall.so;./?.so'

local argparser = require("argparse")

local parser = argparse()
    :name "sudokuSolver"
    :description "lua argument parser to connect with the solver graphic interface"
    :epilog "not finished yet"







