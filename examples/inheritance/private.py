from accessify import private


class Car:

    @private
    def start_engine(self):
        return 'Engine sound.'


class Tesla(Car):

    def run(self):
        return self.start_engine()


if __name__ == '__main__':
    tesla = Tesla()
    tesla.run()
