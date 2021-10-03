# Тестовое задание на _Python_-программиста

В этом репозитории реализовано API приложения для планирования пикников, состоящие из сущностей:

- Город
- Пикник
- Пользователь
- Регистрация пользователя на пикник

## Запуск проекта

1. `docker-compose build`
2. `docker-compose up`

## Запуск тестов

`docker-compose run --rm backend pytest -v`

## Результат выполнения задания

1. Изменена архитектура проекта + изменен docker-compose файл для работы авторелоада при изменении файлов
2. Добавлены виртуальные переменные
3. Поиск городов по аргументу осуществляется с помощью метода filter
4. Максимальный/минимальный фильтр по возрасту реализуется с помощью func.max и func.min
5. Ошибка в запросе picnic-add: заменён метод на POST, указаны обязательные поля, сами параметры в body, фильтрация
   города
6. Подключена PostgreSQL, для наименования города включена индексация в БД
7. Реализован метод picnic-register
8. Изменена фильтрация пользователя по макс./мин. возрасту, подправлены pydantic-models у пользователя, добавлены
   сервисы для работы с пользователями
9. Добавлены сервисы для работы с пикниками, изменено описание полей на pydantic классы, добавлена валидация для API
   методов пикника
10. Описание всех полей классами
11. Логирование в файл, начиная от уровня WARNING
12. Отрефакторен файл external_requests.py