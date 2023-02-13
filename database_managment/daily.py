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
    

    for fecha in fechas_finales:

        datetime_object = datetime.strptime(str(fecha), '%Y-%m-%d')
        datetime_object = datetime_object.date()
        print(fecha_actual, datetime_object)

        if fecha_actual > datetime_object:

            number = fechas_finales.index(fecha)
            print(str(list(data['ID_USUARIO'])[number]))
            usuario = getUserById(str(list(data['ID_USUARIO'])[number]))
            visita_al_historial = [list(data['ID_VISITA'])[number], list(data['RUT'])[number], list(data['NOMBRE'])[number]
            , list(data['APELLIDO'])[number], list(data['FECHA_INI'])[number], list(data['FECHA_FIN'])[number], int(list(data['CODIGO'])[number])
            , list(data['CELULAR'])[number], list(data['TIPO'])[number], list(data['ID_USUARIO'])[number], list(data['OBSERVACIONES'])[number]
            , list(data['PATENTE'])[number], list(data['CLAVE'])[number], list(data['HORA_INICIO'])[number], list(data['HORA_FINAL'])[number]
            , list(data['ID_DOMICILIO'])[number], list(data['EMPRESA'])[number], list(data['ESTADO'])[number]]
            addToTable('VISITAS', str(tabla+'_historial'), visita_al_historial)
            print(usuario)

            if deleteVisitJustById(str(list(data['ID_VISITA'])[number]), usuario):
                print(f"visita eliminada del usuario {usuario}, por termino de vigencia")

        else:
            print("no")
            pass