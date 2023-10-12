
import shutil
import mysql.connector
import os

# Establecer la conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="copiadoDeImagenesCD",
    port = '3306'
)

# Define el ID de la corrida que deseas procesar
id_corrida = 2