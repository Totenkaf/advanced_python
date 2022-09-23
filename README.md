[![.github/workflows/ci.yml](https://github.com/Totenkaf/advanced_python/actions/workflows/ci.yml/badge.svg)](https://github.com/Totenkaf/advanced_python/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Totenkaf/advanced_python/branch/main/graph/badge.svg?token=5jHkOnOQib)](https://codecov.io/gh/Totenkaf/advanced_python)

# VK | SEM II_Advanced Python | HW_2

================================================================ 
  
Усцов Артем Алексеевич.  
Группа ML-21.  
Преподаватели: Геннадий Кандауров, Антон Кухтичев

### Написать функцию, которая в качестве аргументов принимает строку json, список полей, которые необходимо обработать, список имён, которые нужно найти и функцию-обработчика имени, который срабатывает, когда в каком-либо поле было найдено ключевое имя.

- Функция, должна принимать строку, в которой содержится json, и произвести парсинг этого json. Упростим немного и представим, что json представляет из себя только коллекцию ключей-значений. Причём ключами и значениями являются только строки.

```
def parse_json(json_str: str, required_fields=None, keywords=None, keyword_callback)
```

- Например, представим, что json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}', а required_fields = ["key1"], keywords = ["word2"]. Тогда keyword_callback будет вызвана только для слова 'word2' для ключа 'key1'.  

Распарсить json можно так:
```
import json

...
json_doc = json.loads(json_str)
```

Можно использовать ещё ujson, но его предварительно нужно установить с помощью pip.

### Использовать mock-объект при тестировании  
Использовать mock-объект, например, keyword_callback и проверить, что заглушка вызывалась n число раз.  

### Использовать factory boy  
Для генерации данных и ключевых слов, нужно использовать factory boy.

### Узнать степень покрытия тестами с помощью библиотеки coverage  

