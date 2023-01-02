import mysql.connector
import sys
#inicia la conexión

mariadb_conexion = mysql.connector.connect(host='localhost', user='papo', passwd='6pjrQ18auqxVAYw80drvqmpKPdBqc399oV9kÑ-15', auth_plugin='mysql_native_password')
cursor = mariadb_conexion.cursor()
print("successfull connection!!!")
cursor.execute("USE USUARIOS;")
idd = input("rut: ")
nombre = input("nombre: ")
apellido = input("apellido: ")
try:
    tipo = int(input("tipo: "))
except Exception as e:
    print(f"error: {e}")
    sys.exit()
correo = input("correo: ")
clave = input("clave: ")
id_domicilio = input("id domicilio: ")
condominio = input("condominio: ")
cursor.execute(f"INSERT INTO USUARIOS VALUES({idd},{rut},{nombre},{apellido},{tipo},{correo},{clave},{id_domicilio},{condominio});")