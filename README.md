Дипломный проект курса Яндекс.Практикум. Сервис для публикации рецептов. Позволяет размещать рецепты, есть возможность подписки на автора, добавлять рецепты в избранное, а также скачивать список ингредиентов к покупке в формате pdf.

Workflow

    tests - Проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest. Дальнейшие шаги выполнятся только если push был в ветку master или main.
    build_and_push_to_docker_hub - Сборка и доставка докер-образов на Docker Hub
    deploy - Автоматический деплой проекта на боевой сервер. Выполняется копирование файлов из репозитория на сервер:

Подготовка для запуска workflow

Отредактируйте файл infra/nginx.conf и в строке server_name впишите IP виртуальной машины (сервера).
Скопируйте подготовленные файлы docker-compose.yaml и infra/nginx.conf из вашего проекта на сервер:

Зайдите в репозиторий на локальной машине и отправьте файлы на сервер.

scp docker-compose.yaml <username>@<host>:/home/<username>/docker-compose.yaml
sudo mkdir nginx
scp nginx.conf <username>@<host>:/home/<username>/nginx/nginx.conf

В репозитории на Гитхабе добавьте данные в Settings -> Secrets -> Actions secrets:

-- Docker --

DOCKER_USERNAME - имя пользователя в DockerHub
DOCKER_PASSWORD - пароль пользователя в DockerHub

-- Server --

HOST - ip-адрес сервера
USER - пользователь
SSH_KEY - приватный ssh-ключ (публичный должен быть на сервере)
PASSPHRASE - кодовая фраза для ssh-ключа (если есть)

-- Database -- 

DB_ENGINE - django.db.backends.postgresql
DB_HOST - db
DB_PORT - 5432
DB_NAME - postgres (по умолчанию)
POSTGRES_USER - postgres (по умолчанию)
POSTGRES_PASSWORD - postgres (по умолчанию)

-- Django --

SECRET_KEY - секретный ключ приложения django (необходимо чтобы были экранированы или отсутствовали скобки)
ALLOWED_HOSTS - список разрешённых адресов

Как запустить проект на сервере:

Установите Docker и Docker-compose:

sudo apt install docker.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

Проверьте корректность установки Docker-compose:

sudo  docker-compose --version

После успешного деплоя:

Соберите статические файлы (статику):

sudo docker-compose exec backend python manage.py collectstatic --no-input

Примените миграции:

sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate --noinput

Создайте суперпользователя:

sudo docker-compose exec backend python manage.py createsuperuser

Чтобы загрузить список ингредиентов:

sudo docker-compose exec backend python manage.py load_ingredients


 
Авторы:

    Mikutaitsis Dzianis - Backend, Docker, GitHub Actions, Yandex.Cloud.
    Yandex-Practikum - Frontend
