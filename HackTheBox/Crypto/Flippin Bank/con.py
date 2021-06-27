import socket
import sys
import binascii


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('188.166.169.77', 32441))
print(s.recv(4096).decode())
s.send(b'admin')
print(s.recv(4096).decode())
last_chr = b'x'
s.send(b'g0ld3n_b0' + last_chr)
print(s.recv(4096).decode())
leak = s.recv(4096).decode().split('\n')[0][19:]
print(leak)
leak3 = binascii.unhexlify(leak)
print(leak3)
s.close()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('188.166.169.77', 32441))
print(s.recv(4096).decode())
s.send(b'admin')
print(s.recv(4096).decode())
last_chr = b'z'
s.send(b'g0ld3n_b0' + last_chr)
print(s.recv(4096).decode())
leak = s.recv(4096).decode().split('\n')[0][19:]
print(leak)
leak2 = binascii.unhexlify(leak)
print(leak2)
for i in range(len(leak)):
    if leak2[i] != leak3[i]:
        print(i)
        break
s.close()
