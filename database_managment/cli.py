import mysql.connector
import sys
import hashlib
import sys
from sqlConnect import *

def check_safety_of_password(password):
    
    score=0
    state=0
    password_list = list(password)
    
    if len(password) > 10 and len(password) < 18:
        score+=1
    elif len(password) >= 18:
        score+=2
    if (any(x.islower() for x in password_list)):
        score+=1
    if(any(x.isupper() for x in password_list)):
        score+=1
    if(any(x.isdigit() for x in password_list)):
        score+=1

    longitud = len(password)
    with open('passwords.txt', 'r') as f:
        for i in range(0, 999997):
            if password+'\n' == f.readline():
                score-=1
                state = -1
                break
            elif f.readline().strip('\n') in password and longitud<18:
                score-=1
                state = -1
                break
    if state==0:
        score+=2
    return score

def getCondominios():
    tablas = getTables('VISITAS')
    tablas_real = []
    for i in tablas:
        if '_historial' in i:
            pass
        else:
            tablas_real.append(i)
    return tablas_real

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
        return False
    
    correo = input("correo: ")
    clave_state = False
    while True:
        if clave_state==True:
            break
        clave = input("clave: ")
        try:
            score = check_safety_of_password(clave)
            if score>5:
                clave = generatePassword(clave)
                clave_state=True
                break
            elif score <=5 and score >= 3:
                while True:
                    opcion_temporal = input("la clave ingresada es poco segura, desea ingresarla otra mas segura?[y/n]")
                    if opcion_temporal=='y':
                        break
                    elif opcion_temporal=='n':
                        clave = generatePassword(clave)
                        clave_state = True
                        break
                    else:
                        print("ingrese una opción válida")
            elif score<3:
                print("clave muy insegura, score: ",score,"/7")
        except Exception as e:
            print("error en la clave: ",e)

    id_domicilio = input("id domicilio: ")
    condominio = input("condominio: ")
    data = accessTable('USUARIOS', 'USUARIOS', ['ID', 'RUT', 'NOMBRE', 'APELLIDO', 'TIPO', 'CORREO', 'CLAVE', 'ID_DOMICILIO', 'CONDOMINIO'])
    ids = list(data['ID'])
    if condominio not in getCondominios():
        print("condominio no existe")
        return False
    id_usuario = len(ids)
    try:
        cursor.execute("USE USUARIOS;")
        cursor.execute(f"INSERT INTO USUARIOS VALUES('{id_usuario}', '{idd}','{nombre}','{apellido}',{tipo},'{correo}','{clave}',{id_domicilio},'{condominio}');")
        mariadb_conexion.commit()
    except Exception as e:
        print("ocurrio un error: ",e)
    print("usuario agregado exitosamente")
    return True

def deleteUser():
    data = accessTable('USUARIOS', 'USUARIOS', ['ID', 'RUT', 'NOMBRE', 'APELLIDO', 'TIPO', 'CORREO', 'CLAVE', 'ID_DOMICILIO', 'CONDOMINIO'])
    usuario = input("ingrese el usuario a eliminar(correo): ")
    condominio = input("ingrese su condominio: ")
    id_domicilio = input("ingrese su id de domicilio: ")
    usuarios = list(data['CORREO'])
    ids_domicilio = list(data['ID_DOMICILIO'])
    if condominio not in getCondominios():
        print("condominio no existe")
        return False
    if usuario not in usuarios:
        print("usuario no existe")
        return False
    try:
        if usuarios.index(usuario) != ids_domicilio.index(int(id_domicilio)):
            print("el usuario no esta registrado en ese domicilio")
            return False
    except Exception as e:
        print(e)
    confirmacion = ''
    while confirmacion != 'y' and confirmacion != 'n':
        confirmacion = input("esta seguro que desea eliminar a este usuario? [y/n]: ")
        if confirmacion == 'y':
            deleteDataFromTable('USUARIOS', 'USUARIOS', 'CORREO', f"'{usuario}'")
            print("usuario eliminado")
            return True
        elif confirmacion == 'n':
            return False
def main():
    print("\n\tBienvenido a la CLI del administrador :)")

    while True:
        
        print("1.- añadir usuario")
        print("2.- eliminar usuario")
        opcion = input("ingrese la opcion: ")
        if opcion=='exit':
            sys.exit()
        opcion = int(opcion)

        if opcion == 1:
            addUser()
        elif opcion == 2:
            deleteUser()

if __name__ == '__main__':
    main()