# Polls App API
[![Build Status](https://travis-ci.com/Aliendrop/dj-polls.svg?branch=master)](https://travis-ci.com/Aliendrop/dj-polls)
[![Coverage Status](https://coveralls.io/repos/github/Aliendrop/dj-polls/badge.svg?branch=master)](https://coveralls.io/github/Aliendrop/dj-polls?branch=master)
## Install & run locally
```
pip install -r requirements/common.txt
pip install -r requirements/dev.txt (optional)
cd back; python manage.py migrate; python manage.py test; python manage.py runserver
```
## API
| Function | URL | Method | Rights |
| ------ | ------ | ------ | ------ |
| Получение списка активных опросов/добавление опросов | /api/polls/ | GET, POST | IsStaffUserOrReadOnly |
| Изменение/удаление опросов | /api/polls/<poll_id>/ | GET, PUT, PATCH, DELETE | IsStaffUserOrReadOnly |
| Добавление вопросов в опросе | /api/polls/<poll_id>/question/ | POST | IsStaffUserOrReadOnly |
| Изменение/удаление вопросов в опросе | /api/polls/<poll_id>/question/<question_id>/ | PUT, PATCH, DELETE | IsStaffUserOrReadOnly |
| Прохождение опроса | /api/user-response/<poll_id>/ | POST | AllowAny |
| Ответ на вопрос в опросе | /api/user-response/<poll_id>/question/<question_id>/ | POST | AllowAny |
| Получение пройденных пользователем опросов | /api/user-statistics/<user_id>/ | GET | AllowAny |
| Получение детализации по ответам пройденного пользователем опроса | /api/user-detail/<response_id>/ | GET | AllowAny |
| Получение ключа доступа | /api/api-token-auth/ | POST | AllowAny |
### About
Python 3.8, Django 2.2.10, djangorestframework
