""""
Provide configurations for testing with pytest.
"""
import os

import pytest


@pytest.fixture
def enable_accessify():
    """
    Enabling the accessify.
    """
    try:
        del os.environ['DISABLE_ACCESSIFY']
    except KeyError:
        pass


@pytest.fixture
def disable_accessify():
    """
    Disabling the accessify.
    """
    os.environ['DISABLE_ACCESSIFY'] = 'True'
