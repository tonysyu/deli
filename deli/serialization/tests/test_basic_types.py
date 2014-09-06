import numpy as np
from numpy.testing import assert_allclose
from nose.tools import assert_almost_equal, assert_equal
from traits.api import Array, Dict, Float, Int, List, Str

from deli.core.component import Component
from deli.serialization.api import serialization_manager
from deli.serialization.default_adapter import create_simple_adapter


# Use `Component` subclass since this has a registered serializer
class MockObject(Component):

    a_dict = Dict

    a_float = Float

    a_list = List

    a_str = Str

    an_int = Int

    an_array = Array


mock_adapter = create_simple_adapter(['a_dict', 'a_float', 'an_int',
                                      'a_list', 'a_str', 'an_array'])
# Copy so we don't alter the global serialization manager
MANAGER = serialization_manager.copy()
MANAGER.register(mock_adapter, MockObject)


def test_int():
    output = MANAGER.serialize(MockObject(an_int=42))
    assert_equal(output['an_int'], 42)


def test_float():
    output = MANAGER.serialize(MockObject(a_float=1.1))
    assert_almost_equal(output['a_float'], 1.1)


def test_list():
    a_list = ['a', 42, 1.1, {'a': 2}]
    output = MANAGER.serialize(MockObject(a_list=a_list))
    assert_equal(output['a_list'], a_list)


def test_dict():
    a_dict = {'a': 1, 'b': {'a': 1}, 'c': 'hello'}
    output = MANAGER.serialize(MockObject(a_dict=a_dict))
    assert_equal(output['a_dict'], a_dict)


def test_array():
    an_array = np.arange(10)
    output = MANAGER.serialize(MockObject(an_array=an_array))
    assert_allclose(output['an_array'], an_array)
