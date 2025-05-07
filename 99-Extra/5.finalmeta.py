class FinalMeta(type):

    def __new__(mcs, name, bases, attrs):
        for cls in bases:
            if isinstance(cls, FinalMeta):
                raise TypeError(f"Can't inherit {name} class from final {cls.__name__}")
        return super().__new__(mcs, name, bases, attrs)


if __name__ == '__main__':
    class A(metaclass=FinalMeta):
        """От меня нельзя наследоваться!"""
        pass

    class B(A):
        pass
