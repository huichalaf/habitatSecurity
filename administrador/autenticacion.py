import mysql.connector
import os,sys
import time as tm

mariadb_conexion = mysql.connector.connect(host='localhost', user='papo', passwd='6pjrQ18auqxVAYw80drvqmpKPdBqc399oV9kÑ-15', auth_plugin='mysql_native_password')
cursor = mariadb_conexion.cursor()
print("successfull connection!!!")

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

def autenticateUserAdmin(user, password):

	data = accessTable('USUARIOS', 'USUARIOS', ['ID', 'RUT', 'NOMBRE', 'APELLIDO', 'TIPO', 'CORREO', 'CLAVE', 'ID_DOMICILIO'])
	usuarios = list(data['CORREO'])
	passwords = list(data['CLAVE'])
	tipo = list(data['TIPO'])
	for i in range(len(usuarios)):
		if usuarios[i] == user and passwords[i] == password and tipo[i] == 1:
			return True
	return False

def addToTable(database, table, values):#values debe ser ingresado como lista

	cursor.execute(f"USE {database};")
	print(f'USE {database};')
	try:
		if int(values[0]) == values[0]:
			valores = str(values[0])
	except:
		try:
			if str(values[0]) == values[0]:
				valores = f"'{str(values[0])}'"
		except Exception as e:
			print(e, values[0])
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

def deleteDataFromTable(database, table, tipo, value):
	cursor.execute(f"USE {database};")
	print(f"DELETE FROM {table} WHERE {tipo}={value};")
	cursor.execute(f"DELETE FROM {table} WHERE {tipo}={value};")
	mariadb_conexion.commit()
	return True