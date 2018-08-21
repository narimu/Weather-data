# -*- coding: utf-8 -*-
#東京か大阪の特定の日付の気象情報をOpenWeatherMapWEBAPIを利用して取得したのちSQLに書き込む

import json
import datetime
import os
import requests
import sys
import mysql.connector
from pytz import timezone
NUM=input("Please choose city \n t=Tokyo \n o=Osaka-shi\n:")
if NUM=="t":
    CITY='tokyo,JP'
elif NUM=="o":
    CITY='Osaka-shi,JP'
else:
    print("ERROR") 
  
API_KEY = '8316462883ee6e8ba36a61b549ebe519'
API_URL = 'http://api.openweathermap.org/data/2.5/forecast?q={0}&units=metric&lang=ja&APPID={1}'
def getWeatherForecast():
    url = API_URL.format(CITY, API_KEY)
    response = requests.get(url)
    forecastData = json.loads(response.text)
    if not ('list' in forecastData):
        print('ERROR2')
        return

    Y=input("Please input YYYYMMDD: ")
    D=input("Please input HHMM: ")

    conn = mysql.connector.connect(user='root', password='KEY', host='localhost', database='forecast_db')
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS `CITY_F`")
    cur.execute("""CREATE TABLE IF NOT EXISTS `CITY_F` (`日付` int(11) NOT NULL,`時間`int(11) NOT NULL,`天気` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,`気温(℃)` float(11) NOT NULL,`雨量(mm)` float(11) NOT NULL,PRIMARY KEY (`日付`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""")


    for item in forecastData['list']:
        forecastDatetime = timezone(
            'Asia/Tokyo').localize(datetime.datetime.fromtimestamp(item['dt']))
        YMDforecastDatetime=forecastDatetime.strftime('%Y%m%d')
        HMforecastDatetime=forecastDatetime.strftime('%H%M')
        weatherDescription = item['weather'][0]['description']
        temperature = item['main']['temp']
        rainfall = 0
        if 'rain' in item and '3h' in item['rain']:
            rainfall = item['rain']['3h']
            if Y == YMDforecastDatetime and D==HMforecastDatetime:

                cur.execute('INSERT INTO CITY_F VALUES(%s,%s,%s,%s,%s)',(YMDforecastDatetime,HMforecastDatetime,weatherDescription,temperature,rainfall))

                print('以下の情報がDB=forecast_db Table:CITY_F に記録されました \n日時:{0} 天気:{1} 気温(℃):{2} 雨量(mm):{3} {4}'.format(forecastDatetime, weatherDescription, temperature, rainfall,CITY))

    conn.commit()
    cur.close
    conn.close

getWeatherForecast()

