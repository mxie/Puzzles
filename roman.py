#!/usr/bin/python
import sys

base_roman = { 1:"I", 5:"V", 10:"X", 50:"L", 100:"C", 500:"D", 1000:"M" }
special_roman = { 4:"IV", 9:"IX", 40:"XL", 90:"XC", 400:"CD", 900:"CM" }

def get_roman(num):
    result = []
    num = num[::-1]         # reverse the digits
    for i in range(len(num)):
        place = 10 ** i     # initially ones place, then tens, etc.
        actual_num = int(num[i]) * place
        if actual_num in base_roman:        # 1, 5, 10, 50, ...
            result.append(base_roman[actual_num])
        elif actual_num in special_roman:   # 4, 9, 40, ...
            result.append(special_roman[actual_num])
        else:                               # any other number
            result.append(parse_num(actual_num, place))
    # join the roman rep of each digit in reverse order of the list
    return ''.join(result[::-1])

def parse_num(num, place):
    four_mult = 4*place
    five_mult = 5*place
    n = num if num < four_mult else num-five_mult
    # start off with the roman rep of the five multiple if greater
    result = '' if num < four_mult else base_roman[five_mult] 
    while n > 0:
        result += base_roman[place]
        n -= place
    return result

def main():
    if (sys.argv):
        number = sys.argv[1]
        print get_roman(number)

if __name__ == "__main__":
    main()
