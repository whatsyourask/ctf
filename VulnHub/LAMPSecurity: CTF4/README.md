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

* SquirrelMail 1.4.17. Exploit: Squirrelmail 1.4.x - 'Redirect.php' Local File Inclusion.

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

* user: jdurbin

#### whatweb

* PHP 5.1.6
```
PHP 5.1.6 - 'Chunk_Split()' Integer Overflow                                                                                                                                                      
PHP 5.1.6 - 'Imap_Mail_Compose()' Remote Buffer Overflow                                                                                                                                               
PHP 5.1.6 - 'Msg_Receive()' Memory Allocation Integer Overflow       
PHP 5.1.6 - Mb_Parse_Str Function Register_Globals Activation
```

#### dirb
 
## Thread modeling

## Vulnerability analysis

## Exploitation

## Post exploitation

