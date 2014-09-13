from unittest import TestCase

from numpy.testing.decorators import skipif

from traits.api import Dict, HasStrictTraits
from traits.testing.unittest_tools import UnittestTools


class TestDict(TestCase, UnittestTools):

    @skipif(True)
    def test_dict_update(self):

        class Foo(HasStrictTraits):
            data = Dict

        # This should work, right?
        obj_with_dict = Foo()
        with self.assertTraitChanges(obj_with_dict, 'data', count=1):
            obj_with_dict.data['a'] = 1
