#!/usr/bin/python
# coding: utf-8

import sys
import platform

import getopt

import sqlite3
import json

implementation = platform.python_implementation()

if implementation != "IronPython":
	print 'This script runs only on IronPython'

import clr

clr.AddReference('System.Xml')
from System.Xml import XmlReader, XmlNodeType, XmlDocument

clr.AddReference('System.Xml.Linq')
from System.Xml.Linq import *

from System.IO import TextReader

class PythonFileReader(TextReader):
    def __init__(self, f):
        self.f = f
    def Read(self, buffer, index, count):
        chars = self.f.read(count).ToCharArray()
        chars.CopyTo(buffer, index)
        return len(chars)
        

def insert_record(conn, key, val):
	sql = 'INSERT INTO test_table VALUES ( NULL, ?, ? );'
	conn.execute(sql, [key, val])

def dump_records_array(conn):
	# 配列で取り出す
	sql = 'SELECT id, key, val FROM test_table';
	cur = conn.cursor()
	cur.execute(sql)
	for row in cur:
		print(str(row[0]) + ", " + row[1] + ", " + row[2])

def dump_records_name(conn):
	# column名で取り出す
	conn.row_factory = sqlite3.Row
	sql = 'SELECT id, key, val FROM test_table';
	cur = conn.cursor()
	cur.execute(sql)
	for row in cur:
		print(str(row["id"]) + ", " + row["key"] + ", " + row["val"])

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
	
	print "connect {0}".format(output)
	
	conn = sqlite3.connect(output)
	
	sql = "DROP TABLE IF EXISTS test_table;"
	conn.execute(sql)
	
	sql = "CREATE TABLE test_table ( id INTEGER PRIMARY KEY AUTOINCREMENT, key VARCHAR(256), val VARCHAR(256));"
	conn.execute(sql)
	
	conn.commit()
	
	insert_record(conn, 'hoge', 'foo')
	
	for input in args:
		print "read {0}".format(input)
		reader = XmlReader.Create(PythonFileReader(open(input)))
		
		while reader.Read():
			nodetype = reader.NodeType
			if nodetype == XmlNodeType.Element:
				name = reader.Name
				if name == "record":
					#print "tag is " + reader.Name
					doc = XElement.Load(reader.ReadSubtree())
					
					#print doc.ToString()
					
					# 複数の値を取り出すときは Descendantsを使う。
					#for node in doc.Descendants("key"):
					#	key = node.Value
					#for node in doc.Descendants("val"):
					#	val = node.Value
					
					# 値を1つ取り出すときはElementを使う。
					# convert utf-8 string to unicode
					key = unicode(doc.Element("key").Value, 'utf-8')
					val = unicode(doc.Element("val").Value, 'utf-8')

					
					print 'key is ' + key
					insert_record(conn, key, val)
					
			elif nodetype == XmlNodeType.Text:
				#print reader.Value
				pass
			elif nodetype == XmlNodeType.EndElement:
				name = reader.Name
				if name == "record":
					#print "end of " + reader.Name
					pass

		reader.Close()

	conn.commit()
	
	dump_records_name(conn)
	
	conn.close()


if __name__ == "__main__":
	main()
