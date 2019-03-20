"""
Provide utils for testing the library.
"""
ENGINE_HAS_BEEN_STARTED_RESPONSE = \
    'Engine has been started! Details: type is `{type_}`, model is `{model}`, company is `{company}`.'


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
