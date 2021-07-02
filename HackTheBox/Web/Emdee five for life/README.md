# Emdee five for life

Completed: Yes
Date: July 2, 2021 → July 2, 2021
Platform: HackTheBox

You need to encrypt the given string fast. Simple `going to the md5 online encryption site` will not work. You need a script. I made one in python:

1. send HTTP GET request and receive a result.
2. parse the result and extract the string that you need to encrypt.
3. encrypt the string with md5.
4. send HTTP POST request to the server with a specified body.

To see what the body looks like you can intercept the post request in the burp suite.