from traits.api import Bool, Either, HasStrictTraits, Str

from deli.tools.key_spec import alt_key, control_key, KeySpec, shift_key


class MockEvent(HasStrictTraits):

    character = Either(None, Str)

    alt_down = Bool(False)
    control_down = Bool(False)
    shift_down = Bool(False)


# -------------------------------------------------------------------------
#  Test basic interface
# -------------------------------------------------------------------------

def test_single_character():
    key = KeySpec('a')
    assert key.match(MockEvent(character='a'))
    assert not key.match(MockEvent(character='a', control_down=True))


def test_ignore():
    key = KeySpec('a', ignore='control')
    assert key.match(MockEvent(character='a'))
    assert key.match(MockEvent(character='a', control_down=True))


def test_modifier():
    key = KeySpec('a', modifier='control')
    assert key.match(MockEvent(character='a', control_down=True))
    assert not key.match(MockEvent(character='a'))


# -------------------------------------------------------------------------
#  Test multiple inputs
# -------------------------------------------------------------------------

def test_multiple_keys():
    key = KeySpec(['a', 'b'])
    assert key.match(MockEvent(character='a'))
    assert key.match(MockEvent(character='b'))
    assert not key.match(MockEvent(character='c'))


def test_multiple_modifiers():
    key = KeySpec('a', modifier=['alt', 'shift'])
    assert not key.match(MockEvent(character='a'))
    assert not key.match(MockEvent(character='a', alt_down=True))
    assert not key.match(MockEvent(character='a', shift_down=True))
    assert key.match(MockEvent(character='a', alt_down=True, shift_down=True))


def test_multiple_ignore():
    key = KeySpec('a', ignore=['alt', 'shift'])
    assert key.match(MockEvent(character='a'))
    assert key.match(MockEvent(character='a', alt_down=True))
    assert key.match(MockEvent(character='a', shift_down=True))
    assert key.match(MockEvent(character='a', alt_down=True, shift_down=True))


# -------------------------------------------------------------------------
#  Test custom key-specs
# -------------------------------------------------------------------------

def test_alt_key():
    assert alt_key.match(MockEvent(character='Alt'))
    assert alt_key.match(MockEvent(character='Alt', alt_down=True))


def test_control_key():
    assert control_key.match(MockEvent(character='Control'))
    assert control_key.match(MockEvent(character='Control', control_down=True))


def test_shift_key():
    assert shift_key.match(MockEvent(character='Shift'))
    assert shift_key.match(MockEvent(character='Shift', shift_down=True))
