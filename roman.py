#!/usr/bin/python
import sys

roman_nums = dict({ "1":"I", "5":"V", "10":"X", "50":"L", "100":"C", "500":"D", "1000":"M" })
spec_nums = dict({ "4":"IV", "9":"IX", "40":"XL", "90":"XC", "400":"CD", "900":"CM" })

def get_roman(num):
    result = []
    place = 1;
    num = num[::-1]
    for i in num:
        i_num = int(i)
        actual = str(i_num*place)
        if (i in roman_nums):
            result.append(roman_nums[actual])
        elif (i in spec_nums):
            result.append(spec_nums[actual])
        else:
            result.append(parse_num(i, place))
        place *= 10
        num.replace(i, '', 1)
    
    return ''.join(result[::-1])

def parse_num(num, place):
    i = int(num)
    n = i if (i < 4) else i-5
    result = '' if (i < 4) else roman_nums["5"] 
    while (n > 0):
        result += roman_nums[str(place)]
        n -= 1

    return result

def main():
    if (sys.argv):
        number = sys.argv[1]
        print get_roman(number)

if __name__ == "__main__":
    main()
