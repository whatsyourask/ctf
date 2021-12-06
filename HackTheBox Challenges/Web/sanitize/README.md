# sanitize

Completed: Yes
Platform: HackTheBox

The title of the web page says what to do with this challenge. It is a simple beginner-like SQL injection. `admin' --`. So, the query will be something like that: `select username, password from users where username = 'admin' -- and password = password;`. The rest after `—` will become a comment.