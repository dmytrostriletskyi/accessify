"""
Provide tests for private accessibility level that is used in cases of unfollowing naming convention.
"""
import pytest
from accessify.access import private
from accessify.errors import (
    INACCESSIBLE_DUE_TO_ITS_PROTECTION_LEVEL_EXCEPTION_MESSAGE,
    InaccessibleDueToItsProtectionLevelException,
)
from tests.utils import ENGINE_HAS_BEEN_STARTED_RESPONSE


class CarWithPrivateEngine:

    @private
    def start_engine(this, type_, model, company='Tesla'):
        return ENGINE_HAS_BEEN_STARTED_RESPONSE.format(type_=type_, model=model, company=company)

    def run(this):
        return this.start_engine('electric', 'S', company='Tesla')


class Tesla:

    @classmethod
    def run(this):
        car = CarWithPrivateEngine()
        return car.start_engine('electric', 'S', company='Tesla')


def test_private_access_inside_class(enable_accessify):
    """
    Case: access to the private member, which do not follow naming convention, inside member's class.
    Expect: private member is accessible.
    """
    car = CarWithPrivateEngine()

    assert ENGINE_HAS_BEEN_STARTED_RESPONSE.format(type_='electric', model='S', company='Tesla') == car.run()


def test_private_access_through_object(enable_accessify):
    """
    Case: access to the private member, which do not follow naming convention, through member's class object.
    Expect: inaccessible due to its protection level error message.
    """
    car = CarWithPrivateEngine()

    expected_error_message = INACCESSIBLE_DUE_TO_ITS_PROTECTION_LEVEL_EXCEPTION_MESSAGE.format(
        class_name=CarWithPrivateEngine.__name__, class_method_name='start_engine',
    )

    with pytest.raises(InaccessibleDueToItsProtectionLevelException) as error:
        car.start_engine()

    assert expected_error_message == error.value.message


def test_private_access_through_caller_object(enable_accessify):
    """
    Case: access to private member, which do not follow naming conv., through member's class object in another class.
    Expect: inaccessible due to its protection level error message.
    """
    tesla = Tesla()

    expected_error_message = INACCESSIBLE_DUE_TO_ITS_PROTECTION_LEVEL_EXCEPTION_MESSAGE.format(
        class_name=CarWithPrivateEngine.__name__, class_method_name='start_engine',
    )

    with pytest.raises(InaccessibleDueToItsProtectionLevelException) as error:
        tesla.run()

    assert expected_error_message == error.value.message
