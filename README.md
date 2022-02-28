![example workflow](https://github.com/Igoryarets/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## Проект YaMDb


## Описание:

В проекте YaMDb реализован API с помощью Django REST Framework, его задача
собирать отзывы (Review) пользователей на произведения (Titles). Пользователи
оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку
в диапозоне от одного до десяти (целое число). На одно произведение пользователь
может оставить только один отзыв.

## Запуск с использованием CI/CD

Установить docker, docker-compose на боевом сервере

```
ssh <username>@<server_ip>
sudo apt install docker.io
https://docs.docker.com/compose/install/ # docker-compose
```
Заполнить в настройках репозитория секреты:

```
DOCKER_USERNAME  <ваш docker id>

DOCKER_PASSWORD  <ваш docker пароль>

PROJECT_NAME     <ваше имя проекта>

HOST             <ip боевого сервера>

USER             <имя пользователя под которым выполняется вход на сервер>

SSH_KEY          <SSH ключ>

PASSPHRASE       <Если ваш ssh-ключ защищён фразой-паролем>

TELEGRAM_TO      <id telegram аккаунта>

TELEGRAM_TOKEN   <токен вашего бота>

DB_ENGINE        <например: django.db.backends.postgresql>

DB_NAME          <например: postgres>

POSTGRES_USER    <например: postgres>

POSTGRES_PASSWORD <ваш пароль БД>

DB_HOST          <например: db>

DB_PORT          <порт подключения к БД 5432>

```

В docker-compose web:image установить свой контейнер

## Скопировать на сервер настройки docker-compose и nginx/default.conf

```
scp docker-compose.yaml <username>@<server_ip>:/home/<username>/
scp -r nginx/ <username>@<server_ip>:/home/<username>/nginx/
```

## Алгоритм регистрации пользователей:  

1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами
   email и username на эндпоинт /api/v1/auth/signup/.

2. YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.

3. Пользователь отправляет POST-запрос с параметрами username и confirmation_code на
   эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).

  

## Пользовательские роли:  

1. Аноним — может просматривать описания произведений, читать отзывы и комментарии.

2. Аутентифицированный пользователь (user) — может, как и Аноним, читать всё, дополнительно
   он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может 
   комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта 
   роль присваивается по умолчанию каждому новому пользователю.

3. Модератор (moderator) — те же права, что и у Аутентифицированного пользователя плюс право
   удалять любые отзывы и комментарии.

4. Администратор (admin) — полные права на управление всем контентом проекта. Может создавать
   и удалять произведения, категории и жанры. Может назначать роли пользователям.

5. Суперюзер Django — обладет правами администратора (admin)



## Доступные эндпоинты:

```

1. /api/v1/auth/signup/ (POST) регистрация пользователей (Доступно без токена)

2. /api/v1/auth/token/ (POST) получение jwt токена (Доступно без токена)

```

```

3. /api/v1/categories/ (GET) получение списка всех категорий (Доступно без токена)

4. /api/v1/categories/ (POST) добавление новой категории (Администратор)

5. /api/v1/categories/{slug}/ (DELETE) удаление категории (Администратор)

```

```

6. /api/v1/genres/ (GET) получение списка всех жанров (Доступно без токена)

7. /api/v1/genres/ (POST) добавление жанра (Администратор)

8. /api/v1/genres/{slug} (DELETE) удаление жанра (Администратор)

```

```

9. /api/v1/titles/ (GET) получение списка всех произведений (Доступно без токена)

10. /api/v1/titles/ (POST) добавление произведения (Администратор)

```

```

11. /api/v1/titles/{titles_id}/ (GET) получение информации о произведении (Доступно без токена)

12. /api/v1/titles/{titles_id}/ (PATCH) частичное обновление информации о произведении (Администратор)

13. /api/v1/titles/{titles_id}/ (DELETE) удаление произведения (Администратор)

```

```

14. /api/v1/titles/{title_id}/reviews/ (GET) получение списка всех отзывов (Доступно без токена)

15. /api/v1/titles/{title_id}/reviews/ (POST) добавление нового отзыва (Аутентифицированные пользователи)

16. /api/v1/titles/{title_id}/reviews/{review_id}/ (GET) полуение отзыва по id (Доступно без токена)

17. /api/v1/titles/{title_id}/reviews/{review_id}/ (PATCH) частичное обновление отзыва по id (Автор отзыва, модератор или администратор)

18. /api/v1/titles/{title_id}/reviews/{review_id}/ (DELETE) удаление отзыва по id (Автор отзыва, модератор или администратор)

```

```

19. /api/v1/titles/{title_id}/reviews/{review_id}/comments/ (GET) получение списка всех комментариев к отзыву (Доступно без токена)

20. /api/v1/titles/{title_id}/reviews/{review_id}/comments/ (POST) добавление комментария к отзыву (Аутентифицированные пользователи)

21. /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ (GET) получение комментария к отзыву (Доступно без токена)

22. /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ (PATCH) частичное обновление комментария к отзыву (Автор комментария, модератор или администратор)

23. /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ (DELETE) удаление комментария к отзыву (Автор комментария, модератор или администратор)

```

```

24. /api/v1/users/ (GET) получение списка всех пользователей (Администратор)

25. /api/v1/users/ (POST) добавление пользователя (Администратор)

26. /api/v1/users/{username}/ (GET) получение пользователя по username (Администратор)

27. /api/v1/users/{username}/ (PATCH) изменение данных пользователя по username (Администратор)

28. /api/v1/users/{username}/ (DELETE) удаление пользователя по username (Администратор)

```

## Примеры запросов к API:

### Регистрация пользователя:

Post запрос на /api/v1/auth/signup/

в теле запроса передаем:

```
{
    "email": "test_user@gmail.com",
    "username": "test_user"
}
```

ответ:

```
{
    "username": "test_user",
    "email": "test_user@gmail.com"
}
```


### Получение jwt токена:

Post запрос на /api/v1/auth/token/

в теле запроса передаем:

```
{
    "username": "test_user",
    "confirmation_code": "5us-bd95dfc09a195a8eea88"
}
```

ответ:


```
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1N......"
}
```

### Добавление произведения: 

Post запрос на /api/v1/titles/

в теле запроса передаем:

```
{

    "name": "test_user",
    "year": 2021,
    "description": "тестовое описание",
    "genre": 

    [
        "drama"
    ],
    "category": "movie"

}
```

ответ:

```
{
    "id": 33,
    "rating": 0,
    "description": "тестовое описание",
    "genre": [
        {
            "name": "Драма",
            "slug": "drama"
        }
    ],
    "category": {
        "name": "Фильм",
        "slug": "movie"
    },
    "name": "test_user",
    "year": 2021
}
```

### Добавление отзыва: 

Post запрос на /api/v1/titles/{title_id}/reviews/

в теле запроса передаем

```
{
    "text": "тестовый отзыв",
    "score": 5
}
```

ответ:

```
{
    "id": 76,
    "text": "тестовый отзыв",
    "author": "test_user",
    "score": 5,
    "pub_date": "2021-10-11T06:34:25.872741Z"
}
```
