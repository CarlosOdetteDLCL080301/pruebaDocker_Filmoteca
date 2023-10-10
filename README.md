# pruebaDocker_Filmoteca
Estamos realizando pruebas para dockerizar, el programa mainAppCopia.py y que este mismo tenga una ejecución con la base de datos que previamente se crea, pero que tenga la capacidad de transportar este programa sin ningún problema. 

## Construcción de los contenedores
Esto funcionará para crear y ejecutar contenedores basados en la configuración definida en nuestro archivo Docker Compose.
```
docker compose up -d
```
- "docker-compose": Este comando se utiliza para gestionar aplicaciones multi-contenedor definidas en un archivo Docker Compose.
- "up": se utiliza para crear y ejecutar los contenedores según la configuración definida en el archivo Docker Compose.
- "-d" (o --detach): Esta opción indica a Docker que debe ejecutar los contenedores en segundo plano (en modo "detach"). Esto significa que los contenedores se ejecutarán en segundo plano y no bloquearán la terminal actual. Podemos seguir utilizando la terminal para ejecutar otros comandos sin interrupción.
