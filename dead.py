from pyecharts import Geo
from pyecharts import Map
import numpy as np
import sqlite3

conn = sqlite3.connect('15-02-2020.sqlite')
cur = conn.cursor()

cur.execute('''SELECT city FROM coronavirus WHERE longitude IS NOT NULL''')
namelist = cur.fetchall()
name = [x[0] for x in namelist]
cur.execute('''SELECT longitude FROM coronavirus WHERE longitude IS NOT NULL''')
lnglist = cur.fetchall()
lng = [float(x[0]) for x in lnglist]
cur.execute('''SELECT latitude FROM coronavirus WHERE longitude IS NOT NULL''')
latlist = cur.fetchall()
lat = [float(x[0]) for x in latlist]
cur.execute('''SELECT dead FROM coronavirus WHERE longitude IS NOT NULL''')
confirmlist = cur.fetchall()
confirm = [float(x[0]) for x in confirmlist]


confirmmap = Geo("Death case by 14-02-2020", width=1000, height=800)
#confirmmap.use_theme('dark')
for i in range(len(name)):
	confirmmap.add_coordinate(name[i],lng[i],lat[i])
	n = [name[i]]
	c = [confirm[i]]
	confirmmap.add("death case",n,c, maptype='china',
             is_visualmap=True, 
             symbol_size=7*np.power(c*2,0.3),
             border_color = '#fff')
confirmmap.render('15-02-2020 dead.html')