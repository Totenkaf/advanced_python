[![.github/workflows/ci.yml](https://github.com/Totenkaf/advanced_python/actions/workflows/ci.yml/badge.svg)](https://github.com/Totenkaf/advanced_python/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Totenkaf/advanced_python/branch/HW_8/graph/badge.svg?token=5jHkOnOQib)](https://codecov.io/gh/Totenkaf/advanced_python)
# VK | SEM II_Advanced Python | HW_8

================================================================ 
  
Усцов Артем Алексеевич.  
Группа ML-21.  
Преподаватели: Геннадий Кандауров, Антон Кухтичев

### 1. Логирование LRUCache

Добавить логирование разного уровня в файл cache.log для LRUCache.
По аргументу командной строки "-s" дополнительно логировать в stdout с отдельным форматированием.

Логирование должно покрывать как минимум следующие случаи:
- get существующего ключа
- get отсутствующего ключа
- set отсутствующего ключа
- set отсутствующего ключа, когда достигнута ёмкость
- set существующего ключа
- различные debug записи в дополнение и в зависимости от реализации

При запуске модуля должны выполняться все перечисленные операции с кэшом (через функцию в `if __name__ == "__main__"`).

Код решения должен быть целиком в каталоге данного ДЗ без ссылок/импортов на домашки про LRUCache.
Корректность LRUCache в данном задании не проверяется.

### 2. flake8 и pylint

## Quick Start
Run a lru_cache
~~~
python3 main.py -c 10 --ktop=3 --input=data/urls_https.txt --output=data/urls_https_parsed.txt
~~~

Tests and coverage
~~~
coverage run -m pytest tests/*_test.py
coverage report -m
coverage html
~~~
