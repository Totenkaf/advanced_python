class Singleton(type):
    instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__call__(*args, **kwargs)
        return cls.instance


if __name__ == '__main__':

    class User(metaclass=Singleton):
        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return f'<User: {self.name}>'

    u1 = User('Pavel')
    # Начиная с этого момента все пользователи будут Павлами
    u2 = User('Stepan')
    print(u1 is u2)
