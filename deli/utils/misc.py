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
