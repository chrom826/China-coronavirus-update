#coding=utf-8
import re
import sqlite3
import json
import urllib.request, urllib.parse, urllib.error
from pyecharts import Map
import numpy as np
import datetime
import csv

provincedata = {'北京':'Beijing','天津':"Tianjin",'河北':'Hebei', '山西':'Shanxi','辽宁':'Liaoning','吉林':'Jilin', '黑龙江':'Heilongjiang', '上海':'Shanghai', '江苏':'Jiangsu', '浙江':'Zhejiang', '安徽':'Anhui', '福建':'Fujian', '江西':'Jiangxi', '山东':'Shandong', '河南':'Henan', '湖北':'Hubei', '湖南':'Hunan', '广东':'Guangdong','广西':'Guangxi', '海南':'Hainan', '重庆':'Chongqing', '四川':'Sichuan', '贵州':'Guizhou', '云南':'Yunnan', '陕西':'Shaanxi','西藏':'Tibet','台湾':'Taiwan','澳门':'Macau','香港':'Hong Kong','内蒙古':'Inner Mongolia', '甘肃':'Gansu','青海':'Qinghai','宁夏':'Ningxia','新疆':'Xinjiang'}
url = 'http://3g.dxy.cn/newh5/view/pneumonia'
txt = urllib.request.urlopen(url)
data = txt.read().decode('utf-8')

pattern = re.compile('{"provinceName":.*?"cities":.*?]}')
jsondata = re.findall(pattern, data)

print (jsondata)

province = []
confirm = []
suspect = []
cured = []
dead = []

for i in jsondata:
	try:
		js = json.loads(i)
		if js["provinceShortName"]=='待明确地区':
			break
		province.append(js["provinceShortName"])
		confirm.append(js["confirmedCount"])
		suspect.append(js["suspectedCount"])
		cured.append(js["curedCount"])
		dead.append(js["deadCount"])
	except:
		js = None

d = datetime.datetime.today()
d1 = d.strftime('%d-%m-%Y')
provinceeng = [provincedata[x] if x in provincedata else x for x in province]
ls = [provinceeng,confirm,suspect,cured,dead]
ls2 = zip(*ls)
namelist = ["province","confirm","suspect","cured","dead"]
with open(d1+' province.csv','w') as myfile:
	wr = csv.writer(myfile,quoting=csv.QUOTE_ALL,delimiter=';')
	wr.writerow(namelist)
	for item in ls2:
		wr.writerow(item)


map = Map('2019-nCov infected toll', width =1000, height = 800)
confirmlog = np.log(confirm)
map.add("",province,confirmlog,is_map_symbol_show = True, map_type = 'china', is_visualmap=True, visual_text_color='#000', 
    is_label_show=True,visual_range=[np.min(confirmlog),np.max(confirmlog)])
map.render('r2.html')



