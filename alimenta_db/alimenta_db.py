#!/usr/bin/env python
#Script em Python para criar o banco de dados e alimenta-lo randomicamente

import pymysql as MySQLdb
import tweepy

CONSUMER_KEY = 'iisH0BPIUtZm0shzLb42ylzeY'
CONSUMER_SECRET = 'yVqVBWIL8wRKUuylXRaCpzM5OoB7GT4ei5fF3WOHORJVUXxxEd'
ACCESS_TOKEN = "14969574-cnooYvRvm2EkAEjaSQZwW5jwIuyrNj0bK2DNh8ELq"
ACCESS_TOKEN_SECRET = "sIbW3hBxkmSLHhs6rvlRkQEYOgQmXPLEmXFwCb7QH4FF8"

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

class IDPrinter(tweepy.Stream):

    def on_status(self, status):
        latitude = ''
        longitude = ''
        
        usuario = status.user.screen_name
        tweet = status.text

        
        if status.coordinates:
          #print(status.coordinates)
          latitude = status.coordinates['coordinates'][1]
          longitude = status.coordinates['coordinates'][0]            
        if status.place:
          #print(status.place.bounding_box.coordinates)
          latitude = status.place.bounding_box.coordinates[0][0][1]
          longitude = status.place.bounding_box.coordinates[0][0][0]
        if latitude and longitude:
          mycursor = db.cursor()
          record_tupla = (usuario, tweet, longitude, latitude)
          insert_query = """INSERT INTO tweets (username, tweet, longitude, latitude) VALUES (%s, %s, %s, %s)"""
          try:
            mycursor.execute(insert_query, record_tupla)
          except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
          print("Inserido", flush = True)
          db.commit()
          mycursor.close()

# Initialize instance of the subclass
printer = IDPrinter(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Filter realtime Tweets by keyword
printer.filter(track=["covid"])



