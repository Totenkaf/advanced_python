[![.github/workflows/ci.yml](https://github.com/Totenkaf/advanced_python/actions/workflows/ci.yml/badge.svg)](https://github.com/Totenkaf/advanced_python/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Totenkaf/advanced_python/branch/HW_5/graph/badge.svg?token=5jHkOnOQib)](https://codecov.io/gh/Totenkaf/advanced_python)
# VK | SEM II_Advanced Python | HW_5

================================================================ 
  
Усцов Артем Алексеевич.  
Группа ML-21.  
Преподаватели: Геннадий Кандауров, Антон Кухтичев

## 1. LRU-кэш
Интерфейс:

```py
    class LRUCache:

        def __init__(self, limit=42):
            pass

        def get(self, key):
            pass

        def set(self, key, value):
            pass


    cache = LRUCache(2)

    cache.set("k1", "val1")
    cache.set("k2", "val2")

    print(cache.get("k3"))  # None
    print(cache.get("k2"))  # "val2"
    print(cache.get("k1"))  # "val1"

    cache.set("k3", "val3")

    print(cache.get("k3"))  # "val3"
    print(cache.get("k2"))  # None
    print(cache.get("k1"))  # "val1"


    Если удобнее, get/set можно сделать по аналогии с dict:
    cache["k1"] = "val1"
    print(cache["k3"])
```

Реализация любым способом без использования OrderedDict.

### 2. Написать генератор filter_file для чтения и фильтрации файла
Есть текстовый файл, который может не помещаться в память.
В каждой строке файла фраза или предложение: набор слов, разделенных пробелами (знаков препинания нет).

Генератор должен принимать на вход имя файла или файловый объект и список слов для поиска.
Генератор перебирает строки файла и возвращает только те из них (строку целиком), где встретилось хотя бы одно из слов для поиска.
Поиск должен выполняться по полному совпадению слова без учета регистра.

Например, для строки из файла "а Роза упала на лапу Азора" слово поиска "роза" должно сработать, а "роз" или "розан" - уже нет.

Для тестов можноо в том числе использовать StringIO.

### 3. Тесты в отдельном модуле

### 4. Перед отправкой на проверку код должен быть прогнан через flake8 и pylint, по желанию еще black
