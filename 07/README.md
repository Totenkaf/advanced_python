[![.github/workflows/ci.yml](https://github.com/Totenkaf/advanced_python/actions/workflows/ci.yml/badge.svg)](https://github.com/Totenkaf/advanced_python/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Totenkaf/advanced_python/branch/HW_7/graph/badge.svg?token=5jHkOnOQib)](https://codecov.io/gh/Totenkaf/advanced_python)
# VK | SEM II_Advanced Python | HW_7

================================================================ 
  
Усцов Артем Алексеевич.  
Группа ML-21.  
Преподаватели: Геннадий Кандауров, Антон Кухтичев


### 1. Реализовать умножение цепочки матриц на С и сравнить производительность кода
- Python
- Ctypes

### 2. Тесты в отдельном модуле

### 3. Перед отправкой на проверку код должен быть прогнан через flake8 и pylint, по желанию еще black


## Quick Start
Make a dynamic lib
~~~
g++ -fPIC -shared -o matrix_chain_multiplication.so matrixes_cpp.cpp
~~~

Check .py script in Python-like realisation with random numbers
~~~
python main.py --chain=4,2,7,2 --is_random=True --type=python
~~~

Check .cpp lib byself, please uncomment main function and process it manually
~~~
g++ matrixes_cpp.cpp -o multiply_matrixes_cpp
./multiply_matrixes_cpp.out
~~~

Performance test.  
_Be careful test run with 100 iterations of settings and calculate average execution time!_ 
~~~
python3 performance.py --random_num=10 --chain_size=1000
~~~
