"""
Provide errors for accessify implementation.
"""
INACCESSIBLE_DUE_TO_ITS_PROTECTION_LEVEL_EXCEPTION_MESSAGE = \
    '{class_name}.{class_method_name}() is inaccessible due to its protection level'

INTERFACE_MEMBER_HAS_NOT_BEEN_IMPLEMENTED_EXCEPTION_MESSAGE = \
    'class {class_name} does not implement interface member ' \
    '{interface_name}.{interface_method_name}({interface_method_arguments})'

INTERFACE_MEMBER_HAS_BEEN_IMPLEMENTED_WITH_MISMATCHED_ARGUMENT_EXCEPTION_MESSAGE = \
    'class {class_name} implements interface member ' \
    '{interface_name}.{interface_method_name}({interface_method_arguments}) with mismatched arguments'

DECLARED_INTERFACE_EXCEPTION_HAS_NOT_BEEN_IMPLEMENTED_EXCEPTION_MESSAGE = \
    'Declared exception {exception_name} by {interface_name}.{interface_method_name}() ' \
    'member has not been implemented by {class_name}.{class_method_name}({class_method_arguments})'

IMPLEMENTED_INTERFACE_MEMBER_HAS_INCORRECT_ACCESS_MODIFIER_EXCEPTION = \
    '{class_name}.{class_method_name}({class_method_arguments}) mismatches ' \
    '{interface_name}.{interface_method_name}() member access modifier.'


class InaccessibleDueToItsProtectionLevelException(Exception):
    """
    Inaccessible due to its protection level exception.
    """

    def __init__(self, message):
        self.message = message


class InterfaceMemberHasNotBeenImplementedException(Exception):
    """
    Interface member has not been implemented exception.
    """

    def __init__(self, message):
        self.message = message


class InterfaceMemberHasNotBeenImplementedWithMismatchedArgumentsException(Exception):
    """
    Interface member has not been implemented with mismatched arguments exception.
    """

    def __init__(self, message):
        self.message = message


class DeclaredInterfaceExceptionHasNotBeenImplementedException(Exception):
    """
    Declared interface exception has not been implemented exception.
    """

    def __init__(self, message):
        self.message = message


class ImplementedInterfaceMemberHasIncorrectAccessModifierException(Exception):
    """
    Implemented interface member has incorrect access modifier exception.
    """

    def __init__(self, message):
        self.message = message
