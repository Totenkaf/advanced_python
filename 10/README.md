# VK | SEM II_Advanced Python | HW_10

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
Run a lru_cache with cache_limit = 3 and check cache logs
~~~
python3 my_lru_cache.py -c 3
cat debug_cache.log
cat warning_cache.log
~~~

Run a lru_cache with cache_limit = 3 and additional logging to stdout
~~~
python3 my_lru_cache.py -c 3 -s stdout
cat debug_cache.log
cat warning_cache.log
~~~
