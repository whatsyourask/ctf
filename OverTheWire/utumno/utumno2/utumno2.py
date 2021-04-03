from pwn import *


con = ssh('utumno2', 'utumno.labs.overthewire.org', password='ceewaceiph', port=2227)
p = con.process(executable='/utumno/utumno2', argv=[], env={"": "", "": "", "": "", "": "", "": "", "": "", "":"", "": "", "": "", "":""})
gdb.attach(p, "b *main")
