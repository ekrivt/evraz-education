***Начальные настройки***

1) Удалим postgresql c виртуальной машины

        sudo apt-get remove postgresql postgres-contrib

2) Освободим порты

        sudo fuser -vn tcp 5432

Команда вернет список портов и PID процессов использующего этот IP

    sudo kill -9 {указать PID}

3) Добавить IP-адрес виртуальной машины в переменную ALLOWED_HOSTS в следующий файл:
    
        sudo nano Day2/helpdesk_mono/src/ticket_tracker/settings.py 

***Запуск***

    sudo docker-compose up --build -d

***Доступ***

    http://{IP-адрес виртуальной машины}:8000/ - главная страница

***Работа с приложением***

1) Зарегистрируйте пользователя

2) Создайте проект

3) Создайте задачу под проект

***Познакомимся с базой данных***

Для этого зайдем в контейнер базы данных 

    sudo docker exec -it ps01 bash

Запустится командная оболочка из контейнера

Зайдем в базу данных postgres

    psql -U postgres
    \c postgres

Отобразим перечень таблиц

    \dt

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

Произведем выход из СУБД и контейнера

    \q

    exit
    
***Остановка***

    sudo docker-compose down

***Очистка системы***

    sudo docker system prune
