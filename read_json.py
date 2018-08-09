#!/usr/bin/python
# coding: utf-8

import sys

import getopt
import json

def usage():
	print "Usage : {0}".format(sys.argv[0])

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hvo:", ["help", "version", "output="])
	except getopt.GetoptError as err:
		print str(err)
		sys.exit(2)
	
	output = None
	
	for o, a in opts:
		if o == "-v":
			usage()
			sys.exit(0)
		elif o in ("-h", "--help"):
			usage()
			sys.exit(0)
		elif o in ("-o", "--output"):
			output = a
		else:
			assert False, "unknown option"
	
	ret = 0
	
	if output == None :
		print "no output option"
		ret += 1
	
	if ret != 0:
		sys.exit(1)
		
	fp_out = open(output, "w")
	
	for input in args:
		print "arg : " + input
		fp_in = open(input, "r")
		
		data = json.load(fp_in)
		print json.dumps(
			data,
			indent=4)
		
		print "hoge is " + data["hoge"]
		print "array[1] is " + data["array"][1]
		fp_in.close()
	
	fp_out.write("json test\n")
	
	fp_out.close()
	
if __name__ == "__main__":
	main()
