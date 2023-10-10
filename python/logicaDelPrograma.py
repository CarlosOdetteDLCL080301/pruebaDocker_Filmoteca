

import sys
import os
import re
import datetime
import shutil
import serviciosCopia as servicios
import inicializaApp as init
import logging
logging.basicConfig(filename='appCopiaImagenes.log', filemode='a', level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

# Esto no es lo mas ortodoxo pero sirve para ver la consola feedback y 
# saber que el programa va avanzndo y al final datos del proceso.
contadorCarpetasProcesadas  = 0 
contadorCarpetasInsertadas = 0
contadorCarpetasNoInsertadasEnSQL = 0
contadorArchivosProcesados  = 0 
contadorArchivosCopiados = 0
contadorArchivosEnSQL_NoCopiados = 0
contadorArchivosNiEnSQL_NiCopiados = 0


"""deslpliega el error de os.walk()"""
def maneja_error_de_os_walk(instanciaOsError):
    logging.error("error de os.walk:", exc_info=True)
    logging.error("codigo de error:\n"+instanciaOsError.strerror)
    sys.exit()


#----------------------------------------------------

def obtenAliasSinCaracteresNoAdmitidos(nombreOriginal) :
      # reemplazamos vocales acentuadas, eñes y 'ü' con diéresis
    nuevo = nombreOriginal.replace("Á", "A").replace(
        "É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U")
    nuevo = nuevo.replace("á", "a").replace("é", "e").replace(
        "í", "i").replace("ó", "o").replace("ú", "u")
    nuevo = nuevo.replace("Ñ", "NI").replace(
        "ñ", "ni").replace("Ü", "U").replace("ü", "u").replace("ä","a").replace("ë","e").replace("ï","i").replace("ö","o").replace("ü","u").replace("Ä","A").replace("Ë","E").replace("Ï","I").replace("Ö","O").replace("Ü","U")
    # finalmente reemplazamos uno o más espacios por un guión bajo
    nuevo = re.sub("\s+", "_", nuevo)
    return nuevo

def recorreArbolCopiandoYCambiandoNombres(carpetaRaiz, carpetaDestino):
    """
    se asume que el argumento es la raiz de una carpeta porque
    no estamos checando en esta funcion que el argumento en efecto lo sea

    """
    global contadorCarpetasProcesadas 
    global contadorCarpetasNoInsertadasEnSQL 
    global contadorCarpetasInsertadas
    global contadorArchivosProcesados 
    global contadorArchivosCopiados
    global contadorArchivosEnSQL_NoCopiados
    global contadorArchivosNiEnSQL_NiCopiados
    
    for rutaDeCarpeta, carpetas, archivos in os.walk(carpetaRaiz,False, maneja_error_de_os_walk):
        #old iUltimoSlash = rutaDeCarpeta.rfind(os.path.sep)
        #old aliasRutaPropuesto = obtenAliasSinCaracteresNoAdmitidos(rutaDeCarpeta[iUltimoSlash:])
        try:
            idRegPadre = servicios.insertaNombreDeCarpeta(rutaDeCarpeta, len(archivos))
            contadorCarpetasInsertadas +=1
        except:
            contadorCarpetasNoInsertadasEnSQL +=1
            logging.error("Error al insertar en nombresCarpetas:", exc_info=True)
            logging.error(f"Carpeta fallida y ningun archivo copiado:", rutaDeCarpeta)
            continue # ignoramos procesar sus archivos omitiendo el siguiente ciclo
        for nombreDeArchivo in archivos:
            # Ahora hay que obtener el nombre único del archivo,
            # para este efecto, inserta en la tabla 'nombresArchivos' la siguiente invocación.
            copiaArchivoConNombreUnico(rutaDeCarpeta, idRegPadre, nombreDeArchivo, carpetaDestino)
            # Feedback a la consola cada 200 archivos
            contadorArchivosProcesados += 1
            feedBack = contadorArchivosProcesados % 200
            if feedBack == 0 :
                fechaHora = datetime.datetime.now()
                print("\nFECHA HORA: %s" %fechaHora)
                print(f"Llevamos {contadorArchivosProcesados} archivos procesados.")
                logging.info("FECHA HORA: %s" %fechaHora)
                logging.info(f"Llevamos {contadorArchivosProcesados} archivos procesados.")
        contadorCarpetasProcesadas +=1

    
    # Para terminar, reporta cantidades
    print(f"Total de carpetas  PROCESADAS: {contadorCarpetasProcesadas}")
    logging.info(f"Total de carpetas  PROCESADAS: {contadorCarpetasProcesadas}")
    
    print(f"Total de carpetas INSERTADAS: {contadorCarpetasInsertadas}")
    logging.info(f"Total de carpetas INSERTADAS: {contadorCarpetasInsertadas}")
    
    print(f"Total de carpetas NO insertadas en SQL: {contadorCarpetasNoInsertadasEnSQL}")
    logging.info(f"Total de carpetas NO insertadas en SQL: {contadorCarpetasNoInsertadasEnSQL}")
    
    sumaDeCasosDeCarpetas = contadorCarpetasNoInsertadasEnSQL+contadorCarpetasInsertadas
    
    logging.info(f"Suma de 3 casos para capetas (debe igaular a procesadas): {sumaDeCasosDeCarpetas}")    
    if(sumaDeCasosDeCarpetas != contadorCarpetasProcesadas or contadorCarpetasNoInsertadasEnSQL != 0):
        logging.error("********** FRACASO, NO COINCIDEN LAS CIFRAS DE CONTROL PARA CARPETAS ")
        print("********** FRACASO, NO COINCIDEN LAS CIFRAS DE CONTROL PARA CARPETAS ")
    else:
        logging.info("********* SUMAS DE CONTROL PARA CARPETAS OK")
        print("********* SUMAS DE CONTROL PARA CARPETAS OK")
    
    print(f"Total de archivos  procesados: {contadorArchivosProcesados}")
    logging.info(f"Total de archivos  procesados: {contadorArchivosProcesados}")

    print(f"Total de archivos copiados: {contadorArchivosCopiados}")
    logging.info(f"Total de archivos copiados: {contadorArchivosCopiados}")

    print(f"Total de archivos en SQL NO copiados: {contadorArchivosEnSQL_NoCopiados}")
    logging.info(f"Total de archivos en SQL NO copiados: {contadorArchivosEnSQL_NoCopiados}")

    print(f"Total de archivos Ni en SQL Ni copiados: {contadorArchivosNiEnSQL_NiCopiados}")
    logging.info(f"Total de archivos Ni en SQL Ni copiados: {contadorArchivosNiEnSQL_NiCopiados}")

    sumaDeCasosDeArchivos = contadorArchivosCopiados+contadorArchivosEnSQL_NoCopiados+contadorArchivosNiEnSQL_NiCopiados
    logging.info(f"Suma de 3 casos para archivos (debe igaular a procesados): {sumaDeCasosDeArchivos}")
    if(sumaDeCasosDeArchivos != contadorArchivosProcesados or contadorArchivosEnSQL_NoCopiados != 0 or
    contadorArchivosNiEnSQL_NiCopiados != 0):
        logging.error("********** FRACASO, NO COINCIDEN LAS CIFRAS DE CONTROL PARA ARCHIVOS ")
        print("********** FRACASO, NO COINCIDEN LAS CIFRAS DE CONTROL PARA ARCHIVOS ")
    else:
        logging.info("********* EXITO, SUMAS DE CONTROL PARA ARCHIVOS OK")
        print("********* EXITO, SUMAS DE CONTROL PARA ARCHIVOS OK")
    

"""    
    ADVERTENCIA IMPORTANTE.*****************
    Cuando a la entrada hay dos carpetas que difieren de nombre, pero
    al cambiar sus nombres estos son iguales. Se perderá para siempre
    el primero que resulta duplicado.
    """
def copiaArchivoConNombreUnico(rutaDeCarpetaPadreOriginalCompleta, idPadre, nombreOriginal, carpetaDestino) :
    global contadorArchivosCopiados, contadorArchivosEnSQL_NoCopiados
    global contadorArchivosNiEnSQL_NiCopiados

    try:
        aliasPropuesto = obtenAliasSinCaracteresNoAdmitidos(nombreOriginal)
        alias = servicios.insertaNombreDeArchivoYsuAlias(nombreOriginal, aliasPropuesto, idPadre)
    except:
        logging.error(f"*Error desconicido :{rutaDeCarpetaPadreOriginalCompleta + os.path.sep + nombreOriginal}")
        logging.error("@logicaDelPrograma.copiaArchivoConNombreUnico:", exc_info=True)
        logging.info(f"{rutaDeCarpetaPadreOriginalCompleta + os.path.sep + nombreOriginal} :alias fallido:{aliasPropuesto} :idPadre: {idPadre}")
        return #regresamos para continuar con el siguiente archivo

    if(alias != "") : #copio solo cuando se que el alias es único y se insertó en SQL.
        try:
            shutil.copyfile(rutaDeCarpetaPadreOriginalCompleta + os.path.sep + nombreOriginal,
                    carpetaDestino + os.path.sep + alias)
            contadorArchivosCopiados += 1
        except:
            # como por alguna razon desconocida falló copiar el archivo,
            # lo informamos al log
            contadorArchivosEnSQL_NoCopiados += 1
            logging.error(f"*EnTableSQL_NoCopiado:{rutaDeCarpetaPadreOriginalCompleta + os.path.sep + nombreOriginal}")
            logging.error("error de shutil.copyfile@logicaDelPrograma.copiaArchivoConNombreUnico:", exc_info=True)
            logging.info(f"{rutaDeCarpetaPadreOriginalCompleta + os.path.sep + nombreOriginal} :alias fallido:{aliasPropuesto} :idPadre: {idPadre}")
            servicios.marcaArchivoNoCopiado(idPadre, nombreOriginal)
    else:
        logging.info(f"*NiEnTablaSQL_NiCopiado:{rutaDeCarpetaPadreOriginalCompleta + os.path.sep + nombreOriginal}")
        contadorArchivosNiEnSQL_NiCopiados +=1

