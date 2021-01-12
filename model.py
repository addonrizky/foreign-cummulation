from database import *

class Model:
    table = "list_saham"
    def __init__(self):
        self.cnx = Database.mysql_connect()

    def save(self, field, value, kode_saham): 
        cursor = self.cnx.cursor()

        sql = ("UPDATE " + self.table + " SET "+field+" ='"+str(value)+"' WHERE kode_saham = '" + kode_saham + "'")

        # Insert new row
        cursor.execute(sql)
        lastRecordId = cursor.lastrowid

        # Make sure data is committed to the database
        self.cnx.commit()
        cursor.close()
        self.cnx.close()
        
        print("Item saved with ID: {}" . format(lastRecordId))