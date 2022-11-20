[![.github/workflows/ci.yml](https://github.com/Totenkaf/advanced_python/actions/workflows/ci.yml/badge.svg)](https://github.com/Totenkaf/advanced_python/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Totenkaf/advanced_python/branch/HW_8/graph/badge.svg?token=5jHkOnOQib)](https://codecov.io/gh/Totenkaf/advanced_python)
# VK | SEM II_Advanced Python | HW_8

================================================================ 
  
Усцов Артем Алексеевич.  
Группа ML-21.  
Преподаватели: Геннадий Кандауров, Антон Кухтичев


### 1. Скрипт для асинхронной обкачки урлов
Написать скрипт для обкачки списка урлов с возможностью задавать количество одновременных запросов, используя асинхронное программирование.
Клиент можно использовать любой, например, из aiohttp.
Так, 10 одновременных запросов могут задаваться командой:

`python fetcher.py -c 10 urls.txt`
или
`python fetcher.py 10 urls.txt`

### 2. Тесты в отдельном модуле

### 3. Перед отправкой на проверку код должен быть прогнан через flake8 и pylint, по желанию еще black

## Quick Start
Run a fetcher
~~~
c
~~~

Tests and coverage
~~~
coverage run -m pytest *_test.py
coverage report -m
coverage html
~~~
