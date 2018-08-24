from datetime import date, datetime, timedelta
import requests,time,os
from requests.auth import HTTPDigestAuth
import json
import mysql.connector
mydb = mysql.connector.connect(	host="10.75.5.16",user="webloguser",password="Passw0rd#",database='XP_NDF_DB')

xff = os.path.exists("xff_id.txt")
if not xff:
	with open("xff_id.txt",'w') as xff_file:
		xff_file.write("0")

def getIPDetails():	
	with open("xff_id.txt", "r") as f2:
		old_count = f2.readline()	
			
	c1 = mydb.cursor(buffered=True)
	c1.execute("Select max(id) from XFF_Info")
	for x in c1:
		new_count =x[0]  

	if old_count != new_count:
		c2 = mydb.cursor(buffered=True)    
		c2.execute("Select ip,id from XFF_Info where id>'"+str(old_count)+"' AND id<='"+str(new_count)+"'")
		for row in c2:    
			url = "http://api.ipstack.com/"+row[0].strip()+"?access_key=2f8c01c0484028dc8cb07748187bc350"
			myResponse = requests.get(url)
			if(myResponse.ok):
				jData = json.loads(myResponse.content)			
				del jData["location"]
				for var in jData:
					jData[var] = jData[var] if  jData[var] !=None else "-"

				temp_string=""
				for var2 in jData:
					temp_string += var2+"='"+str(jData[var2])+"',"

				sql_query = "UPDATE XFF_Info SET "+temp_string[:-1]+" WHERE ip='"+jData['ip']+"'"
				print(sql_query)
				mydb.cursor().execute(sql_query)            
				print("\nRecord updated...!\n")
			else:
				myResponse.raise_for_status()
	with open("xff_id.txt", "w") as f1:
		f1.write(str(new_count))
		mydb.commit()
		
getIPDetails()