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

In order to ensure that the dates recoded are accurate, the user will have to run the script once a day. All the user has to do is download the alert sheet to the right folder and run the script. 

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
  
  
  
  
  
