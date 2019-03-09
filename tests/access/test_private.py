"""
Provide tests for private accessibility level.
"""
import pytest

from accessify.access import (
    accessify,
    private,
)
from accessify.errors import InaccessibleDueToItsProtectionLevelException
from tests.utils import custom_decorator


@accessify
class CarWithPrivateEngine:

    @private
    def start_engine(self, type_, model, company='Tesla'):
        return 'Engine has been started! ' \
               'Details: type is `{type_}`, model is `{model}`, company is `{company}`.'.format(
            type_=type_, model=model, company=company,
        )

    def run(self):
        return self.start_engine('electric', 'S', company='Tesla')


@accessify
class CarWithPrivateStaticMethodEngine:

    @private
    @staticmethod
    def start_engine(type_, model, company='Tesla'):
        return 'Engine has been started! ' \
               'Details: type is `{type_}`, model is `{model}`, company is `{company}`.'.format(
            type_=type_, model=model, company=company,
        )

    def run(self):
        return self.start_engine('electric', 'S', company='Tesla')


@accessify
class CarWithPrivateClassMethodEngine:

    @private
    @classmethod
    def start_engine(cls, type_, model, company='Tesla'):
        return 'Engine has been started! ' \
               'Details: type is `{type_}`, model is `{model}`, company is `{company}`.'.format(
            type_=type_, model=model, company=company,
        )

    def run(self):
        return self.start_engine('electric', 'S', company='Tesla')


@accessify
class CarWithPrivateCustomDecoratorEngine:

    @private
    @custom_decorator
    def start_engine(cls, type_, model, company='Tesla'):
        return 'Engine has been started! ' \
               'Details: type is `{type_}`, model is `{model}`, company is `{company}`.'.format(
            type_=type_, model=model, company=company,
        )

    def run(self):
        return self.start_engine('electric', 'S', company='Tesla')


@pytest.mark.parametrize(
    "class_", [
    CarWithPrivateEngine,
    CarWithPrivateStaticMethodEngine,
    CarWithPrivateClassMethodEngine,
    CarWithPrivateCustomDecoratorEngine,
])
def test_private(class_):
    """
    Case: access to the private member of the class.
    Expect: protected member not in dir(), raise access to private method exception.
    """
    car = class_()

    assert 'Engine has been started! Details: type is `electric`, model is `S`, company is `Tesla`.' == \
           car.run()

    assert 'start_engine' not in dir(car)

    with pytest.raises(InaccessibleDueToItsProtectionLevelException) as error:
        car.start_engine('electric', 'S', company='Tesla')

    assert '{class_with_method}.start_engine() is inaccessible due ' \
           'to its protection level'.format(class_with_method=class_.__name__) == \
           error.value.message
