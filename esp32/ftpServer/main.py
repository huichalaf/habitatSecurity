from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import logging
from sqlConnect import *
import cv2
import asyncio
import threading
import os

def authenticate_esp32(id_esp32):
    data = accessTable('ESP32', 'DEVICES', ['ID_DEVICE', 'CONDOMINIO', 'FECHA_CREACION'])
    ids = list(data['ID_DEVICE'])
    condominios = list(data['CONDOMINIO'])
    if id_esp32 in ids:
        return True
    else:
        return False
        
def getCodeOfVisitsByUser(user, password):
	dicto = []
	table = getCondominioByUser(user, password)
	data = accessTable('VISITAS', table, ['ID_VISITA', 'RUT', 'NOMBRE', 'APELLIDO', 'FECHA_INI', 'FECHA_FIN', 'CODIGO', 'CELULAR', 'TIPO', 'ID_USUARIO', 'OBSERVACIONES', 'PATENTE', 'CLAVE'])
	return data

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

def compareQrCode(pathOfImage, user, password) -> bool:

    try:
        code = readcode(pathOfImage)
    except Exception as e:
        print(e)
        return False
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
                fecha = codes['FECHA_INI'][indice]
                return True
        return False
    else:
        return False

def get_esp_id_from_database(condominio):
    data = accessTable('ESP32', 'DEVICES', ['ID_DEVICE', 'CONDOMINIO', 'FECHA_CREACION'])
    for i in range(len(data['CONDOMINIO'])):
        if data['CONDOMINIO'][i] == condominio:
            return data['ID_DEVICE'][i]
        else:
            pass
    return ''

def getAdminByCondominio(condominio):
    data = accessTable('USUARIOS', 'USUARIOS', ['ID', 'RUT', 'NOMBRE', 'APELLIDO', 'TIPO', 'CORREO', 'CLAVE', 'ID_DOMICILIO', 'CONDOMINIO'])
    for i in range(len(data['CONDOMINIO'])):
        if data['TIPO'][i] == 1 and data['CONDOMINIO'][i] == condominio:
            return data['CORREO'][i], data['CLAVE'][i]
        else:
            pass
    return '', ''

async def verficarCodigo(pathOfImage):
    
    condominio = pathOfImage.split('_')[0]
    user, password = getAdminByCondominio(condominio)
    id_esp32 = get_esp_id_from_database(condominio)
    if compareQrCode(pathOfImage, user, password):
        with open(condominio+'_esp32_1', 'w') as f:
            f.write(id_esp32)
            return True
    else:
        return False
        
def main():
    logging.basicConfig(filename='ftp.log', level=logging.INFO)
    authorizer = DummyAuthorizer()
    authorizer.add_user("papo", "papo123", "./", perm="elradfmw")

    handler = FTPHandler
    handler.authorizer = authorizer

    #handler.masquerade_address = '179.60.70.219'
    #handler.passive_ports = range(60000, 65535)

    server = FTPServer(("192.168.1.18", 21), handler)
    print("ready")
    server.serve_forever()

#subsystem es una funcion que funciona siempre, se encarga de estar constantemente revisando si ha llegado otra imagen la cual se pueda analizar, para esto vee usando la libreria os, los archivos que hay en el directorio y los compara con el anterior
def subsystem():

    filesAnteriores = []
    files = []
    while True:
    
        files = os.listdir()
        if len(files) > 1:
            for i in files:
                if i.endswith('.jpg') and i not in filesAnteriores:
                    filesAnteriores.append(i)
                    print('nuevo archivo: ', i)
                    asyncio.run(verficarCodigo(i))
            filesAnteriores = files

        else:
            pass

if __name__ == '__main__':
    hilo1 = threading.Thread(target=subsystem)
    hilo2 = threading.Thread(target=main)
    hilo1.start()
    hilo2.start()