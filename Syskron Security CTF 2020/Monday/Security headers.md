Go to the www.senork.de with Burpsuite and enabled cert for https.

Response:

~~~
HTTP/1.1 304 Not Modified
Server: nginx
Date: Sat, 24 Oct 2020 14:47:01 GMT
Last-Modified: Thu, 01 Oct 2020 05:23:33 GMT
Connection: close
ETag: "5f7567d5-1774"
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=31536000; includeSubdomains; preload
Feature-Policy: fullscreen 'self'
Referrer-Policy: no-referrer
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Flag-Policy: syskronCTF{y0u-f0und-a-header-flag}
Content-Security-Policy: default-src 'none'; img-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'; font-src 'self'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'; manifest-src 'self'
~~~
