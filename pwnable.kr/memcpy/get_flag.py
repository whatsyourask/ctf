"""
Here we need to pass all speed checks to get flag.
So i went to gdb and got an error in fast_copy in assembly part.
Then i googled the instruction with error and got information that this instruction works with 16 bytes.
But in heap memory we don't have a 16 bytes. You just need to identify it. I did bruteforce.
We had a complete flag with diff 4+
"""
from pwn import *


def get_flag():
    # bruteforce of difference between the size of heap memory chunk and memory size from input
    for diff in range(0, 9):
        send_sizes(diff)


def send_sizes(diff): 
    # Connect to the server
    con = remote('pwnable.kr', 9022)
    # Create a sizes with diff
    # from 16 to 8192
    sizes = ' '.join([str(2 ** i - diff) for i in range(4, 14)])
    con.sendline(sizes)
    print(con.recvall().decode('utf-8'))


if __name__=='__main__':
    get_flag()
