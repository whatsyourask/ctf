import telnetlib


tn = telnetlib.Telnet('socket.cryptohack.org', 11112)
tn.write(b'{"buy":"flag"}')
print(tn.read_all())
