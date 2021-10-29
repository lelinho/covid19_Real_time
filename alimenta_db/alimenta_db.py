#!/usr/bin/env python
#Script em Python para criar o banco de dados e alimenta-lo randomicamente

import pymysql as MySQLdb
import random
import time

while True:
    try:
        db = MySQLdb.connect(host='db',user='root',password='password')
        print('CONECTADO!', flush=True)
        break
    except:
        print('DB_LOADING', flush=True)
        time.sleep(3)

mycursor = db.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS tweets;")
mycursor.execute("USE tweets;")
mycursor.execute("CREATE TABLE IF NOT EXISTS tweets (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), tweet VARCHAR(255), longitude FLOAT, latitude FLOAT)")
mycursor.execute("GRANT ALL ON *.* TO 'root'@'%' IDENTIFIED BY 'password' WITH GRANT OPTION")
mycursor.execute("FLUSH PRIVILEGES;")
db.commit()
mycursor.close()

usuarios = ["joaozinho", "zezinho", "mariazinha", "joaquim", "joão", "josé", "mário", "marcos"]
tweets = ["Que tosse!", "Dor de garganta", "Hoje eu tomei a primeira dose da vacina", "Meu avô está internado com COVID", "Tomei a vacina!!!"]

while True:
  mycursor = db.cursor()
  time.sleep(random.randint(2,4))
  usuario = usuarios[random.randint(0,7)]
  tweet = tweets[random.randint(0,4)]
  latitude = random.uniform(-24,-21)
  longitude = random.uniform(-42,-49)
  record_tupla = (usuario, tweet, longitude, latitude)
  insert_query = """INSERT INTO tweets (username, tweet, longitude, latitude) VALUES (%s, %s, %s, %s)"""
  try:
    mycursor.execute(insert_query, record_tupla)
  except mysql.connector.Error as error:
    print("Failed to insert into MySQL table {}".format(error))
  print("Inserido", flush = True)
  db.commit()
  mycursor.close()
