from abc import ABC, abstractmethod

from behaviors import FlyBehavior
from behaviors import FlyNoWay
from behaviors import FlyWithWings
from behaviors import MuteQuack
from behaviors import Squeak
from behaviors import Quack
from behaviors import QuackBehavior


class Duck(ABC):
    """Abstract super-class for all ducks"""
    quack_behavior: QuackBehavior = None
    fly_behavior: FlyBehavior = None

    @staticmethod
    @abstractmethod
    def display() -> None:
        ...

    def fly(self) -> None:
        self.fly_behavior.fly()

    def quack(self) -> None:
        self.quack_behavior.quack()

    def set_quack_behavior(self, quack_behavior: QuackBehavior) -> None:
        self.quack_behavior = quack_behavior

    def set_fly_behavior(self, fly_behavior: FlyBehavior) -> None:
        self.fly_behavior = fly_behavior

    @staticmethod
    def swim() -> None:
        print("All ducks float, even decoys!!")


class MallardDuck(Duck):

    def __init__(self):
        self.fly_behavior = FlyWithWings()
        self.quack_behavior = Quack()

    @staticmethod
    def display():
        print("I'm a real Mallard duck")


class DecoyDuck(Duck):

    def __init__(self):
        self.fly_behavior = FlyNoWay()
        self.quack_behavior = MuteQuack()

    @staticmethod
    def display():
        print("I'm a duck Decoy")


class RubberDuck(Duck):

    def __init__(self):
        self.fly_behavior = FlyNoWay()
        self.quack_behavior = Squeak()

    @staticmethod
    def display():
        print("I'm a rubber duckie")


class RedHeadDuck(Duck):

    def __init__(self):
        self.fly_behavior = FlyWithWings()
        self.quack_behavior = Quack()

    @staticmethod
    def display():
        print("I'm a real Red Headed duck")


class ModelDuck(Duck):

    def __init__(self):
        self.fly_behavior = FlyNoWay()
        self.quack_behavior = Quack()

    @staticmethod
    def display():
        print("I'm a model duck")
