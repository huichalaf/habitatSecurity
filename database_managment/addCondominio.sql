USE VISITAS;
CREATE TABLE IF NOT EXISTS valle_del_rincon(ID_VISITA INT, RUT VARCHAR(10), NOMBRE VARCHAR(30)
                                    , APELLIDO VARCHAR(30), FECHA_INI DATE, FECHA_FIN DATE, CODIGO VARCHAR(10)
                                    , CELULAR VARCHAR(10), TIPO INT, ID_USUARIO INT, OBSERVACIONES VARCHAR(120)
                                    , PATENTE VARCHAR(6), CLAVE VARCHAR(64), HORA_INICIO TIME, HORA_FINAL TIME 
                                    , ID_DOMICILIO INT, EMPRESA VARCHAR(30), ESTADO INT);
CREATE TABLE IF NOT EXISTS valle_del_rincon_historial(ID_VISITA INT, RUT VARCHAR(10), NOMBRE VARCHAR(30)
                                    , APELLIDO VARCHAR(30), FECHA_INI DATE, FECHA_FIN DATE, CODIGO VARCHAR(10)
                                    , CELULAR VARCHAR(10), TIPO INT, ID_USUARIO INT, OBSERVACIONES VARCHAR(120)
                                    , PATENTE VARCHAR(6), CLAVE VARCHAR(64), HORA_INICIO TIME, HORA_FINAL TIME 
                                    , ID_DOMICILIO INT, EMPRESA VARCHAR(30), ESTADO INT);