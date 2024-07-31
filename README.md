# habits_tracker
В 2018 году Джеймс Клир написал книгу «Атомные привычки», которая посвящена приобретению новых полезных привычек и искоренению старых плохих привычек. 
Проект представляет собой API приложение для поддержки выполнения пользователем задуманных привычек, а также вознаграждение за их выполнение.

<!-- ABOUT THE PROJECT -->
## О проекте
*Бэкенд-часть SPA веб-приложения.*

- В проекте представлены приложения *users*, *habits*.
- Реализованы модели (User, Habit).
- Для реализации CRUD используются Viewsets и Generic-классы.
- Для работы контроллеров описаны сериализаторы.
- В проекте используется JWT-авторизация, каждый эндпоинт закрыт авторизацией.
- Реализованы права доступа для объектов:
  - каждый пользователь имеет доступ только к своим привычкам по механизму CRUD;
  - пользователь может видеть список публичных привычек без возможности их как-то редактировать или удалять.
- Настроена валидация для сохранения привычки:
  - исключен одновременный выбор связанной привычки и указания вознаграждения;
  - время выполнения не больше 120 секунд;
  - в связанные привычки могут попадать только привычки с признаком приятной привычки;
  - у приятной привычки не может быть вознаграждения или связанной привычки;
  - нельзя выполнять привычку реже, чем 1 раз в 7 дней;
- Реализована пагинация для вывода привычек.
- Написаны тесты для проверки всех имеющихся эндпоинтов в проекте (покрытие - 88%).
- Подключен и настроен вывод документации для проекта. Для работы с документацией проекта использовалась библиотека drf-yasg.
- Настроена интеграцию с Телеграмом.
- Реализована периодическая задача *send_reminder* в Celery с использованием celery-beat для напоминания о том, в какое время какие привычки необходимо выполнять.
- Настроен CORS.


- Описаны Dockerfile и docker-compose.yaml.
- Docker Compose используется для управления контейнерами.
- Для сервисов django, postgresql, redis, celery созданы отдельные контейнеры.


- Проект готов быть размещенным на удаленном сервере.

<!-- GETTING STARTED -->
## Подготовка к работе

Чтобы запустить локальную копию, выполните следующие простые шаги:

### Установка

1. Клонируйте проект
   ```sh
   git@github.com:aukhadieva/habits_tracker.git
   ```
2. Убедитесь, что вы получили из удаленного репозитория все ветки и переключились на ветку разработки develop
   ```sh
   git checkout develop
   ```
3. Установите зависимости проекта (в случае, если не установились при клонировании)
   ```sh
   poetry install
   ```
4. Создайте в корне проекта файл .env и заполните переменные среды в соответствии с желаемой конфигурацией, используя файл .env_sample
5. Примените миграции
   ```sh
   python manage.py migrate
   ```

### Запуск приложения
1. Для запуска проекта выполните команду
   ```sh
   python3 manage.py runserver
   ```
2. Работу каждого эндпоинта можно проверять с помощью Postman.

### Запуск приложения в Docker
Для сборки образа и запуска контейнера, выполните команду
   ```sh
   docker-compose up -d --build
   ```

### Запуск задач в Celery
В проекте реализованы отложенные и периодические задачи.
Для запуска **периодической задачи**, выполните команды
```sh
   celery -A config  worker --loglevel=info
   ```
и
```sh
    celery -A config beat -l INFO -S django
   ```

### Тестирование
Для запуска тестов, находясь в виртуальном окружении проекта, выполните команды
```sh
   coverage run --source='.' manage.py test
   ```
и
```sh
   coverage report
   ```
Для генерации HTML-отчета в целях оценки покрытия тестами выполните команду
```sh
   coverage html
   ```

Из папки htmlcov запустите файл index.html, в открывшемся окне выберите модуль, покрытие которого хотите проверить


<!-- GETTING STARTED -->
## Деплой

_____
### Деплой приложения на удаленный сервер в ручном режиме.
1. Установите зависимости на удаленный сервер
```sh
   sudo apt-get update
   sudo apt-get install postgresql postgresql-contrib python3-pip
   apt install gunicorn
   apt install nginx
   ```

2. Установите виртуальное окружение на удаленном сервере
```sh
   python3 -m venv venv
   ```

3. Активируйте виртуальное окружение
```sh
   source venv/bin/activate
   ```

4. Клонируйте свой проект на сервер
```sh
   git clone <ssh вашего проекта с гит>
   ```

5. Установите зависимости проекта
   ```sh
   poetry install
   ```

6. Опишите настройки для демона gunicorn на удаленном сервере в файле /etc/systemd/system/yourproject.service
```sh
   [Unit]
   Description=gunicorn daemon for Your Project # Описание вашего сервиса
   After=network.target # Сервис, от которого будет зависеть запуск проекта
    
   [Service]
   User=yourusername # Имя пользователя владельца проекта в Linux
   Group=yourgroupname # Группа, к которой относится пользователь
   WorkingDirectory=/path/to/your/project # Путь к рабочей директории проекта
   ExecStart=/path/to/venv/bin/gunicorn --config /path/to/gunicorn_config.py your_project.wsgi:application # Команда для запуска проекта
    
    [Install]
    WantedBy=multi-user.target
   ```

7. Запустите сервис
```sh
   sudo systemctl start yourproject
   ```

8. Опишите настройки для Nginx для работы со статикой вашего проекта в файле /etc/nginx/sites-available/yourproject
```sh
   server {
    listen 80;
    server_name <ip адрес или доменное имя сервера>;

    location /static/ {
			root /path/to/your/project/;
    }

    location /media/ {
			root /path/to/your/project/;
    }

    location / {
			include proxy_params;
			proxy_pass /path/to/your/project/project.sock
    }

}
   ```

9. Проверьте корректность заполнения файла с помощью утилиты `nginx -t`

10. Подключите сайт к отображению
```sh
   ln -s /etc/nginx/sites-available/my_site /etc/nginx/sites-enabled
   ```

11. Выполнить команду для определение статики проекта
```sh
   python3 manage.py collectstatic
   ```

_____
### Деплой приложения на удаленный сервер череез Docker.
1. Выполнить шаги 1,3,5,6,7,8

2. Установить docker и docker-compose на удаленный сервер
```sh
   apt install docker docker-compose
   ```

3Для сборки образа и запуска контейнера, выполните команду
```sh
   docker compose up -d --build
   ```

_____
### Подключение CI/CD.
1. Загрузите в GitLab свой проект следуя инструкциям GitLab
2. В разделе settings -> CI/CD -> Runners создайте runner
3. В разделе settings -> CI/CD -> Variables добавьте переменные окружения для .env файла
4. Установите GitLab Runner на удаленном сервере
```sh
   curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" | sudo bash
   sudo apt-get install gitlab-runner
   ```