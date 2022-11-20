"""
Profiling project
Copyright 2022 by Artem Ustsov
"""

import time
from typing import Callable
from functools import wraps
import weakref
from memory_profiler import profile
import cProfile, pstats, io


# pr = cProfile.Profile()
# pr.enable()
# # ... do something ...
# pr.disable()
# s = io.StringIO()
# sortby = "cumulative"
# ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
# ps.print_stats()
# print(s.getvalue())


# python -m cProfile -o output.txt ptest.py
# import pstats
# p = pstats.Stats("output.txt")
# p.strip_dirs().sort_stats(-1).print_stats()

# @profile
# def some_func():
#  lst1 = []
#  lst2 = "1" * 100000
# python -m memory_profiler run.py

class SuperAttribute:
    def __init__(self, attribute):
        self.attribute = attribute


class BaseAttributes:
    def __init__(self, a, b, c, d, e, f, g):
        self.a = Int(a)
        self.b = Str(b)
        self.c = List(c)
        self.d = SuperAttribute(d)
        self.e = Set(e)
        self.f = Dict(f)
        self.g = Tuple(g)


class SlotsAttributes:
    __slots__ = ("a", "b", "c", "d", "e", "f", "g")

    def __init__(self, a, b, c, d, e, f, g):
        self.a = Int(a)
        self.b = Str(b)
        self.c = List(c)
        self.d = SuperAttribute(d)
        self.e = Set(e)
        self.f = Dict(f)
        self.g = Tuple(g)


class Int:
    def __init__(self, attribute):
        self.attribute = attribute


class List(list):
    pass


class Dict(dict):
    pass


class Str(str):
    pass


class Tuple:
    def __init__(self, attribute):
        self.attribute = attribute


class Set(set):
    pass


class WeakRefAttributes:
    def __init__(self, a, b, c, d, e, f, g):
        self.a = weakref.ref(Int(a))
        self.b = weakref.ref(Str(b))
        self.c = weakref.ref(List(c))
        self.d = weakref.ref(SuperAttribute(d))
        self.e = weakref.ref(Set(e))
        self.f = weakref.ref(Dict(f))
        self.g = weakref.ref(Tuple(g))


def time_it(num_of_repeats):
    def repeat(function):
        @wraps(function)
        def wrapped(*args):
            total_time = 0
            for _ in range(num_of_repeats):
                start_time = time.monotonic()
                function(*args)
                total_time += time.monotonic() - start_time
            print(f"Average time: {(total_time * 1000 / num_of_repeats):.3f} ms")

        return wrapped

    return repeat


def profile_deco():
    pass


def make_class_manipulation(classname: Callable, num_of_classes: int, verbose: bool = False):
    num_of_repeats = 100
    class_creation_time = 0
    class_attributes_changing_time = 0
    class_attributes_accessing_time = 0
    class_attributes_deletion_time = 0
    for _ in range(num_of_repeats):
        start_creation_time = time.monotonic()
        classes = [
            classname(
                10,
                "avada_keedavra",
                ["python", "is", "our", "world"],
                "SuperAttribute",
                {"a", "b", "c"},
                {"my_attribute": 10},
                (10, 20),
            )
            for _ in range(num_of_classes)
        ]
        class_creation_time += time.monotonic() - start_creation_time

        start_accessing_time = time.monotonic()
        for class_ in classes:
            class_.a
            class_.b
            class_.c
            class_.d
            class_.e
            class_.f
            class_.g
        class_attributes_accessing_time += time.monotonic() - start_accessing_time

        start_changing_time = time.monotonic()
        for class_ in classes:
            class_.a = Int(20)
            class_.b = "imperio"
            class_.c = ["c", "plus", "plus", "is", "cool"]
            class_.d = "HyperAttribute"
            class_.e = {"d", "e", "f"}
            class_.f = {"another_attribute": 20}
            class_.g = (30, 40)
        class_attributes_changing_time += time.monotonic() - start_changing_time

        start_deletion_time = time.monotonic()
        for class_ in classes:
            del class_.a
            del class_.b
            del class_.c
            del class_.d
            del class_.e
            del class_.f
            del class_.g
        class_attributes_deletion_time += time.monotonic() - start_deletion_time

    if verbose:
        print(
            f"Average class creation time: {(class_creation_time * 1000 / num_of_repeats):.3f} ms"
        )
        print(
            f"Average attribute accessing time: {(class_attributes_accessing_time * 1000 / num_of_repeats):.3f} ms"
        )
        print(
            f"Average attribute changing time: {(class_attributes_changing_time * 1000 / num_of_repeats):.3f} ms"
        )
        print(
            f"Average attribute deletion time: {(class_attributes_deletion_time * 1000 / num_of_repeats):.3f} ms\n"
        )


if __name__ == "__main__":
    num_objects = 100000
    print(f"Manipulations for {num_objects} of {BaseAttributes.__name__} objects")
    make_class_manipulation(BaseAttributes, num_objects, verbose=True)
    print(f"Manipulations for {num_objects} of {SlotsAttributes.__name__} objects")
    make_class_manipulation(SlotsAttributes, num_objects, verbose=True)
    print(f"Manipulations for {num_objects} of {WeakRefAttributes.__name__} objects")
    make_class_manipulation(WeakRefAttributes, num_objects, verbose=True)
