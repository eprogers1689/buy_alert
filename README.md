# buy_alert
Buy Alert Report
```
This script takes a "buy alert", saves it to a SQLite database, and then produces an HTML report using Jinja2.

To run this script, 
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
  
  
  
  
  
