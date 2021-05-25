***Шаг №1. Настройка системы***

1) Удалим postgresql c виртуальной машины

```shell
sudo apt-get remove postgresql postgres-contrib
```
        
   Если мы видимо ошибку:
   `E: Unable to locate package postgres-contrib`,
   то запускаем команду:
   
```shell
sudo dpkg --purge postgresql postgres-contrib
```
  
2) Освободим порты

```shell
sudo fuser -vn tcp 5432
```

Команда вернет список портов и PID процессов, использующих эти порты

```shell
sudo kill -9 {указать PID}
```

3) Добавим IP-адрес виртуальной машины в переменную ALLOWED_HOSTS в следующий файл:

```shell
sudo nano Day2/helpdesk_mono/src/ticket_tracker/settings.py
```
    
***Шаг №2. Запуск приложения***

1) Посмотрим содержимое `docker-compose.yml` файла:
```shell
cat docker-compose.yml
```
2) Запустим приложение:
```shell
docker-compose up --build -d
```
3) Проверим, что наше приложение доступно. Для этого в браузере зайдем на 8000 порт:
```shell
http://{IP-адрес виртуальной машины}:8000/
```

***Шаг №3. Работа с приложением***

1) Зарегистрируйте пользователя (Status: admin, client, staff)

2) Создайте проект

3) Создайте задачу под проект

***Шаг №4. Работа с базой данных***

Для этого зайдем в контейнер базы данных 
```shell
docker exec -it ps01 bash
```

Запустится командная оболочка из контейнера

Зайдем в базу данных postgres

```shell
psql -U postgres
\c postgres
```

Отобразим перечень таблиц
```shell
\dt
```

Нас интересуют таблица

    public | accounts_userprofile       | table | postgres
    public | auth_user                  | table | postgres
    public | authtoken_token            | table | postgres
    public | comment_comment            | table | postgres
    public | project_project            | table | postgres
    public | task_description           | table | postgres
    public | task_task                  | table | postgres

Просмотрим некоторые из них

    SELECT * FROM accounts_userprofile;
    SELECT * FROM project_project;
    SELECT * FROM task_task;

Выйдем из СУБД и контейнера
```shell
\q
exit
```
    
***Шаг №5. Остановка***

```shell
docker-compose down
```

***Шаг №6. Очистка системы***
```shell
docker system prune
```

