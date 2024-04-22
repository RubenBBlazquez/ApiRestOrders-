# ApiRestOrders-
Api Rest to get orders and products from mysql using hexagonal architecture.

## Como ejecutar el proyecto
#### Lo primero que tendremos que hacer será configurar las variables de entorno, para ello en la carpeta de config tendrás un .env_sample, al ser credenciales de mysql, el .env nunca se sube a github, por lo que tendrás que coger el **.env_sample**, y renombrarlo a **.env**, tiene la siguiente forma:
```
MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=orders
MYSQL_USER=root
MYSQL_HOST=db
MYSQL_PORT=3306
```
Por defecto está puesta la credencial de root como root, pero eres libre de ponerla lo dificil que quieras!

#### Instalaremos las dependencias mediante el fichero requirements.txt ejecutando el siguiente comando:
```
pip install -r requirements.txt
```

#### Tras instalar las dependencias ejecutaremos el siguiente comando:
```
python manage.py setup_project
```
este comando se encargará de lanzar el servicio de mysql y el servidor de django mediante docker

#### Si no quieres instalar las dependencias en tu ordenador, y conoces docker compose, puedes ahorrarte los 2 pasos anteriores, el de las dependencias y el del comando, ejecutando lo siguiente estando en la raiz del proyecto:
```
docker compose up --build -d
```

#### Una vez tengamos los servicios levantados, podremos acceder al api desde la siguiente URL:
```
http://localhost:8080/
```

#### Cuando ya esté todo funcionando, podemos ver una prueba de los endpoints en PostMan mediante el siguiente fichero que se encuentra en la ruta del proyecto:
```
ApiRestPedidos.postman_collection.json
```
