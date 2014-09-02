import sys
from traceback import format_exception_only

from .backend import backend_path


# This is set to the api module path for the selected backend.
_toolkit_backend = None


def _init_toolkit():
    """ Initialise the current toolkit. """

    # Import the selected backend
    backend = 'deli.app.{}'.format(backend_path)
    try:
        __import__(backend)
    except (ImportError, SystemExit):
        t, v, _tb = sys.exc_info()
        exception = format_exception_only(t, v)
        msg = "Unable to import {!r} backend (reason: {})."
        raise ImportError(msg.format(backend, exception))

    # Save the imported toolkit module.
    global _toolkit_backend
    _toolkit_backend = backend


# Do this once then disappear.
_init_toolkit()
del _init_toolkit


def toolkit_object(name):
    """ Return the toolkit specific object with the given name. """

    try:
        tk_object = getattr(sys.modules[_toolkit_backend], name)
    except AttributeError:
        msg = "{!r} doesn't implement {!r}"
        raise NotImplementedError(msg.format(_toolkit_backend, name))

    return tk_object
