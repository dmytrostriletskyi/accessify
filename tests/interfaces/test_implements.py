"""
Provide tests for implements interface implementation.
"""
import pytest

from accessify.access import (
    private,
    protected,
)
from accessify.errors import (
    InterfaceMemberHasNotBeenImplementedException,
    ImplementedInterfaceMemberHasIncorrectAccessModifierException,
)
from accessify.interfaces import implements
from tests.utils import custom_decorator


def test_implements():
    """
    Case: implement interfaces.
    Expect: no errors during class initialization.
    """
    class HumanNameInterface:

        @property
        def name(self):
            return

        @name.setter
        def name(self, new_name):
            return

        @name.deleter
        def name(self):
            return

    class HumanBasicsInterface:

        def love(self, who, *args, **kwargs):
            pass

        @staticmethod
        def eat(food, *args, allergy=None, **kwargs):
            pass

        @classmethod
        def think(cls, about, *args, **kwargs):
            pass

    class HumanSoulInterface:

        @private
        @staticmethod
        @custom_decorator
        def dream(about, *args, **kwargs):
            pass

        @protected
        @classmethod
        @custom_decorator
        def die(cls, when, *args, **kwargs):
            pass

    @implements(HumanBasicsInterface, HumanNameInterface, HumanSoulInterface)
    class HumanWithImplementation:

        @property
        def name(self):
            return

        @name.setter
        def name(self, new_name):
            return

        @name.deleter
        def name(self):
            return

        @staticmethod
        def eat(food, *args, allergy=None, **kwargs):
            pass

        def love(self, who, *args, **kwargs):
            pass

        @classmethod
        def think(cls, about, *args, **kwargs):
            pass

        @private
        @staticmethod
        @custom_decorator
        def dream(about, *args, **kwargs):
            pass

        @protected
        @classmethod
        @custom_decorator
        def die(cls, when, *args, **kwargs):
            pass

    assert HumanWithImplementation() is not None


def test_not_implements_private_access():
    """
    Case: do not match member private access.
    Expect: class mismatches interface member access modifier error message.
    """
    class HumanSoulInterface:

        @private
        @staticmethod
        @custom_decorator
        def dream(about, *args, **kwargs):
            pass

    with pytest.raises(ImplementedInterfaceMemberHasIncorrectAccessModifierException) as error:

        @implements(HumanSoulInterface)
        class HumanSoul:

            @staticmethod
            @custom_decorator
            def dream(about, *args, **kwargs):
                pass

    assert 'HumanSoul.dream(about, args, kwargs) mismatches ' \
           'HumanSoulInterface.dream() member access modifier.' == error.value.message


def test_not_implements_protected_access():
    """
    Case: do not match member protected access.
    Expect: class mismatches interface member access modifier error message.
    """
    class HumanSoulInterface:

        @protected
        @classmethod
        @custom_decorator
        def die(cls, when, *args, **kwargs):
            pass

    with pytest.raises(ImplementedInterfaceMemberHasIncorrectAccessModifierException) as error:

        @implements(HumanSoulInterface)
        class HumanSoul:

            @classmethod
            @custom_decorator
            def die(cls, when, *args, **kwargs):
                pass

    assert 'HumanSoul.die(cls, when, args, kwargs) mismatches ' \
           'HumanSoulInterface.die() member access modifier.' == error.value.message


def test_implements_no_implementation_getter():
    """
    Case: do not implement getter.
    Expect: class does not implement interface member error message.
    """
    class HumanNameInterface:

        @property
        def name(self):
            return

    with pytest.raises(InterfaceMemberHasNotBeenImplementedException) as error:

        @implements(HumanNameInterface)
        class HumanWithoutImplementation:
            pass

    assert 'class HumanWithoutImplementation does not implement ' \
           'interface member HumanNameInterface.name(self)' == error.value.message


def test_implements_no_implementation_setter():
    """
    Case: do not implement setter.
    Expect: class does not implement interface member error message.
    """
    class HumanNameInterface:

        @property
        def name(self):
            return

        @name.setter
        def name(self, new_name):
            return

    with pytest.raises(InterfaceMemberHasNotBeenImplementedException) as error:

        @implements(HumanNameInterface)
        class HumanWithoutImplementation:

            @property
            def name(self):
                return

    assert 'class HumanWithoutImplementation does not implement ' \
           'interface member HumanNameInterface.name(self, new_name)' == error.value.message


def test_implements_no_implementation_deleter():
    """
    Case: do not implement deleter.
    Expect: class does not implement interface member error message.
    """
    class HumanNameInterface:

        @property
        def name(self):
            return

        @name.deleter
        def name(self):
            return

    with pytest.raises(InterfaceMemberHasNotBeenImplementedException) as error:

        @implements(HumanNameInterface)
        class HumanWithoutImplementation:

            @property
            def name(self):
                return

    assert 'class HumanWithoutImplementation does not implement ' \
           'interface member HumanNameInterface.name(self)' == error.value.message


def test_implements_no_implementation_static_method():
    """
    Case: do not implement staticmethod.
    Expect: class does not implement interface member error message.
    """
    class HumanBasicsInterface:

        @staticmethod
        def eat(food, *args, allergy=None, **kwargs):
            pass

    with pytest.raises(InterfaceMemberHasNotBeenImplementedException) as error:

        @implements(HumanBasicsInterface)
        class HumanWithoutImplementation:
            pass

    assert 'class HumanWithoutImplementation does not implement ' \
           'interface member HumanBasicsInterface.eat(food, args, allergy, kwargs)' == error.value.message


def test_implements_no_implementation_instance_method():
    """
    Case: do not implement instance method.
    Expect: class does not implement interface member error message.
    """
    class HumanBasicsInterface:

        def love(self, who, *args, **kwargs):
            pass

    with pytest.raises(InterfaceMemberHasNotBeenImplementedException) as error:

        @implements(HumanBasicsInterface)
        class HumanWithoutImplementation:
            pass

    assert 'class HumanWithoutImplementation does not implement ' \
           'interface member HumanBasicsInterface.love(self, who, args, kwargs)' == error.value.message
