"""
Notes on Usage:
This class demonstrates all available Python dunder methods as of Python 3.10.

Not all methods need to be implemented in a real class - only implement what you need.
Some methods are mutually exclusive (like __getattr__ and __getattribute__).

Some methods are rarely used in practice (__complex__, __index__, etc.).

The implementations are simplified for demonstration - real-world usage would need more robust error handling.

To use any of these methods, you would typically just use the corresponding Python operation and the dunder
method will be called automatically.

For example:
0 print(obj) calls __str__
- len(obj) calls __len__
- obj + 5 calls __add__
- with obj: calls __enter__ and __exit__
"""


class DunderDemo:
    """
    A demonstration class showcasing all available Python dunder (double underscore) methods.
    Each method is commented to explain its purpose and usage.
    """

    # 1. Object Initialization and Representation

    def __new__(cls, name, bases, namespace, **kwargs):
        """Called to create the class object itself"""
        print(f"Meta __new__: Creating class {name}")
        # Add a class attribute to all classes using this metaclass
        namespace['created_by_meta'] = True
        return super().__new__(cls, name, bases, namespace)

    def __init__(self, name, bases, namespace, **kwargs):
        """Called after the class is created to initialize it"""
        print(f"Meta __init__: Initializing class {name}")
        super().__init__(name, bases, namespace)

    def __del__(self):
        """Destructor - Called when object is about to be destroyed"""
        print(f"Class __del__: Deleting instance with value {self.value}")

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        """
        Метод __prepare__ в Python используется для настройки пространства имен (namespace),
        которое будет использоваться при создании класса.
        Метод должен вернуть объект-словарь, который интерпретатор заполняет в момент парсинга тела класса

        - Сохранение порядка объявления атрибутов класса (класс Enum)
        class EnumMeta(type):
            @classmethod
            def __prepare__(cls, name, bases):
                return {}

            def __new__(mcls, name, bases, namespace):
                # Автоматически нумеруем значения
                for i, name in enumerate(namespace.get('_member_names', [])):
                    namespace[name] = i
                return super().__new__(mcls, name, bases, namespace)

        class Color(metaclass=EnumMeta):
            _member_names = ['RED', 'GREEN', 'BLUE']

        - Предварительная обработка атрибутов перед созданием класса
        class UpperCaseAttributes(type):
            @classmethod
            def __prepare__(cls, name, bases):
                return defaultdict(str)  # Все атрибуты будут uppercase

        - Логирование или отслеживание создания атрибутов
        class LoggingMeta(type):
            @classmethod
            def __prepare__(cls, name, bases):
                class LoggingDict(dict):
                    def __setitem__(self, key, value):
                        print(f"Defining attribute: {key} = {value}")
                        super().__setitem__(key, value)
                return LoggingDict()

        - Валидация атрибутов на этапе определения класса
        class ValidationMeta(type):
            @classmethod
            def __prepare__(cls, name, bases):
                class ValidatingDict(dict):
                    def __setitem__(self, key, value):
                        if key.startswith('_'):
                            raise ValueError("Protected attributes not allowed")
                        super().__setitem__(key, value)
                return ValidatingDict()

        Когда НЕ нужно использовать __prepare__:
        - Для обычных классов без метаклассов
        - Когда не требуется контроль над пространством имен
        - Для простых случаев, где достаточно стандартного dict

        Важные особенности:
        - __prepare__ должен быть классметодом (@classmethod)
        - Должен возвращать объект, поддерживающий интерфейс словаря
        - Вызывается перед __new__ и __init__ метакласса
        - Работает только в Python 3 и выше
        """
        print(f"Class __prepare__: Preparing namespace for {name}")
        return {}

    @classmethod
    def __instancecheck__(cls, instance):
        """Override isinstance() check for this class"""
        print(f"Class __instancecheck__: Checking {instance}")
        return hasattr(instance, 'value')

    @classmethod
    def __subclasscheck__(cls, subclass):
        """Override issubclass() check for this class"""
        print(f"Class __subclasscheck__: Checking {subclass}")
        return True

    def __call__(cls, *args, **kwargs):
        """Called when an instance is 'called' (instantiated)"""
        print(f"Meta __call__: Creating instance of {cls.__name__}")
        # Custom instance creation - could modify or wrap the standard behavior
        instance = super().__call__(*args, **kwargs)
        instance._meta_created = True
        return instance

    def __repr__(self):
        """Unambiguous string representation - Used by repr() and for debugging"""
        return f"DunderDemo({self.value!r})"

    def __str__(self):
        """Readable string representation - Used by str() and print()"""
        return f"DunderDemo with value: {self.value}"

    def __format__(self, format_spec):
        """Custom formatting - Used by format() and f-strings"""
        return f"Formatted: {self.value:{format_spec}}"

    def __bytes__(self):
        """Byte representation - Used by bytes()"""
        return bytes(str(self).encode('utf-8'))

    # 2. Rich Comparison Methods

    def __eq__(self, other):
        """Equality check - Used by =="""
        if not isinstance(other, DunderDemo):
            return NotImplemented
        return self.value == other.value

    def __ne__(self, other):
        """Inequality check - Used by !="""
        if not isinstance(other, DunderDemo):
            return NotImplemented
        return self.value != other.value

    def __lt__(self, other):
        """Less than - Used by <"""
        if not isinstance(other, DunderDemo):
            return NotImplemented
        return self.value < other.value

    def __le__(self, other):
        """Less than or equal - Used by <="""
        if not isinstance(other, DunderDemo):
            return NotImplemented
        return self.value <= other.value

    def __gt__(self, other):
        """Greater than - Used by >"""
        if not isinstance(other, DunderDemo):
            return NotImplemented
        return self.value > other.value

    def __ge__(self, other):
        """Greater than or equal - Used by >="""
        if not isinstance(other, DunderDemo):
            return NotImplemented
        return self.value >= other.value

    # 3. Arithmetic Operations

    def __add__(self, other):
        """Addition - Used by +"""
        if not isinstance(other, (DunderDemo, int, float)):
            return NotImplemented
        other_val = other.value if isinstance(other, DunderDemo) else other
        return DunderDemo(self.value + other_val)

    def __sub__(self, other):
        """Subtraction - Used by -"""
        if not isinstance(other, (DunderDemo, int, float)):
            return NotImplemented
        other_val = other.value if isinstance(other, DunderDemo) else other
        return DunderDemo(self.value - other_val)

    def __mul__(self, other):
        """Multiplication - Used by *"""
        if not isinstance(other, (DunderDemo, int, float)):
            return NotImplemented
        other_val = other.value if isinstance(other, DunderDemo) else other
        return DunderDemo(self.value * other_val)

    def __truediv__(self, other):
        """True division - Used by /"""
        if not isinstance(other, (DunderDemo, int, float)):
            return NotImplemented
        other_val = other.value if isinstance(other, DunderDemo) else other
        return DunderDemo(self.value / other_val)

    def __floordiv__(self, other):
        """Floor division - Used by //"""
        if not isinstance(other, (DunderDemo, int, float)):
            return NotImplemented
        other_val = other.value if isinstance(other, DunderDemo) else other
        return DunderDemo(self.value // other_val)

    def __mod__(self, other):
        """Modulo - Used by %"""
        if not isinstance(other, (DunderDemo, int, float)):
            return NotImplemented
        other_val = other.value if isinstance(other, DunderDemo) else other
        return DunderDemo(self.value % other_val)

    def __divmod__(self, other):
        """Divmod - Used by divmod()"""
        if not isinstance(other, (DunderDemo, int, float)):
            return NotImplemented
        other_val = other.value if isinstance(other, DunderDemo) else other
        return divmod(self.value, other_val)

    def __pow__(self, other, modulo=None):
        """Exponentiation - Used by ** or pow()"""
        if not isinstance(other, (DunderDemo, int, float)):
            return NotImplemented
        other_val = other.value if isinstance(other, DunderDemo) else other
        return DunderDemo(pow(self.value, other_val, modulo))

    # 4. Unary Operations

    def __neg__(self):
        """Negation - Used by -"""
        return DunderDemo(-self.value)

    def __pos__(self):
        """Unary plus - Used by +"""
        return DunderDemo(+self.value)

    def __abs__(self):
        """Absolute value - Used by abs()"""
        return DunderDemo(abs(self.value))

    def __invert__(self):
        """Bitwise inversion - Used by ~"""
        return DunderDemo(~self.value)

    # 5. Type Conversion

    def __int__(self):
        """Integer conversion - Used by int()"""
        return int(self.value)

    def __float__(self):
        """Float conversion - Used by float()"""
        return float(self.value)

    def __complex__(self):
        """Complex conversion - Used by complex()"""
        return complex(self.value)

    def __bool__(self):
        """Boolean conversion - Used by bool() and truthiness testing"""
        return bool(self.value)

    def __index__(self):
        """Integer conversion for slicing - Used by operators expecting integers"""
        return int(self.value)

    # 6. Container Methods (for sequence-like behavior)

    def __len__(self):
        """Length - Used by len()"""
        return len(str(self.value))

    def __getitem__(self, key):
        """Indexing - Used by obj[key]"""
        return str(self.value)[key]

    def __setitem__(self, key, value):
        """Assignment to index - Used by obj[key] = value"""
        temp = list(str(self.value))
        temp[key] = str(value)
        self.value = int(''.join(temp))

    def __delitem__(self, key):
        """Deletion of index - Used by del obj[key]"""
        temp = list(str(self.value))
        del temp[key]
        self.value = int(''.join(temp))

    def __contains__(self, item):
        """Membership test - Used by 'in' operator"""
        return str(item) in str(self.value)

    def __reversed__(self):
        """Reverse iteration - Used by reversed()"""
        return reversed(str(self.value))

    # 7. Context Managers

    def __enter__(self):
        """Enter context - Used by 'with' statement"""
        print("Entering context")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context - Used by 'with' statement"""
        print("Exiting context")
        if exc_type is not None:
            print(f"Exception occurred: {exc_val}")
        return False  # Don't suppress exceptions

    # 8. Callable Objects

    def __call__(self, *args, **kwargs):
        """Make instance callable - Used by obj()"""
        print(f"Called with args: {args}, kwargs: {kwargs}")
        return self.value

    # 9. Attribute Access

    def __getattribute__(self, name):
        """Called for all attribute access (use with caution!)"""
        print(f"__getattribute__: Accessing {name}")
        try:
            return super().__getattribute__(name)
        except AttributeError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __getattr__(self, name):
        """Called when attribute not found - Used by obj.missing_attr"""
        print(f"Accessing missing attribute: {name}")
        return f"Dummy value for {name}"

    def __setattr__(self, name, value):
        """Called on all attribute assignment"""
        print(f"Setting attribute: {name} = {value}")
        super().__setattr__(name, value)

    def __delattr__(self, name):
        """Called on attribute deletion - Used by del obj.attr"""
        print(f"Deleting attribute: {name}")
        super().__delattr__(name)

    def __dir__(self):
        """Customize dir() listing"""
        base = super().__dir__()
        return base + ['extra_attr1', 'extra_attr2']

    # 10. Descriptors

    def __get__(self, instance, owner):
        """Descriptor getter - Used when class is attribute of another class"""
        print(f"Descriptor get: instance={instance}, owner={owner}")
        return self.value

    def __set__(self, instance, value):
        """Descriptor setter"""
        print(f"Descriptor set: instance={instance}, value={value}")
        self.value = value

    def __delete__(self, instance):
        """Descriptor deleter"""
        print(f"Descriptor delete: instance={instance}")
        del self.value

    # 11. Numeric Type Emulation

    def __radd__(self, other):
        """Reverse addition - Used when left operand doesn't support +"""
        return self.__add__(other)

    def __rsub__(self, other):
        """Reverse subtraction"""
        return DunderDemo(other - self.value)

    def __rmul__(self, other):
        """Reverse multiplication"""
        return self.__mul__(other)

    def __rtruediv__(self, other):
        """Reverse true division"""
        return DunderDemo(other / self.value)

    def __rfloordiv__(self, other):
        """Reverse floor division"""
        return DunderDemo(other // self.value)

    def __rmod__(self, other):
        """Reverse modulo"""
        return DunderDemo(other % self.value)

    def __rdivmod__(self, other):
        """Reverse divmod"""
        return divmod(other, self.value)

    def __rpow__(self, other):
        """Reverse power"""
        return DunderDemo(other ** self.value)

    def __iadd__(self, other):
        """In-place addition - Used by +="""
        self.value += other.value if isinstance(other, DunderDemo) else other
        return self

    def __isub__(self, other):
        """In-place subtraction - Used by -="""
        self.value -= other.value if isinstance(other, DunderDemo) else other
        return self

    def __imul__(self, other):
        """In-place multiplication - Used by *="""
        self.value *= other.value if isinstance(other, DunderDemo) else other
        return self

    def __itruediv__(self, other):
        """In-place true division - Used by /="""
        self.value /= other.value if isinstance(other, DunderDemo) else other
        return self

    def __ifloordiv__(self, other):
        """In-place floor division - Used by //="""
        self.value //= other.value if isinstance(other, DunderDemo) else other
        return self

    def __imod__(self, other):
        """In-place modulo - Used by %="""
        self.value %= other.value if isinstance(other, DunderDemo) else other
        return self

    def __ipow__(self, other):
        """In-place power - Used by **="""
        self.value **= other.value if isinstance(other, DunderDemo) else other
        return self

    # 12. Bitwise Operations

    def __and__(self, other):
        """Bitwise AND - Used by &"""
        if not isinstance(other, (DunderDemo, int)):
            return NotImplemented
        other_val = other.value if isinstance(other, DunderDemo) else other
        return DunderDemo(self.value & other_val)

    def __or__(self, other):
        """Bitwise OR - Used by |"""
        if not isinstance(other, (DunderDemo, int)):
            return NotImplemented
        other_val = other.value if isinstance(other, DunderDemo) else other
        return DunderDemo(self.value | other_val)

    def __xor__(self, other):
        """Bitwise XOR - Used by ^"""
        if not isinstance(other, (DunderDemo, int)):
            return NotImplemented
        other_val = other.value if isinstance(other, DunderDemo) else other
        return DunderDemo(self.value ^ other_val)

    def __lshift__(self, other):
        """Left shift - Used by <<"""
        if not isinstance(other, (DunderDemo, int)):
            return NotImplemented
        other_val = other.value if isinstance(other, DunderDemo) else other
        return DunderDemo(self.value << other_val)

    def __rshift__(self, other):
        """Right shift - Used by >>"""
        if not isinstance(other, (DunderDemo, int)):
            return NotImplemented
        other_val = other.value if isinstance(other, DunderDemo) else other
        return DunderDemo(self.value >> other_val)

    def __rand__(self, other):
        """Reverse bitwise AND"""
        return self.__and__(other)

    def __ror__(self, other):
        """Reverse bitwise OR"""
        return self.__or__(other)

    def __rxor__(self, other):
        """Reverse bitwise XOR"""
        return self.__xor__(other)

    def __rlshift__(self, other):
        """Reverse left shift"""
        return DunderDemo(other << self.value)

    def __rrshift__(self, other):
        """Reverse right shift"""
        return DunderDemo(other >> self.value)

    def __iand__(self, other):
        """In-place bitwise AND - Used by &="""
        self.value &= other.value if isinstance(other, DunderDemo) else other
        return self

    def __ior__(self, other):
        """In-place bitwise OR - Used by |="""
        self.value |= other.value if isinstance(other, DunderDemo) else other
        return self

    def __ixor__(self, other):
        """In-place bitwise XOR - Used by ^="""
        self.value ^= other.value if isinstance(other, DunderDemo) else other
        return self

    def __ilshift__(self, other):
        """In-place left shift - Used by <<="""
        self.value <<= other.value if isinstance(other, DunderDemo) else other
        return self

    def __irshift__(self, other):
        """In-place right shift - Used by >>="""
        self.value >>= other.value if isinstance(other, DunderDemo) else other
        return self

    # 13. Class Creation

    def __init_subclass__(cls, **kwargs):
        """Called when subclass is created"""
        print(f"Initializing subclass: {cls.__name__}")
        super().__init_subclass__(**kwargs)

    @classmethod
    def __class_getitem__(cls, item):
        """Class generic type parameters - Used by Class[type]"""
        print(f"Class getitem with: {item}")
        return cls

    # 14. Asynchronous Operations

    def __await__(self):
        """Return iterator for await expression"""

        async def _await():
            return self.value

        return _await().__await__()

    # 15. Other Special Methods

    def __hash__(self):
        """Hash value - Used by hash() and when object is dictionary key"""
        return hash(self.value)

    def __instancecheck__(self, instance):
        """Custom isinstance() check"""
        return isinstance(instance, DunderDemo)

    def __subclasscheck__(self, subclass):
        """Custom issubclass() check"""
        return issubclass(subclass, DunderDemo)

    def __copy__(self):
        """Shallow copy - Used by copy.copy()"""
        return DunderDemo(self.value)

    def __deepcopy__(self, memo):
        """Deep copy - Used by copy.deepcopy()"""
        from copy import deepcopy
        return DunderDemo(deepcopy(self.value, memo))

    def __reduce__(self):
        """Pickling support - Used by pickle.dump()"""
        return (self.__class__, (self.value,))

    def __reduce_ex__(self, protocol):
        """Pickling support with protocol version"""
        return self.__reduce__()

    def __getstate__(self):
        """Custom state for pickling"""
        return {'value': self.value}

    def __setstate__(self, state):
        """Restore state when unpickling"""
        self.value = state['value']

    def __sizeof__(self):
        """Size in memory - Used by sys.getsizeof()"""
        return object.__sizeof__(self) + self.value.__sizeof__()

    def __matmul__(self, other):
        """Matrix multiplication - Used by @"""
        if not isinstance(other, (DunderDemo, int, float)):
            return NotImplemented
        other_val = other.value if isinstance(other, DunderDemo) else other
        return DunderDemo(self.value * other_val)  # Simple example

    def __rmatmul__(self, other):
        """Reverse matrix multiplication"""
        return self.__matmul__(other)

    def __imatmul__(self, other):
        """In-place matrix multiplication - Used by @="""
        self.value *= other.value if isinstance(other, DunderDemo) else other
        return self
