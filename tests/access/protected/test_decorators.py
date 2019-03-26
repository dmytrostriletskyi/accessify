"""
Provide tests for protected accessibility level that are wrapped to an yet one decorator.
"""
import pytest
from accessify.access import protected
from accessify.errors import InaccessibleDueToItsProtectionLevelException
from tests.utils import (
    ENGINE_HAS_BEEN_STARTED_RESPONSE,
    custom_decorator,
)


class CarWithProtectedEngine:

    @protected
    def start_engine(self, type_, model, company='Tesla'):
        return ENGINE_HAS_BEEN_STARTED_RESPONSE.format(type_=type_, model=model, company=company)

    def run(self):
        return self.start_engine('electric', 'S', company='Tesla')


class CarWithProtectedStaticMethodEngine:

    @protected
    @staticmethod
    def start_engine(type_, model, company='Tesla'):
        return ENGINE_HAS_BEEN_STARTED_RESPONSE.format(type_=type_, model=model, company=company)

    def run(self):
        return self.start_engine('electric', 'S', company='Tesla')


class CarWithProtectedClassMethodEngine:

    @protected
    @classmethod
    def start_engine(cls, type_, model, company='Tesla'):
        return ENGINE_HAS_BEEN_STARTED_RESPONSE.format(type_=type_, model=model, company=company)

    def run(self):
        return self.start_engine('electric', 'S', company='Tesla')


class CarWithProtectedCustomDecoratorEngine:

    @protected
    @custom_decorator
    def start_engine(cls, type_, model, company='Tesla'):
        return ENGINE_HAS_BEEN_STARTED_RESPONSE.format(type_=type_, model=model, company=company)

    def run(self):
        return self.start_engine('electric', 'S', company='Tesla')


@pytest.mark.parametrize(
    "class_", [
        CarWithProtectedEngine,
        CarWithProtectedStaticMethodEngine,
        CarWithProtectedClassMethodEngine,
        CarWithProtectedCustomDecoratorEngine,
])
def test_protected_access_with_decorators(class_, enable_accessify):
    """
    Case: access to the protected member of the class that is wrapped to an yet one decorator.
    Expect: inaccessible due to its protection level error message.
    """
    car = class_()

    assert ENGINE_HAS_BEEN_STARTED_RESPONSE.format(type_='electric', model='S', company='Tesla') == car.run()

    with pytest.raises(InaccessibleDueToItsProtectionLevelException) as error:
        car.start_engine('electric', 'S', company='Tesla')

    assert '{class_with_method}.start_engine() is inaccessible due ' \
           'to its protection level'.format(class_with_method=class_.__name__) == \
           error.value.message
