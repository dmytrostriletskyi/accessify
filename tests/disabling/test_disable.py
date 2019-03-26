"""
Provide tests for disabling accessify accessibility levels and implementing interfaces checking.
"""
from accessify import (
    implements,
    private,
    protected,
)


class CarInterface:

    def start_engine(self, type, model):
        pass


def test_disabling_accessify(disable_accessify):
    """
    Case: disable accessify checking accessibility levels and interfaces with disabling accessify environment variable.
    Expect: accessify does not check accessibility levels and implementing interfaces.
    """
    @implements(CarInterface)
    class Car:

        @private
        def private_start_engine(self):
            return 'Engine sound.'

        @protected
        def protected_start_engine(self):
            return 'Engine sound.'

        def run(self):
            return self.private_start_engine() + ' ' + self.protected_start_engine()

    car = Car()

    assert 'Engine sound. Engine sound.' == car.run()

    assert 'Engine sound.' == car.private_start_engine()
    assert 'Engine sound.' == car.protected_start_engine()
