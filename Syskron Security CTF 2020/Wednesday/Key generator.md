Download the binary, set the x bit and then:

~~~
root@kali:~/Downloads# ltrace ./keygen                                                                                                    = 83
printf("Enter machine number (e.g. B9999"...)                                                                                                    = 37
__isoc99_scanf(0x55555555644e, 0x7fffffffe770, 0, 0Enter machine number (e.g. B999999): AAAAAAAAAAAAA
)                                                                                             = 1
strlen("AAAAAAA")                                                                                                                                = 7
strlen("!!aksal")                                                                                                                                = 7
strcmp("AAAAAAA", "laska!!")                                                                                                                     = -43
printf("Key for %s: ", "AAAAAAA")                                                                                                                = 17
puts("\nDO NOT SHARE!!!!"Key for AAAAAAA: 59606162636465
DO NOT SHARE!!!!
)                                                                                                                       = 18
+++ exited (status 0) +++
~~~

`strcmp("AAAAAAA", "laska!!")` that is interesting.

Try to input `laska!!`:

~~~
root@kali:~/Downloads# ./keygen
/********************************************************************************
* Copyright (C) BB Industry a.s. - All Rights Reserved
* Unauthorized copying of this file, via any medium is strictly prohibited
* Proprietary and confidential
* Written by Marie Tesařová <m.tesarova@bb-industry.cz>, April 2011
********************************************************************************/

Enter machine number (e.g. B999999): laska!!
1639171916391539162915791569103912491069173967911091119123955915191639156967955916396391439125916296395591439609104911191169719175
You are not done yet! ಠ‿ಠ
~~~

It was strange output for me. Moreover, I decided to reverse it with Hopper or radare2 or just gdb. But it didn't give a result, cause this output was placed in binary, not generated.

In the end, I realized that it was octal with '9' as separator between characters.

Python helped me with nines deleting: `s.replace('9', ' ', s.count('9'))`. Then google a random translator and got the flag: syskronCTF{7HIS-isn7-s3cUr3-c0DIN9}
