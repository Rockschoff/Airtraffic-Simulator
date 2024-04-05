#Incident Log takes the datetime, Code, and notes
import mysql.connector
    
class IncidentLogAccess():
    
    def __init__(self):
        global IncidentLog
        IncidentLog = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="Incident_Log"
        )
        global IncidentLogCursor
        IncidentLogCursor = IncidentLog.cursor()
    
        print("Showing Tables for incident log:")
        IncidentLogCursor.execute("SHOW TABLES")

        for x in IncidentLogCursor:
            print(x)
            
    def add_Row(self, code, notes):
        sql = "INSERT INTO logs (date, code, notes) VALUES ( NOW(), %s, %s)"
        val = (code, notes)
        IncidentLogCursor.execute(sql, val)
        IncidentLog.commit()
        print(IncidentLogCursor.lastrowid)
    
    def get_Incident_Logs(self):
        sql = "SELECT date, code, notes FROM logs"
        IncidentLogCursor.execute(sql)
        return IncidentLogCursor.fetchall()
