import qrcode
from datetime import date, timedelta
import os, sys
import cv2
from codeGenerator import *

def readcode(path):
	
	img = cv2.imread(path)
	detector = cv2.QRCodeDetector()
	data, bbox, straight_qrcode = detector.detectAndDecode(img)

	return data

def generateQr():
	
	code = randomdCodeGenerator(64)
	fecha1 = str(fecha1)
	fecha2 = str(fecha2)
	img = qrcode.make(code)
	f = open(f'{namePersonHabitante}_{fecha1}.png', "wb")
	img.save(f)
	f.close()
	return True
