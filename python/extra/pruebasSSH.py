#Importamos el metodo getpass de la biblioteca getpass
from getpass import getpass
import os
#Importamos la biblioteca paramiko el cual nos ayudará a establecer una conexión por ssh, ftp y ctp
import paramiko
#Importamos el metodo sleep de la biblioteca 
from time import sleep
#Aqui se agrega la IP a la cual se conectará



host = "192.168.0.131"
#Se agrega el usuario con el que se conectará al servidor
user = 'odette2001'
psswrd = 'odette2001'


"""if __name__ == '__main__':
    try:
        #Asignamos la clase paramiko en la variable client 
        client = paramiko.SSHClient()
        client.load_host_keys('C:\\Users\\CONTI SS\\.ssh\\known_hosts')
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #Se solicita contraseña, pero se busca la seguridad del servidor al que se accederá, es un "input" seguro
        #psswrd = getpass('Ingresa tu contraseña:\t')
        #Se intenta establecer una conexión con los datos proporcionados
        client.connect(host,username=user,password=psswrd)
        #Esta igualdad retorna tres valores los cuales retornará, sin embargo, solo usaremos stdout
        stdin, stdout, stderr = client.exec_command('mkdir -p AlmacenamientoExterno')
        #Sirve para "sincronizar", ya que a veces la conexión puede estar lenta
        sleep(1)
        #esto permite que sea posible leer la terminal del servidor en nuestra terminal remota
        result = stdout.read().decode()
        #Se visualiza la terminal del servidor SSH 
        print(result)
        #Es necesario cerrar la conexión
        client.close()
    #Esta except surge cuando no logra autenticarse con el servidor
    except paramiko.ssh_exception.AuthenticationException as e:
        print('La autentificación falló')
"""

import paramiko
import shutil

# Configuramos la conexión SSH
host = "192.168.0.131"
username = "odette2001"
password = "odette2001"
port = 22

# Obtenemos la ruta de la carpeta específica
remote_folder = "/home/users/IntentoRemoto1/"
local_folder = "C:\\Users\\CONTI SS\\Desktop\\Filmoteca\\Proporcionado\\tmp"

"""
import paramiko

# Configuramos la conexión SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host,port,username, password)

# Obtenemos la ruta de la carpeta específica
ruta_carpeta = "/home/users/IntentoRemoto1/"
ruta_destino = "C:\\Users\\CONTI SS\\Desktop\\Filmoteca\\Proporcionado\\tmp"
# Creamos un objeto SFTPClient para la carpeta específica
sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())

# Iteramos sobre los archivos y carpetas de la carpeta específica
for archivo in sftp.listdir(ruta_carpeta):
    # Obtenemos los atributos del archivo
    lstatout = str(sftp.lstat(ruta_carpeta + "/" + archivo)).split()[0]

    # Si el archivo es una carpeta, lo imprimimos
    if 'd' in lstatout:
        print("\n"+archivo + " is a directory")
        print(ruta_carpeta+'/'+archivo,ruta_destino)
        sftp.get(ruta_carpeta+'/'+archivo,ruta_destino)

    # Si el archivo es un archivo, lo imprimimos
    else:
        print("\n"+archivo + " is a file")
        print(archivo,ruta_destino+"\\"+archivo)
        #sftp.get(archivo,ruta_destino+"\\"+archivo)
    
# Cerramos la conexión SSH
ssh.close()
"""

import os
# Establecer la conexión SSH
client = paramiko.SSHClient()
client.load_host_keys('C:\\Users\\CONTI SS\\.ssh\\known_hosts')
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host,port,username,password)

remoto = "/home/users/IntentoRemoto1"
local = "C:\\Users\\CONTI SS\\Desktop\\Filmoteca\\Proporcionado\\tmp"

sftp = client.open_sftp()

sftp.get("/home/users/IntentoRemoto1/hola/ana.txt","/tmp/ana.txt")
sftp.close()
