class KeySpec(object):
    """
    Creates a key specification to facilitate tools interacting with the
    keyboard. A tool can declare either a class attribute::

        magic_key = KeySpec("Right", "control", ignore=['shift'])

    or a trait::

        magic_key = Instance(KeySpec, args=("Right", "control"), kw={'ignore': ['shift']})

    and then check to see if the key was pressed by calling::

        if self.magic_key.match(event):
            # do stuff...

    The names of the keys come from Enable, so both examples above
    are specifying the user pressing Ctrl + Right_arrow with Alt not pressed
    and Shift either pressed or not.
    """
    def __init__(self, key, *modifiers, **kwmods):
        """ Creates this key spec with the given modifiers. """
        if isinstance(key, basestring):
            key = [key]
        ignore = kwmods.get('ignore', [])
        if isinstance(ignore, basestring):
            ignore = [ignore]

        self.keys = key
        mods = set(m.lower() for m in modifiers)
        self.alt = "alt" in mods
        self.shift = "shift" in mods
        self.control = "control" in mods
        self.ignore = set(m.lower() for m in ignore)

    def match(self, event):
        """
        Returns True if the given Enable key_pressed event matches this key
        specification.
        """
        pressed_key = getattr(event, 'character', None)
        return (pressed_key in self.keys) and \
           ('alt' in self.ignore or self.alt == event.alt_down) and \
           ('control' in self.ignore or self.control == event.control_down) and \
           ('shift' in self.ignore or self.shift == event.shift_down)
