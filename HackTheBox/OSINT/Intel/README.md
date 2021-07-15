# Intel

Completed: Yes
Platform: HackTheBox

Searching in google for `flinchsec`.

Found this account: [https://www.linkedin.com/in/ractor-burton-5179771b9/](https://www.linkedin.com/in/ractor-burton-5179771b9/). 

Another account if you will search `ractor-burton-5179771b9` : [https://www.linkedin.com/in/johnny-dorfmeister-1135a6179](https://www.linkedin.com/in/johnny-dorfmeister-1135a6179).

In contact info of second account found out about his twitter account: [https://twitter.com/johnnydorfmeis1](https://twitter.com/johnnydorfmeis1).

> Webdeveloper / owner of [http://howitshould.be](http://howitshould.be/)

On this site, we see a small link `Auth`. Page source: `<!-- Authentication script by Johnny Dorfmeister. [https://github.com/JohnnyDorfmeister/authentication-requests](https://github.com/JohnnyDorfmeister/authentication-requests) !-->`.

Code:

```bash
<html>
<body>
<title>Auth</title>
<?php
if(!isset($_POST['username']))
{
	die("Eat shit and die...");
}
if($_POST['username'] == "johnny" && $_POST['password'] == removed for security reasons)
{
	$_SESSION["loggedin"] = "true";
	include("flag.php");
	die();
}else{
	echo "<form method=\"POST\" action=\"" . $_SERVER['PHP_SELF'] . "\">\n";
	echo "<table align=\"center\">\n";
	echo "	<tr><td>Username:&nbsp;<td><input type=\"text\" name=\"username\"></tr>\n";
	echo "	<tr><td>Password:&nbsp;<td><input type=\"password\" name=\"password\"></tr>\n";
	echo "	<tr><td colspan=2 align=\"right\"><input type=\"submit\" name=\"submit\" value=\"log in\"></tr>\n";
	echo "</table>\n";
	echo "</form>\n";
	die();
}
?>
</body>
</html>
```

Use git and see other commits:

```bash
<html>
<body>
<title>Auth</title>
<?php
if(!isset($_POST['username']))
{
	die("Eat shit and die...");
}
if($_POST['username'] == "johnny" && $_POST['password'] == "letmein")
{
	$_SESSION["loggedin"] = "true";
	include("flag.php");
	die();
}else{
	echo "<form method=\"POST\" action=\"http://authentication.howitshould.be/auth.php\">\n";
	echo "<table align=\"center\">\n";
	echo "	<tr><td>Username:&nbsp;<td><input type=\"text\" name=\"username\"></tr>\n";
	echo "	<tr><td>Password:&nbsp;<td><input type=\"password\" name=\"password\"></tr>\n";
	echo "	<tr><td colspan=2 align=\"right\"><input type=\"submit\" name=\"submit\" value=\"log in\"></tr>\n";
	echo "</table>\n";
	echo "</form>\n";
	die();
}
?>
</body>
</html>
```

Using python to send post request:

```python
$ python3
Python 3.8.10 (default, Jun  2 2021, 10:49:15) 
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import requests
>>> data = {}
>>> data['username']='johnny'
>>> data['password']='letmein'
>>> res = requests.post('http://authentication.howitshould.be/auth.php', data=data)
>>> 
>>> print(res.text)
<html>
<body>
<title>Auth</title>
<!-- Authentication script by Johnny Dorfmeister. https://github.com/JohnnyDorfmeister/authentication-requests !-->
congratulations, the flag is g1ttern00b
>>>
```

But this flag is wrong.

Found WordPress: [http://www.howitshould.be/wp-login.php?redirect_to=http%3A%2F%2Fwww.howitshould.be%2Fwp-admin%2F&reauth=1](http://www.howitshould.be/wp-login.php?redirect_to=http%3A%2F%2Fwww.howitshould.be%2Fwp-admin%2F&reauth=1).

Return to Twitter and go to this URL: [https://twitter.com/johnnydorfmeis1/status/1084935200352727046](https://twitter.com/johnnydorfmeis1/status/1084935200352727046).

 There is some zip archive. Within zip-archive endless drozen.zip archive, so, just do the strings and get ([tykje.com/quine.zip](http://tykje.com/quine.zip)). In this link Chinese message: 当前地址疑似下载文件,已被系统自动禁止,如是误报,请联系客服!. Go to google translator: `The current address seems to be downloading files, and it has been automatically prohibited by the system. If it is a false report, please contact customer service!.` It seems the wrong way. Let's return to the start point.

Found in contact this site: [http://w3h3lpp3opl3.tk/](http://w3h3lpp3opl3.tk/).

 The site is no longer available. Johnny said something about copying and archiving the site... Let's search in [https://web.archive.org/web/*/http://w3h3lpp3opl3.tk/](https://web.archive.org/web/*/http://w3h3lpp3opl3.tk/). This site found 2 pages: [https://web.archive.org/web/20201030104512/http://w3h3lpp3opl3.tk/](https://web.archive.org/web/20201030104512/http://w3h3lpp3opl3.tk/).

Okay, they have another Github: [https://github.com/8e9c9259882e7e768160672f019971b1](https://www.notion.so/8e9c9259882e7e768160672f019971b1).

 In repo nothing interesting except tags where we can see archives and exe file. Took exe file. Strings didn't show me a new hint. It is malware: [https://www.virustotal.com/gui/file/e2d6bb50f10f5f108a4f9883e76cc970fc904e8c19d3bdaf410c8be68f9ade3c/details](https://www.virustotal.com/gui/file/e2d6bb50f10f5f108a4f9883e76cc970fc904e8c19d3bdaf410c8be68f9ade3c/details). In details, you can find the flag:

```python
normalbinary.exe
    HTB{051N7_F0R_M3}.exe
```