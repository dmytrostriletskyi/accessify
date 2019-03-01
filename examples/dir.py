from accessify import accessify, private


@accessify
class Car:

    @private
    def start_engine(self):
        return 'Engine sound.'

if __name__ == '__main__':
    car = Car()

    assert 'start_engine' not in dir(car)
