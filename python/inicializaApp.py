# en adelante no debe modificarse.
import os
import daoSql
import logging
logging.basicConfig(filename='appCopiaImagenes.log', filemode='a', level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

from pathlib import Path

# PATH de la carpeta RAIZ con archivos y carpetas a copiar.
# este path está restringido a 700 caracteres.
#pathRaiz = "/home/gerardo/repogit/copia_imagenes/copiador/rÁizDePruebas08"
pathRaiz = "C:\\Users\\CONTI SS\\Desktop\\originales\\Application_original"
#pathRaiz = "/home/gerardo/repogit/renombra_imagenes/renombrador/rÁizDePruebas 16"
#pathRaiz = "/home/gerardo/vmware/FotoMontajes"
#pathRaiz = "/home/gerardo/vmware/rÁizCopiáDePruebas"

# PATH DESTINO es la carpeta PADRE en donde una de sus SUBCARPETAS se
# harán las copias de archivos (cambiando sus nombres).
# El nombre de la SUBCARPETA lo pide el programa durante su inicialización.
#pathDestino = "/home/gerardo/repogit/copia_imagenes/copiador/conti_imagenesCentroDeDoc"
pathDestino = "C:\\Users\\CONTI SS\\Desktop\\clonados"

# Datos de la conexion QUE ES NECESARIO DEFINIR SUS VALORES:
usuario = "root"
pasaporte = "root"
hostDeBD = 'mysql'
baseDeDatos ='db'
puerto ='3306'



def inicializaSql():
    global usuario, pasaporte, hostDeBD, baseDeDatos, puerto
    daoSql.dameConexion(usuario, pasaporte, hostDeBD, baseDeDatos, puerto)

def damePathRaiz():
    global pathRaiz
    return pathRaiz

"""Como es conveniente separar archivos por su disco de proveniencia,
    fabricamos un nombre de subdirectorio y lo creamos como hijo del destino."""
gPathDestinoCreado = False
def damePathDestino():
    global pathDestino, gPathDestinoCreado
    if gPathDestinoCreado == False : # Al inicio creamos la subcarpeta de destino.
        try:
            p = Path(pathDestino)
            p.mkdir()
        except FileExistsError: #la carpeta PADRE de subcarpeta destino ya existe
            pass
        print("Hay que crear una subcarpeta con un nombre para la colección de imágenes o archivos.")
        subCarpeta = input("Introduce un nombre distintivo único: ")
        try:
            pathDestino = pathDestino + os.path.sep + subCarpeta
            print(os.path.sep)
            p = Path(pathDestino)
            p.mkdir()
        except FileExistsError:
            logging.warning("LA SUBCARPETA DE DESTINO YA EXISTE:", exc_info=True)
            print( "CUIDADO, LA SUBCARPETA DE DESTINO YA EXISTE.")
            continuo = input("Deseas que continue el programa (y,s,Y,S): ")
            if continuo.upper() != 'Y' and continuo.upper() != 'S':
                logging.warning(f"EL USUARIO ABORTÓ PORQUE LA SUBCARPETA {subCarpeta} DE DESTINO YA EXISTE:", exc_info=True)
                exit()
        except:
            logging.error("Error de damePathDestino():", exc_info=True)
            logging.info(f"{pathDestino}")
            raise
        gPathDestinoCreado = True
    return pathDestino
