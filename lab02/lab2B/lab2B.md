# Solution of lab2B

Just like in lab02C i did the buffer overflow and got the segmentation fault:

![segmentation fault](screenshots/seg_fault.png)

To see if there is a shell function I used `radare2 lab2B` and went through the disassembly, you also can use `objdump -d lab2B`.

![radare2](screenshots/radare2.png)

I tried to jump to shell function from return address but it didn't work:

![jump](screenshots/jump.png)

Then you need to pay attention and go through the shell disassembly. There is no defined string with "/bin/sh". Again i looked at radare analysys and found the string "/bin/sh":

![/bin/sh](screenshots/binsh.png)

Now, we need to push onto the stack our string "/bin/sh". I set a breakpoint where i can look at the stack.

![stack](screenshots/stack.png)

Here we see a piece of our As line. I'm going to `0x080486bd` because the old ebp needs to be pushed onto the stack to define `ebp + 0x8`. Then I thought that if I push onto the stack as a line after the address we are jumping to, maybe I can set ebp + 0x8 to the '/ bin / sh' line address.

![add As](screenshots/add_a.png)

I set ebp + 0x8 to 0x41414141:

![add As 2](screenshots/add_a2.png)

Add 0x080487d0:

![shell](screenshots/shell.png)
