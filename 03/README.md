[![.github/workflows/ci.yml](https://github.com/Totenkaf/advanced_python/actions/workflows/ci.yml/badge.svg)](https://github.com/Totenkaf/advanced_python/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Totenkaf/advanced_python/branch/HW_3/graph/badge.svg?token=5jHkOnOQib)](https://codecov.io/gh/Totenkaf/advanced_python)
# VK | SEM II_Advanced Python | HW_3

================================================================ 
  
Усцов Артем Алексеевич.  
Группа ML-21.  
Преподаватели: Геннадий Кандауров, Антон Кухтичев

### Реализовать класс, отнаследованный от списка
При этом один список:

- Можно вычитать из другого CustomList([5, 1, 3, 7]) - CustomList([1, 2, 7]) = CustomList([4, -1, -4, 7]);  
- Можно складывать с другим CustomList([5, 1, 3, 7]) + CustomList([1, 2, 7]) = CustomList([6, 3, 10, 7]);  
- Результатом сложения/вычитания должен быть новый кастомный список;  

Сложение/вычитание также должно работать с обычными списками:  
[1, 2] +- CustomList([3, 4]) -> CustomList(...)  
CustomList([3, 4]) +- [1, 2] -> CustomList(...)  

- При неравной длине, дополнять меньший список нулями только на время выполнения операции. Исходные списки не должны изменяться;
- При сравнении списков должна сравниваться сумма элементов списков;
- Должен быть переопределен str, чтобы выводились элементы списка и их сумма;
- Списки можно считать всегда числовыми;  

### На все должны быть тесты в отдельном модуле;  
### Перед отправкой на проверку код должен быть прогнан через flake8 и pylint, по желанию еще black.
