# buy_alert

## Buy Alert Report

This script takes a "buy alert" sheet, saves it to a SQLite database, and then produces an elegant HTML report using Jinja2.

The "buy alert" sheet is a daily report of items that had a qty of zero at the end of the previous business day. This script saves the buy alert sheets to a little database. The database has three tables:

```
  ITEM - for recording item numbers, Manufacturer/Prodct/Vendor codes from our system
  ENTRY - for recording the dates on which an item number appeard on a buy alert sheet.
  HASH - records and md5 hash of each file entered to make sure a file is not added more than once.
```

When the script is run it loops through all of the buy alert sheets the 'alertsheets' folder on the users desktop. As it loops through it creates a HASH of the file and checks that against the HASH table to ensure that files are never run more than once (which would skew the data). If a file as not been run before items are added to the ITEM table as needed and an ENTRY for that Item is added to the entry table. 

In order to ensure that the dates recoded in the ENTRY are accurate, the user will have to run the script once a day. All the user has to do is download the alert sheet, move it to the alertsheets folder and run the script. 

The script prompts the user for how many days of history they would like to include in the report. The script then performs some sql queries and pulls out all of the items that have appeared on the buy alert sheets more than once. The items are grouped by frequency (or "HITS", as they are called on the report). The report then shows each items Description, Manufacturer/Prodct/Vendor codes (two letter codes like "NB CF SM", Item number, and then a list of all of the dates on which the item appeared ona buy alert sheet.

At the top of the report, is are a series of filters that can help the user view items containing certain text or MPV codes or both.

The report is generated using jinja2. I used bootstrap for stying and jquery to add some functionality. Check it out!



## Sample
To view a sample report, checkout the reports folder. 


## Setup
```
  1.) Make sure Python, Sqlite3, and all the required libraries are installed (e.g. use pip install xlrd and pip install jinja2).
  2.) In order for the script to work you need folders on your desktop like this:
    Desktop
     ├── Alertsheets
     |   ├── example alert sheet1.xls
     |   ├── example alert sheet2.xls
     |   ├── example alert sheet3.xls
     |   └── example alert sheet4.xls
     └── Buy Alert
         ├── Dev
         |   ├── buyalert.py
         |   ├── db_dev
         |   ├── htmltemplate2.html
         |   └── seed.py
         ├── Old Buy Alert Sheets
         |   ├── example alert sheet1.xls
         |   ├── example alert sheet2.xls
         |   ├── example alert sheet3.xls
         |   └── example alert sheet4.xls
         ├── Reports   
         |   ├── example alert report1.html
         |   ├── example alert report1.html
         |   ├── example alert report1.html
         |   └── example alert report1.html
         └── Buy_Env (only use this if you want to have a virtual env)
  3.) Place buy alert sheet(s) in Alersheets folder on desktop and then run buyalert.py
  4.) Check Desktop/Buy Alert/Reports for an HTML report.
 
```
There is also a handy seed script I used during development for troubleshooting. In order to use this you need to have TKINTER installed (pip install tkinter). Run the script, and navigate to the folder that has 'buy alert' sheets in it, and include as many as you want. I ususally do about 10 or so. The script will use the items in the sheets to seed the ITEM, ENTRY, and HASH tables. It also loops through all of the items on the sheets 10 times and creates random dates between Feb 2019 and Feb 2020.
  
  
  
  
