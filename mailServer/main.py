from email.message import EmailMessage
import smtplib
import mimetypes

from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
#rom email.Encod import encode_base64

def send_mail(destinatario, subject, file_name):
    remitente = "habitat.segura.chile@gmail.com"
    mensaje = "¡Hola, mundo!"

    email = MIMEMultipart()
    email["From"] = remitente
    email["To"] = destinatario
    email["Subject"] = subject
    file = open(file_name, "rb")
    attach_image = MIMEImage(file.read())
    attach_image.add_header('Content-Disposition', f'attachment; filename = {file_name}')
    email.attach(attach_image)

    with open('token', 'r') as f:
        token = str(f.read())
    smtp = smtplib.SMTP_SSL("smtp.gmail.com")
    smtp.login(remitente, token)
    smtp.sendmail(remitente, destinatario, email.as_string())
    smtp.quit()