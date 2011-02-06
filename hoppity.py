#!/usr/bin/python
def get_num(s):
	import re
	m = re.match(r"\s*(\d+)\s*", s)
	return m.group()


def make_hops(num):
	output = open('result.txt', 'wa')

#for loop here

	output.close()

if __name__ == "__main__":
	import sys

	input = open(sys.argv[1])
	num = get_num(input.read())
	input.close()

	make_hops(num)
