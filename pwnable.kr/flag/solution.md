Firstly, `strings -n 8 flag` gives a result with 'UPX service'.
Secondly, `upx -d flag` and we now got the normal executable file.
Thirdly, some sort of debugging: set a breakpoint in the end of the main function, then try to read the address of flag and you'll get it.
