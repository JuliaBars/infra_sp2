# Проект REST API YaMDb

### ![Я](https://yastatic.net/q/logoaas/v2/Яндекс.svg?circle=black&color=000&first=white)![Практикум](https://yastatic.net/q/logoaas/v2/Практикум.svg?color=000)

Проект собирает отзывы пользователей на произведения.

_Благодаря этому проекту можно:_

- оставлять к произведениям отзывы
- ставить произведению оценку
- комментировать отзывы других пользователей
- получить список всех произведений, категорий, жанров, комментариев, отзывов

***
_Репозиторий на Github [ссылка](https://github.com/JuliaBars/api_yamdb)._
***

### Установка

- Клонируйте проект

```
git clone <ссылка>
```

- Установите и активируйте виртуальное окружение
- Установите зависимости из файла requirements.txt

```
pip install -r requirements.txt
```

- В папке с файлом manage.py выполните команду:

```
python manage.py runserver
```

### Шаблон заполнения .env в директории infra/.env

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

### Запуск приложения в контейнерах

- Переходим в папку с файлом docker-compose.yaml:

```bash
cd infra/
```

- Собираем контейнеры (infra_db_1, infra_web_1, infra_nginx_1):

```bash
docker-compose up -d --build
```

- Выполняем миграции:

```
docker-compose exec web python manage.py migrate
```

- Создаем суперпользователя:

```bash
docker-compose exec web python manage.py createsuperuser
```

- Собираем статику:

```bash
docker-compose exec web python manage.py collectstatic --no-input
```

- В проекте есть дамп локальной базы, для заполнения базы выполните команду:

```
docker-compose exec web python manage.py loaddata fixtures.json
```

- Останавка контейнера:

```
docker-compose down -v
```

### Документация API YaMDb

Документация доступна по эндпойнту /redoc:  [ссылка](http://localhost/redoc/)

___

### Автор

Студент Я.Практикум - _Юлия Орлова_
