def get_protocol(obj):
    return obj.__class__.__name__


def serialize_children(obj, children, handler):
    return {name: handler.serialize(getattr(obj, name)) for name in children}


def serialize_dict(obj, handler):
    return {key: handler.serialize(value) for key, value in obj.iteritems()}
