from .constants import KEY_MAP


def key_from_event(event_type, event):
    if event_type == 'character':
        key = unicode(event.text())
    else:
        # Convert the keypress to a standard enable key if possible,
        # otherwise to text.
        key_code = event.key()
        key = KEY_MAP.get(key_code)
        if key is None:
            key = unichr(key_code).lower()
    return key
