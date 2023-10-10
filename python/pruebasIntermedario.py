import paramiko
import shutil

# Configuramos los parámetros de conexión
host = "192.168.1.1"
port = 22
username = "user"
password = "password"

# Creamos un objeto SSHClient
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port, username, password)

# Creamos un objeto sftp
sftp = ssh.open_sftp()

# Obtenemos la lista de archivos de la carpeta remota
remote_path = "/home/users/IntentoRemoto1"
remote_files = sftp.listdir(remote_path)

# Recorremos la lista de archivos
for file in remote_files:

    # Obtenemos el nombre del archivo
    filename = file

    # Creamos el path local
    local_path = "C:\\Users\\CONTI SS\\Desktop\\Filmoteca\\Proporcionado\\tmp" + filename

    # Descargamos el archivo
    sftp.get(remote_path + "/" + filename, local_path)

# Cerramos el objeto sftp
sftp.close()

# Cerramos el objeto SSHClient
ssh.close()
