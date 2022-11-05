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


If you want to check .py script in Python-like realisation with random numbers
~~~
cd 07
python main.py --chain=4,2,7,2 --is_random=True
~~~

or with own input
~~~
cd 07
python main.py --chain=4,2,7,2 --is_random=True --input=your_filename.txt
~~~


If you want to check .py script in Ctypes-like realisation with random numbers
Make a dynamic lib
~~~
cd 07
g++ -fPIC -shared -o matrix_chain_multiplication.so matrixes_cpp.cpp
~~~
Run script
~~~
cd 07
python main.py --chain=4,2,7,2 --type=cpp --edge=5
~~~

If you want to check .cpp lib byself, please uncomment main function and process it manually
~~~
cd 07
g++ matrixes_cpp.cpp -o multiply_matrixes_cpp
./multiply_matrixes_cpp.out
~~~

Run performance test
~~~
cd 07
python3 matrixes/tests/perf/pert_test.py --random_num=10 --chain_size=1000
~~~
