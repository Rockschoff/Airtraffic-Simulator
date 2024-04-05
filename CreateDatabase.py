import mysql.connector

class CreateDatabase():
    
    def __init__(self):
        db = mysql.connector.connect(
            host="localhost",
            user="user",
            password="password"
        )

        dbcursor = db.cursor()

        # Master Log
        dbcursor.execute("CREATE DATABASE Master_Log;")
        dbcursor.execute("Use Master_Log;")
        dbcursor.execute("CREATE TABLE logs (date DATETIME PRIMARY KEY, action_performed VARCHAR(3000), additional_details VARCHAR(3000), had_incident BOOLEAN, aircraft_number INT);")

        # Incident log
        dbcursor.execute("CREATE DATABASE Incident_Log;")
        dbcursor.execute("Use Incident_Log;")
        dbcursor.execute("CREATE TABLE logs(date datetime, code int, notes varchar(3000));")


c =  CreateDatabase()

