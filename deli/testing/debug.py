
BLOCK_FORMAT = """\
{}(
{}
)\
"""

# Indent should be 4 spaces, not 8 (\t)
INDENT = '    '

INDENT_FORMAT = "{}{{}},".format(INDENT)


def indented_lines(*lines):
    return '\n'.join(INDENT_FORMAT.format(ln) for ln in lines)


def layout_info(component):
    class_name = component.__class__.__name__
    origin = (component.left.value, component.bottom.value)
    size = (component.layout_width.value, component.layout_height.value)
    attrs = indented_lines(
        'id = {}'.format(component.id),
        'origin = {}'.format(origin),
        'size = {}'.format(size),
    )
    return BLOCK_FORMAT.format(class_name, attrs)
