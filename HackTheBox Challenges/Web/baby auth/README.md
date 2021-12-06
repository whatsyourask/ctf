# baby auth

Completed: Yes
Platform: HackTheBox

Firstly, I tried to create a new user. After that and logging in, I received the message that I'm not an admin. Intercepted request with a burp and found there PHPSESSID cookie which is encoded string. Decoded URL and Base64 and got `{"username":"test"}` that's my username. I changed the test on admin and encoded it as it was before. Thus, this web app does authentication based on cookies, but it is not a secure way to implement authentication because the attacker can easily change the cookie.