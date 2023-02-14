# Как запустить проект:
Создайте env и envdsn файлы в той же директории, где описаны их example файлы

Запустите docker-compose командой:
```
docker-compose up -d
```
Создайте миграции и соберите статику командой:
```
make setup
```
Загрузите данные командой (не забудьте заполнить .envdsn файл в папке django_api/sqlite_to_postgres):
```
make load_data
```
Создайте суперпользователя Django:
```
make admin
```
# Запуск в браузере
- Открытие административного сайта - http://127.0.0.1:80/admin/
- Django Api - http://127.0.0.1:80/api/v1/movies/
- Swagger для тестирования API проекта - http://127.0.0.1:8082

# Проектное задание: Docker-compose

Настроены запуск всех компонентов системы — Django, Nginx и Postgresql — с использованием docker-compose.

- Написан dockerfile для Django.
- Настроен nginx

# Реализация API для кинотеатра

Создано API, возвращающее список фильмов в формате, описанном в openapi-файле, и позволяющий получить информацию об одном фильме.

Проверить результат работы API можно при помощи Postman. Запустите сервер на 127.0.0.1:8000 и воспользуйтесь тестами из файла `movies API.postman_collection.json`. В тестах предполагается, что в вашем API установлена пагинация и выводится по 50 элементов на странице.

