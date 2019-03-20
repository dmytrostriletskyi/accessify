"""
Provide tests for setting errors that could be raised in the particular function implementation.
"""
import pytest
from accessify.errors import DeclaredInterfaceExceptionHasNotBeenImplementedException
from accessify.interfaces import (
    implements,
    throws,
)


class HumanDoesNotExistError(Exception):
    pass


class HumanAlreadyInLoveError(Exception):
    pass


class HumanBasicsInterface:

    @throws(HumanDoesNotExistError, HumanAlreadyInLoveError)
    def love(self, who, *args, **kwargs):
        pass


def test_throws(enable_accessify):
    """
    Case: set human does not exist and human already in love errors as required to be raised on the interface function.
    Expect: interface function has the tuple of the errors in magic method called `__throws__`.
    """
    human_basic_interface = HumanBasicsInterface()
    assert human_basic_interface.love.__throws__ == (HumanDoesNotExistError, HumanAlreadyInLoveError, )


def test_throw_not_implemented(enable_accessify):
    """
    Case:
    Expect:
    """
    with pytest.raises(DeclaredInterfaceExceptionHasNotBeenImplementedException) as error:

        @implements(HumanBasicsInterface)
        class HumanWithoutImplementedException:

            def love(self, who, *args, **kwargs):
                if who is None:
                    raise HumanDoesNotExistError

    assert 'Declared exception HumanAlreadyInLoveError by HumanBasicsInterface.love() member has not ' \
           'been implemented by HumanWithoutImplementedException.love(self, who, args, kwargs)' == error.value.message
