import mysql.connector
import os,sys

mariadb_conexion = mysql.connector.connect(host='localhost', user='papo', passwd='6pjrQ18auqxVAYw80drvqmpKPdBqc399oV9kÑ-15', auth_plugin='mysql_native_password')
cursor = mariadb_conexion.cursor()
print("successfull connection!!!")

databases = ["USUARIOS"]
tables_by_database = {"USUARIOS": []}
args_of_table = {}

for i in databases:
    cursor.execute(f"CREATE DATABASE {i};")
    for table in tables_by_database[i]:
        cursor.execute(f"CREATE TABLE {table}({args_of_table[table]});")