class Bunch(object):
    """Collect a Bunch of named items.

    This class is taken directly from the Python Cookbook, recipe 4.18.
    Initialize a bunch of named items that are saved as class attributes. New
    attributes can be added later (just like any other class).

    >>> point = Bunch(x=1, name='important point')
    >>> point.x
    1
    >>> point.name
    'important point'
    >>> point.y = 2.0
    >>> point.y
    2.0
    """
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)
        self._kwargs = kwargs

    def to_dict(self):
        return self._kwargs
