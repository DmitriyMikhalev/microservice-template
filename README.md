[![microservice template workflow](https://github.com/DmitriyMikhalev/microservice-template/actions/workflows/microservice_workflow.yaml/badge.svg?branch=main)](https://github.com/DmitriyMikhalev/microservice-template/actions/workflows/microservice_workflow.yaml)

# Microservice template
------------
This project is a microservice template based on Django REST Framework, nginx, Gunicorn. When using it, you don't need to configure the basic working environment, connect to the database, link containers and perform other routine tasks.

The structure contains the simplest example of the API part of the TODO project, in which serializers, JWT authentication, CRUD views, logger, endpoints (including metrics from prometheus), tests, and auto-documentation are created, used as an example of your microservice.

# Installation and local deploy
Follow these simple steps to local deploy.
* Clone the repo:
```
git clone git@github.com:DmitriyMikhalev/microservice-template.git
```
* Create .env file using sample.env and put it at infra directory
* Make sure the Docker app is working and start docker-compose:
```
docker-compose up -d
```
* Apply migrations at backend container
```
docker-compose exec microservice_backend python manage.py migrate
```
* Collect static files for admin panel
```
docker-compose exec microservice_backend python manage.py collectstatic --noinput
```
* App is available. Follow the link and make sure it's working
```
http://localhost/redoc/
```

# Deploy at server
If you want to deploy this project on remote host, follow the instruction
* Connect to the server
* Make sure you have already installed docker and docker-compose
* Clone the repo
```
git clone git@github.com:DmitriyMikhalev/microservice-template.git
```
* Locally change infra/nginx.conf: write your server IP at 'server_name'
* Clone nginx config file and infra directory to server:
```
scp nginx.conf <username>@<server>:/etc/nginx/conf.d/default.conf
scp -r infra <username>@<server>:/home/<username>/app/docker-compose.yaml
```
* Create .env file. Sample you can find at infra directory
* Open infra directory and start containers
```
sudo docker-compose up -d
```
* Service is available on your server.
* Don't forget to migrate data and collect static.

# Available API endpoints 

------------

List of available endpoints see at documentation using http://<host>:80/redoc/ or http://<host>:80/swagger/.