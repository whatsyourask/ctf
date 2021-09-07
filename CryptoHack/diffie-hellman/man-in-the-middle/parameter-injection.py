from pwn import *
import json


con = remote('socket.cryptohack.org', 13371)
print(con.read().decode())
alice_data = con.read().decode()
closed = alice_data.find('}')
alice_data = alice_data[:closed + 1]
print(alice_data)
alice_data = json.loads(alice_data)
p = alice_data['p']
g = alice_data['g']
A = alice_data['A']

data = {}
data["p"] = p
data["g"] = g
int_a = int(A, 16) // 2
int_g = int(g, 16)
int_p = int(p, 16)
new_A = pow(int_g, int_a, int_p)
data["A"] = hex(new_A)
data = str(data).replace('\'', '"')
print(data)
con.send(data.encode())

print(con.recv().decode())
bob_data = con.recv().decode()
closed = bob_data.find('}')
bob_data = bob_data[:closed + 1]
print(bob_data)
bob_data = json.loads(bob_data)
B = bob_data['B']
int_b = int(B, 16) // 2
new_b = pow(int_g, int_b, int_p)
data = {}
data["B"] = hex(int_b)
data = str(data).replace('\'', '"')
print(data)
con.send(data.encode())
print(con.recv())
print(con.recv())
print("Shared secret: ", pow(int(B, 16), int_a, int_p))
