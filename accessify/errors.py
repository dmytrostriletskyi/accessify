"""
Provide errors for accessibility levels.
"""
INACCESSIBLE_DUE_TO_ITS_PROTECTION_LEVEL_EXCEPTION_MESSAGE = \
    '{class_name}.{method_name}() is inaccessible due to its protection level'


class InaccessibleDueToItsProtectionLevelException(Exception):
    """
    Inaccessible due to its protection level exception.
    """

    def __init__(self, message):
        self.message = message