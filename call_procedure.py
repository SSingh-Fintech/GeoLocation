import MySQLdb

mydb = MySQLdb.connect(
	host="localhost",
	user="webuser",
	passwd="Passw0rd#",
	db="XP_NDF_DB",
        port=3306
)
def call_iis_xff_procedure():	
	cur1 = mydb.cursor()
	cur1.callproc('SP_IIS_XFF')
	cur1.close()
	mydb.commit()

call_iis_xff_procedure()