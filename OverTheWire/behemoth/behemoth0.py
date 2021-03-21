from pwn import *

'''
Just did ltrace on the binary and saw the password within strcmp call
'''
con = ssh('behemoth0', 'behemoth.labs.overthewire.org', password='behemoth0', port=2221)
p = con.process('/behemoth/behemoth0')
p.sendline('eatmyshorts')
p.recv()
p.recv()
p.sendline('cat /etc/behemoth_pass/behemoth1')
p.recv()
print(p.recv())
