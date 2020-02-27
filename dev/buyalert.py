import xlrd
import sqlite3
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askopenfilenames
from datetime import datetime
import os
import sys
import jinja2
import hashlib

desktop = os.path.join(os.path.join(os.environ['USERPROFILE']),'Desktop')

buy_alert_dev = os.path.join(desktop, "buy alert","dev")
buy_alert_reports = os.path.join(desktop, "buy alert","reports")
buy_alert_oldsheets = os.path.join(desktop, "buy alert","old buy alert sheets")
buy_alert_newsheets = os.path.join(desktop, "alertsheets")
md5_returned = ""

workbook_dirs = [] #list for holding all of the filenames in the alertsheets folder
newworkbod_dirs = [] #list for holding all of the new filenames for the buy alert sheets 

skip_to_report = False

for filename in os.listdir(buy_alert_newsheets):
	if filename.endswith(".xls"):
		workbook_dirs.append(os.path.join(buy_alert_newsheets,filename))

if len(workbook_dirs) > 1:
	print("Only run one sheet at a time. Remove any extra sheets from the 'alertsheets' folder and try again.")
	input("Press enter to exit...")
	sys.exit()

if len(workbook_dirs) < 1:
	print("No sheets found in the 'alertsheets' folder. Double check to make sure there is a buy alert sheet the folder.")
	do_report = ""
	while do_report is "":
		do_report = input("Would you like to run a report with existing data? Enter \"Y\" for YES or \"N\" for NO...: ").upper()
		print(do_report)
		if do_report == "N":
			sys.exit()
		elif do_report == "Y": 
			skip_to_report = True
			now = datetime.now()
			today = now.strftime("%Y-%m-%d") #save date as string
		else:
			do_report = ""


if not skip_to_report:
	#set date to user in the data base database
	today = ""
	while today is "":
		today = input("Enter a date for this buy alert sheet in the format: yyyy-mm-dd (e.g. 2020-01-01):")
		if len(today) != 10:
			print("\nSomething whent wrong, try again and make sure you use the format yyyy-mm-dd (e.g. 2020-01-01).")
			today = ""
		else:
			try:
				datetime.strptime(today,"%Y-%m-%d")
			except Exception as e:
				print("\nSomething whent wrong, try again and make sure you use the format yyyy-mm-dd (e.g. 2020-01-01).")
				today = ""


#open sqlite connection
conn = sqlite3.connect('db_dev')
c = conn.cursor()


if not skip_to_report:
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
				entry = (nextEntryId, itemNum, str(today))
				entries.append(entry)
				nextEntryId += 1

			c.executemany('INSERT INTO Entry VALUES (?,?,?)', entries)
			conn.commit()
		else:
			print("Skipping: " + workbook_dir)
		


#get report options
days = 0
while days == 0:
	days = input("How many days of history would you like to include in the report (enter a number, e.g. 30, 60, 90): ")
	try:
		days = int(days) #convert to int to ensure the query will work
	except:
		print("Give a number...")
		days = 0

days = days + 1 # adding a full day and converting back to string to account for the sql query



#query db for report
query = '''
	SELECT ItemNum, COUNT(*)
	FROM Entry
	GROUP BY ItemNum
	HAVING COUNT(*) > 1
	ORDER BY COUNT(*) DESC
'''
c.execute('SELECT ItemNum, COUNT(*) FROM Entry WHERE (SELECT julianday() - julianday(date) <= ?) GROUP BY ItemNum HAVING COUNT(*) > 1 ORDER BY COUNT(*) DESC', [days])
itemsToReport = c.fetchall()

if len(itemsToReport) > 0:

	collections = []

	hitCount = itemsToReport[0][1]


	while hitCount >= 2:
		itemCounter = 0
		collection = {'frequency' : hitCount,
					'itemCount' : 0,
					'items' : []}
		for item in itemsToReport:
			if item[1] == hitCount:
				itemCounter += 1
				c.execute('SELECT Desc1, Desc2, MF, PD, VN FROM Item WHERE(ItemNum=?)',[item[0]])
				itemData = c.fetchone()
				itemDict = {
					'itemNum' : item[0],
					'desc1' : itemData[0],
					'desc2' : itemData[1],
					'mf'    : itemData[2],
					'pd'    : itemData[3],
					'vn'    : itemData[4],
					'dates' : [],
				}
				c.execute('SELECT Date FROM Entry WHERE(ItemNum=?) AND (julianday() - julianday(date)) <= ?',[item[0], days])
				dates = c.fetchall()
				for date in dates:
					itemDict['dates'].append(date[0])
				collection['items'].append(itemDict)
		collections.append(collection)
		collection['itemCount'] = itemCounter
		hitCount -= 1


	#create report
	templateLoader = jinja2.FileSystemLoader(searchpath="./")
	templateEnv = jinja2.Environment(loader=templateLoader)
	TEMPLATE_FILE = "htmltemplate2.html"
	template = templateEnv.get_template(TEMPLATE_FILE) 


	days = days - 1
	outputText = template.render(collections=collections,today=today,days=days)

	html_output = open(buy_alert_reports + '/BUY ALERT ' + today + '.html', 'w')
	html_output.write(outputText)
	html_output.close()
else:
	print('\nAll data from the BUY ALERT sheet was saved to the database.')
	print('\nThere is nothing to report at this time.')
	print('\nIf you want to see a report, rerun the program and increase the number of days to serach for.')
	input('\nPress enter to move OLD BUY alert sheets to archive folder...')
	print('Goodbye')

#close database connection
conn.close()

#move worksheets to 
for filename in os.listdir(buy_alert_newsheets):
	if filename.endswith(".xls"):
		new_filename = "Old Buy Alert - " + today + " - (" + str(md5_returned) + ").xls"
		print(filename)
		os.rename(os.path.join(buy_alert_newsheets,filename), os.path.join(buy_alert_oldsheets, new_filename))
