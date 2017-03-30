# -*- coding: UTF-8 -*-

from idaapi import *
from idc import *
from collections import Counter
import math
from sets import Set
import copy
import time

from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression

classifier =(joblib.load('C:\MLModel\classifier.model'))

def strncmp(str1, strlst):
    for str2 in strlst:
        if (str1[0:len(str2)] == str2):
            return True
    return False

class funAnalyzer(object):  # analyze onle one function

    __basicType = ["addr", "name", "instNum", "instTypeNum" ,"stack","call" , "jump" , "xor" ,"blocks","hascircle"]

    def __init__(self, fun):
        self.attr = {}
        self.Blocks = Set()   # startEA of blocks the func have
        self.__func = fun
        self._Edges = Set()   # save jump egde in function
        for i in funAnalyzer.__basicType:
            self.attr[i] = 0.0

    def startAnalyze(self):
        self.attr["addr"] = self.__func.startEA
        self.attr["name"] = str(GetFunctionName(self.__func.startEA))
        self.attr["stack"] = GetFrameSize(self.__func.startEA)
        self.alzInst()
        self.attr["hascircle"] = self.isCircle()

        input_array = [[self.attr['instTypeNum'], self.attr['xor'], self.attr['instNum'], self.attr['jump'], self.attr['call'], self.attr['blocks'], self.attr['stack'], self.attr['hascircle']]]
        # print 'input_array:' , input_array
        pre_result = classifier.predict(input_array)
        if(pre_result[0] == 1):
            print self.attr["addr"] , self.attr["name"]
        return self.attr

    def alzInst(self):
        self.Blocks = self.count_blocksOfFun()
        self.attr["blocks"] = len(self.Blocks)
        inst_list = []
        func = self.__func
        it = func_item_iterator_t(func)  # a function iterator
        t = True
        while (t):
            hasInternal = False
            ea = it.current()
            inst = ua_mnem(ea)
            inst_list.append(inst) # the instructions at ea :jmp mov add
            if strncmp(inst , ["xor"]):
                self.attr["xor"]+=1
            blk = xrefblk_t()
            i = blk.first_from(ea,XREF_ALL)
            while i :
                ref = blk.to
                if blk.type == dr_O:
                    seg = getseg(blk.to)
                elif blk.type in [fl_CN, fl_CF]:
                    self.attr["call"] += 1
                elif blk.type in [fl_JN , fl_JF]:
                    self.attr["jump"] += 1
                    if func_contains(func , ref):
                        hasInternal = True
                        if isFlow(GetFlags(ref)):
                            self.mkEgde(PrevHead(ref , get_fchunk(ref).startEA) , ref)
                        if ph.id == PLFM_MIPS:
                            self.mkEgde(NextHead(ea) , ref)
                        else:
                            self.mkEgde(ea, ref)
                i = blk.next_from()
            t = it.next_code()
            if hasInternal and t:
                next_ea = it.current()
                if ph.id == PLFM_MIPS:
                    t2 = it.next_code()
                    if t2 and isFlow(GetFlags(it.current())):
                        self.mkEgde(next_ea, it.current())
                    # print "Lin3:%x %x"%(next_ea,it.current())
                    it.set(func, next_ea)
                else:
                    if isFlow(GetFlags(next_ea)):
                        self.mkEgde(ea, next_ea)
        c = Counter(inst_list)
        # print '1',self.attr['name']
        # print 'keys' , c.keys()
        # print 'values' , c.values()
        self.attr["instNum"] = sum(c.values())
        self.attr["instTypeNum"] = len(c.keys())
    def mkEgde(self ,x ,y):
        if x != BADADDR and y != BADADDR:
            # print 'edge:',hex(x),hex(y)
            self._Edges.add((x,y))
            # get the startEA of every block

    # get the startEA of every block
    def count_blocksOfFun(self):
        bb_list = []
        fc = FlowChart(self.__func) #flowchart
        for j in range(0,fc.size):
            bb = fc.__getitem__(j)
            if bb.startEA == bb.endEA:
                break
            if bb.startEA != PrevHead(bb.endEA , bb.startEA):
                self.mkEgde(bb.startEA ,PrevHead(bb.endEA , bb.startEA))
            bb_list.append(bb.startEA)
        return bb_list


    def isCircle(self):# does function flowchart have a ring? use Topological algrithom

        start = []
        end = []
        isremove = []
        indegree = []
        len_arr = len(self._Edges)
        if len_arr<2:
            return 0
        for item in self._Edges:
            start.append(item[0])
            end.append(item[1])
            isremove.append(0)
            indegree.append(0)
        for i in range(0,len_arr):
            for j in range(0,len_arr):
                if end[i] == start[j]:
                    indegree[j]+=1
        # print start
        # print end

        while True:
            haswork = False
            for i in range(0, len_arr):
                if isremove[i]==0:
                    if(indegree[i] == 0):
                        k = i
                        for j in range(0, len_arr):
                            if (isremove[j]==0 and start[j]==end[i]):
                                indegree[j]-=1
                                k = j
                                # print 'indegree j',j,indegree[j]
                        isremove[i] = 1
                        i = k
                        # print 'removed :' ,i
                        haswork = True
            if not haswork:
                break

        for i in range(0,len_arr):
            if(isremove[i] == 0):
                return 1




        return 0



def main():  # response for executing
    flst = {}
    for i in range(0, get_func_qty()):
        fun = getn_func(i)  # getn_func() returns a func_t struct for the function
        segname = get_segm_name(fun.startEA)  # get the segment name of the function by address (fun.startEA is start address)
        if segname[1:3] not in ["OA","OM","te"]:
            continue
        # if 'Hash'  in str(GetFunctionName(fun.startEA)):
        #     print '---------',GetFunctionName(fun.startEA)
        if True:
            f = funAnalyzer(fun)
            flst[fun.startEA] = f.startAnalyze()


    # for idx in flst:
    #     attr = flst[idx]
    #     print attr['instTypeNum'],attr['xor'],attr['instNum'],attr['jump'],attr['call'],attr['blocks'],attr['stack'],attr['hascircle']

if __name__ == "__main__":
    main()



