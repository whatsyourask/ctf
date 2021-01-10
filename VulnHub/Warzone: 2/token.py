import hashlib

username = open('creds/1337_username.txt', 'r').read()[:-1]
password = open('creds/1337_password.txt', 'r').read()[:-1]
user_pass_upper = username.encode('utf-8') + password.encode('utf-8')
upper_token = hashlib.sha256(user_pass_upper).hexdigest()
print(user_pass_upper, upper_token)
user_pass_lower = username.lower().encode('utf-8') + password.lower().encode('utf-8')
lower_token = hashlib.sha256(user_pass_lower).hexdigest()
print(user_pass_lower, lower_token)

