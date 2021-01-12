# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
import decimal
from constant import *

class Database:
    table = 'list_saham'
    
    def mysql_connect():
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print("ANJING " + err)

    def mysql_close(conn):
        conn.close()
