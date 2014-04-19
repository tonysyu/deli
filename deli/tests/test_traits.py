from unittest import TestCase

from traits.api import Dict, HasStrictTraits
from traits.testing.unittest_tools import UnittestTools


class TestDict(TestCase, UnittestTools):

    def test_dict_update(self):

        class Foo(HasStrictTraits):
            data = Dict

        obj_with_dict = Foo()
        with self.assertTraitChanges(obj_with_dict, 'data', count=1):
            obj_with_dict.data['a'] = 1


if __name__ == '__main__':
    from numpy import testing
    testing.run_module_suite()
