"""
Provide utils for testing the library.
"""


def custom_decorator(func):
    """
    Custom decorator that could exist in some project that uses library.

    Needed for testing that accessibility levels works properly with possible custom decorators.
    """
    def wrapper(*args, **kwargs):
        """
        Custom decorator wrapper.
        """
        return func(*args, **kwargs)

    return wrapper
