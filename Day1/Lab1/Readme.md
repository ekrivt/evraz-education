***Требования***

В системе должна быть установлен

- Docker >= 19

- PostgresSQL >= 13.2

- Go >= 1.1

- пакеты alocate

***Установка Docker:***

    sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release
    
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \ 
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update

    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose

***Установка и настройка PostgreSQL:***

    chmod +x prereq.sh postgres.sh
    ./prereq.sh
    ./postgres.sh

***Регистрация в DockerHub***

Перейдем на сайт https://hub.docker.com/ и зарегистрируем бесплатную учетную запись

Зайдем в свой аккаунт

***Авторизация через Docker***

    docker login

***Получение образа nginx***

    docker pull nginx

***Запуск образа nginx***

    docker run -it -p 80:80 nginx
    
Перейдем в браузере по адресу http://127.0.0.1/

В новом терминале 

    docker ps

    docker container ls

    docker stop *

    docker prune

***Просмотр локальных образов***

    docker image ls

    docker image rm *

    docker image prune

***Очистка docker***

    docker system prune

***Создаем JSON файл с информацией для доступа к БД***

В папке app создадим файл dbcred.json следующего содержания:

    {
        "HOST":"192.168.1.2",
        "PORT":"5432",
        "DBNAME":"lab1_db",
        "USER":"admin",
        "PASS":"evraz2021",
        "SSLMODE":"disable"
    }

***Установка GO:***

    apt install golang-go

***Скачиваем исходный код приложения из github: ${Адрес репозитория на гитхабе с файлом main.go}***

Добавим файл с исходным кодом приложения main.go в папку app и перейдем в нее

Запустим go mod для подготовки списка модулей

    go mod init main.go

***Запустим контенер Nginx***

    docker run --name nginx-proxy -it -p 80:80 -p 443:443 -v /etc/nginx/vhost.d \
    -v /usr/share/nginx/html -v /var/run/docker.sock:/tmp/docker.sock:ro \
    -v /etc/nginx/certs jwilder/nginx-proxy

***Создадим сеть***

    docker network create lab-net

    docker network connect lab-net nginx-proxy

***Создадим Dockerfile для контенерезации приложения***

Добавим в папку app файл Dockerfile со следующим содержанием

    FROM golang:alpine AS build
    RUN apk --no-cache add gcc g++ make git
    WORKDIR /go/src/app
    COPY . .
    RUN go get ./...
    RUN GOOS=linux go build -ldflags="-s -w" -o ./bin/web-app ./main.go
    FROM alpine:3.9
    RUN apk --no-cache add ca-certificates
    WORKDIR /usr/bin
    COPY --from=build /go/src/app/bin /go/bin
    COPY dbcred.json /go/bin
    EXPOSE 80
    ENTRYPOINT /go/bin/web-app --port 80

***Соберем образ из Dockerfile'а***

    docker build -t lab1-app -f Dockerfile .

    docker run -it -e VIRTUAL_HOST=192.168.0.110 --network lab-net lab1-app


***Создадим два Docker-compose файла для ускорения развертывания***

**nginx-compose.yaml**

    version: '3'
    services:
        nginx-proxy:
            restart: always
            image: jwilder/nginx-proxy
            ports:
            - "80:80"
            - "443:443"
            volumes:
            - "/etc/nginx/vhost.d"
            - "/usr/share/nginx/html"
            - "/var/run/docker.sock:/tmp/docker.sock:ro"
            - "/etc/nginx/certs"

**lab1-compose**

    version: '3'
    services:
        lab1-app:
            restart: always
            build:
                dockerfile: Dockerfile
                context: .
            environment:
            - VIRTUAL_HOST=192.168.1.2

***Запустим Docker-compose для сборки и запуска контейнеров***

    docker-compose -f nginx-compose.yaml up -d 
    docker-compose -f lab1-compose.yaml up -d 

Проверим корректность работы приложения перейдя на адрес 192.168.1.2 в браузере

***Остановка контейнеров через Docker-compose***

    docker-compose -f nginx-compose.yaml down -d 
    docker-compose -f lab1-compose.yaml down -d

***Объединим оба compose-файла в один***

**nginx-compose.yaml**

    version: '3'
    services:
    lab1-app:
        restart: always
        container_name: lab1-app
        depends_on:
        - nginx-proxy
        build:
        dockerfile: Dockerfile
        context: .
        environment:
        - VIRTUAL_HOST=192.168.0.110

    nginx-proxy:
        restart: always
        container_name: nginx-proxy
        image: jwilder/nginx-proxy
        ports:
        - "80:80"
        - "443:443"
        volumes:
        - "/etc/nginx/vhost.d"
        - "/usr/share/nginx/html"
        - "/var/run/docker.sock:/tmp/docker.sock:ro"
        - "/etc/nginx/certs"

***Запустим и проверим общий compose-файла***

    docker-compose -f lab1-final-compose.yaml up -d 

***Остановим все контейнеры и очистим систему***

    docker-compose -f lab1-final-compose.yaml down

    docker system prune