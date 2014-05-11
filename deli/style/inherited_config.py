class InheritedConfig(dict):
    """Configuration dictionary where non-existent keys can inherit values.

    This class allows you to define parameter names that can match exactly, but
    if it doesn't, parameter names will be searched based on key inheritance.
    For example, the key 'text.size' will default to 'size'.

    Note that indexing into the dictionary will raise an error if it doesn't
    match exactly, while `InheritedConfig.get` will look up values based on
    inheritance.

    Parameters
    ----------
    config_values : dict or list of (key, value) pairs
        Default values for a configuration, where keys are the parameter names
        and values are the associated value.
    cascade_map : dict
        Dictionary defining cascading defaults. If a parameter name is not
        found, indexing `cascade_map` with the parameter name will return
        the parameter to look for.
    kwargs : dict
        Keyword arguments for initializing dict.

    Examples
    --------
    The ``get`` method supports the pattern commonly used for optional keyword
    arguments to a function. For example:

    >>> def print_value(key, **kwargs):
    ...     print kwargs.get(key, 0)
    >>> print_value('size')
    0
    >>> print_value('size', size=1)
    1

    Instead, you would create a config class and write:

    >>> config = InheritedConfig(size=0, error_if_missing=False)
    >>> def print_value(key, **kwargs):
    ...     print kwargs.get(key, config.get(key))
    >>> print_value('size')
    0
    >>> print_value('size', size=1)
    1
    >>> print_value('non-existent')
    None
    >>> print_value('text.size')
    0

    """

    _separator = '.'

    def __init__(self, config_values=None, error_if_missing=True, **kwargs):
        assert 'config_values' not in kwargs

        if config_values is None:
            config_values = {}

        self._current_chain = []
        self.error_if_missing = error_if_missing

        super(InheritedConfig, self).__init__(config_values, **kwargs)

    def get(self, name, default=None, _prev=None):
        """Return best matching config value for `name`.

        Get value from configuration. The search for `name` is in the following
        order:

            - `self` (Value in global configuration)
            - `default`
            - Alternate name specified by "inheritance"

        See class docstring for examples.

        See examples below for a demonstration of the inherited of
        configuration names.

        Parameters
        ----------
        name : str
            Name of config value you want.
        default : object
            Default value if name doesn't exist in instance.

        Examples
        --------
        >>> config = InheritedConfig(size=0)
        >>> config.get('size')
        0
        >>> top_choice={'size': 1}
        >>> top_choice.get('size', config.get('size'))
        1
        >>> config.get('non-existent', 'unknown')
        'unknown'
        >>> config.get('text.size')
        0
        >>> config.get('text.size', 2)
        2
        >>> top_choice.get('size', config.get('text.size'))
        1
        """
        if _prev is None:
            self._current_chain = [name]
        else:
            self._current_chain.append(name)

        if name in self:
            return self[name]
        elif default is not None:
            return default
        elif self._separator in name:
            return self.get(self._parent(name), _prev=name)
        elif self.error_if_missing:
            msg = "Could not find key in the following inheritance chain:\n{}"
            raise KeyError(msg.format('\n'.join(self._current_chain)))
        else:
            return None

    def _parent(self, name):
        parts = name.split(self._separator)
        # Remove penultimate part: Last part is the attribute name, and
        # everything before is a class from general to specific.
        parts = parts[:-2] + parts[-1:]
        return self._separator.join(parts)


def test_get_non_existent():
    config = InheritedConfig()
    assert config.get('size') is None


def test_get_simple():
    config = InheritedConfig({'imread': 'matplotlib'})
    assert config.get('imread') == 'matplotlib'


def test_get_default():
    config = InheritedConfig()
    assert config.get('size', 10) == 10


def test_get_best():
    config = InheritedConfig({'size': 0, 'text.size': 1})
    assert config.get('text.size') == 1


def test_get_multi_level():
    config = InheritedConfig({'size': 0})
    assert config.get('text.title.size') == 0
    config['text.size'] = 1
    assert config.get('text.title.size') == 1
    config['text.title.size'] = 2
    assert config.get('text.title.size') == 2


if __name__ == '__main__':
    import doctest
    from numpy import testing

    doctest.testmod()
    testing.run_module_suite()
