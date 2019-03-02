from accessify import private


class Car:

    @private
    def start_engine(self):
        return 'Engine sound.'

    def run(self):
        return self.start_engine()


if __name__ == '__main__':
    car = Car()

    assert 'Engine sound.' == car.run()

    car.start_engine()
