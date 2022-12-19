import mysql.connector
import os,sys
from .autenticacion import *
from datetime import datetime, date, timedelta
#from qrVerification.qr import *
from datetime import date, timedelta
import os, sys
import cv2
from random import choice
import qrcode

mariadb_conexion = mysql.connector.connect(host='localhost', user='papo', passwd='6pjrQ18auqxVAYw80drvqmpKPdBqc399oV9kÑ-15', auth_plugin='mysql_native_password')
cursor = mariadb_conexion.cursor()
print("successfull connection!!!")

def randomCodeGenerator(longitud):
    valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ<=>@#%&+"

    p = ""
    p = p.join([choice(valores) for i in range(longitud)])
    return p

def randomCodeVerification(realCode, codeReceived):
    
    realCodeList = list(realCode)
    codeReceivedList = list(codeReceived)
    counter = 0
    if len(realCodeList) == len(codeReceivedList):
        for i in range(len(realCode)):
            if realCodeList[i] == codeReceivedList[i]:
                counter+=1
    if counter == len(realCode): return True
    else: return False

def readcode(path):
	
	img = cv2.imread(path)
	detector = cv2.QRCodeDetector()
	data, bbox, straight_qrcode = detector.detectAndDecode(img)
	print(data, bbox, straight_qrcode)
	return data

def generateQr(namePersonHabitante, namePersonVisita):

	fecha = date.today()
	code = randomCodeGenerator(64)
	img = qrcode.make(code)
	with open(f'ORIGINAL_{namePersonHabitante}_{namePersonVisita}_{fecha}.png', "wb") as f:
		img.save(f)
		f.close()
	
	os.system(f'mv ORIGINAL_{namePersonHabitante}_{namePersonVisita}_{fecha}.png administrador/media/')
	return code

def autenticateUserResidente(user, password):

	data = accessTable('USUARIOS', 'USUARIOS', ['ID', 'RUT', 'NOMBRE', 'APELLIDO', 'TIPO', 'CORREO', 'CLAVE', 'ID_DOMICILIO'])
	usuarios = list(data['CORREO'])
	passwords = list(data['CLAVE'])
	tipo = list(data['TIPO'])
	for i in range(len(usuarios)):
		if usuarios[i] == user and passwords[i] == password and tipo[i] == 2:
			return True
	return False
	
def getReservationsByUserResidente(user, password):
	
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

def getCodeOfVisitsByUser(user, password):
	dicto = []
	table = getCondominioByUser(user, password)
	data = accessTable('VISITAS', table, ['ID_VISITA', 'RUT', 'NOMBRE', 'APELLIDO', 'FECHA_INI', 'FECHA_FIN', 'CODIGO', 'CELULAR', 'TIPO', 'ID_USUARIO', 'OBSERVACIONES', 'PATENTE', 'CLAVE'])
	return data

def compareQrCode(pathOfImage, user, password):
	code = readcode(pathOfImage)
	#print(code)
	codes = getCodeOfVisitsByUser(user, password)
	print('code: ',code, ';')

	if codes != [] and code != '':
		for i in codes['CLAVE']:
			#print(i, code)
			if i == code:
				indice = codes['CLAVE'].index(i)
				usuario = codes['NOMBRE'][indice]
				apellido = codes['APELLIDO'][indice]
				rut = codes['RUT'][indice]
				id = codes['ID_VISITA'][indice]
				return [id, usuario, apellido, rut]
		return 404
	else:
		return False
	

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

def getReservationsByUser(user, password):
	
	if autenticateUserAdmin(user, password) == False: return False
	condominio = getCondominioByUser(user, password)
	data = accessTable('VISITAS', condominio, ['ID_VISITA', 'RUT', 'NOMBRE', 'APELLIDO', 'FECHA_INI', 'FECHA_FIN', 'CODIGO', 'CELULAR', 'TIPO', 'ID_USUARIO', 'OBSERVACIONES', 'PATENTE'])
	dicto = []
	idsVisitas = list(data['ID_VISITA'])
	for i in range(len(data['NOMBRE'])):
		dicto.append({'number': idsVisitas[i], 'nombre': data['NOMBRE'][i], 'apellido': data['APELLIDO'][i], 'fechainicio': data['FECHA_INI'][i], 'fechafinal': data['FECHA_FIN'][i]})
	return dicto

def getReservationsByUserDay(user, password):
	
	if autenticateUserAdmin(user, password) == False: return False
	condominio = getCondominioByUser(user, password)
	data = accessTable('VISITAS', condominio, ['ID_VISITA', 'RUT', 'NOMBRE', 'APELLIDO', 'FECHA_INI', 'FECHA_FIN', 'CODIGO', 'CELULAR', 'TIPO', 'ID_USUARIO', 'OBSERVACIONES', 'PATENTE'])
	dicto = []
	idsVisitas = list(data['ID_VISITA'])
	hoy = date.today()
	for i in range(len(data['NOMBRE'])):
		if hoy >= data['FECHA_INI'][i] and hoy <= data['FECHA_FIN'][i]:
			dicto.append({'number': idsVisitas[i], 'nombre': data['NOMBRE'][i], 'apellido': data['APELLIDO'][i], 'fechainicio': data['FECHA_INI'][i], 'fechafinal': data['FECHA_FIN'][i]})
	return dicto

def addVisit(user, password, form):
	if autenticateUserAdmin(user, password) == True:

		condominio = getCondominioByUser(user, password)
		reservacionesExistentes = getReservationsByUser(user, password)
		largoReservaciones = 0
		print(type(reservacionesExistentes))
		for i in range(len(reservacionesExistentes)):
			largoReservaciones+=1
		data = accessTable('USUARIOS', 'USUARIOS', ['ID', 'RUT', 'NOMBRE', 'APELLIDO', 'TIPO', 'CORREO', 'CLAVE', 'ID_DOMICILIO'])
		
		usuarios = list(data['CORREO'])
		passwords = list(data['CLAVE'])
		ids = list(data['ID'])

		for i in range(len(usuarios)):
			if usuarios[i] == user and passwords[i] == password:
				idUsuario = ids[i]

		code = generateQr(user, form['Nombre'])
		values = {'ID_VISITA': largoReservaciones,'RUT': form['Rut'],'NOMBRE': form['Nombre'],'APELLIDO': form['Apellido'],
		'FECHA_INI': form['FechaInicio'],'FECHA_FIN': form['FechaFinal'], 'CODIGO': 1,'CELULAR': form['Celular'],'TIPO': form['Tipo'],
		'ID_USUARIO': idUsuario,'OBSERVACIONES': form['Observaciones'],'PATENTE': form['Patente'], 'CLAVE': code}
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

	if autenticateUserAdmin(user, password) == True:
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