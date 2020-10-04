#!/usr/bin/env python3


def luhn_algorithm(number, sum_digit, count):
    for i in range(count):
        temp = int(number[i])
        if not i % 2:
            temp *= 2
            if temp > 9:
                temp = 1 + temp % 10
        sum_digit += temp
    return not sum_digit % 10


card_begin = '543210'
card_end   = '1234'
number     = 123457
count      = 6
sum_digit  = 29
for i in range(0, 1000000):
    s    = str(i)
    s    = '0' * (count - len(s)) + s
    card = card_begin + s + card_end
    res  = luhn_algorithm(list(s), sum_digit, count)
    if res and not int(card) % number:
        print(card)
