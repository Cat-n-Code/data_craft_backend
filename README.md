
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
Перед использованием вам нужно пройти аутенфикацию:
1.	Выберите сервер в левом верхнем углу экрана /docs servers (localhost или 176.109.107.222).

