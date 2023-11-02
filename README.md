# Проект Foodgram
Проект Foodgram дает возможность пользователям делиться рецептами приготовления блюд, выкладывая их в общий блог.
Функционал для неавторизованных пользователей ограничивается просмотром всех рецептов и детальной информации о каждом. Может быть расширен путем регистрации пользователя на сайте.
Функционал для авторизованных пользователей намного обширнее. Кроме перечисленного выше, они могут: создавать рецепты, просматривать страницы авторов рецептов и подписываться на них, добавлять рецепты в список избранного и в список для покупок с возможностью загрузки получившегося списка отдельным файлом.

# Ключевые ресурсы API Foodgram
**AUTH**: аутентификация.

**USERS**: пользователи.

**RECIPES**: рецепты.

**INGREDIENTS**: ингредиенты.

# Алгоритм регистрации пользователей
1. Пользователь отправляет POST-запрос с параметрами: email, username, first_name, last_name на эндпоинт /api/users/.
2. Пользователь отправляет POST-запрос с параметрами: email, username на эндпоинт /api/auth/token/login/ для получения токена.

# Установка
1. Склонируйте репозиторий. 
2. Находясь в папке с кодом, создайте виртуальное окружение `python -m venv venv`, активируйте его (Windows: `source venv\Scripts\activate`; Linux/Mac: `sorce venv/bin/activate`). 
3. Установите зависимости `python -m pip install -r requirements.txt`.
