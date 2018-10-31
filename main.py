import os
import sys
import sqlite3 as sql
from datetime import datetime, date, time

# Make sqlite3 database connection
conn = sql.connect('reminder_db.db')
cursor = conn.cursor()

# Reminder ASCII Art for style
header = """
 ___           _         _         
| _ \___ _ __ (_)_ _  __| |___ _ _ 
|   / -_) '  \| | ' \/ _` / -_) '_|
|_|_\___|_|_|_|_|_||_\__,_\___|_|"""

# If a table is exists then drop and make a fresh one
def create_table():
	cursor.executescript("""
        DROP TABLE IF EXISTS reminder;
		CREATE TABLE reminder (
    	id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    	title    TEXT,
		create_date TEXT,
		remind_date TEXt);
		""")

# Function for insert reminds to the database 
def insert_remind(rem_name, rem_create_date, rem_date):
	cursor.execute('''INSERT OR IGNORE INTO reminder (
		title, create_date, remind_date) 
        VALUES ( ?, ?, ? )''', ( rem_name, rem_create_date, rem_date)) 
	conn.commit()
	

# Reminder creation function like get date and content
def create_reminder():
	os.system('clear')
	current_year = datetime.now().year
	
	remind_content = input('What you want to remind? ')
	remind_year = input("Which year you get remind (eg: > "+str(current_year)+")? ")
	if int(remind_year) < current_year:
		input("This is not valid because the year less current year...! [Press ENTER]")
		create_reminder()
	remind_month = input('Which month you get remind (eg: 6)? ')
	remind_day = input('Which day you get remind (eg: 29)? ')
	remind_hour = input('Which hour you get remind (eg: 12)? ')
	remind_mind = input('Which minute you get remind (eg: 10)? ')

	# get full date like year, month, day
	full_date = date(int(remind_year), int(remind_month), int(remind_day))
	# get the full time like hour and minutes
	full_time = time(int(remind_hour), int(remind_mind))
	# combined date and time 
	combined_date = datetime.combine(full_date, full_time)
	
	insert_remind(remind_content, datetime.now(), combined_date)

# View the reminders as full and specific view
def view_remind(rec=0):
	if rec == 0:
		os.system('clear')
		cursor.execute("SELECT *FROM reminder")
		data = cursor.fetchall()
		print("{} {} {} {} ".format("|id|", "|title|", "|created date|", "|remind date|"))
		print("{} {} {} {} ".format("-"*4, "-"*7, "-"*14, "-"*13))
		for item in data:
			print("{0:3} {1:10} {2:11} {3:3} ".format(str(item[0]), item[1], item[2], item[3]))
	else:
		os.system('clear')
		cursor.execute("SELECT *FROM reminder WHERE id = ?", (rec, ))
		data = cursor.fetchall()
		print("{} {} {} {} ".format("|id|", "|title|", "|created date|", "|remind date|"))
		print("{} {} {} {} ".format("-"*4, "-"*7, "-"*14, "-"*13))
		for item in data:
			print("{} {} {} {} ".format(item[0], item[1], item[2], item[3]))

# Update the already exists reminders
def update_reminder():
	#os.system('clear')
	current_year = datetime.now().year
	task_id = input("What is the task ID? ")
	view_remind(task_id)
	print("\n{0:~^20s}".format("Update section"))

	remind_content = input('What you want to remind? ')
	remind_year = input('Which year you get remind (2018)? ')
	if int(remind_year) < current_year:
		input("This is not valid because the year less current year...! [Press ENTER]")
		update_reminder()
	remind_month = input('Which month you get remind (eg: 6)? ')
	remind_day = input('Which day you get remind (eg: 29)? ')
	remind_hour = input('Which hour you get remind (eg: 12)? ')
	remind_mind = input('Which minute you get remind (eg: 10)? ')

	full_date = date(int(remind_year), int(remind_month), int(remind_day))
	full_time = time(int(remind_hour), int(remind_mind))
	combined_date = datetime.combine(full_date, full_time)

	cursor.execute('''UPDATE reminder 
					SET title = ?,
					create_date = ?,
					remind_date = ? 
					WHERE id =?''', (remind_content, 
						datetime.now(),
						combined_date,
						task_id)) 
	conn.commit()

# Dict for store the CLI menus items
menuItems = [
    { "Create reminder": 0 },
    { "Update reminder": 1 },
	{ "View specific": 2 },
    { "View all": 3 },
	{ "Exit": 4 },
]
			
def main_menu():
                                   
	while True:

		#os.system('clear')
		print(header,"\n")
		for item in menuItems:
			print(menuItems.index(item), list(item.keys())[0])
		choice = input(">>> ")
		try:
			if int(choice) < 0: pass
			elif int(choice) == 0:
				create_reminder()

			elif int(choice) == 1:
				update_reminder()

			elif int(choice) == 2:
				
				view_remind(input("Which reminder you want to view? "))

			elif int(choice) == 3:
				view_remind(0)

			elif int(choice) == 4:
				sys.exit(0)
			else:
				pass
		except ValueError:
			pass
		except IndexError:
			pass

if __name__ == '__main__':
	#create_table()
	main_menu()