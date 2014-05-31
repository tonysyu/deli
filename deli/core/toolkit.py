import sys
from traceback import format_exception_only

from traits.etsconfig.api import ETSConfig


# This is set to the api module path for the selected backend.
_toolkit_backend = None


def _init_toolkit():
    """ Initialise the current toolkit. """

    toolkit = ETSConfig.toolkit
    backend = ETSConfig.kiva_backend

    # Import the selected backend
    backend = 'deli.core.%s.%s' % (toolkit, backend)
    try:
        __import__(backend)
    except (ImportError, SystemExit):
        t, v, _tb = sys.exc_info()
        exception = format_exception_only(t, v)
        msg = "Unable to import {!r} backend for {!r} toolkit (reason: {})."
        raise ImportError(msg.format(backend, toolkit, exception))

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
        msg = "The {}.{} enable backend doesn't implement {!r}"
        args = (ETSConfig.toolkit, ETSConfig.kiva_backend, name)
        raise NotImplementedError(msg.format(*args))

    return tk_object
