import mysql.connector
import sys
import hashlib
import sys

#inicia la conexión

mariadb_conexion = mysql.connector.connect(host='localhost', user='papo', passwd='6pjrQ18auqxVAYw80drvqmpKPdBqc399oV9kÑ-15', auth_plugin='mysql_native_password')
cursor = mariadb_conexion.cursor()
print("successfull connection!!!")

def generatePassword(contraseña):
    
    hash = hashlib.sha256(contraseña.encode()).hexdigest()
    return hash

def addUser():
    
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
    
    return True

def addCondominio():
    
    cursor.execute("USE VISITAS");
    name = input("nombre del condominio: ")
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {name}(ID_VISITA INT, RUT VARCHAR(10), NOMBRE VARCHAR(30), APELLIDO VARCHAR(30), FECHA_INI DATE, FECHA_FIN DATE, CODIGO VARCHAR(10), CELULAR INT, TIPO INT, ID_USUARIO INT, OBSERVACIONES VARCHAR(120), PATENTE VARCHAR(6), CLAVE VARCHAR(64), HORA_INICIO TIME, HORA_FINAL TIME, ID_DOMICILIO INT);")
    return True

print("\n\tBienvenido a la CLI del administrador :)")

while True:
    
    print("1.- añadir usuario")
    print("2.- eliminar usuario")
    print("3.- añadir condominio")
    print("4.- eliminar condominio")
    opcion = input("ingrese la opcion: ")

    if opcion == 1:
        addUser()
    elif opcion == 2:
        deleteUser()
    elif opcion == 3:
        addCondominio()
    elif opcion == 4:
        deleteCondominio()