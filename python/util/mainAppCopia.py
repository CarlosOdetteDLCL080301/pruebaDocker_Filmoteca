"""
Instrucciones de uso.

1) De ser necesario, hay que montar el drive en que recide la carpeta raiz
 de un sistema de archivos a copiar.
2) Hay que modificar 'pathRaiz' en inicializaApp.py con la ruta a la carpeta raiz.
3) Hay que modificar 'pathDestino' en inicializaApp.py con la ruta a la carpeta 
a donde se van a copiar todas las imagenes.
3) Finalmente, ejecutar este programa (mainAppCopia.py).

NOTAS IMPORTANTES ANTE FALLOS.
1) si el path de una carpeta tiene nombre demasiado largo (esto es 4096 o mas caracteres o más)
 no cabe en el campo de la tabla, entonces:
    # Truncamos el path original completo para poder continuar.
    poniéndole el prefijo *truncada* bajo la siguiente lógica en logicaDelPrograma.py
    if len(rutaCompletaOriginal) > 4095 : 
        # 4084 viene de 4095 restándole 10 del prefijo '*truncada*'
        rutaCompletaOriginal = "*truncada*"+
                      rutaCompletaOriginal[len(rutaCompletaOriginal)-4084:]
        
2) cuando el copiado de un archivo falla,
continuamos sin copiar el archivo pero marcamos su registro correspondiente
con el valor 0 (cero) en el campo nombresArchivos.copiado
de manera que estos fallos se corrijan manualmente para el archivo con nombre indicado en
la tabla y registro correspondiente. 

Note que appCopiaImagenes.log también tiene estos registros para verificar lo que quede en SQL.
Note que los campos nombresCarpetas.renombrada o nombresArchivos.renombrado por
omisión tiene el valor 1 (uno) el cual se cambia a cero ante un correspondiente 
fallo de os.rename()

"""
import serviciosCopia as servicios
import inicializaApp as init
import logicaDelPrograma as ldp
import logging
import datetime
logging.basicConfig(filename='appCopiaImagenes.log', filemode='a', level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

fechaHora = datetime.datetime.now()

logging.info("\n\n***************************** NUEVA CORRIDA *******************")
logging.info("\n****** HORA DE INICIO DE LA CORRIDA: %s" %fechaHora)
print("\n****** HORA DE INICIO DE LA CORRIDA: %s" %fechaHora)


init.inicializaSql()

""" Asegurate de que no estamos repitiendo una corrida
    y, si no, entonces genera el número de corrida
    y asígnalo al modulo daoSQL. """
origen = init.damePathRaiz()
print("raiz de origen:"+origen)
destino = init.damePathDestino()
print("path destino:"+destino)
servicios.registraPathsDeRaiz_y_Destino_y_NumeraCorrida(origen, destino)

# Haz el trabajo.
ldp.recorreArbolCopiandoYCambiandoNombres(origen, destino)

servicios.commitSql()     
servicios.cierraConexionSql()

fechaHora = datetime.datetime.now()
logging.info("\n****** HORA DE TERMINACION DE LA CORRIDA: %s" %fechaHora)
print("\n****** HORA DE TERMINACION DE LA CORRIDA: %s" %fechaHora)