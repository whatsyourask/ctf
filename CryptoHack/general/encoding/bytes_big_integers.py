from Crypto.Util.number import long_to_bytes


given_int = '11515195063862318899931685488813747395775516287289682636499965282714637259206269'
hex_int = long_to_bytes(given_int)
print(hex_int)
