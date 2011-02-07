#!/usr/bin/python
def get_num(s):
	import re
	m = re.match(r"\s*(\d+)\s*", s)
	return int(m.group())


def make_hops(num):
	output = open('result.txt', 'wa')

	for i in range(1, num+1):
		s = ""
		if (not ((i%3) or (i%5))):
			s += "Hop\n"
		elif (i%3 == 0):
			s += "Hoppity\n"
		elif (i%5 == 0):
			s += "Hophop\n"
		
		output.write(s)

	output.close()

if __name__ == "__main__":
	import sys

#TODO: add arg check

	input = open(sys.argv[1])
	num = get_num(input.read())
	input.close()

	make_hops(num)
