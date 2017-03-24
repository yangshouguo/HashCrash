# a IDAPython script : give two  instruction close to each other like move add , it find their binary representation

from idaapi import *
from idc import *
import os
import sys
class Inst_search:

    def __init__(self , *argv):
        self.arg = argv[0]
        self.instr_num = len(argv)
        self.filename = 'error'
        self.openfile()

    def printself(self):
        print self.inst1,self.inst2
    def printAinstr(self,startea, Itemsize):
        out = []
        strr = '0000000'
        for i in range(startea, Itemsize+startea):
            strq = str(bin(GetOriginalByte(i)))[2:]
            n = len(strq)
            strq = strr[0:8 - n] + strq
            out.append(strq)
        return str(''.join(out))
    def searchinfun(self,fun):
        start = fun.startEA
        endad = FindFuncEnd(start)
        nowindex = start
        instr_match = [] # instructions will be matched
        instr_size = []
        instr_ea = []
        instr_match_size = 0
        while nowindex<endad:
            instsize = ItemSize(nowindex)
            inst = ua_mnem(nowindex)
            instr_match.append(inst)
            instr_ea.append(nowindex)
            instr_size.append(instsize)
            instr_match_size += 1
            if (instr_match_size == self.instr_num):
                #cmp instructions
                matched = False
                for i in range(self.instr_num):
                    if (self.arg[i] == instr_match[i]):
                        matched = True
                    else:
                        matched = False
                        break
                # print instr_match
                # print instr_ea
                # print instr_size
                #if true
                if(matched):
                    for i in range(self.instr_num):
                        x = self.printAinstr(int(instr_ea[i]),int(instr_size[i]))
                        self.fhandle.write(x+' ')
                        print x
                    self.fhandle.write('\n')
                #else

                instr_ea.pop(0)
                instr_match.pop(0)
                instr_size.pop(0)
                instr_match_size -= 1
            nowindex+=instsize


    def openfile(self):
        self.filename = str(os.getcwd())+os.sep
        self.filename += GetInputFile()+'_'
        for str1 in self.arg:
            self.filename+=str1
        self.filename+='.txt'
        self.fhandle = open(self.filename, 'w+')
        print self.filename

    def search(self):
        for i in range(get_func_qty()):

            fun = getn_func(i)
            print 'search in function : ',i, str(GetFunctionName(fun.startEA))
            # print self.filename
            self.searchinfun(fun)
        self.fhandle.close()


print idc.ARGV
numarg = len(idc.ARGV)
if( len(idc.ARGV) < 3):
    instrsear = Inst_search('move','move','move')
    instrsear.search()
else:
    instrsear = Inst_search(idc.ARGV[1:])
    instrsear.search()
