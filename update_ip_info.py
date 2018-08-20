
from datetime import date, datetime, timedelta
import requests,time,os
from requests.auth import HTTPDigestAuth
import json

# import mysql.connector #For windows
import MYSQLdb   #For ubuntu

mydb = mysql.connector.connect(

#------------For Ubuntu----------------	
	host="localhost",              
	user="webloguser",
    passwd="Passw0rd#",           
	db='XP_NDF_DB',      
    port=3306      

#------------For Windows----------------
    # host="192.168.33.71",
	# user="webuser",               
	# password="Passw0rd#",        
    # database='XP_NDF_DB'
	
)

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
			row = str(row[0])
			# print("\nNew IP found: {} \n".format(row))
			myResponse = requests.get(url)
			if(myResponse.ok):
				jData = json.loads(myResponse.content)
			
				ip= 'no' if jData['ip'] ==None else jData['ip']
				jtype = 'no' if jData['type'] ==None else jData['type']
				continent_code= 'no' if jData['continent_code'] ==None else jData['continent_code']
				continent_name='no' if jData['continent_name'] ==None else jData['continent_name']
				
				country_code= 'no' if jData['country_code'] ==None else jData['country_code']
				country_name= 'no' if jData['country_name'] ==None else jData['country_name']

				region_code = 'no' if jData['region_code'] ==None else jData['region_code']
				region_name = 'no' if jData['region_name'] ==None else jData['region_name']
								
				city = 'no' if jData['city'] ==None else jData['city']
				jzip = 'no' if jData['zip'] ==None else jData['zip']

				latitude = 'no' if jData['latitude'] ==None else jData['latitude']
				longitude = 'no' if jData['longitude'] ==None else jData['longitude']
				
				sql3 = "UPDATE XFF_Info SET \
						ip='"+str(ip)+"',\
						type='"+str(jtype)+"',\
						continent_code='"+str(continent_code)+"',\
						continent_name='"+str(continent_name)+"',\
						country_code='"+str(country_code)+"',\
						country_name='"+str(country_name)+"',\
						region_code='"+str(region_code)+"',\
						region_name='"+str(region_name)+"',\
						city='"+str(city)+"',\
						zip='"+str(jzip)+"',\
						latitude='"+str(latitude)+"',\
						longitude='"+str(longitude)+"' WHERE ip='"+str(row)+"'"
				# print(sql3)
				c3 = mydb.cursor()
				c3.execute(sql3)
				c3.close()            
				# print("\nRecord updated...!\n")
			else:
				myResponse.raise_for_status()
		c2.close()

	with open("xff_id.txt", "w") as f1:
		f1.write(str(new_count))
		mydb.commit()

# print("Listening your databases..!")

getIPDetails()