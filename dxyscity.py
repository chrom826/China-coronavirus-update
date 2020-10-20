#coding=utf-8
import re
import sqlite3
import json
import urllib.request, urllib.parse, urllib.error
from pyecharts import Map
import numpy as np
import datetime
import csv
import codecs

provincedata = {'北京':'Beijing','天津':"Tianjin",'河北':'Hebei', '山西':'Shanxi','辽宁':'Liaoning','吉林':'Jilin', '黑龙江':'Heilongjiang', '上海':'Shanghai', '江苏':'Jiangsu', '浙江':'Zhejiang', '安徽':'Anhui', '福建':'Fujian', '江西':'Jiangxi', '山东':'Shandong', '河南':'Henan', '湖北':'Hubei', '湖南':'Hunan', '广东':'Guangdong','广西':'Guangxi', '海南':'Hainan', '重庆':'Chongqing', '四川':'Sichuan', '贵州':'Guizhou', '云南':'Yunnan', '陕西':'Shaanxi','西藏':'Tibet','台湾':'Taiwan','澳门':'Macau','香港':'Hong Kong','内蒙古':'Inner Mongolia', '甘肃':'Gansu','青海':'Qinghai','宁夏':'Ningxia','新疆':'Xinjiang'}


url = 'http://3g.dxy.cn/newh5/view/pneumonia'
txt = urllib.request.urlopen(url)
data = txt.read().decode('utf-8')

pattern = re.compile('{"provinceName":.*?"cities":.*?]}')
jsondata = re.findall(pattern, data)

province = []
city = []
confirm = []
suspect = []
cured = []
dead = []

print(jsondata)

for i in jsondata:
	try:
		js = json.loads(i)
		citylist = js["cities"]
		if js["provinceShortName"] in ["北京","上海","重庆","天津","香港","澳门","台湾"]:
			province.append(js["provinceShortName"])
			city.append(js["provinceShortName"])
			confirm.append(js["confirmedCount"])
			suspect.append(js["suspectedCount"])
			cured.append(js["curedCount"])
			dead.append(js["deadCount"])
			continue
		for j in citylist:
			n = j["cityName"]
			if n in city:
				break
			province.append(js["provinceShortName"])
			city.append(n)
			confirm.append(j["confirmedCount"])
			suspect.append(j["suspectedCount"])
			cured.append(j["curedCount"])
			dead.append(j["deadCount"])
	except:
		js = None

d = datetime.datetime.today()
d1 = d.strftime('%d-%m-%Y')
provinceeng = [provincedata[x] if x in provincedata else x for x in province]
ls = [provinceeng,city,confirm,cured,dead]
ls2 = zip(*ls)

conn = sqlite3.connect(d1+'.sqlite')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS coronavirus (id INTEGER PRIMARY KEY, province TEXT, city TEXT, confirm integer, cured integer, dead integer)''')

for i in ls2:
	cur.execute('''INSERT OR IGNORE INTO coronavirus (province,city,confirm,cured,dead) VALUES (?,?,?,?,?)''', i)
	conn.commit()
