import os
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

# Crear un cursor
cursor = conexion.cursor()
############    Obtenemos el directorio del LTO
# Consulta SQL para obtener el pathDestino
consulta_sql = f"SELECT pathDestino FROM corridaYcarpetaRaiz WHERE idCorrida = {id_corrida}"

# Ejecutar la consulta SQL
cursor.execute(consulta_sql)

# Obtener el resultado de la consulta
resultado = cursor.fetchone()

# Comprobar si se obtuvo un resultado
if resultado:
    directorio_origen = resultado[0]
    print(f"Directorio origen (LTO): {directorio_origen}")
else:
    print("No se encontró un directorio origen para la corrida especificada.")
    

############ Obtenemos el directorio de la unidad que se recuperará la copia de respaldo

# Consulta SQL para obtener el pathDestino
consulta_sql = f"SELECT pathRaiz FROM corridaYcarpetaRaiz WHERE idCorrida = {id_corrida}"

# Ejecutar la consulta SQL
cursor.execute(consulta_sql)

# Obtener el resultado de la consulta
resultado = cursor.fetchone()

# Comprobar si se obtuvo un resultado
if resultado:
    directorio_destino = resultado[0]
    print(f"Directorio destino (HDD): {directorio_destino}")
else:
    print("No se encontró un directorio origen para la corrida especificada.")


# Consulta SQL para obtener la información de los archivos a mover
# Asegúrate de que esta consulta recupere los archivos que deseas mover
consulta_sql = """
select nombresArchivos.alias as modificado, nombresCarpetas.original as Destino, nombresArchivos.original as nombreReal from nombresCarpetas inner join nombresArchivos on nombresCarpetas.idreg = nombresArchivos.idregPadre where nombresArchivos.idCorrida = 2
"""

# Ejecuta la consulta SQL
cursor.execute(consulta_sql)

# Obtiene los resultados de la consulta
resultados = cursor.fetchall()

# Imprime los resultados
for resultado in resultados:
    #Obtenemos de la nueva tabla la columna de modicado
    modificado = resultado[0]
    #Obtenemos de la nueva tabla la columna de destino
    destino = resultado[1]
    #Obtenemos de la nueva tabla la columna de nombreReal
    nombreReal = resultado[2]
    
    #Armamos el formato del directorio destino
    ruta_destino = os.path.join(directorio_destino,destino,nombreReal)
    
    #Armamos el formato del directorio origen
    ruta_origen = os.path.join(directorio_origen,modificado)
    
    try:
        # Copia el archivo desde la carpeta de origen a la carpeta de destino
        shutil.copy(ruta_origen, ruta_destino)
        #Lanzamos una alerta de que se copio correctamente    
        print(f'Archivo "{modificado}" copiado como "{nombreReal}" en la carpeta de destino')
    except Exception as e:
        #Lanzamos una alerta de que no se copio correctamente
        print(f'Error al copiar "{modificado}": {str(e)}')

# Cierra la conexión a la base de datos
cursor.close()
conexion.close()