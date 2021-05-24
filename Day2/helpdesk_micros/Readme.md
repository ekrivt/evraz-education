***Шаг № 1. Настройка***

1) Создадим новую docker-сеть 
```shell
docker network create lab2-net
```
2) Перейдем в папку `evraz-education`. Добавим IP-адрес виртуальной машины в переменную ALLOWED_HOSTS в следующих файлах:
```shell
sudo nano Day2/helpdesk_micros/ticker_tracker_service/src/ticket_tracker_service/settings.py
```

***Шаг №2. Запуск***

```shell
cd Day2/helpdesk_micros/user_manager_service
docker-compose up --build -d
cd ../ticker_tracker_service
docker-compose up --build -d
```

Проверим доступность нашего приложения:
```shell
http://{IP-адрес виртуальной машины}:8000/registration
```

***Шаг №3. Работа с приложением***

1) Зарегистрируйте пользователя

2) Создайте проект

3) Создайте задачу под проект



***Шаг №4. Работа с базами данных***

**User Manager Service**

Для этого зайдем в контейнер базы данных 
```shell
docker exec -it ps01 bash
```

Запустится командная оболочка из контейнера

Зайдем в базу данных postgres

    psql -U postgres
    \c postgres

Отобразим перечень таблиц

    \dt

Нас интересуют таблицы

    public | auth_user                  | table | postgres
    public | authtoken_token            | table | postgres

Просмотрим некоторые из них

    SELECT * FROM auth_user;

Выйдем из СУБД и контейнера

    \q

    exit

**Ticket Tracker Service**

Для этого зайдем в контейнер базы данных 
```shell
docker exec -it ps02 bash
```

Запустится командная оболочка из контейнера

Зайдем в базу данных postgres

    psql -U postgres
    \c postgres

Отобразим перечень таблиц

    \dt

Нас интересуют таблицы

    public | project_project            | table | postgres
    public | task_task                  | table | postgres

Просмотрим некоторые из них

    SELECT * FROM project_project;
    SELECT * FROM task_task;

Выйдем из СУБД и контейнера

    \q

    exit
    
***Шаг №5. Остановка***
```shell
docker-compose down
```

***Шаг №6. Очистка системы***
```shell
docker system prune
```
