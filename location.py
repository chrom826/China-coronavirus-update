#coding=utf-8
import urllib.request, urllib.parse, urllib.error
import json
import sqlite3
import re

conn = sqlite3.connect('15-02-2020.sqlite')
cur = conn.cursor()

baseurl = 'http://api.map.baidu.com/geocoder/v2/?ak=2ae1130ce176b453fb29e59a69b18407&callback=renderOption&output=json&address='

cur.execute('''ALTER TABLE coronavirus ADD longitude varchar(30)''')
cur.execute('''ALTER TABLE coronavirus ADD latitude varchar(30)''')

cur.execute('''SELECT city FROM coronavirus WHERE longitude IS NULL''')
namelist = cur.fetchall()
osml = []
ptt = re.compile('\((.*?)\)')
for names in namelist:
	names = names[0]
	names1 = names
	if names == '湘西自治州':
		names1 = '吉首'
	if names == '伊犁州':
		names1 = '伊宁'
	url = baseurl + urllib.parse.quote(names1.encode('utf-8'))
	raw = urllib.request.urlopen(url)
	data = raw.read().decode()
	data = re.findall(ptt,data)[0]
	#print (type(data))
	try:
		js = json.loads(data)
	#print (type(js['status']))
	except:
		js = None
	#print(data)
	if js['status'] != 0:
		print ("retrieve failure: ", names)
		if names == "香港":
			lng = 114.15
			lat = 22.15
		if names == "台湾":
			lng = 121.30
			lat = 25.03
		cur.execute('''UPDATE coronavirus SET longitude = ? WHERE city = ?''', (lng, names))
		cur.execute('''UPDATE coronavirus SET latitude = ? WHERE city = ?''',(lat,names))
		osml.append(names)
		continue

	lng = js["result"]["location"]["lng"]
	#print(lng)
	lat = js["result"]["location"]["lat"]

	cur.execute('''UPDATE coronavirus SET longitude = ? WHERE city = ?''', (lng, names))
	cur.execute('''UPDATE coronavirus SET latitude = ? WHERE city = ?''',(lat,names))
	conn.commit()