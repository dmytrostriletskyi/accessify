"""
Provide implementation of accessibility levels.
"""
import copy
import inspect
import os

from accessify.errors import (
    INACCESSIBLE_DUE_TO_ITS_PROTECTION_LEVEL_EXCEPTION_MESSAGE,
    InaccessibleDueToItsProtectionLevelException,
)
from accessify.utils import (
    ACCESS_WRAPPERS_NAMES,
    DISABLE_ACCESSIFY_ENV_VARIABLE_NAME,
    ClassMemberMagicMethodNames,
    ClassMemberTypes,
    does_classes_contain_private_method,
    find_decorated_method,
    get_method_class_by_frame,
)


def accessify(cls):
    """
    Mark class as class that uses accessibility levels.

    Check if called method is covered by accessibility level decorators, then remove it from __dir__.
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

        if os.environ.get(DISABLE_ACCESSIFY_ENV_VARIABLE_NAME) is None:
            method = find_decorated_method(function=func)

            does_class_contain_private_method, class_that_contains_private_method = \
                does_classes_contain_private_method(classes=instance_class_parents, method=method)

            if does_class_contain_private_method:
                raise InaccessibleDueToItsProtectionLevelException(
                    INACCESSIBLE_DUE_TO_ITS_PROTECTION_LEVEL_EXCEPTION_MESSAGE.format(
                        class_name=class_that_contains_private_method.__name__, class_method_name=method.__name__,
                    ),
                )

            method_caller_frame = inspect.currentframe().f_back
            method_caller_class = get_method_class_by_frame(frame=method_caller_frame)

            if instance_class is not method_caller_class:
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

        if os.environ.get(DISABLE_ACCESSIFY_ENV_VARIABLE_NAME) is None:
            method = find_decorated_method(function=func)

            method_caller_frame = inspect.currentframe().f_back
            method_caller_class = get_method_class_by_frame(frame=method_caller_frame)

            if instance_class is not method_caller_class:
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

    return protected_wrapper
