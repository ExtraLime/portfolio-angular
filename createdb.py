#!/usr/bin/env python3

#to initialize a postgres db in python
import psycopg2
from psycopg2 import sql

#initialize db
conn = psycopg2.connect(host="localhost", dbname="postgres",
                        user="postgres", password="postgres", port='5432')
cursor = conn.cursor()
query = ''' CREATE DATABASE {} ;'''
name = 'online-exam'

conn.autocommit = True
cursor.execute(sql.SQL(query).format(
    sql.Identifier(name)))

cursor.close()
conn.close()