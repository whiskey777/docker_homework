# docker_homework
# 1 Лекция
Написать Dockerfile для frontend располагается в директории /frontend, собрать и запустить
# 2 Лекция
Написать Dockerfile для backend который располагается в директории /lib_catalog(для сборки контейнера необходимо использовать файл /lib_catalog/requirements.txt), для работы backend необходим postgresql, т.е. необходимо собрать 2 контейнера:
1. backend
2. postgresql

Осуществить сетевые настройки, для работы связки backend и postgresql
# 3 Лекция
Написать docker-compose.yaml, для всего проекта, собрать и запустить

# Критерий оценки финального задания
1. Dockerfile должны быть написаны согласно пройденным best practices
2. Для docker-compose необходимо использовать локальное image registry
3. В docker-compose необходимо сетевые настройки 2 разных интерфейса(bridge), 1 - для фронта, 2 - для бека с postgresql

4.* Осуществить сборку проекта самим docker-compose команда docker-compose build(при использовании этого подхода необходимо исключить 2 пункт из критерии оценки)

## added by AVK

1. Completed. Container created. Images used: node:lts-alpine and nginx:alpine. Multistage build. Final size 25,35mb
2. Completed. Containers created. Images used: python:3.8-alpine and postgres:14-alpine. Connected to back-network. Data loaded and shown in API
    Test link http://localhost:8000/api/v1/lib/bbk/
3. Completed. docker-compose run - working fine. Frontend connected to front-network. Backend and database connected to back-network.
    Test link http://localhost:8080/bbks

## Preparing networks

docker network create --driver bridge --subnet 10.10.250.0/24 --ip-range 10.10.250.0/24 front-network
docker network create --driver bridge --subnet 10.10.251.0/24 --ip-range 10.10.251.0/24 back-network

## Frontend

docker build -t frontend:01 -f Dockerfile.front .
docker run -d --restart=on-failure:10 -p 8080:80 --network front-network --ip 10.10.250.2 --name frontend frontend:01

## database. 

docker build -t database:01 -f Dockerfile.db .
# autoremove container
docker run -d -rm --restart=on-failure:10 -e POSTGRES_PASSWORD=django -e POSTGRES_USER=django -e POSTGRES_DB=django -e USERMAP_UID=999 -e USERMAP_GID=999 -d -v ./postgres:/var/lib/postgresql/data --network back-network --ip 10.10.251.3 --name database database:01
# or leave it intact after exit
docker run -d --restart=on-failure:10 -e POSTGRES_PASSWORD=django -e POSTGRES_USER=django -e POSTGRES_DB=django -e USERMAP_UID=999 -e USERMAP_GID=999 -d -v ./postgres:/var/lib/postgresql/data --network back-network --ip 10.10.251.3 --name database database:01

## backend.

docker build -t backend:01 -f Dockerfile.back .
docker run -d -p 8000:8000 --restart=on-failure:10 --name backend --network back-network --ip 10.10.251.2 backend:01

## Docker compose

# build'n'run
docker-compose run
# delete all traces os user images (postgres image will be intact)
docker-compose down & docker image rm docker_homework_backend & docker image rm docker_homework_frontend