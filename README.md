# pruebaDocker_Filmoteca
Estamos realizando pruebas para dockerizar, el programa mainAppCopia.py y que este mismo tenga una ejecución con la base de datos que previamente se crea, pero que tenga la capacidad de transportar este programa sin ningún problema. 

## Levantar los contenedores
Esto funcionará para crear y ejecutar contenedores basados en la configuración definida en nuestro archivo Docker Compose.
```
docker compose up -d
```
- "docker-compose": Este comando se utiliza para gestionar aplicaciones multi-contenedor definidas en un archivo Docker Compose.
- "up": se utiliza para crear y ejecutar los contenedores según la configuración definida en el archivo Docker Compose.
- "-d" (o --detach): Esta opción indica a Docker que debe ejecutar los contenedores en segundo plano (en modo "detach"). Esto significa que los contenedores se ejecutarán en segundo plano y no bloquearán la terminal actual. Podemos seguir utilizando la terminal para ejecutar otros comandos sin interrupción.

### Entrar a la configuración python
Vamos a necesitar abrir una sesión en bash de forma interactiva, en nuestro contenedor "pythonapp" (previamente definido así)
Esto nos permitirá acceder al entorno del contenedor y ejecutar comandos dentro del mismo. Esto se hace con el siguiente comando: 
```
docker compose exec pythonapp bash
```
- docker-compose: Es el comando principal para gestionar las aplicaciones multi-contenedor definidas en un archivo Docker Compose.
- exec: Este subcomando se utiliza para ejecutar un comando en el contenedor previamente definido.
- pythonapp: Es el nombre del contenedor en el que deseamos ejecutar el comando. Previamente en el Docker Compose, lo definimos y esto nos permite acceder especificamente a él
- bash: Esto especifica que deseamos abrir una sesión bash interactiva en el contenedor "pythonapp." Cuando lo ejecutamos, nos meterá al contenedor y podemos usar un shell bash para ejecutar comandos.

#### Entrar al bash del contenedor pythonapp
Una vez dentro del Shell de nuestro contenedor tenemos todo listo para ejecutar nuestro programa, entonces para ejecutarlo, procedemos a ejecutarlo con el siguiente comando desde bash
```
root@eeddfdd0a79e:/usr/app/src# python3 mainAppCopia.py
```
##### Ejecución del programa *mainAppCopia.py*
Cuando ejecutamos el programa, sí el programa nos pregunta la carpeta en la que se quiere crear y almacenar significa que el programa logra hacer la conexión con el contenedor de nuestra base de datos (MySQL)
![image](https://github.com/CarlosOdetteDLCL080301/pruebaDocker_Filmoteca/assets/54251397/768b393b-1d46-4e43-88c4-00b5d847bbeb)

Entonces al momento de ingresar el nombre de esta nueva carpeta, nos mostrará el registro correcto o erroneo de nuestro programa
![image](https://github.com/CarlosOdetteDLCL080301/pruebaDocker_Filmoteca/assets/54251397/3caf9809-e9cf-4506-8632-d4558234b385)

En este punto ya tenemos la ejecución del programa correctamente, ya que nos creó los archivos en la carpeta designada en <em>inicializaApp.py</em> ,esta dirección almacena nuestra nueva carpeta y la adaptación del nombre.
![image](https://github.com/CarlosOdetteDLCL080301/pruebaDocker_Filmoteca/assets/54251397/baf48833-da8f-4f4b-b254-3828e5db7006)

### Comprobar el almacenamiento de estos registros en MySQL
Vamos a necesitar abrir una sesión en bash de forma interactiva, en nuestro contenedor "mysql" (previamente definido así)
Esto nos permitirá acceder al entorno del contenedor y ejecutar comandos dentro del mismo, que nos permitirá visualizar el contenido de nuestra base de datos (*db*). Esto se hace con el siguiente comando: 
```
docker compose exec mysql bash
```
- docker-compose: Es el comando principal para gestionar las aplicaciones multi-contenedor definidas en un archivo Docker Compose.
- exec: Este subcomando se utiliza para ejecutar un comando en el contenedor previamente definido.
- mysql: Es el nombre del contenedor en el que deseamos ejecutar el comando. Previamente en el Docker Compose, lo definimos y esto nos permite acceder especificamente a él
- bash: Esto especifica que deseamos abrir una sesión bash interactiva en el contenedor "pythonapp." Cuando lo ejecutamos, nos meterá al contenedor y podemos usar un shell bash para ejecutar comandos.

#### Entrar al bash del contenedor mysql
Para entrar al entorno de MySQL, es necesario acceder de la siguiente forma, en la que nos solicitaŕa nuestros datos para permitirnos acceder en modo root, sin embargo son los valores especificados previamente en el *Docker-Compose.yml*
```
bash-4.4# mysql -u root -p
```
El comando anterior, nos solicitará nuestra contraseña, en nuestro caso en las variables de entorno declaramos que la contraseña del usuario root, es *root*, una vez ejecutado nos dara acceso a MySQL. Como se muestra en la imagen a continuación:
![image](https://github.com/CarlosOdetteDLCL080301/pruebaDocker_Filmoteca/assets/54251397/8bab4d7b-fae3-4b25-911c-cd5882bab222)
##### Comprobar que se crearon correctamente las tablas
Si queremos comprobar que nuestra base de datos y sus respectivas tablas se crearon correctamente, entonces procedemos a visualizar el contenido de la base de datos, para comprobar que coincida con el nuestro.
```
mysql> use db; show tables;
```

Una vez ejecutado el comando, podemos ver que nuestro archivos de hace un rato, si se registraron en nuestra base de datos, con el siguiente comando
```
mysql> SELECT * FROM nombresArchivos;
```
En nuestro caso, al ser la unica y primer ejecución nos aparece el siguiete resultado:
![image](https://github.com/CarlosOdetteDLCL080301/pruebaDocker_Filmoteca/assets/54251397/1c83c4f9-619b-46a7-943a-ae37ec31922c)

## Eliminar contenedores
En el caso que necesitemos eliminar por alguna razón nuestro contenedor unicamente dependemos de un comando extenso, el cual es el siguiente:
```
docker compose down --rmi all
```
El cual utilizaremos para detener y eliminar imagenes, network y contenedores definidos en el archivo Docker Compose.
- down: El subcomando "down" se utiliza para detener y eliminar servicios y contenedores definidos en el archivo Docker Compose. También puede realizar otras tareas de limpieza, según las opciones que se le pasen.
- --rmi all: Esta opción se utiliza para eliminar todas las imágenes de contenedores que se crearon para los servicios definidos en el archivo Docker Compose.
