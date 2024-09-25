API новостей

Требования для запуска:
- docker 24.0.7 

Для запуска в docker контрейнере выполните след. команду: docker-compose up -d --build
Endpoints:
- http://127.0.0.1:8000/authors/ (GET/POST) - получение списка авторов / добавление автора
- http://127.0.0.1:8000/authors/{int} (GET) - получение данных автора по id
- http://127.0.0.1:8000/posts/  (GET/POST) - получение списка новостей / добавление новости
- http://127.0.0.1:8000/posts/{id} (GET/PUT/DELETE) - получение новости/обновление/удаление по id

Документация доступна по ссылке - http://127.0.0.1:8000/docs
