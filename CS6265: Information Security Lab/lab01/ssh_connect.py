from pwn import *


# Connect to your target server with this function
s = ssh('user', '192.168.88.232', password='user')
payload = 'HELLO'
# Invoke a process in the target
p = s.process('./crackme0x00', cwd='/home/user/tut01-crackme')
p.sendline(payload)
p.interactive()
