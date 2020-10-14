Just like in lab02C i did the buffer overflow and got the segmentation fault:

![segmentation fault](screenshots/seg_fault.png)

To see if there is a wrapper function I used `radare2 lab2B` and just went through the disassembly, you also can use `objdump -d lab2B`.

![radare2](screenshots/radare2.png)

I just tried to jump to shell function from return address but it didn't work:

![jump](screenshots/jump.png)

Then you need to pay attention and go through the shell disassembly. There is no defined string with "/bin/sh". Again i looked at radare analysys and found the string "/bin/sh":

![/bin/sh](screenshots/binsh.png)
