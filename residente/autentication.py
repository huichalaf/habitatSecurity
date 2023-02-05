import mysql.connector
import os,sys
import time as tm
import cv2
from random import choice
import qrcode
from datetime import date
from mailServer.main import send_mail
from sqlConnect import *

def randomCodeGenerator(longitud):
    valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ<=>@#%&+"

    p = ""
    p = p.join([choice(valores) for i in range(longitud)])
    return p

def generateQr(namePersonHabitante, namePersonVisita):

	fecha = date.today()
	code = randomCodeGenerator(64)
	img = qrcode.make(code)
	with open(f'ORIGINAL_{namePersonHabitante}_{namePersonVisita}_{fecha}.png', "wb") as f:
		img.save(f)
		f.close()
	
	os.system(f'mv ORIGINAL_{namePersonHabitante}_{namePersonVisita}_{fecha}.png administrador/media/')
	try:
		send_mail(namePersonHabitante, f'Código Qr para visita {namePersonVisita}', f'administrador/media/ORIGINAL_{namePersonHabitante}_{namePersonVisita}_{fecha}.png')
	except Exception as e:
		print("error al mandar el correo: ",e)
	return code

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

def addVisit(user, password, form):
	#if autenticateUserResidente(user, password) == True:

	condominio = getCondominioByUser(user, password)
	reservacionesExistentes = getReservationsByUserResidente(user, password)
	largoReservaciones = 1
	try:
		largoReservaciones = len(list(reservacionesExistentes['NOMBRE']))
	except:
		largoReservaciones = 1
	data = accessTable('USUARIOS', 'USUARIOS', ['ID', 'RUT', 'NOMBRE', 'APELLIDO', 'TIPO', 'CORREO', 'CLAVE', 'ID_DOMICILIO'])
	
	usuarios = list(data['CORREO'])
	passwords = list(data['CLAVE'])
	ids = list(data['ID'])
	idsDomicilio = list(data['ID_DOMICILIO'])

	for i in range(len(usuarios)):
		if usuarios[i] == user and passwords[i] == password:
			idUsuario = ids[i]
			idDomicilio = idsDomicilio[i]

	code = generateQr(user, form['Nombre'])
	values = {'ID_VISITA': largoReservaciones,'RUT': form['Rut'],'NOMBRE': form['Nombre'],'APELLIDO': form['Apellido'],
	'FECHA_INI': form['FechaInicio'],'FECHA_FIN': form['FechaFinal'], 'CODIGO': 1,'CELULAR': form['Celular'],'TIPO': form['Tipo'],
	'ID_USUARIO': idUsuario,'OBSERVACIONES': form['Observaciones'],'PATENTE': form['Patente'], 'CLAVE': code
	, 'HORA_INICIO': form['HoraInicio'], 'HORA_FINAL': form['HoraFinal'], 'ID_DOMICILIO': idDomicilio
	, 'EMPRESA': form['Empresa'], 'ESTADO': 0}
	valuesList = []
	
	for i in values.keys():
		try:
			valuesList.append(int(values[i]))
		except:
			valuesList.append(str(values[i]))

	addToTable('VISITAS', condominio, valuesList)
