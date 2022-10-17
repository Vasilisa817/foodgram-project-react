### :hammer_and_wrench: Стек технологий:


[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

<div>
    <img src="https://github.com/devicons/devicon/blob/master/icons/docker/docker-original-wordmark.svg" title="Docker" alt="Docker" width="40" height="40"/>&nbsp;
</div>

# Проект Foodgram
https://github.com/vasilisa817/foodgram-project-react

## Описание
Cайт Foodgram - онлайн-сервис, на котором пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд. Проект использует базу данных PostgreSQL. Проект запускается в трёх контейнерах (nginx, PostgreSQL и Django) (контейнер frontend используется лишь для подготовки файлов) через docker-compose на сервере. Образ с проектом загружается на Docker Hub. foodgram-main

### Пользовательские роли
Гость (неавторизованный пользователь)
## Что могут делать неавторизованные пользователи:

Создать аккаунт.
Просматривать рецепты на главной.
Просматривать отдельные страницы рецептов.
Просматривать страницы пользователей.
Фильтровать рецепты по тегам.
Авторизованный пользователь
## Что могут делать авторизованные пользователи:

Входить в систему под своим логином и паролем.
Выходить из системы (разлогиниваться).
Менять свой пароль.
Создавать/редактировать/удалять собственные рецепты
Просматривать рецепты на главной.
Просматривать страницы пользователей.
Просматривать отдельные страницы рецептов.
Фильтровать рецепты по тегам.
Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов.
Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл со количеством необходимых ингридиентов для рецептов из списка покупок.
Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок.
Администратор
Администратор обладает всеми правами авторизованного пользователя. Плюс к этому он может:

изменять пароль любого пользователя,
создавать/блокировать/удалять аккаунты пользователей,
редактировать/удалять любые рецепты,
добавлять/удалять/редактировать ингредиенты.
добавлять/удалять/редактировать теги.
Ресурсы API Foodgram
Ресурс auth: аутентификация.
Ресурс users: пользователи.
Ресурс tags: получение данных тега или списка тегов рецепта.
Ресурс recipes: создание/редактирование/удаление рецептов, а также получение списка рецептов или данных о рецепте.
Ресурс shopping_cart: добавление/удаление рецептов в список покупок.
Ресурс download_shopping_cart: cкачать файл со списком покупок.
Ресурс favorite: добавление/удаление рецептов в избранное пользователя.
Ресурс subscribe: добавление/удаление пользователя в подписки.
Ресурс subscriptions: возвращает пользователей, на которых подписан текущий пользователь. В выдачу добавляются рецепты.
Ресурс ingredients: получение данных ингредиента или списка ингредиентов.


## Примеры запросов по API:

[GET] /api/users/ - Получить список всех пользователей.
[POST] /api/users/ - Регистрация пользователя.
[GET] /api/tags/ - Получить список всех тегов.
[POST] /api/recipes/ - Создание рецепта.
[GET] /api/recipes/download_shopping_cart/ - Скачать файл со списком покупок.
[POST] /api/recipes/{id}/favorite/ - Добавить рецепт в избранное.
[DEL] /api/users/{id}/subscribe/ - Отписаться от пользователя.
[GET] /api/ingredients/ - Список ингредиентов с возможностью поиска по имени.
Автор: Немоляева Василиса
https://github.com/vasilisa817
