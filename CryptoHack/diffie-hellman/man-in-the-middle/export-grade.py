from pwn import *
import json
from math import log


con = remote('socket.cryptohack.org', 13379)

print(con.recv().decode())
print(con.recv().decode())

data = {}
# Downgrade to 64
supported = ["DH64"]
data['supported'] = supported
data = str(data).replace('\'', '"')
con.send(data)

print(con.recv().decode())
data = con.recv().decode().split('\n')[0]
print('data: ', data)
#data = {}
#data["chosen"] = "DH64"
#data = str(data).replace('\'', '"')
con.send(data)

print(con.recv().decode())
data = con.recv().decode().split('\n')
alice_data = json.loads(data[0])
p = int(alice_data['p'], 16)
print('p: ', p)
g = int(alice_data['g'], 16)
print('g: ', g)
A = int(alice_data['A'], 16)
print('alice data: ', alice_data)
begin_ind = data[1].find('{')
bob_data = json.loads(data[1][begin_ind:])
print('bob data: ', bob_data)
begin_ind = data[2].find('{')
alice_second_data = json.loads(data[2][begin_ind:])
print('alice data: ', alice_second_data)
