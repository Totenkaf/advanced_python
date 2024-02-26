from ducks import MallardDuck
from ducks import ModelDuck
from behaviors import FlyRocketPowered


if __name__ == '__main__':
    mallard = MallardDuck()
    mallard.quack()
    mallard.fly()

    model = ModelDuck()
    model.quack()
    model.fly()
    model.set_fly_behavior(FlyRocketPowered())
    model.fly()
