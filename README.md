# pruebaDocker_Filmoteca
Estamos realizando pruebas para dockerizar, el programa mainAppCopia.py y que este mismo tenga una ejecución con la base de datos que previamente se crea, pero que tenga la capacidad de transportar este programa sin ningún problema. 

## Construcción de los contenedores

### Levantar los contenedores
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
