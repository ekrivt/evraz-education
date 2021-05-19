***Начальные настройки***

1) Создадим новую docker-сеть 

        sudo docker network create lab2-net

3) Добавить IP-адрес виртуальной машины в переменную ALLOWED_HOSTS в следующих файлах:

        sudo nano Day2/helpdesk_micros/ticker_tracker_service/src/ticket_tracker_service/settings.py 

***Запуск***

    cd Day2/helpdesk_micros/user_manager_service
    sudo docker-compose up --build -d
    cd -

    cd Day2/helpdesk_micros/ticker_tracker_service
    sudo docker-compose up --build -d

***Доступ***

    http://{IP-адрес виртуальной машины}:8000/ - главная страница

***Работа с приложением***

1) Зарегистрируйте пользователя

2) Создайте проект

3) Создайте задачу под проект

***Познакомимся с базами данных***

**User Manager Service**

Для этого зайдем в контейнер базы данных 

    docker exec -it ps01 bash

Запустится командная оболочка из контейнера

Зайдем в базу данных postgres

    psql -U postgres
    \c postgres

Отобразим перечень таблиц

    \dt

Нас интересуют таблицв

    public | auth_user                  | table | postgres
    public | authtoken_token            | table | postgres

Просмотрим некоторые из них

    SELECT * FROM auth_user;

Произведем выход из СУБД и контейнера

    \q

    exit

**Ticket Tracker Service**

Для этого зайдем в контейнер базы данных 

    docker exec -it ps02 bash

Запустится командная оболочка из контейнера

Зайдем в базу данных postgres

    psql -U postgres
    \c postgres

Отобразим перечень таблиц

    \dt

Нас интересуют таблицв

    public | project_project            | table | postgres
    public | task_task                  | table | postgres

Просмотрим некоторые из них

    SELECT * FROM project_project;
    SELECT * FROM task_task;

Произведем выход из СУБД и контейнера

    \q

    exit
    
***Остановка***

    docker-compose down

***Очистка системы***

    docker system prune