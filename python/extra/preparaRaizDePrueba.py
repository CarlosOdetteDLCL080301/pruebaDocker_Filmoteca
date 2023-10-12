"""
PRUEBA LOCAL
1) Utilizando este programa, se copia una jerarquía de carpetas - subcarpetas - y archivos 
de prueba. El destino de esta copia se establece como argumento a la invocación de
shutil.copytree() que se hace en la última línea de este archivo: preparaRaizDePrueba.py.
Puede también cambiarse el origen de esta copia de ser necesario.

2) Ejecuta el programa 'mainAppRenombra.py' sobre la copia de carpetas de prueba,
esto requiere modificar la global 'pathRaiz' en 'inicializaApp.py'.
Ver comentarios al inicio de 'mainAppRenombra.py'

Nota: Así se monta el remoto:
sudo mount -t cifs //192.168.10.1/S4_3 /home/gerardo/vnx -o username=Administrator,password='secreto',rw,dir_mode=0777,file_mode=0777
"""
import shutil

#    try:
#       shutil.rmtree("rÁizCopiáDePruebas6")
#   except:
#       pass

shutil.copytree(
    #"rAizDePruebas_16",
    "rÁizOriginalDePrúebaParaCopiarNoAlterar", # origen
    #"/home/gerardo/vnx/rÁizDePruebas26", #destino
    #"rÁizDePruebas01", #destino
    #"/home/gerardo/vnx/rÁizCopiáDePruebas", #destino
    "/home/gerardo/vmware/raizCopiaDePruebas", #destino
    symlinks=True, dirs_exist_ok=False)