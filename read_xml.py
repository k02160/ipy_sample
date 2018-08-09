#!/usr/bin/python
# coding: utf-8

import sys

import getopt
import json

from pprint import pprint

import clr

clr.AddReference('System.Xml')
from System.Xml import XmlReader, XmlNodeType, XmlDocument

clr.AddReference('System.Xml.Linq')
from System.Xml.Linq import *

clr.AddReferenceToFile('Newtonsoft.Json.dll')
from Newtonsoft.Json import *

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
		data = fp_in.read()
		
		doc = XDocument().Parse(data)

		print doc.ToString().decode('utf-8')
		
		# get json string
		json_str = JsonConvert.SerializeXNode(doc, Formatting.Indented)

		# print json string
		print json_str.decode('utf-8')

		# convert json string to object
		json_dict = json.loads(json_str)
		
		pprint(json_dict)
		print "records -> record -> 1 -> key is " + json_dict['records']['record'][1]['key']
		fp_in.close()
		
	fp_out.write("xml test\n")
	
	fp_out.close()

if __name__ == "__main__":
	main()
