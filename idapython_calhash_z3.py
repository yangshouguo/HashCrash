
# get three part (init part , loop part , end part) from function

from idaapi import *
from idc import *
import os
import sys
class Inst_search:

    def __init__(self, func_addr):
        self.store_instr = []
        self.init_body = []
        self.loop_body = []
        self.end_body = []
        self.func_addr = func_addr
        self.filename = 'error'
        self.loop_start = 0 #start address of loop
        self.loop_end = 0 # end address of loop

    def searchinfun(self,funstartEA):
        start = funstartEA
        endad = FindFuncEnd(start)
        nowindex = start
        while nowindex<endad:
            instsize = ItemSize(nowindex)
            inst = ua_mnem(nowindex)
            oneinstr = str(inst)
            optype = 1
            i = 0
            while True:

                optype = GetOpType(nowindex,i)
                if( optype==0 or optype == -1 ):
                    i = 0;
                    break;
                else:
                    oneinstr+=(" "+GetOpnd(nowindex,i))
                    i+=1
            if (inst == "jmp"):#get loop start
                ls = oneinstr.find("loc_")
                add_str = oneinstr[ls+4:]
                self.loop_end = int(add_str,16)
            elif(inst == 'jnz'):
                ls = oneinstr.find("loc_")
                add_str = oneinstr[ls+4:]
                self.loop_start = int(add_str,16)
            self.store_instr.append(((nowindex),oneinstr))
            nowindex += instsize


    def search(self):
        self.searchinfun(self.func_addr)
        # print hex(self.loop_start)
        # print hex(self.loop_end)

    def simplifyinstr(self): # simplify the instructions , get 3 part of the function
        init_body = []
        loop_body = []
        end_body = []
        if (self.loop_end == 0 or self.loop_start==0):
            print "loop error"
            return 0
        end_flag = False
        for item in self.store_instr:
            if(item[0] < self.loop_start):
                self.init_body.append(item[1])
            elif (item[0] >= self.loop_start and item[0] < self.loop_end):
                self.loop_body.append(item[1])
            elif (item[0] > self.loop_end):
                if(end_flag):
                    self.end_body.append(item[1])
                if ("jnz" in item[1]):
                    end_flag = True
        # print init_body
        # print loop_body
        # print end_body


func_addr = 0x40052D
instrReplace = Inst_search(func_addr)
instrReplace.search()
instrReplace.simplifyinstr()
print instrReplace.init_body
print instrReplace.loop_body
print instrReplace.end_body
# print idc.ARGV
import funcz3
aa = funcz3.getZ3expr(instrReplace.init_body,instrReplace.loop_body,instrReplace.end_body,4)
aa.solve()
# numarg = len(idc.ARGV)
# if( len(idc.ARGV) < 3):
#     instrsear = Inst_search('move','move','move')
#     instrsear.search()
# else:
#     instrsear = Inst_search(idc.ARGV)
#     instrsear.search()
# idc.Exit(0)

