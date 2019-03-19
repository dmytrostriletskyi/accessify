"""
Provide implementation of interfaces.
"""
import inspect
import os

from accessify.errors import (
    DECLARED_INTERFACE_EXCEPTION_HAS_NOT_BEEN_IMPLEMENTED_EXCEPTION_MESSAGE,
    IMPLEMENTED_INTERFACE_MEMBER_HAS_INCORRECT_ACCESS_MODIFIER_EXCEPTION,
    INTERFACE_MEMBER_HAS_BEEN_IMPLEMENTED_WITH_MISMATCHED_ARGUMENT_EXCEPTION_MESSAGE,
    INTERFACE_MEMBER_HAS_NOT_BEEN_IMPLEMENTED_EXCEPTION_MESSAGE,
    DeclaredInterfaceExceptionHasNotBeenImplementedException,
    ImplementedInterfaceMemberHasIncorrectAccessModifierException,
    InterfaceMemberHasNotBeenImplementedException,
    InterfaceMemberHasNotBeenImplementedWithMismatchedArgumentsException,
)
from accessify.utils import (
    DISABLE_ACCESSIFY_ENV_VARIABLE_NAME,
    MARK_MEMBER_RAISES_EXCEPTION,
    ClassMemberMagicMethodNames,
    find_decorated_method,
    get_class_members,
)


def throws(*exceptions):
    """
    Keep track exceptions implemented function should raise.
    """
    def decorator(function):
        """
        Throws decorator.
        """
        find_decorated_method(function=function).__throws__ = exceptions
        return function

    return decorator


def implements(*interfaces):
    """
    Implement detecting whether class that implements interface has been implemented all members of the interface.

    Rules:
        - get class members, get interfaces members, compare it,
        - match interface member is presented in the class,
        - match interface member arguments with class member arguments,
        - check if interface member has exception to throw, if yes, inspect class member source code if it raise it.
    """
    def decorator(class_):
        """
        Provide logic of implementing interface.
        """
        if os.environ.get(DISABLE_ACCESSIFY_ENV_VARIABLE_NAME) is not None:
            return class_

        class_members = get_class_members(class_=class_)

        for interface in interfaces:
            interface_members = get_class_members(class_=interface)

            for interface_method_unique_identifier, interface_method in interface_members.items():
                class_member = class_members.get(interface_method_unique_identifier)

                if class_member is None:
                    raise InterfaceMemberHasNotBeenImplementedException(
                        INTERFACE_MEMBER_HAS_NOT_BEEN_IMPLEMENTED_EXCEPTION_MESSAGE.format(
                            class_name=class_.__name__,
                            interface_name=interface.__name__,
                            interface_method_name=interface_method.name,
                            interface_method_arguments=interface_method.arguments_as_string,
                        ),
                    )

                if interface_method.access_type != class_member.access_type:
                    raise ImplementedInterfaceMemberHasIncorrectAccessModifierException(
                        IMPLEMENTED_INTERFACE_MEMBER_HAS_INCORRECT_ACCESS_MODIFIER_EXCEPTION.format(
                            class_name=class_.__name__,
                            class_method_name=interface_method.name,
                            class_method_arguments=class_member.arguments_as_string,
                            interface_name=interface.__name__,
                            interface_method_name=interface_method.name,
                        ),
                    )

                if class_member.arguments_as_string != interface_method.arguments_as_string:
                    raise InterfaceMemberHasNotBeenImplementedWithMismatchedArgumentsException(
                        INTERFACE_MEMBER_HAS_BEEN_IMPLEMENTED_WITH_MISMATCHED_ARGUMENT_EXCEPTION_MESSAGE.format(
                            class_name=class_.__name__,
                            interface_name=interface.__name__,
                            interface_method_name=interface_method.name,
                            interface_method_arguments=interface_method.arguments_as_string,
                        ),
                    )

                if hasattr(interface_method.method, ClassMemberMagicMethodNames.THROWS):
                    source_code = inspect.getsource(class_member.method)

                    for exception in interface_method.method.__throws__:
                        if MARK_MEMBER_RAISES_EXCEPTION.format(exception_name=exception.__name__) not in source_code:
                            raise DeclaredInterfaceExceptionHasNotBeenImplementedException(
                                DECLARED_INTERFACE_EXCEPTION_HAS_NOT_BEEN_IMPLEMENTED_EXCEPTION_MESSAGE.format(
                                    exception_name=exception.__name__,
                                    interface_name=interface.__name__,
                                    interface_method_name=interface_method.name,
                                    class_name=class_.__name__,
                                    class_method_name=interface_method.name,
                                    class_method_arguments=class_member.arguments_as_string,
                                ),
                            )

        return class_
    return decorator
