import hashlib
import os

def calcular_checksum_archivo(archivo):
    hasher = hashlib.md5()
    with open(archivo, 'rb') as f:
        while True:
            data = f.read(4096)  # Lee datos por bloques
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

def calcular_checksum_carpeta(carpeta):
    checksums = []
    for directorio_raiz, directorios, archivos in os.walk(carpeta):
        for archivo in archivos:
            ruta_archivo = os.path.join(directorio_raiz, archivo)
            checksum = calcular_checksum_archivo(ruta_archivo)
            checksums.append(checksum)
    # Combinar los checksums individuales para obtener un checksum global de la carpeta
    checksum_global = hashlib.md5(''.join(checksums).encode()).hexdigest()
    return checksum_global

carpeta_a_verificar = 'C:\\Users\\CONTI SS\\Desktop\\originales\\Application_original'
checksum_carpeta = calcular_checksum_carpeta(carpeta_a_verificar)
print(f'Checksum global de la carpeta: {checksum_carpeta}')
