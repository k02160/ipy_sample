#!/usr/bin/python
# coding: utf-8

import sqlite3

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

database = 'test.db'

conn = sqlite3.connect(database)

sql = "DROP TABLE IF EXISTS test_table;"
conn.execute(sql)

sql = "CREATE TABLE test_table ( id INTEGER PRIMARY KEY AUTOINCREMENT, key VARCHAR(256), val VARCHAR(256));"
conn.execute(sql)

conn.commit()

insert_record(conn, 'hoge', 'foo')


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


reader = XmlReader.Create(PythonFileReader(open('sample.xml')))

while reader.Read():
	nodetype = reader.NodeType
	if nodetype == XmlNodeType.Element:
		name = reader.Name
		if name == "record":
			#print "tag is " + reader.Name
			doc = XElement.Load(reader.ReadSubtree())
			print doc.ToString()
			for node in doc.Descendants("key"):
				#print "key is " + node.Value
				key = node.Value
			for node in doc.Descendants("val"):
				#print "val is " + node.Value
				val = node.Value
			insert_record(conn, key, val)
			
	elif nodetype == XmlNodeType.Text:
		print reader.Value
	elif nodetype == XmlNodeType.EndElement:
		name = reader.Name
		if name == "record":
			#print "end of " + reader.Name
			pass

#	if reader.IsStartElement():
#		print reader.Name

conn.commit()

dump_records_name(conn)

conn.close()
