from __future__ import absolute_import

from traits.api import Property
from .misc import getattr_recurse, setattr_recurse


def Alias(name):
    return Property(lambda obj: getattr_recurse(obj, name),
                    lambda obj, val: setattr_recurse(obj, name, val))


def switch_trait_handler(old, new, observed_trait_name, handler):
    """Move handler from one `HasTraits` object to another.

    Parameters
    ----------
    old, new : HasTraits instance
        HasTraits objects with a trait that's being observed.
    observed_trait_name : str
        Observed trait on `old` and `new` `HasTraits` objects.
    handler : function
        The handler function that's fired when the oberved trait changes.
    """
    if old is not None:
        old.on_trait_change(handler, observed_trait_name, remove=True)
    if new is not None:
        new.on_trait_change(handler, observed_trait_name)
