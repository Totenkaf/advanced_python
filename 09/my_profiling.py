"""
Profiling project
Copyright 2022 by Artem Ustsov
"""

import argparse
import time
from functools import wraps
import weakref
import cProfile
import pstats

pr = cProfile.Profile()


# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=unnecessary-pass
# pylint: disable=pointless-statement
class SuperAttribute:
    """SuperAttribute class"""

    def __init__(self, attribute):
        self.attribute = attribute


class BaseAttributes:
    """Class with base creation of attributes"""

    def __init__(self, a, b, c, d, e, f, g):
        self.a = Int(a)
        self.b = Str(b)
        self.c = List(c)
        self.d = SuperAttribute(d)
        self.e = Set(e)
        self.f = Dict(f)
        self.g = Tuple(g)


class SlotsAttributes:
    """Class with only slots attributes"""

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
    """Int wrapper for weakref"""

    def __init__(self, attribute):
        self.attribute = attribute


class List(list):
    """List wrapper for weakref"""

    pass


class Dict(dict):
    """Dict wrapper for weakref"""

    pass


class Str(str):
    """String wrapper for weakref"""

    pass


class Tuple:
    """Tuple wrapper for weakref"""

    def __init__(self, attribute):
        self.attribute = attribute


class Set(set):
    """Set wrapper for weakref"""

    pass


class WeakRefAttributes:
    """Class with only weakref attributes"""

    def __init__(self, a, b, c, d, e, f, g):
        self.a = weakref.ref(Int(a))
        self.b = weakref.ref(Str(b))
        self.c = weakref.ref(List(c))
        self.d = weakref.ref(SuperAttribute(d))
        self.e = weakref.ref(Set(e))
        self.f = weakref.ref(Dict(f))
        self.g = weakref.ref(Tuple(g))


def profile_deco(function):
    """cProfile decorator"""

    @wraps(function)
    def wrapped(*args, **kwargs):
        """Make a profile for function"""

        pr.enable()
        res = function(*args, **kwargs)
        pr.disable()
        ps = pstats.Stats(pr).sort_stats("cumulative")
        setattr(wrapped, "print_stats", ps.print_stats)
        return res

    return wrapped


# @profile
@profile_deco
def create_classes(classname, num_of_classes):
    """Create classes function"""

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
    delta_creation_time = time.monotonic() - start_creation_time
    return classes, delta_creation_time


# @profile
@profile_deco
def get_class_attributes(classes):
    """Get class attributes function"""

    start_accessing_time = time.monotonic()
    for class_ in classes:
        class_.a
        class_.b
        class_.c
        class_.d
        class_.e
        class_.f
        class_.g
    delta_accessing_time = time.monotonic() - start_accessing_time
    return delta_accessing_time


# @profile
@profile_deco
def change_class_attributes(classes):
    """Change class attributes function"""

    start_changing_time = time.monotonic()
    for class_ in classes:
        class_.a = Int(20)
        class_.b = "imperio"
        class_.c = ["c", "plus", "plus", "is", "cool"]
        class_.d = "HyperAttribute"
        class_.e = {"d", "e", "f"}
        class_.f = {"another_attribute": 20}
        class_.g = (30, 40)
    delta_attributes_changing_time = time.monotonic() - start_changing_time
    return delta_attributes_changing_time


# @profile
@profile_deco
def make_class_manipulation(
    classname,
    num_of_classes,
    num_of_repeat,
):
    """Make class manipulations with executing time measuring"""

    print(
        f"Manipulations for {num_objects} of {classname.__name__} objects "
        f"with {num_of_repeat} repeats"
    )
    class_creation_time = 0
    class_attributes_changing_time = 0
    class_attributes_accessing_time = 0
    class_attributes_deletion_time = 0
    for _ in range(num_of_repeat):
        classes, delta_time = create_classes(classname, num_of_classes)
        class_creation_time += delta_time
        delta_time = get_class_attributes(classes)
        class_attributes_accessing_time += delta_time
        delta_time = change_class_attributes(classes)
        class_attributes_changing_time += delta_time
        start_deletion_time = time.monotonic()
        del classes
        class_attributes_deletion_time += \
            time.monotonic() - start_deletion_time

    create_time = class_creation_time / num_of_repeat
    access_time = class_attributes_accessing_time / num_of_repeat
    change_time = class_attributes_changing_time / num_of_repeat
    delete_time = class_attributes_deletion_time / num_of_repeat

    print(
        f"{create_time=:0.3f} s\n"
        f"{access_time=:0.3f} s\n"
        f"{change_time=:0.3f} s\n"
        f"{delete_time=:0.3f} s\n"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--objects", type=int, default=10000)
    parser.add_argument("-r", "--repeats", type=int, default=1)

    opts = parser.parse_args()

    num_objects = opts.objects
    num_repeats = opts.repeats

    make_class_manipulation(
        BaseAttributes,
        num_objects,
        num_of_repeat=num_repeats,
    )

    make_class_manipulation(
        SlotsAttributes,
        num_objects,
        num_of_repeat=num_repeats,
    )

    make_class_manipulation(
        WeakRefAttributes,
        num_objects,
        num_of_repeat=num_repeats,
    )

    create_classes.print_stats()
    get_class_attributes.print_stats()
    change_class_attributes.print_stats()
    make_class_manipulation.print_stats()
