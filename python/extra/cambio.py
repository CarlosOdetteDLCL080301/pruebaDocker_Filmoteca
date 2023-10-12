import os
directorio = "C:\\Users\\CONTI SS\\Desktop\\originales\\Application"
raiz = os.listdir(directorio)
sustituir = {'a':'á',
             'e':'é',
             'i':'í',
             'o':'ó',
             'u':'ú',
             'A':'Á',
             'E':'É',
             'I':'Í',
             'O':'Ó',
             'U':'Ú',
             'n':'ñ',
             'N':'Ñ'}

def cambiar_nombres_archivos(ruta,diccionario):
    # Obtener la lista de elementos en la carpeta
    elementos = os.listdir(ruta)

    # Iterar sobre los elementos
    for elemento in elementos:
        # Construir la ruta completa del elemento
        ruta_completa = os.path.join(ruta, elemento)
        
        # Si no es una carpeta, renombrarla
        if not os.path.isdir(ruta_completa):
            nuevo_nombre = elemento
            for clave, valor in diccionario.items():
                nuevo_nombre = nuevo_nombre.replace(clave, valor)
            
            # Construir la nueva ruta completa con el nuevo nombre
            nueva_ruta_completa = os.path.join(ruta, nuevo_nombre)

            # Renombrar la carpeta
            os.rename(ruta_completa, nueva_ruta_completa)
        # Si es una subcarpeta, llamar recursivamente a la función
        else:
            cambiar_nombres_archivos(ruta_completa,diccionario)

def cambiar_nombres_carpetas(ruta, diccionario):
    # Obtener la lista de elementos en la carpeta
    elementos = os.listdir(ruta)

    # Iterar sobre los elementos
    for elemento in elementos:
        # Construir la ruta completa del elemento
        ruta_completa = os.path.join(ruta, elemento)

        # Si es una carpeta, renombrarla y llamar recursivamente a la función
        if os.path.isdir(ruta_completa):
            nuevo_nombre = elemento
            for clave, valor in diccionario.items():
                nuevo_nombre = nuevo_nombre.replace(clave, valor)

            # Construir la nueva ruta completa con el nuevo nombre
            nueva_ruta_completa = os.path.join(ruta, nuevo_nombre)

            # Renombrar la carpeta
            os.rename(ruta_completa, nueva_ruta_completa)

            # Llamar recursivamente a la función para procesar subcarpetas
            cambiar_nombres_carpetas(nueva_ruta_completa, diccionario)

cambiar_nombres_archivos(directorio,sustituir)
cambiar_nombres_carpetas(directorio,sustituir)