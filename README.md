# Проектная работа 10 спринта

Проектные работы в этом модуле в команде. Задания на спринт вы найдёте внутри тем.

Для запуска проекта выполнить:
```shell
cd notification && python manage.py collectstatic
python manage.py migrate
cd .. && docker-compose up -d --build
```

Ссылки проекта:
- панель менеджера контента: http://0.0.0.0/admin/
- панель RabbitMQ: http://0.0.0.0/rabbitmq/#/