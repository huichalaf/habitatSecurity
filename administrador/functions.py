from sqlConnect import *
from datetime import date
import os
import cv2
from random import choice
import qrcode
from mailServer.main import send_mail


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
	try:
		send_mail(namePersonHabitante, f'Código Qr para visita {namePersonVisita}', f'administrador/media/ORIGINAL_{namePersonHabitante}_{namePersonVisita}_{fecha}.png')
	except Exception as e:
		print("error al mandar el correo: ",e)
	return code


def getCodeOfVisitsByUser(user, password):
	dicto = []
	table = getCondominioByUser(user, password)
	data = accessTable('VISITAS', table, ['ID_VISITA', 'RUT', 'NOMBRE', 'APELLIDO', 'FECHA_INI', 'FECHA_FIN', 'CODIGO', 'CELULAR', 'TIPO', 'ID_USUARIO', 'OBSERVACIONES', 'PATENTE', 'CLAVE'])
	return data

def compareQrCode(pathOfImage, user, password):
	code = readcode(pathOfImage)
	#print(code)
	codes = getCodeOfVisitsByUser(user, password)
	#print('code: ',code, ';')

	if codes != [] and code != '':
		for i in codes['CLAVE']:
			#print(i, code)
			if i == code:
				indice = codes['CLAVE'].index(i)
				usuario = codes['NOMBRE'][indice]
				apellido = codes['APELLIDO'][indice]
				rut = codes['RUT'][indice]
				id = codes['ID_VISITA'][indice]
				fecha = codes['FECHA_INI'][indice]
				return {'id': id, 'nombre': usuario, 'apellido': apellido, 'rut': rut, 'fecha': fecha}
		return 404
	else:
		return False
	
def addVisit(user, password, form):

	condominio = getCondominioByUser(user, password)
	reservacionesExistentes = getReservationsByUser(user, password)
	largoReservaciones = len(reservacionesExistentes)
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
	,'EMPRESA': form['Empresa'], 'ESTADO': 0}
	valuesList = []
	
	for i in values.keys():
		try:
			valuesList.append(int(values[i]))
		except:
			valuesList.append(str(values[i]))

	addToTable('VISITAS', condominio, valuesList)

	return True