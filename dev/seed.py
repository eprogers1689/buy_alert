import xlrd
import sqlite3
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askopenfilenames
import datetime
import os
import sys
import jinja2
import hashlib
import random

def get_random_date():
	month = round(random.random() * 11 ) + 1
	day = round(random.random() * 29 ) + 1
	if month <= 2 and day <= 14:
		year = 2020
	else:
		year = 2019
	return str(year) + "-" + str(month) + "-" + str(day)

#set NOW for recording date to database
now = datetime.datetime.now()
today = now.strftime("%Y-%m-%d") #save date as string

#open sqlite connection
conn = sqlite3.connect('db_dev')
c = conn.cursor()


#drop tables and make new tables
c.execute('''
	DROP TABLE IF EXISTS Entry
''')

c.execute('''
	CREATE TABLE Entry (
	ID int NOT NULL PRIMARY KEY,
	ItemNum VARCHAR(255) NOT NULL,
	Date VARCHAR(20) NOT NULL,
	FOREIGN KEY (ItemNum) REFERENCES Item(Itemnum)
)''')

c.execute('''
	DROP TABLE IF EXISTS Item
''')

c.execute('''
	CREATE TABLE Item (
	ItemNum VARCHAR(255) NOT NULL PRIMARY KEY,
	PD CHARACTER(20),
	MF CHARACTER(20),
	VN CHARACTER(20),
	DESC1 VARCHAR(255) NOT NULL,
	DESC2 VARCHAR(255)
)''')

c.execute('''
	DROP TABLE IF EXISTS Hash
''')

c.execute('''
	CREATE TABLE Hash (
	ID int NOT NULL PRIMARY KEY,
	HASH VARCHAR(255) NOT NULL,
	Date VARCHAR(20) NOT NULL
	)
''')



#pick a workbook
Tk().withdraw()
workbook_dirs = askopenfilenames(defaultextension=".xlsx", filetypes=[('BUYALERT','*.xls')]) #returns tuple of file names

for x in range(1,10):
	print("loop #", x)
	for workbook_dir in workbook_dirs:
		#check md5 check sum to see if this file has been imported yet
		with open(workbook_dir, 'rb') as file_to_check:
		    # read contents of the file
		    data = file_to_check.read()    
		    # pipe contents of the file through
		    md5_returned = hashlib.md5(data).hexdigest()


		# get max entry id
		c.execute('''SELECT MAX(ID) FROM hash''')
		nextHashId = c.fetchone()[0]
		if nextHashId is None:
			nextHashId = 1
		else:
			nextHashId += 1

		c.execute('SELECT hash FROM hash WHERE(hash=?)',[md5_returned])
		returnedHash = c.fetchone()
		if returnedHash is None or returnedHash[0] != md5_returned:
			print("Adding: " + workbook_dir)
			newHashEntry = (nextHashId, md5_returned, today)
			c.execute('INSERT INTO hash VALUES(?,?,?)', newHashEntry)
			conn.commit()
		#get read workbook and count rows
		workbook = xlrd.open_workbook(workbook_dir)
		worksheet = workbook.sheet_by_index(0)
		num_rows = worksheet.nrows

		#get max entry id
		c.execute('''SELECT MAX(ID) FROM Entry''')
		nextEntryId = c.fetchone()[0]
		if nextEntryId is None:
			nextEntryId = 1
		else:
			nextEntryId += 1

		#loop through sheet - add new items, record all entries
		entries = []

		for i in range(1, num_rows):
			pd = worksheet.cell_value(i,1)
			mf = worksheet.cell_value(i,0)
			vn = worksheet.cell_value(i,2)
			itemNum = worksheet.cell_value(i,3)
			desc1 = worksheet.cell_value(i,4)
			desc2 = worksheet.cell_value(i,5)


			# Check if Item Already in Database
			c.execute('SELECT * FROM Item WHERE(ItemNum=?)', [itemNum])
			if c.fetchone() == None:
				newItem = (itemNum, pd, mf, vn, desc1, desc2)
				c.execute('INSERT INTO Item VALUES (?,?,?,?,?,?)', newItem)
				conn.commit()


			# record entries
			entry = (nextEntryId, itemNum, get_random_date())
			entries.append(entry)
			nextEntryId += 1

		c.executemany('INSERT INTO Entry VALUES (?,?,?)', entries)
		conn.commit()