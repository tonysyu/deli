
def wrap_string_in_list(value):
    if value is None or isinstance(value, basestring):
        value = [value]
    return value


class KeySpec(object):
    """ A key specification to facilitate tools interacting with the keyboard.

    A key-spec should be added to a class as follows:

    >>> magic_key = KeySpec('Right', modifier='control', ignore='shift')

    and then it is used check to see if the key was pressed by calling::

    >>> if self.magic_key.match(event):
    ...     print 'do stuff...'

    Note that all fields---`key`, `modifier` and `ignore`---can be either
    strings or lists of strings.

    If you want to use modifier keys by themselves,as action keys, there are
    convenient instances of KeySpec (`shift_key`, `control_key`, and `alt_key`)
    to facilitate that usage.
    """
    def __init__(self, key, modifier=None, ignore=None):
        self.modifier_names = ('alt', 'shift', 'control')

        ignore = ignore or []
        modifier = modifier or []

        key = wrap_string_in_list(key)
        ignore = wrap_string_in_list(ignore)
        modifier = wrap_string_in_list(modifier)
        modifier = set(m.lower() for m in modifier)

        self.keys = key
        self.ignore = set(key.lower() for key in ignore)
        self.modifier = {key: key in modifier for key in self.modifier_names}
        # XXX: Add menu-modifier (Ctrl-key = "Menu" in OSX)

    def match(self, event):
        """ Returns True if event matches this key specification. """
        pressed_key = getattr(event, 'character', None)
        mod = (self._modifier_match(key, event) for key in self.modifier_names)
        return (pressed_key in self.keys) and all(mod)

    def _modifier_match(self, name, event):
        modifier_spec = self.modifier[name]
        modifier_down = getattr(event, '{}_down'.format(name))
        return (name in self.ignore) or (modifier_down == modifier_spec)


# Key-specs to use modifier-keys as key-matches, rather than as a modifier to
# another key press.
alt_key = KeySpec('Alt', ignore='alt')
control_key = KeySpec('Control', ignore='control')
shift_key = KeySpec('Shift', ignore='shift')
