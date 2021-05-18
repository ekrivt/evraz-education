***Запуск***

    docker-compose up --build

***Доступ***

    POST: http://127.0.0.1:8000/auth/users/ - регистрация пользователя, в body передаются поля username, password
    POST: http://127.0.0.1:8000/auth/jwt/create/ - получение token'а, в body передаются поля username, password
    


***Реквизиты входа***

    login: admin
    pass: 1q2w3e4r5
