# Проект Foodgram
Проект Foodgram дает возможность пользователям делиться рецептами приготовления блюд, выкладывая их в общий блог.
Функционал для неавторизованных пользователей ограничивается просмотром всех рецептов и детальной информации о каждом. Может быть расширен путем регистрации пользователя на сайте.
Функционал для авторизованных пользователей намного обширнее. Кроме перечисленного выше, они могут: создавать рецепты, просматривать страницы авторов рецептов и подписываться на них, добавлять рецепты в список избранного и в список для покупок с возможностью загрузки получившегося списка отдельным файлом.

Сайт проекта - https://myfoodgramm.hopto.org/

API: https://myfoodgramm.hopto.org/api/docs/

# Ключевые ресурсы API Foodgram
**AUTH**: аутентификация.

**USERS**: пользователи.

**RECIPES**: рецепты.

**INGREDIENTS**: ингредиенты.

# Алгоритм регистрации пользователей
1. Пользователь отправляет POST-запрос с параметрами: email, username, first_name, last_name на эндпоинт /api/users/.
2. Пользователь отправляет POST-запрос с параметрами: email, username на эндпоинт /api/auth/token/login/ для получения токена.

# Установка и развертывание проекта на локальном сервере
1. Склонируйте репозиторий. 
2. Запустите Docker Dekstop, в директории проекта создайте файл .env со следующим содержимым:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodpass
POSTGRES_DB=foodgram
DB_HOST=foodgram_db
DB_PORT=5432
SECRET_KEY='Из настроек Django-settings'
```
3. В папке infra выполните команду `docker-compose up`
4. Выполните миграции и загрузите данные ингредиентовЖ
```
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py dataloader
```
5. Соберите и скопируйте статику
```
docker compose exec backend python manage.py collectstatic
docker compose exec backend cp -r /app/collected_static/. /app/static/
```
6. Создайте суперпользователя `docker compose exec backend python manage.py createsuperuser`
7. Запустите проект по адресу: https://localhost/ и создайте через суперпользователя https://localhost/admin/ теги для завтрака, обеда и ужина, указывая в качестве цвета HEX-код для него.

# Установка и развертывание проекта на удаленном сервере:
1. Подключитесь к удаленному серверу с помощью пары открытого-закрытого ключа: `ssh -i путь_до_файла_с_SSH_ключом/название_файла_закрытого_SSH-ключа login@ip`
2. Создайте на сервере папку проекта foodgram-project-react и скопируйте в нее следующие файлы с их содержимым: docker-compose.production.yml, nginx_production.cong и директорию docs с ее содержимым. Создайте .env-file со следующим содержимым:
```
DB_NAME=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodpass
POSTGRES_DB=foodgram
DB_HOST=foodgram_db
DB_PORT=5432
```
3. Откройте настройки внешнего nginx `sudo nano /etc/nginx/sites-enabled/default` и добавьте конфигурацию для проекта foodgram:
```
server {
    server_name 158.160.23.185 myfoodgramm.hopto.org;
    client_max_body_size 20M;

    location / {
        proxy_set_header Host $http_host;
        proxy_pass http://127.0.0.1:8000;
    }
}
```
4. Получите SSL-сертификат `sudo certbot --nginx` для доменного имени проекта
5. В директории проекта запустите сборщик контейнеров `sudo docker compose -f docker-compose.production.yml up -d`
6. Выполните установку и применение миграций и загрузку данных ингредиентов:
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py makemigrations
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.production.yml exec backend python manage.py dataloader
```
7. Соберите и скопируйте статику:
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /app/static/
```
8. Создайте суперпользователя `sudo docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser`
9. Зайдите от имени суперпользователя в админ-зону https://myfoodgramm.hopto.org/admin/ и создайте теги для завтрака, обеда и ужина, указывая в качестве цвета HEX-код для него.
10. Запустите проект по адресу https://myfoodgramm.hopto.org/

# Примеры запросов к сервису:
1. GET-запрос к https://myfoodgramm.hopto.org/recipes/ - страница всех рецептов
2. POST-запрос к https://myfoodgramm.hopto.org/recipes/ - создание рецепта
3. GET-запрос к https://myfoodgramm.hopto.org/recipes/1/ - страница конкретного рецепта
4. GET-запрос к https://myfoodgramm.hopto.org/recipes/?is_favorited=1/ - избранные рецепты
5. GET-запрос к https://myfoodgramm.hopto.org/users/1/ - профиль пользователя (автора)

# Технологии
Python 3.9.10
Django 2.2.19
Docker 24.0.5

# Автор:
Кошурин Артём
