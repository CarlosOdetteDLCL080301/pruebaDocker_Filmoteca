"""
define varias funciones consideradas 'utilerías'
"""

import daoSql
import random
import sys
import logging
logging.basicConfig(filename='appCopiaImagenes.log', filemode='a', level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

"""
Inserta el path de la raiz de esta corrida en la tabla 'carpetasRaiz'.
Este path debe ser único y se inserta sin alterar sus caracteres.

Argumentos: 
'carpetasRaiz' es la cadena que describe el path de la raiz de la corrida.

Valor que toma la función ante éxito: el idCorrida que le corresponde al 
registro del path de la raiz de corrida insertada.

Descripción:

el daoSQL insertaPathRaiz_NumeraCorrida() invocado, regresa
el idCorrida del registro insertado que se utilizará
en todas las inserciones de nombres+alias de carpetas y archivos
por debajo del path de la raiz.
Cuando el path resulta duplicado levanta Excepcion y debe abortar
pues no hay más que hacer.
"""
def registraPathsDeRaiz_y_Destino_y_NumeraCorrida(pathRaiz, pathDestino) :
    idDeEstaCorrida = -1
    idDeEstaCorrida = daoSql.insertaPathRaiz_NumeraCorrida(pathRaiz, pathDestino)
    if idDeEstaCorrida == -1 :
        logging.info("********* Probablemente pathRaiz duplicada ***************")
        sys.exit()
    daoSql.setIdDeEstaCorrida(idDeEstaCorrida)
    logging.info(f"idDeEstaCorrida:{idDeEstaCorrida} \n RAIZ:{pathRaiz} \n DESTINO: {pathDestino}\n")

"""
Inserta nombre original de una carpeta en tabla 'nombresCarpetas'.

Argumentos: 
'original' es la cadena con un nombre de carpeta original,
'numArchivosEnCarpeta' es el número de archivos que contiene la
carpeta de acuerdo a os.walk().

Valor que toma la función ante éxito: instancia de Valores con
el idreg del registro insertado y el alias definitivo para la carpeta.

Descripción:

el daoSQL insertaNombresCarpeta() invocado, regresa
el idreg del registro insertado que se utilizará
al insertar los nombres+alias de sus archivos;
cuando el alias resulta duplicado insertaNombresCarpeta() regresa -1.
Ante duplicados, esta función lo reintenta hasta 100 veces, incrementando en 1 
el sufijo entero, después de 100 intentos que no pueda lograrse
la inserción, levanta Excepcion.

Note que cuando un path es mayor a 1023 caracteres,
el path se trunca y en appCopiaImagenes.log se registra como ẄARNING.
"""
def insertaNombreDeCarpeta(rutaCompletaOriginal, numArchivosEnCarpeta) :
    nombreTruncado = False
    rutaCompletaOrTruncada = rutaCompletaOriginal
    # si la carpeta tiene nombre demasiado largo para la tabla, aborta!
    # Truncamos el path original completo para poder continuar.
    if len(rutaCompletaOriginal) > 4095 : 
        nombreTruncado = True
        # 4084 viene de 4095 - 10 del prefijo '*truncada*'
        rutaCompletaOrTruncada = "*truncada*"+rutaCompletaOriginal[len(rutaCompletaOriginal)- 4084:]
    
    idregPadre = daoSql.insertaNombresCarpeta(rutaCompletaOrTruncada, numArchivosEnCarpeta)
 
    if nombreTruncado:
        logging.warning(f"*RUTA TRUNCADA carpeta de más de 4095 caracteres! En NombresCarpeta.idReg:{idregPadre}")
        logging.warning(f"*RUTA COMPLETA:{rutaCompletaOriginal}")
        logging.warning(f"*RUTA TRUNCADA:{rutaCompletaOrTruncada}")

    return idregPadre


"""
Inserta alias único y nombre original de un archivo en tabla 'nombresArchivos'.

Argumentos: 
'original' es la cadena con un nombre de archivo original,
'argAlias'  es la cadena obtenida de 'original' después de reemplazar
            los caracteres "latinos" y espacios que no acepta LTFS,
'idPadre' es el idreg del nombre de la carpeta padre del archivo
          en la tabla sql 'nombresCarpetas'

La función entrega el valor del 'alias' finalmente insertado cuando hay éxito,
si no logra la inserción, hay dos posibilidades:
   1) 'raise' o arroja la Excepcion desconocida que viene de invocar daoSql.insertaNombresArchivo.
   2) regresa la cadena vacía "" porque intentó la inserción con 100 'alias' aleatorios
      lo que la funcion que usa este servicio debe de manejar.

Descripción:
El daoSQL.insertaNombresArchivo() que se invoca, 
1. regresa True cuando logra la inserción, 
2. regresa False cuando el alias resulta duplicado.
3. arroja excepción desconocida.

La lógica se apoya con UNIQUE INDEX SQL de la columna nombresArchivos.alias,
pues no permite alias duplicados, y detecta al insertar como error de integridad
en la funcion invocada daoSql.insertaNombresArchivo(), que en tal caso entrega
False como el valor que se asigna a 'exitoEnLaInsercionSQL'.

Ante duplicados, esta función reintenta insertar hasta 100 veces, 
variando un sufijo aleatorio para el argAlias.
 , después de 100 intentos que no pueda lograrse
la inserción, levanta Excepcion."""
def insertaNombreDeArchivoYsuAlias(original, argAlias, idPadre) :
    exitoEnLaInsercionSQL = False
    i = 0
    alias = None
    while not exitoEnLaInsercionSQL and i < 100 :
        if i != 0: # la segunda vez en adelante, agregamos un sufijo aleatoreo de 6 digitos
            alias = argAlias+str(int(10**6*random.random()))
        else : 
            """ la primera vez intentamos con el alias obtenido 
                   al eliminar - ninguno o más - caracteres no aceptados por LTFS.
                   Note que el nombre podría ser igual al alias. """
            alias = argAlias
        exitoEnLaInsercionSQL = daoSql.insertaNombresArchivo(original, alias, idPadre)
        i += 1
    if i >= 100:
        return "" # entregamos la cadena nula indicando que el archivo no se copiará
    
    return alias

"""
out       
def marcaCarpetaNoRenombrada(idreg):
    daoSql.marcaCarpetaNoRenombrada(idreg)
"""

def marcaArchivoNoCopiado(idPadre, nombreOriginal):
    daoSql.marcaArchivoNoCopiado(idPadre, nombreOriginal)

def commitSql():
    daoSql.commit()

def cierraConexionSql():
    daoSql.cierraConexion()
    