
## Установка и запуск
1. Убедитесь, что у вас установлен [Docker](https://www.docker.com/)
2. Склонируйте данный репозиторий:
    ```shell
    git clone https://github.com/Cat-n-Code/data_craft_backend.git && cd data_craft_backend
    ```
3. Запустите сервис:
    ```shell
    docker compose -f docker-compose.yaml -f docker-compose.dev.yaml up -d
    ```
4. После запуска, сервис будет доступен по адресу http://localhost:8080. Также
    по адресу http://localhost:8080/docs будет доступна OpenAPI документация.
5. Остановка сервиса:
    ```shell
    docker compose -f docker-compose.yaml -f docker-compose.dev.yaml down
    ```
## Использование
1.	Выберите сервер в левом верхнем углу экрана /docs servers (localhost)
2.  При использовании можно пройти аутентификацию, но сущестующий функционал доступен любому, в том числе неаутентифицированному пользователю
3.  С помощью соответствующих запрсов можно загрузить файл в облачное хранилище и получить ссылку на загруженный ранее файл по его имени (выданному сервисом после выгрузки в хранилище)
