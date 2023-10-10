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

cursor = conexion.cursor()
id_corrida = 2
# Consulta SQL para obtener los nombres de las subcarpetas
cursor.execute(f"SELECT original FROM nombresCarpetas WHERE idCorrida = {id_corrida}")

# Recorrer los resultados y crea carpetas
for (nombre_directorio,) in cursor.fetchall():
    try:
        # Crear la carpeta en el sistema de archivos
        os.makedirs(nombre_directorio)
        print(f"Carpeta {nombre_directorio} creada correctamente")
    except OSError as e:
        print(f"Error al crear la carpeta {nombre_directorio}: {str(e)}")

# Cerrar la conexión a la base de datos
cursor.close()
conexion.close()
