def new_item_name(existing_names, name_template='item_{}'):
    """ Returns a string that is not already used as a plot title.
    """
    n = len(existing_names)
    while True:
        name = name_template.format(n)
        if name not in existing_names:
            break
        else:
            n += 1
    return name


def getattr_recurse(obj, attr_name):
    for name in attr_name.split('.'):
        if name:
            obj = getattr(obj,  name)
    return obj


def setattr_recurse(obj, attr_name, val):
    sub_attrs, _, name = attr_name.rpartition('.')
    obj = getattr_recurse(obj, sub_attrs)
    return setattr(obj, name, val)
