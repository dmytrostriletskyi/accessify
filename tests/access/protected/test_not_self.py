"""
Provide tests for protected accessibility level that is used in cases of unfollowing naming convention.
"""
import pytest
from accessify.access import protected
from accessify.errors import (
    INACCESSIBLE_DUE_TO_ITS_PROTECTION_LEVEL_EXCEPTION_MESSAGE,
    InaccessibleDueToItsProtectionLevelException,
)
from tests.utils import ENGINE_HAS_BEEN_STARTED_RESPONSE


class CarWithProtectedEngine:

    @protected
    def start_engine(this, type_, model, company='Tesla'):
        return ENGINE_HAS_BEEN_STARTED_RESPONSE.format(type_=type_, model=model, company=company)

    def run(this):
        return this.start_engine('electric', 'S', company='Tesla')


class Lamborghini(CarWithProtectedEngine):

    def run(this):
        return this.start_engine('electric', 'S', company='Tesla')


class Tesla:

    @classmethod
    def run(this):
        car = CarWithProtectedEngine()
        return car.start_engine('electric', 'S', company='Tesla')


def test_protected_access_inside_class(enable_accessify):
    """
    Case: access to the protected member, which do not follow naming convention, inside member's class.
    Expect: protected member is accessible.
    """
    car = CarWithProtectedEngine()

    assert ENGINE_HAS_BEEN_STARTED_RESPONSE.format(type_='electric', model='S', company='Tesla') == car.run()


def test_protected_access_inside_child_class(enable_accessify):
    """
    Case: access to the parent protected member, which do not follow naming convention, inside child class.
    Expect: protected member is accessible.
    """
    lamborghini = Lamborghini()

    assert ENGINE_HAS_BEEN_STARTED_RESPONSE.format(type_='electric', model='S', company='Tesla') == lamborghini.run()


def test_protected_access_through_child_class_object(enable_accessify):
    """
    Case: access to the parent protected member, which do not follow naming convention, through member's class child object.
    Expect: inaccessible due to its protection level error message.
    """
    lamborghini = Lamborghini()

    expected_error_message = INACCESSIBLE_DUE_TO_ITS_PROTECTION_LEVEL_EXCEPTION_MESSAGE.format(
        class_name=Lamborghini.__name__, class_method_name='start_engine',
    )

    with pytest.raises(InaccessibleDueToItsProtectionLevelException) as error:
        lamborghini.start_engine()

    assert expected_error_message == error.value.message


def test_protected_access_through_object(enable_accessify):
    """
    Case: access to the protected member, which do not follow naming convention, through member's class object.
    Expect: inaccessible due to its protection level error message.
    """
    car = CarWithProtectedEngine()

    expected_error_message = INACCESSIBLE_DUE_TO_ITS_PROTECTION_LEVEL_EXCEPTION_MESSAGE.format(
        class_name=CarWithProtectedEngine.__name__, class_method_name='start_engine',
    )

    with pytest.raises(InaccessibleDueToItsProtectionLevelException) as error:
        car.start_engine()

    assert expected_error_message == error.value.message


def test_protected_access_through_caller_object(enable_accessify):
    """
    Case: access to protected member, which do not follow naming conv., through member's class object in another class.
    Expect: inaccessible due to its protection level error message.
    """
    tesla = Tesla()

    expected_error_message = INACCESSIBLE_DUE_TO_ITS_PROTECTION_LEVEL_EXCEPTION_MESSAGE.format(
        class_name=CarWithProtectedEngine.__name__, class_method_name='start_engine',
    )

    with pytest.raises(InaccessibleDueToItsProtectionLevelException) as error:
        tesla.run()

    assert expected_error_message == error.value.message
