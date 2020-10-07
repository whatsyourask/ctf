![description](screenshots/description)

From the description we see that we need to write a shellcode.

[writing](shellcode/writing.md)

The shellcode is ready and we see that we have enough space for it(shellcode has a 38 bytes length).

![enough](shellcode/enough.png)

NOP(no operation) chain

+

38 bytes

+

4 bytes address of that shellcode in the stack

There are 8x8 bytes or 64 bytes. So we have next payload:
`"\x90" * 22 + shellcode + [address]`

It remains for us to find out the current address in the stack of our NOP chain

[exploit](exploit.py)
