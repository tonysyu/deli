from __future__ import absolute_import

from traits.api import Dict, Event, HasStrictTraits


class NoisyDict(HasStrictTraits):
    """ Dict-like object that fires an event when keys are added or changed.
    """

    #: Event fired when a new key is added or changed.
    updated = Event

    # The actual dictionary data that this class wraps.
    _dict_data = Dict({})

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def __getitem__(self, name):
        return self._dict_data[name]

    def __setitem__(self, name, value):
        self.update({name: value})

    def update(self, *args, **kwargs):
        data = dict(*args, **kwargs)
        event = {}
        for name in data:
            event.setdefault('added', []).append(name)

        self._dict_data.update(data)
        self.updated = event
