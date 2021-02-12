# LAMPSecurity: CTF4

[Machine](https://www.vulnhub.com/entry/lampsecurity-ctf4,83/ "https://www.vulnhub.com/entry/lampsecurity-ctf4,83/")

## Reconnaissance

### nmap

* ssh
* smtp
* http
* ipp(closed)

### Vulnerable versions

* [ ] ssh

* [x] smtp - Sendmail 8.13.5 - Remote Signal Handling (PoC)

* [ ] http

### http

#### robots.txt

```
User-agent: *
Disallow: /mail/
Disallow: /restricted/
Disallow: /conf/
Disallow: /sql/
Disallow: /admin/
```

#### /mail/

* Log in form.

* SquirrelMail 1.4.17. 

#### /restricted/

* Server authentication window.

#### /conf/

* Internal Server Error.

#### /sql/

* File `db.sql` with queries.

#### /admin/

* Log in form.

#### /calendar/

* Real calendar.

* Log in button.

#### /usage/

* Statistics.

* Webalizer version 2.01 - nothing.

#### /index.html?page=blog&title=Blog

* user: `jdurbin`

#### whatweb

* PHP 5.1.6
```
PHP 5.1.6 - 'Chunk_Split()' Integer Overflow                                                                                                                                                      
PHP 5.1.6 - 'Imap_Mail_Compose()' Remote Buffer Overflow                                                                                                                                               
PHP 5.1.6 - 'Msg_Receive()' Memory Allocation Integer Overflow       
PHP 5.1.6 - Mb_Parse_Str Function Register_Globals Activation
```

#### dirb
 
* http://192.168.88.222/mail/configure - some sh script.

* http://192.168.88.222/admin/inc/blog.php - form with sql error disclosure.

* http://192.168.88.222/mail/contrib/decrypt_headers.php - form with key and string.

### smtp

#### smtp-commands nmap script

`nmap -p25 --script smtp-commands -oA commands 192.168.88.222` - gives nothing.

#### smtp-enum-users nmap script

`nmap --script smtp-enum-users 192.168.88.222` - gives the result that VRFY and EXPN methods is not working.

#### Grab banner

`nc -vn 192.168.88.222 25`. Then `HELO x` and it shows the domain `ctf4.sas.upenn.edu`.

## Thread modeling

1. Exploit: `Squirrelmail 1.4.x - 'Redirect.php' Local File Inclusion.`

2. Exploit: `Sendmail 8.13.5 - Remote Signal Handling (PoC)`

3. Try SQLi at `/admin/inc/blog.php`

4. Examine /mail/contrib/decrypt_headers.php

5. Brute-force admin panels and ssh.

## Vulnerability analysis

1. Local File Inclusion with `src/redirect.php?plugins[]=../../../../etc/passwd%00` doesn't work.

2. PoC exploit seems doesn't work too.

3.  

## Exploitation

## Post exploitation

