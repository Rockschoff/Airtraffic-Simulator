import mysql.connector
import enum

#This file allows access to the Master Log Database
#Objects of this class will be able to interact in a limited capacity with the database

class Column_headers(enum.Enum):
	date = 1
	action_performed = 2
	additional_details = 3
	had_incident = 4
	plane_number = 5

class MasterLogAccess():
	
	def __init__(self):
		global MasterLog
		MasterLog = mysql.connector.connect(
			host="localhost",
			user="root",
			password="password",
			database="Master_Log"
		)
		global MasterLogCursor
		MasterLogCursor = MasterLog.cursor()

		#*Created Table*
		#MasterLogCursor.execute("CREATE TABLE logs (date DATETIME PRIMARY KEY, action_performed VARCHAR(3000), additional_details VARCHAR(3000), had_incident BOOLEAN, aircraft_number INT)")	
		print("Showing Tables for master log:")
		MasterLogCursor.execute("SHOW TABLES")
		for x in MasterLogCursor:
			print(x)

	#Adds a row with the given variables
	def add_Row(self, action_performed, additional_details, had_incident, aircraft_number):
		sql = "INSERT INTO logs (date, action_performed, additional_details, had_incident, aircraft_number) VALUES ( NOW(), %s, %s, %s, %s )"
		val = (action_performed, additional_details, had_incident, aircraft_number)
		MasterLogCursor.execute(sql, val)
		MasterLog.commit()
		#sql = "INSERT INTO logs (date, action_performed, additional_details, had_incident, aircraft_number) VALUES (NOW(), 'Testing', 'Testing addition', 0, 1234)"

	
	#Temporary Search Query for testing
	#Was created to test the display functionality
	def get_Master_Log(self):
		sql = "SELECT date, aircraft_number, action_performed FROM logs"
		MasterLogCursor.execute(sql)
		return MasterLogCursor.fetchall()
