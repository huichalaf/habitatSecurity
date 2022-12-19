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

def autenticateUserResidente(user, password):

	data = accessTable('USUARIOS', 'USUARIOS', ['ID', 'RUT', 'NOMBRE', 'APELLIDO', 'TIPO', 'CORREO', 'CLAVE', 'ID_DOMICILIO'])
	usuarios = list(data['CORREO'])
	passwords = list(data['CLAVE'])
	tipo = list(data['TIPO'])
	for i in range(len(usuarios)):
		if usuarios[i] == user and passwords[i] == password and tipo[i] == 2:
			return True
	return False

def getIDbyUSER(user, password):
	
	if autenticateUserResidente(user, password) == True:
	
		data = accessTable('USUARIOS', 'USUARIOS', ['ID', 'RUT', 'NOMBRE', 'APELLIDO', 'TIPO', 'CORREO', 'CLAVE', 'ID_DOMICILIO'])
		usuarios = list(data['CORREO'])
		ids = list(data['ID'])
	
		for i in range(len(usuarios)):
			if usuarios[i] == user:
				return ids[i]
	return False

def getReservationsByUser(user, password):
	
	if autenticateUserResidente(user, password) == False: return False
	condominio = getCondominioByUser(user, password)
	data2 = accessTable('USUARIOS', 'USUARIOS', ['ID', 'RUT', 'NOMBRE', 'APELLIDO', 'TIPO', 'CORREO', 'CLAVE', 'ID_DOMICILIO'])
	data = accessTable('VISITAS', condominio, ['ID_VISITA', 'RUT', 'NOMBRE', 'APELLIDO', 'FECHA_INI', 'FECHA_FIN', 'CODIGO', 'CELULAR', 'TIPO', 'ID_USUARIO', 'OBSERVACIONES', 'PATENTE'])
	passwords = list(data2['CLAVE'])
	usuarios = list(data2['CORREO'])
	ids = list(data2['ID'])
	idsVisitas = list(data['ID_VISITA'])
	dicto = []
	for i in range(len(usuarios)):
			if usuarios[i] == user and passwords[i] == password:
				idUsuario = ids[i]
	for i in range(len(data['NOMBRE'])):
		if data['ID_USUARIO'][i] == idUsuario:
			dicto.append({'number': idsVisitas[i], 'nombre': data['NOMBRE'][i], 'apellido': data['APELLIDO'][i], 'fechainicio': data['FECHA_INI'][i], 'fechafinal': data['FECHA_FIN'][i]})
	return dicto

def addVisit(user, password, form):
	if autenticateUserResidente(user, password) == True:

		condominio = getCondominioByUser(user, password)
		reservacionesExistentes = getReservationsByUser(user, password)
		largoReservaciones = 1
		try:
			largoReservaciones = len(list(reservacionesExistentes['NOMBRE']))
		except:
			largoReservaciones = 1
		data = accessTable('USUARIOS', 'USUARIOS', ['ID', 'RUT', 'NOMBRE', 'APELLIDO', 'TIPO', 'CORREO', 'CLAVE', 'ID_DOMICILIO'])
		
		usuarios = list(data['CORREO'])
		passwords = list(data['CLAVE'])
		ids = list(data['ID'])

		for i in range(len(usuarios)):
			if usuarios[i] == user and passwords[i] == password:
				idUsuario = ids[i]

		values = {'ID_VISITA': largoReservaciones,'RUT': form['Rut'],'NOMBRE': form['Nombre'],'APELLIDO': form['Apellido'],
		'FECHA_INI': form['FechaInicio'],'FECHA_FIN': form['FechaFinal'], 'CODIGO': 1,'CELULAR': form['Celular'],'TIPO': form['Tipo'],
		'ID_USUARIO': idUsuario,'OBSERVACIONES': form['Observaciones'],'PATENTE': form['Patente']}
		valuesList = []
		
		for i in values.keys():
			try:
				valuesList.append(int(values[i]))
			except:
				valuesList.append(str(values[i]))

		addToTable('VISITAS', condominio, valuesList)
	else:
		return False

def deleteVisitt(user, password, number):

	if autenticateUserResidente(user, password) == True:
		data = getReservationsByUser(user, password)
		condominio = getCondominioByUser(user, password)
		print(data)
		deleteDataFromTable('VISITAS', condominio, 'ID_VISITA', number)
	else:
		return False

def getCondominioByUser(user, password):

	data = accessTable('USUARIOS', 'USUARIOS', ['ID', 'RUT', 'NOMBRE', 'APELLIDO', 'TIPO', 'CORREO', 'CLAVE', 'ID_DOMICILIO', 'CONDOMINIO'])
	usuarios = list(data['CORREO'])
	passwords = list(data['CLAVE'])
	condominio = list(data['CONDOMINIO'])
	for i in range(len(usuarios)):
		if usuarios[i] == user and passwords[i] == password:
			return condominio[i]
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