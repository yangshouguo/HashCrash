

# a IDAPython script : give two  instruction close to each other like move add , it find their binary representation

from idaapi import *
from idc import *
import os
import sys
class Inst_search:

    def __init__(self ):

        self.filename = 'error'
        self.openfile()

    def getoprandType(self,i):
        if(i == 1):
            return 'R'
        elif (i == 2):
            return 'M'
        elif (i == 3):
            return "BI"
        elif (i == 4):
            return "BID"
        elif (i == 5):
            return "Imm"
        elif (i == 6):
            return "ImmFA"
        elif (i == 7):
            return  "ImmNA"
        elif (i>=8 and i <= 12):
            return "SR"
        else:
            return "??"

    def searchinfun(self,fun):
        start = fun.startEA
        endad = FindFuncEnd(start)
        nowindex = start
        while nowindex<endad:
            instsize = ItemSize(nowindex)
            inst = ua_mnem(nowindex)
            self.fhandle.write(str(inst)+" ")
            optype = 1
            i = 0
            while True:
                optype = GetOpType(nowindex,i)
                if( optype==0 or optype == -1 ):
                    i = 0;
                    break;
                else:
                    self.fhandle.write(self.getoprandType(optype)+" ")
                    i+=1
            self.fhandle.write("\n")
            nowindex += instsize

    def openfile(self):
        self.filename = str(os.getcwd())+os.sep
        self.filename += GetInputFile()+'.asm'
        self.fhandle = open(self.filename, 'w+')
        print self.filename

    def search(self):
        for i in range(get_func_qty()):

            fun = getn_func(i)
            print 'search in function : ',i, str(GetFunctionName(fun.startEA))
            # print self.filename
            self.searchinfun(fun)
        self.fhandle.close()

instrReplace = Inst_search();
instrReplace.search();
# print idc.ARGV
# numarg = len(idc.ARGV)
# if( len(idc.ARGV) < 3):
#     instrsear = Inst_search('move','move','move')
#     instrsear.search()
# else:
#     instrsear = Inst_search(idc.ARGV)
#     instrsear.search()


