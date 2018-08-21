#東京の過去の天気データを表示してSQLに保存
import requests
from bs4 import BeautifulSoup
import numpy as np
import mysql.connector
import os
import sys
import re


base_url = "http://www.data.jma.go.jp/obd/stats/etrn/view/hourly_s1.php?prec_no=44&block_no=47662&year=2018&month=%s&day=%s&view=a2"

conn = mysql.connector.connect(user='root', password='key', host='localhost', database='forecast_db')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS `TOKYO`")
cur.execute("""CREATE TABLE IF NOT EXISTS `TOKYO` (`月` int(11) NOT NULL,`日`int(11) NOT NULL,`時間`int(11) NOT NULL,`降水量(mm)` float(11) NOT NULL,`気温(℃)` float(11) NOT NULL,`日照時間(h)`float(11) NOT NULL)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""")


for month in range(1,3):
    for day in range(1,32):
        if month==2 and day==29:
            exit()
        
        r = requests.get(base_url%(month,day))
        r.encoding = r.apparent_encoding

        soup = BeautifulSoup(r.text,'lxml')
        rows = soup.findAll('tr',class_='mtx')
        i = 1

        rows = rows[2:]

        for row in rows:
            data = row.findAll('td')
            if data[10].text=='': 
                data[10]=0
            if data[3].text=="--":
                data[3]=0

            time=str(data[0])
            rain=str(data[3])
            temp=str(data[4])
            sunt=str(data[10])

            time=time.replace('<td style="white-space:nowrap">','').replace('</td>','')
            rain=rain.replace('<td class="data_0_0">','').replace('</td>','')
            temp=temp.replace('<td class="data_0_0">','').replace('</td>','')
            sunt=sunt.replace('<td class="data_0_0">','').replace('</td>','')
            
            cur.execute('INSERT TOKYO VALUES(%s,%s,%s,%s,%s,%s)',(month,day,time,rain,temp,sunt))
            conn.commit()
            print("{0}/{1}".format(month,day))  
            print(time)
            print(rain)
            print(temp)
            print(sunt) 


conn.commit()
cur.close
conn.close
