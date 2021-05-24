***Шаг №1. Установка Docker***

Проверим, установлен ли Docker:

```shell
docker --version
```

Если docker не установлен, переходим к установке

***Установка Docker:***

```shell
sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose
```
Проверим, установился ли Docker:

```shell
docker --version
```

если в результате вы видите ошибку "Permission denied", то запустите

```shell
sudo groupadd docker
sudo usermod -aG docker $USER
exit
```
затем снова заходим по ssh на машину.

***Шаг №2. Скачиваем исходный код приложения***

```shell
git clone https://github.com/ekrivt/evraz-education.git
```

***Шаг №3. Установка и настройка PostgreSQL:***

```shell
sudo apt-get install mlocate
sudo apt install postgresql postgresql-contrib
sudo updatedb
```

```shell
locate postgresql.conf
sudo nano /etc/postgresql/12/main/postgresql.conf
```

найти строчку listen_addresses, удалить первый символ `#` и добавить наш внешний ip aдрес после запятой
сохранить

```shell
cd evraz-education/Day1/Lab1/
sudo ./postgres.sh
```
В результате вы увидите в терминале таблицу:

```shell
Reading the table content...
 id |      name       |   bdate    
----+-----------------+------------
  1 | ERIC CLAPTON    | 1945-03-30
  2 | TOM PETTY       | 1950-10-20
  3 | GEORGE HARRISON | 1943-02-25
  4 | BOB DYLAN       | 1941-05-24
  5 | ROY KELTON      | 1936-04-23
(5 rows)
```

***Шаг №4. Регистрация в DockerHub***

Перейдем на сайт [https://hub.docker.com/](https://hub.docker.com/) и зарегистрируем бесплатную учетную запись

Зайдем в свой аккаунт

***Шаг №5. Авторизация через Docker***

```shell
docker login
```
если в результате вы видите ошибку "Permission denied", то запустите

```shell
sudo groupadd docker
sudo usermod -aG docker $USER
exit
```
затем снова заходим по ssh на машину.

***Шаг №6. Получение образа nginx***

```shell
docker pull nginx
```
***Шаг№7. Запуск образа nginx***

```shell
docker run -idt -p 80:80 nginx
```    
Перейдем в браузере по адресу `http://localhost/` или сделаем curl `http://localhost/`

Видим надпись Thank you for using nginx.

***Шаг№8. Команды для работы с контейнерами***

```shell
docker ps

docker container ls

docker stop *

docker container prune
```

***Шаг №9. Просмотр локальных образов***

```shell
docker image ls

docker image rm *

docker image prune
```
***Шаг №10. Очистка docker***

```shell
docker system prune
```
***Шаг №11. Создаем JSON файл с информацией для доступа к БД***

Перейдем в папку `app`:

```shell
cd app/
```

В папке `app` создадим файл dbcred.json следующего содержания:

```json
{
    "HOST":"внешний ip адрес вашей машины",
    "PORT":"5432",
    "DBNAME":"lab1_db",
    "USER":"postgres",
    "PASS":"evraz2021",
    "SSLMODE":"disable"
}
```

***Шаг №12. Установка GO:***

```shell
sudo apt install golang-go
```

Запустим go mod для подготовки списка модулей

```shell
sudo go mod init main.go
```
***Шаг № 13. Запустим контенер Nginx***

Проверим, что у нас не запущен контейнер nginx:

```shell
docker ps
```

Если контейнер запущен, удалим его.

```shell
docker rm -f Идентификатор контейнера
```
Запустим nginx:

```shell
docker run --name nginx-proxy -it -p 80:80 -p 443:443 -v /etc/nginx/vhost.d \
    -v /usr/share/nginx/html -v /var/run/docker.sock:/tmp/docker.sock:ro \
    -v /etc/nginx/certs -d jwilder/nginx-proxy
```

***Шаг №14. Создадим сеть***

```shell
docker network create lab-net

docker network connect lab-net nginx-proxy
```
***Шаг№ 15. Создадим Dockerfile для контейнеризации приложения***

Добавим в папку app файл Dockerfile

```shell
sudo nano Dockerfile
```

со следующим содержанием

```dockerfile
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
```

***Шаг №16. Соберем образ из Dockerfile'а***

```shell
docker build -t lab1-app -f Dockerfile .

docker run -it -e VIRTUAL_HOST=внешний адрес вашей машины!!! --network lab-net -d lab1-app
```

***Шаг №17. Создадим два Docker-compose файла для ускорения развертывания***

**nginx-compose.yaml**

```yaml
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
```
**lab1-compose.yaml**

```yaml
version: '3'
services:
    lab1-app:
        restart: always
        build:
            dockerfile: Dockerfile
            context: .
        environment:
          - VIRTUAL_HOST=внешний ip адрес вашей машины
```

***Шаг №18. Запустим Docker-compose для сборки и запуска контейнеров***

Проверим, что у нас не запущены другие контейнеры:

```shell
docker ps
```

Если контейнер запущен, удалим его.

```shell
docker rm -f Идентификатор контейнера
```

```shell
docker-compose -f nginx-compose.yaml up -d 
docker-compose -f lab1-compose.yaml up -d 
```
Проверим корректность работы приложения перейдя на адрес external_ip в браузере или curl external_ip.
В результате увидим:

```shell
<table border=1><caption><h2>Birthday list</h2>
</caption><tr><th>Full Name</th><th>Date</th></tr>
<tr><td>ERIC CLAPTON</td><td>1945-03-30</td></tr>
<tr><td>TOM PETTY</td><td>1950-10-20</td></tr>
<tr><td>GEORGE HARRISON</td><td>1943-02-25</td></tr>
<tr><td>BOB DYLAN</td><td>1941-05-24</td></tr>
<tr><td>ROY KELTON</td><td>1936-04-23</td></tr>
```

***Шаг №19. Остановка контейнеров через Docker-compose***

```shell
docker-compose -f nginx-compose.yaml down 
docker-compose -f lab1-compose.yaml down
```
***Шаг № 20. Объединим оба compose-файла в один***

**lab1-final-compose.yaml**

```yaml
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
      - VIRTUAL_HOST=внешний ip адрес

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
```
***Запустим и проверим общий compose-файл***

```shell
docker-compose -f lab1-final-compose.yaml up -d 
```
***Остановим все контейнеры и очистим систему***

```shell
docker-compose -f lab1-final-compose.yaml down

docker system prune
```
