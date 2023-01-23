import mysql.connector
import time as tm
from random import choice
import sys
from datetime import datetime

#inicia la conexión

mariadb_conexion = mysql.connector.connect(host='localhost', user='papo', passwd='6pjrQ18auqxVAYw80drvqmpKPdBqc399oV9kÑ-15', auth_plugin='mysql_native_password')
cursor = mariadb_conexion.cursor()
print("successfull connection!!!")

#devuelve las bases de datos	

def getRutFromUser(user):
	
	table = accessTable('USUARIOS', 'USUARIOS', ['ID', 'RUT', 'NOMBRE', 'APELLIDO', 'TIPO', 'CORREO', 'CLAVE', 'ID_DOMICILIO', 'CONDOMINIO'])
	correos = list(table['CORREO'])
	ruts = list(table['RUT'])
	print(table)
	for correo in correos:
		if correo == user:
			return ruts[correos.index(correo)]
	
	return ''

def generateCode(longitud) -> str:
	
	valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	p = ""
	p = p.join([choice(valores) for i in range(longitud)])
	return p

def saveCode(user, code):
	try:
		rut = getRutFromUser(user)
		deleteDataFromTable2('USUARIOS', 'CODE_USUARIOS', 'RUT', rut)
	except Exception as e:
		rut = ''
		print(e)

	addToTable('USUARIOS', 'CODE_USUARIOS', [rut, user, code])
	return True

def getDatabases():
	
	cursor.execute("show databases;")
	dataUnPured = cursor.fetchall()
	databases=[]
	
	for i in dataUnPured:
	
		if type(i) == tuple and len(i) == 1:
			databases.append(i[0])
		
		if type(i) == tuple and len(i) > 1:
			for o in i:
				databases.append(i)
	mariadb_conexion.commit()
	return databases

#devuelve todas las tablas presentes en una database
def getTables(database):

	cursor.execute(f"USE {database};")
	cursor.execute("show tables;")
	tablasUnPured = cursor.fetchall()
	tablas = []

	for i in tablasUnPured:
	
		if type(i) == tuple and len(i) == 1:
			tablas.append(i[0])
		
		if type(i) == tuple and len(i) > 1:
			for o in i:
				tablas.append(i)
	mariadb_conexion.commit()
	return tablas

#accedemos a los datos de las tablas
def accessTable(database, table, namesColumns): #namesColumns es tipo lista

	cursor.execute(f"USE {database};")
	cursor.execute(f"SELECT * FROM {table};")
	dataUnPured = cursor.fetchall()

	data = {}
	for i in namesColumns:
		data[i] = []

	for i in dataUnPured:
		for o in range(len(namesColumns)):
			data[namesColumns[o]].append(i[o])
	mariadb_conexion.commit()
	return data

#busca dentro de una tabla
def searchInTable(table, elemento, columna):
	
	data = table[columna]
	dataPure = {}

	for i in data:
		if i==elemento:
			indice = data.index(i)
			for o in table.keys():
				dataPure[o] = table[o][indice]
	
	if dataPure == {}:
		return "Error, No matching :("
	return dataPure
#añade un elemento a una tabla
def addToTable(database, table, values):#values debe ser ingresado como lista

	cursor.execute(f"USE {database};")
	print(f'USE {database};')
	try:
		if int(values[0]) == values[0]:
			valores = str(values[0])
	except:
		if str(values[0]) == values[0]:
			valores = f"'{str(values[0])}'"
	values.pop(0)
	for i in values:
		try:
			if int(i) == i:
				valores+=f',{i}'
		except:
			if str(i) == i:
				valores+=f",'{i}'"
	#print(valores)
	print(f"INSERT INTO {table} VALUES({valores});")
	cursor.execute(f"INSERT INTO {table} VALUES({valores});")
	cursor.fetchall()
	mariadb_conexion.commit()
	print(cursor.fetchall())
	return True	

def updateDataFromTable(database, table, tipo, value, tipo2, value2):
	cursor.execute(f"USE {database};")
	cursor.execute(f"UPDATE {table} SET {tipo2}={value2} WHERE {tipo}={value};")
	print(f"UPDATE {table} SET {tipo2}={value2} WHERE {tipo}={value};")
	mariadb_conexion.commit()
	return True

def deleteDataFromTable(database, table, tipo, value):
	cursor.execute(f"USE {database};")
	print(f"DELETE FROM {table} WHERE {tipo}={value};")
	cursor.execute(f"DELETE FROM {table} WHERE {tipo}={value};")
	mariadb_conexion.commit()
	return True


def deleteDataFromTable2(database, table, tipo, value):
	cursor.execute(f"USE {database};")
	print(f"DELETE FROM {table} WHERE {tipo}='{value}';")
	cursor.execute(f"DELETE FROM {table} WHERE {tipo}='{value}';")
	mariadb_conexion.commit()
	return True