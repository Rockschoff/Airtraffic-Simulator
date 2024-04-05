import MasterLogAccess
import IncidentLogAccess
import time

#Temporary class to test the implementation of database functionality
class TestingDatabases():
	
	#Upon its definition, adds some test values to the database
	def __init__(self):
		global Log_access
		Log_access = MasterLogAccess.MasterLogAccess()
		Log_access.add_Row("Test Entry", "This is an entry to test the table insertion method", 0, 1)
		time.sleep(1)
		Log_access.add_Row("Test Entry", "This is an entry to test the table insertion method", 0, 2)
		time.sleep(1)
		Log_access.add_Row("Test Entry", "This is an entry to test the table insertion method", 0, 3)
		time.sleep(1)
		Log_access.add_Row("Test Entry", "This is an entry to test the table insertion method", 1, 4)
		
		Log_access = IncidentLogAccess.IncidentLogAccess()
		Log_access.add_Row(1, "Test Entry")
		Log_access.add_Row(2, "Test Entry 2")

	#Calls the general search method of the Master Log Database Access
	#Then prints the results of the query
	def gen_search():
		query_result = Log_access.general_search()
		for x in query_result:
			print(x)
