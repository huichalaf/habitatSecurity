import os, sys
from sqlConnect import *

def CreateUser(rut, nombre, apellido, tipo, user, password, id_domicilio):

	data = accessTable('USUARIOS', 'USUARIOS', ['ID', 'RUT', 'NOMBRE', 'APELLIDO', 'TIPO', 'CORREO', 'CLAVE', 'ID_DOMICILIO', 'CONDOMINIO'])
	#primero chequeamos si existe
	usuarios = list(data['CORREO'])
	ruts = list(data['RUT'])
	if user in usuarios or rut in ruts:
		return False
	id = len(usuarios)+1
	addToTable('USUARIOS', 'users', [id, rut, nombre, apellido, tipo, user, password, id_domicilio])
	return True

def updatePassword(user, pastPassword, newPassword):
		
	if autenticateUser(user, pastPassword) == True:
		updateDataFromTable('USUARIOS', 'USUARIOS', 'CORREO', user, 'CLAVE', newPassword)
		return True
	return False

def deleteUser(user, password):
	
	if autenticateUser(user, password) == True:
		deleteDataFromTable('USUARIOS', 'USUARIOS', 'CORREO', user)
		return True
	return False

def existUser(user):
	data = accessTable('USUARIOS', 'USUARIOS', ['ID', 'RUT', 'NOMBRE', 'APELLIDO', 'TIPO', 'CORREO', 'CLAVE', 'ID_DOMICILIO', 'CONDOMINIO'])
	usuarios = list(data['CORREO'])
	if user in usuarios:
		return True
	else:
		return False
