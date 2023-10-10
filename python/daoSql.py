import sys
import mysql.connector
import logging
logging.basicConfig(filename='appCopiaImagenes.log', filemode='a', level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

# globales
conexion = None
idCorrida = None
cursorLectura = None
cursorModificaciones = None

queryInsertaRaizConNumeroDeCorrida = (
    "INSERT INTO corridaYcarpetaRaiz (pathRaiz, pathDestino) "
    "VALUES (%s, %s)"
)
queryInsertaNombresCarpeta = (
    "INSERT INTO nombresCarpetas (idCorrida, original, numeroDeArchivos) "
    "VALUES (%s, %s, %s)"
)
queryInsertaNombresArchivo = (
    "INSERT INTO nombresArchivos (idCorrida, original, alias, idregPadre) "
    "VALUES (%s, %s, %s, %s)"
)
queryMarcaArchivoNoCopiado = (
    "UPDATE nombresArchivos SET copiado = 0 "
    "WHERE idCorrida = %s AND idregPadre = %s AND original = %s"
)


"""
Marca en tabla nombresArchivos.copiado = 0
un registro que identifica el nombre de un archivo
que habrá que copiar manualmente con el nombre en nombresArchivos.alias;
pues el nombre del archivo y su alias entraron a la tabla nombresArchivos
pero el copiado falló por razón desconocida. 
Invocada cuando os.rename falla para el registro de
nombresArchivos identificado por idCorrida + idregPadre + original
"""
def marcaArchivoNoCopiado (idregCarpetaPadre, nombreOriginal):
    global idCorrida, queryMarcaArchivoNoCopiado, cursorModificaciones
    try:
        cursorModificaciones.execute(queryMarcaArchivoNoCopiado, 
                                (idCorrida, idregCarpetaPadre, nombreOriginal))
        conexion.commit()
    except:
        logging.error("cachada@daoSql.marcaArchivoNoRenombrado:", exc_info=True)
        sys.exit() # nada más que hacer
  

""" Establece la conexion a la base de datos mySQL y crea cursores de IO
    Los valores de sus argumentos se declaran en inicializaApp.py 
"""
def dameConexion(usuario=None, pasaporte=None, hostDeBD=None, baseDeDatos=None, puerto=None):
    global conexion, cursorLectura, cursorModificaciones
    if(conexion == None):
        try:
            conexion = mysql.connector.connect(
                user = usuario, 
                password = pasaporte,
                host = hostDeBD,
                database = baseDeDatos,
                port = puerto
            )
            cursorLectura = conexion.cursor(buffered=True)
            cursorModificaciones = conexion.cursor(buffered=True)
        except:
            logging.error("cachada", exc_info=True)
            sys.exit() # nada más que hacer
    return conexion

def commit():
    conexion.commit()



def cierraConexion():
    conexion.commit() #defensivamente por las dudas hacemos commit
    conexion.close()

def insertaPathRaiz_NumeraCorrida(pathRaiz, pathDestino) :
    global queryInsertaRaizConNumeroDeCorrida, cursorModificaciones
    try:
        cursorModificaciones.execute(queryInsertaRaizConNumeroDeCorrida, 
                                (pathRaiz,pathDestino))
        conexion.commit()
    except:
        ###PRUEBAS DE LINEAS DE MYSQL 
        cursorModificaciones.execute("SELECT MAX(idCorrida) FROM corridaYcarpetaRaiz")
        last_id = cursorModificaciones.fetchone()[0]

        # SET @sql = CONCAT('ALTER TABLE corridaYcarpetaRaiz AUTO_INCREMENT = ', @last_id);
        sql = f"ALTER TABLE corridaYcarpetaRaiz AUTO_INCREMENT = {last_id}"

        # PREPARE stmt FROM @sql;
        cursorModificaciones.execute("PREPARE stmt FROM %s", (sql,))

        # EXECUTE stmt;
        cursorModificaciones.execute("EXECUTE stmt")

        # DEALLOCATE PREPARE stmt;
        cursorModificaciones.execute("DEALLOCATE PREPARE stmt")
        ###
        logging.error("cachada@insertaPathRaiz_NumeraCorrida", exc_info=True)
        print(f"Inserción erronea en la base de datos y corrección")
        sys.exit() # nada más que hacer
    return cursorModificaciones.lastrowid

def setIdDeEstaCorrida(idDeEstaCorrida):
    global idCorrida
    idCorrida = idDeEstaCorrida

"""Inserta el nombre de carpeta visitada con su número de archivos.
    Regresa el valor del autoincrementable 'nombresCarpetas.idreg' asignado por mySQL,
    o regresa -1 cuando el alias está duplicado y no logra insertar en 'nombresArchivos'.
    Aborta ante cualquier otra excepcion."""
def insertaNombresCarpeta(elOriginal, numArchivosHijo):
    global idCorrida, queryInsertaNombresCarpeta, cursorModificaciones
    try:
        cursorModificaciones.execute(queryInsertaNombresCarpeta, 
                                (idCorrida, elOriginal, numArchivosHijo))
        conexion.commit()
    except:
        cursorModificaciones.execute('ROLLBACK')
        logging.error("cachada@daoSql.insertaNombresCarpeta", exc_info=True)
        raise
    return cursorModificaciones.lastrowid

"""Inserta el par de nombres (alias,original) referenciando la carpeta padre.
    regresa True si hay exito (es decir no hubo duplicados), o
            False si hay alias duplicado i.e. no hubo exito, o
    arroja ante cualquier otra excepcion diferente a error de integridad
    que presumiblemente suceda ante 'alias' duplicados."""
def insertaNombresArchivo(elOriginal, elAlias, idCarpetaPadre):
    global idCorrida, queryInsertaNombresArchivo, cursorModificaciones
    try:
        cursorModificaciones.execute(queryInsertaNombresArchivo, 
                                (idCorrida, elOriginal, elAlias, idCarpetaPadre))
        conexion.commit()
        return True
    except mysql.connector.errors.IntegrityError:
        return False
    except:
        cursorModificaciones.execute('ROLLBACK')
        logging.error("cachada@daoSql.insertaNombresArchivo", exc_info=True)
        logging.error(f"Nombre original: {elOriginal}, alias: {elAlias}, idReg carpeta padre: {idCarpetaPadre}")
        raise

""" Lee y despliega todos los registros de la tabla basuara. Codigo de referencia,
se puede eliminar. """
def leeYdespliegaTodosLosRegistros():
    global cursorLectura
    queryConsultar = ("SELECT * FROM nombresArchivos;")
    #Creamos un cursor con buffer (para que cargue de forma más óptima)
    #Con el comando .execute, ejecutamos el cursor con la función incluida entre paréntesis.
    cursorLectura.execute(queryConsultar)
    #Con fetchone y el while unicamente imprimiremos en pantalla el contenido de la tabla en la BD.
    # fetch de los registro leídos de la BD
    hayMasRegistros = cursorLectura.fetchone()
    # despliga los registros
    while hayMasRegistros:
        print(hayMasRegistros)
        hayMasRegistros = cursorLectura.fetchone()



