"""
Provide tests for inheritance private accessibility level.
"""
import pytest

from accessify.access import (
    accessify,
    private,
)
from accessify.errors import InaccessibleDueToItsProtectionLevelException
from tests.utils import custom_decorator


@accessify
class CarWithPrivateEngineToBeInherited:

    @private
    def start_engine(self, type_, model, company='Tesla'):
        return 'Engine has been started! ' \
               'Details: type is `{type_}`, model is `{model}`, company is `{company}`.'.format(
            type_=type_, model=model, company=company,
        )

    def run(self):
        return self.start_engine('electric', 'S', company='Tesla')


@accessify
class CarWithPrivateStaticMethodEngineToBeInherited:

    @private
    @staticmethod
    def start_engine(self, type_, model, company='Tesla'):
        return 'Engine has been started! ' \
               'Details: type is `{type_}`, model is `{model}`, company is `{company}`.'.format(
            type_=type_, model=model, company=company,
        )

    def run(self):
        return self.start_engine('electric', 'S', company='Tesla')


@accessify
class CarWithPrivateClassMethodEngineToBeInherited:

    @private
    @classmethod
    def start_engine(self, type_, model, company='Tesla'):
        return 'Engine has been started! ' \
               'Details: type is `{type_}`, model is `{model}`, company is `{company}`.'.format(
            type_=type_, model=model, company=company,
        )

    def run(self):
        return self.start_engine('electric', 'S', company='Tesla')


@accessify
class CarWithPrivateCustomDecoratorsAndStaticMethodEngineToBeInherited:

    @private
    @staticmethod
    @custom_decorator
    @custom_decorator
    def start_engine(type_, model, company='Tesla'):
        return 'Engine has been started! ' \
               'Details: type is `{type_}`, model is `{model}`, company is `{company}`.'.format(
            type_=type_, model=model, company=company,
        )

    def run(self):
        return self.start_engine('electric', 'S', company='Tesla')


@pytest.mark.parametrize(
    "class_", [
    CarWithPrivateEngineToBeInherited,
    CarWithPrivateStaticMethodEngineToBeInherited,
    CarWithPrivateClassMethodEngineToBeInherited,
    CarWithPrivateCustomDecoratorsAndStaticMethodEngineToBeInherited,
])
def test_private(class_):
    """
    Case: access to the parent class private method while inheritance.
    Expect: access to the parent class private method while inheritance exception error message is raised.
    """
    class YetAnotherClass:
        pass

    class YetAnotherClassSecond:
        pass

    class YetAnotherClassThird:
        pass

    class ParticularCarWithoutAccessToParentEngine(
        YetAnotherClass, YetAnotherClassSecond, class_, YetAnotherClassThird,
    ):

        def run(self):
            return self.start_engine('electric', 'M', company='Tesla')

    particular_car = ParticularCarWithoutAccessToParentEngine()

    with pytest.raises(InaccessibleDueToItsProtectionLevelException) as error:
        particular_car.run()

    assert '{parent_class_name}.start_engine() is inaccessible due ' \
           'to its protection level'.format(parent_class_name=class_.__name__) == \
           error.value.message
