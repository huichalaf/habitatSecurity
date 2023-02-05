from sqlConnect import *
from datetime import datetime, date
import time as tm

fecha_actual = date.today()
tablasDisponibles = getTables("VISITAS")
tablasDisponiblesReal = []

for i in tablasDisponibles:
    if '_historial' in i:
        pass
    else:
        tablasDisponiblesReal.append(i)

for tabla in tablasDisponiblesReal:

    data = accessTable("VISITAS", tabla, ['ID_VISITA', 'RUT', 'NOMBRE', 'APELLIDO', 'FECHA_INI', 'FECHA_FIN', 'CODIGO', 'CELULAR', 'TIPO', 'ID_USUARIO', 'OBSERVACIONES', 'PATENTE', 'CLAVE', 'HORA_INICIO', 'HORA_FINAL', 'ID_DOMICILIO', 'EMPRESA', 'ESTADO'])
    fechas_finales = list(data['FECHA_FIN'])
    id_visita = list(data['ID_VISITA'])
    ruts = list(data['RUT'])
    nombres = list(data['NOMBRE'])
    apellidos = list(data['APELLIDO'])
    fechas_iniciales = list(data['FECHA_INI'])
    codigos = list(data['CODIGO'])
    celulares = list(data['CELULAR'])
    tipos = list(data['TIPO'])
    id_usuarios = list(data['ID_USUARIO'])
    observaciones = list(data['OBSERVACIONES'])
    patentes = list(data['PATENTE'])
    claves = list(data['CLAVE'])
    hora_inicio = list(data['HORA_INICIO'])
    hora_final = list(data['HORA_FINAL'])
    id_domicilio = list(data['ID_DOMICILIO'])
    empresa = list(data['EMPRESA'])
    estado = list(data['ESTADO'])

    for fecha in fechas_finales:

        datetime_object = datetime.strptime(str(fecha), '%Y-%m-%d')
        datetime_object = datetime_object.date()
        print(fecha_actual, datetime_object)

        if fecha_actual > datetime_object:

            indice = fechas_finales.index(fecha)
            usuario = getUserById(str(elemento['ID_USUARIO']))
            visita_al_historial = [id_visita[indice], ruts[indice], nombres[indice], apellidos[indice], fechas_iniciales[indice], fechas_finales[indice], codigos[indice]
            , celulares[indice], tipos[indice], id_usuarios[indice], observaciones[indice], patentes[indice], claves[indice], hora_inicio[indice]
            , hora_final[indice], id_domicilio[indice], empresa[indice], estado[indice]]
            addToTable('VISITAS', str(tabla+'_historial'), visita_al_historial)

            if deleteVisitJustByIdUser(str(elemento['ID_VISITA']), usuario):
                print(f"visita eliminada del usuario {usuario}, por termino de vigencia")

        else:
            print("no")
            pass