# VK | SEM II_Advanced Python | HW_9

================================================================ 
  
Усцов Артем Алексеевич.  
Группа ML-21.  
Преподаватели: Геннадий Кандауров, Антон Кухтичев

## Результаты
I. [Замер](https://github.com/Totenkaf/advanced_python/blob/HW_9/09/results/Task_1.%20Simple%20Time%20Measuring.png) времени на создание 1 000 000 объектов, доступ, изменение атрибутов, удаление объектов.  
Видно, что использование __slots__ существенно сокращает время на создание классов, что очевидно в связи с ненадобностью
в создании дополнительных атрибутов.

Слабые ссылки позволили сократить время на создание в связи с ненадобностью увеличивать счетчики ссылок.  


II. Профилирование памяти с __memory_profiler__.   

[2.1.1](https://github.com/Totenkaf/advanced_python/blob/HW_9/09/results/Task_2_1_1.%20MemProfiling.%20BaseAttributes%20class.png) MemProfiling. BaseAttributes. Support functions. 
[2.1.2](https://github.com/Totenkaf/advanced_python/blob/HW_9/09/results/Task_2_1_2.%20MemProfiling.%20BaseAttributes%20class.png) MemProfiling. BaseAttributes. Main function. 

[2.2.1](https://github.com/Totenkaf/advanced_python/blob/HW_9/09/results/Task_2_2_1.%20MemProfiling.%20SlotsAttributes%20class.png) MemProfiling. SlotsAttributes. Support functions. 
[2.2.2](https://github.com/Totenkaf/advanced_python/blob/HW_9/09/results/Task_2_2_2.%20MemProfiling.%20SlotsAttributes%20class.png) MemProfiling. SlotsAttributes. Main functions. 

[2.3.1](https://github.com/Totenkaf/advanced_python/blob/HW_9/09/results/Task_2_3_1.%20MemProfiling.%20WeakRefAttributes%20class.png) MemProfiling. WeakRefAttributes. Support functions. 
[2.3.2](https://github.com/Totenkaf/advanced_python/blob/HW_9/09/results/Task_2_3_2.%20MemProfiling.%20WeakRefAttributes%20class.png) MemProfiling. WeakRefAttributes. Main functions.  

Такая же тенденция наблюдается и по памяти. Слабые ссылки существенно снижают затраты на создание объектов. Однако интересен факт, что во время изменения атрибутов уже сущестующих классов, память вновь выделяется.  

2.4 Профилирование времени с __cProfile__. 
[2.4.1](https://github.com/Totenkaf/advanced_python/blob/HW_9/09/results/Task_2_4_1.%20cProfiling.%20BaseAttributes%20class.png) cProfiling. BaseAttributes. 

[2.4.2](https://github.com/Totenkaf/advanced_python/blob/HW_9/09/results/Task_2_4_2.%20cProfiling.%20SlotsAttributes%20class.png) cProfiling. SlotsAttributes. 

[2.4.3](https://github.com/Totenkaf/advanced_python/blob/HW_9/09/results/Task_2_4_3.%20cProfiling.%20WeakRefAttributes%20class.png) cProfiling. WeakRefAttributes.  

cProfiling подтверждает измерения из пункта I. Слабые ссылки и slots отрабатывают быстрее.  
