import smtplib

# Dirección del servidor SMTP y puerto
SMTP_SERVER = 'smtp-mail.outlook.com'
SMTP_PORT = 587

# Dirección de correo electrónico y contraseña del remitente
USERNAME = 'pablo.huichalaf.prisdai@outlook.com'
PASSWORD = 'JENGA9292jenga9292'

# Direcciones de correo electrónico del destinatario y del remitente
TO = 'papo9292@gmail.com'
FROM = 'pablo.huichalaf.prisdai@outlook.com'

# Asunto y cuerpo del mensaje
SUBJECT = 'Prueba de correo electrónico'
TEXT = 'Este es un mensaje de prueba enviado desde Python'

# Creamos el mensaje
message = f"From: {FROM}\nTo: {TO}\nSubject: {SUBJECT}\n\n{TEXT}"

# Establecemos conexión con el servidor SMTP
smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
smtp.ehlo()
smtp.starttls()
smtp.ehlo()

# Iniciamos sesión en el servidor con nuestra dirección de correo y contraseña
smtp.login(USERNAME, PASSWORD)
print("sesion iniciada :)")
# Enviamos el correo electrónico
smtp.sendmail(FROM, TO, message)

# Cerramos la conexión con el servidor
smtp.quit()
