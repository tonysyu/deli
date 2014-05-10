from string import maketrans


_translation_table = {}


def _get_translation(src, dst):
    global _translation_table

    key = (src, dst)
    if key not in _translation_table:
        _translation_table[key] = maketrans(src, dst)
    return _translation_table[key]


def switch_delimiters(text, from_delim, to_delim):
    translation_table = _get_translation(from_delim, to_delim)
    return text.translate(translation_table)
