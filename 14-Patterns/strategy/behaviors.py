from typing import Protocol


class FlyBehavior(Protocol):
    @staticmethod
    def fly():
        ...


class FlyWithWings(FlyBehavior):
    def fly():
        print("I'm flying!!")


class FlyNoWay(FlyBehavior):
    @staticmethod
    def fly():
        print("I can't fly")


class FlyRocketPowered(FlyBehavior):
    @staticmethod
    def fly():
        print("I'm flying with a rocket!")


class QuackBehavior(Protocol):
    @staticmethod
    def quack():
        ...

class Quack(QuackBehavior):
    @staticmethod
    def quack():
        print("Quack")


class MuteQuack(QuackBehavior):
    @staticmethod
    def quack():
        print("<< Silence >>")


class Squeak(QuackBehavior):
    @staticmethod
    def quack():
        print("Squeak")


class FakeQuack(QuackBehavior):
    @staticmethod
    def quack():
        print("Qwak")
