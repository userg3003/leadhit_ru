# leadhit_test
Web-приложение для определения заполненных форм (тестовое задание)

[Тестовое задание на вакансию разработчик Python](https://docs.google.com/document/d/1fMFwPBs53xzcrltEFOpEG4GWTaQ-5jvVLrNT6_hmC7I/edit?usp=sharing)

В качестве хранилища используется база данных MongoDb. База может быть развёрнута локально (с использованием
Docker-контейнера) или на удалённом сервере.

Способ использования базы задаётся в конфигурационном файле.

# Установка

Требуется: Python 3.7.*, Опционально: make, Docker, Docker-Compose.

Примечание: *использование make предусмотрено только в Linux.*

Для установки следует выполнить клонирование репозитория, выполнив команду:

> git clone https://github.com/userg3003/leadhit_test.git


Для установки необходимых пакетов выполнить:
> pip install -r requirements.txt.

или

> make deps

Для установки пакетов, необходимых для запуска тестов, выполнить:
> pip install -r requirements_dev.txt.

или

> make deps-dev

## Конфигурирование

Параметры запуска сервиса задаются в файле конфигурации, расположенном в папке
*.deploy/.envs*.

Структура конфигурационного файла:

> SERVER_HOST = http://127.0.0.1  
> SERVER_PORT = 54102  
> MONGO_URI=mongodb://0.0.0.0:27017/  
> COLLECTION=leadhit

где:

- **SERVER_HOST** - адрес хоста на котором будет запущен сервис.
- **SERVER_PORT** - порт на котором будет запущен сервис.
- **MONGO_URI** - uri для доступа к серверу БД. При задании адреса в виде ***mongodb://0.0.0.0:27017/***
  доступ будет осуществляться к серверу БД в Docker-контейнере на локальном сервере. Задание в виде : ***mongodb+srv:
  //user:password@host***, будет вызывать обращение к удалённому серверу.

- **COLLECTION** - наименование коллекции для хранения данных.

## Запуск тестов

Перед запуском тестов следует войти в папку с проектом и активировать виртуальное окружение:  
Для Windows:
> *venv\Scripts\activate*


Для Linux:
> *source venv\bin\activate*



### Запуск тестов при расположении MongoDb на удалённом сервере

Предварительно следует активировать виртуальное окружение и установить переменную окружения
(для Windows) командой:
> set APP_ENV=leadhit.test.env

> *pytest -v -l --disable-warnings tests*

В Linux запуск тестов предпочтительно запускать через *make*:

> make tests



### Запуск тестов при расположении MongoDb на локальном хосте

Перед запуском тестов следует запустить Docker-контейнер с Mongo-Db, для этого выполнить команду (команду следует
выполнять в отдельном окне терминала):
> *make run-mongo*

После запуска можно запустить на выполнение тесты:

> *pytest -v -l --disable-warnings tests*

или (в Linux)
> make tests

## Запуск сервиса в Docker-контейнере

***Примечание***:  *запуск сервиса в Docker-контейнере (в данной конфигурации)
должен выполняться в Linux.*

Перед запуском сервиса следует выполнить сборку контейнера, выполнив команду:
> make build-image

В результате будет собран образ контейнера, который может быть запущен командой:

> make run-full

Сервис будет доступен по адресу *http://host:port*, где host - адрес хоста заданный
в файле конфигурации, port - номер порта заданный в файле конфигурации. По адресу 
*http://host:port/docs* можно просмотреть содержимое базы данных.

## Запуск сервиса 

Сервис должен запускаться при активированном виртуальном окружении.  
Перед запуском сервиса следует запустить контейнер с базой данных (*make run-mongo*),
если она расположена на локальном хосте.  

Предварительно следует установить переменную окружения (для Windows) командой:
> set APP_ENV=leadhit.env


Для запуска сервиса следует выполнить:

> python -m app.main

Запуск сервиса в Linux предпочтительно выполнять через ***make***. Выполнив команду:
> make run

Для просмотра содержимого базы данных можно перейти в браузере по адресу:
*http://host:port/docs*, где host - адрес хоста заданный в файле конфигурации, port - номер порта заданный в файле
конфигурации.


## Заполнение базы данных 

Для выполнения запросов к базе данных, необходимо загрузить исходные данные. Для этого
выполнить скрипт (предварительно установив переменню окружения *set APP_ENV=leadhit.env*):

> python -m scripts.fill_base

В Linux заполнение базы данных может выполняться командой:
> make fill-db

Исходные данные размещены в файле *data/data.py* переменные *templates_1* и *templates_1*. 

Перед заполнением базы данных, скрипт выполняет полную очистку базы.


## Выполнение запросов к сервису

Для выполнения запроса к сервису можно использовать утилиту *curl*.

Пример выполнения запроса:
> curl -X 'POST' 'http://localhost:54102/get_forms?user_email=ivanov@mail.com&user_phone=%2B7%20123%20456%2078%2090' -H 'accept: application/json' -d ''

При выполнении запросов в номере телефона знак "+" должен быть заменён на код "%2b", 
пробелы на код "%20".

*Примечание*: при выполнении запроса в Windows одинарные кавычки **'**, должны быть заменены на двойные **"**. 

Примеры запросов:

> curl -X "POST" "http://localhost:54102/get_forms?user_email=ivanov@mail.com&user_phone=%2B7%20123%20456%2078%2090" -H "accept: application/json" -d ""
> 
> curl -X "POST" "http://localhost:54102/get_forms?user_phone=%2B7%20123%20456%2078%2090" -H "accept: application/json" -d ""
> 
> curl -X "POST" "http://localhost:54102/get_forms?info_email=ivanov@mail.com" -H "accept: application/json" -d ""

# Примечание
По заданию:  
**Выходные данные**:  
***Имя наиболее подходящей данному списку полей формы***...

Учитывая, что в запросе может быть задано больше полей, чем содержится в шаблоне, результатом выполнения
запроса может быть несколько шаблонов. В связи с этим ответом от сервиса (при удачном поиске) является список 
с наименованиями подходящих форм.



