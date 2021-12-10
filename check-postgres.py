#!/usr/local/bin/python
import os
import time
import psycopg2

while True:
  try:
    conn = psycopg2.connect(host="database", database="django", user="django", password="django")
    break
  except psycopg2.Error:
    print("No connection to database. Waiting.")
    time.sleep(1)
    continue

print("Database detected. Starting migrate")
os.system("python manage.py migrate")