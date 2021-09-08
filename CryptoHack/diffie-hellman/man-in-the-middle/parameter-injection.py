from pwn import *
import json
import os

# Found the solution here: https://github.com/JesseEmond/matasano-cryptopals#set-5-diffie-hellman-and-friends

con = remote('socket.cryptohack.org', 13371)

# Intercept data from Alice
print(con.read().decode())
alice_data = con.read().decode()
closed = alice_data.find('}')
alice_data = alice_data[:closed + 1]
print(alice_data)
alice_data = json.loads(alice_data)
p = alice_data['p']
g = alice_data['g']

# Create wrong data for Bob from Alice
data = {}
data["p"] = p
data["g"] = g
# Replaced A with p which gives us the next case:
# Bob will calculate p ^ b mod p = 0 
data["A"] = p
data = str(data).replace('\'', '"')
print(data)
con.send(data.encode())

# Intercept data from Bob
print(con.recv().decode())
bob_data = con.recv().decode()
closed = bob_data.find('}')
bob_data = bob_data[:closed + 1]
print(bob_data)
bob_data = json.loads(bob_data)
B = bob_data['B']
data = {}
# Again replace B with p and the Alice will calculate: p ^ a mod p = 0
data["B"] = p
data = str(data).replace('\'', '"')
print(data)
con.send(data.encode())
print(con.recv())

flag = con.recv()
flag = json.loads(flag)
print(flag)
print("Shared secret: ", 0)
os.system(f'python3 decrypt.py 0 {flag["iv"]} {flag["encrypted_flag"]}')
