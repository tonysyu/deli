from pyface.qt import QtCore

from .constants import KEY_MAP


MODIFIER_MAP = {
    'alt_down': QtCore.Qt.AltModifier,
    'shift_down': QtCore.Qt.ShiftModifier,
    'control_down': QtCore.Qt.ControlModifier,
}


BUTTON_MAP = {
    'left_down': QtCore.Qt.LeftButton,
    'middle_down': QtCore.Qt.MidButton,
    'right_down': QtCore.Qt.RightButton,
}


def key_from_event(event_type, event):
    # Convert the keypress to a standard key if possible, otherwise to text.
    key_code = event.key()
    key = KEY_MAP.get(key_code)
    if key is None:
        key = unichr(key_code).lower()
    return key


def get_modifier_state(modifiers):
    return {name: bool(modifiers & key_type)
            for name, key_type in MODIFIER_MAP.iteritems()}


def get_button_state(buttons):
    return {name: bool(buttons & button_type)
            for name, button_type in BUTTON_MAP.iteritems()}
