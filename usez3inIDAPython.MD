
1. firstly you should copy all z3 file to the  youridapath/python/lib/python2.7/


2. in the file that you use z3 , you type this: 
  from z3 import *
  init('youridapath/python/lib/python2.7/z3/lib')
  
  
  remember , cause ida is a 32bit software , so you must use 32bit z3 libz3.so
 3. how to get a 32-bit libz3.so ?
 
  ...
