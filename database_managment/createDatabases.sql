CREATE DATABASE IF NOT EXISTS USUARIOS;
CREATE DATABASE IF NOT EXISTS VISITAS;
CREATE DATABASE IF NOT EXISTS ESP32;

USE USUARIOS;
CREATE TABLE IF NOT EXISTS USUARIOS(ID INT, RUT VARCHAR(10), NOMBRE VARCHAR(30)
                                    , APELLIDO VARCHAR(30), TIPO INT, CORREO VARCHAR(50)
                                    , CLAVE VARCHAR(64), ID_DOMICILIO INT, CONDOMINIO VARCHAR(20));

CREATE TABLE IF NOT EXISTS CODE_USUARIOS(CORREO VARCHAR(50), CODE VARCHAR(64), TIEMPO TIME);

USE ESP32;
CREATE TABLE IF NOT EXISTS DEVICES(ID_DEVICE VARCHAR(64), CONDOMINIO VARCHAR(20), FECHA_CREACION DATE);