"""
Provide tests for private accessibility level that are wrapped to an yet one decorator.
"""
import pytest
from accessify.access import private
from accessify.errors import (
    INACCESSIBLE_DUE_TO_ITS_PROTECTION_LEVEL_EXCEPTION_MESSAGE,
    InaccessibleDueToItsProtectionLevelException,
)
from tests.utils import (
    ENGINE_HAS_BEEN_STARTED_RESPONSE,
    custom_decorator,
)


class CarWithPrivateEngine:

    @private
    def start_engine(self, type_, model, company='Tesla'):
        return ENGINE_HAS_BEEN_STARTED_RESPONSE.format(type_=type_, model=model, company=company)

    def run(self):
        return self.start_engine('electric', 'S', company='Tesla')


class CarWithPrivateStaticMethodEngine:

    @private
    @staticmethod
    def start_engine(type_, model, company='Tesla'):
        return ENGINE_HAS_BEEN_STARTED_RESPONSE.format(type_=type_, model=model, company=company)

    def run(self):
        return self.start_engine('electric', 'S', company='Tesla')


class CarWithPrivateClassMethodEngine:

    @private
    @classmethod
    def start_engine(cls, type_, model, company='Tesla'):
        return ENGINE_HAS_BEEN_STARTED_RESPONSE.format(type_=type_, model=model, company=company)

    def run(self):
        return self.start_engine('electric', 'S', company='Tesla')


class CarWithPrivateCustomDecoratorEngine:

    @private
    @custom_decorator
    def start_engine(cls, type_, model, company='Tesla'):
        return ENGINE_HAS_BEEN_STARTED_RESPONSE.format(type_=type_, model=model, company=company)

    def run(self):
        return self.start_engine('electric', 'S', company='Tesla')


@pytest.mark.parametrize(
    "class_", [
        CarWithPrivateEngine,
        CarWithPrivateStaticMethodEngine,
        CarWithPrivateClassMethodEngine,
        CarWithPrivateCustomDecoratorEngine,
])
def test_private_access_with_decorators(class_, enable_accessify):
    """
    Case: access to the private member of the class that is wrapped to an yet one decorator.
    Expect: inaccessible due to its protection level error message.
    """
    car = class_()

    assert ENGINE_HAS_BEEN_STARTED_RESPONSE.format(type_='electric', model='S', company='Tesla') == car.run()

    expected_error_message = INACCESSIBLE_DUE_TO_ITS_PROTECTION_LEVEL_EXCEPTION_MESSAGE.format(
        class_name=class_.__name__, class_method_name='start_engine',
    )

    with pytest.raises(InaccessibleDueToItsProtectionLevelException) as error:
        car.start_engine('electric', 'S', company='Tesla')

    assert expected_error_message == error.value.message
