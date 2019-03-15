"""
Provide implementation of accessibility levels.
"""
import copy
import inspect

from accessify.errors import (
    INACCESSIBLE_DUE_TO_ITS_PROTECTION_LEVEL_EXCEPTION_MESSAGE,
    InaccessibleDueToItsProtectionLevelException,
)
from accessify.utils import (
    ACCESS_WRAPPERS_NAMES,
    ClassMemberDefaultArguments,
    ClassMemberMagicMethodNames,
    ClassMemberTypes,
    does_parents_contain_private_method,
    find_decorated_method,
)


def accessify(cls):
    """
    Mark class as class that uses accessibility levels.

    Rules:
        - check if called method is covered by private access decorator,
        - remove method that covered by private access decorator from __dir__.
    """
    class_locals = copy.deepcopy(dir(cls))

    for name, func in list(cls.__dict__.items()):

        if hasattr(func, ClassMemberMagicMethodNames.NAME):

            if func.__name__ in ACCESS_WRAPPERS_NAMES:
                class_locals.remove(name)

    def dir_magic_method_mock(_):
        return class_locals

    cls.__dir__ = dir_magic_method_mock

    return cls


def private(func):
    """
    Provide private accessibility level.
    """
    def private_wrapper(*args, **kwargs):
        """
        Provide private accessibility level wrapper.
        """
        instance, *arguments_without_instance = args
        instance_class = instance.__class__
        instance_class_parents = instance.__class__.__bases__

        method = find_decorated_method(function=func)

        does_contain, class_contain = does_parents_contain_private_method(classes=instance_class_parents, method=method)

        if class_contain:
            raise InaccessibleDueToItsProtectionLevelException(
                INACCESSIBLE_DUE_TO_ITS_PROTECTION_LEVEL_EXCEPTION_MESSAGE.format(
                    class_name=class_contain.__name__, class_method_name=method.__name__,
                ),
            )

        if inspect.currentframe().f_back.f_locals.get(ClassMemberDefaultArguments.SELF) is None:
            raise InaccessibleDueToItsProtectionLevelException(
                INACCESSIBLE_DUE_TO_ITS_PROTECTION_LEVEL_EXCEPTION_MESSAGE.format(
                    class_name=instance_class.__name__, class_method_name=method.__name__,
                ),
            )

        if func.__class__.__name__ == ClassMemberTypes.CLASS_METHOD:
            arguments = (instance_class, ) + tuple(arguments_without_instance)
            return func.__func__(*arguments, **kwargs)

        elif func.__class__.__name__ == ClassMemberTypes.STATIC_METHOD:
            return func.__func__(*arguments_without_instance, **kwargs)

        else:
            return func(*args, **kwargs)

    return private_wrapper


def protected(func):
    """
    Provide private accessibility level.
    """
    def protected_wrapper(*args, **kwargs):
        """
        Provide private accessibility level wrapper.
        """
        instance, *arguments_without_instance = args
        instance_class = instance.__class__

        method = find_decorated_method(function=func)

        if inspect.currentframe().f_back.f_locals.get(ClassMemberDefaultArguments.SELF) is None:
            raise InaccessibleDueToItsProtectionLevelException(
                INACCESSIBLE_DUE_TO_ITS_PROTECTION_LEVEL_EXCEPTION_MESSAGE.format(
                    class_name=instance_class.__name__, class_method_name=method.__name__,
                ),
            )

        instance, *arguments_without_instance = args
        instance_class = instance.__class__

        if func.__class__.__name__ == ClassMemberTypes.CLASS_METHOD:
            arguments = (instance_class, ) + tuple(arguments_without_instance)
            return func.__func__(*arguments, **kwargs)

        elif func.__class__.__name__ == ClassMemberTypes.STATIC_METHOD:
            return func.__func__(*arguments_without_instance, **kwargs)

        else:
            return func(*args, **kwargs)

    return protected_wrapper
