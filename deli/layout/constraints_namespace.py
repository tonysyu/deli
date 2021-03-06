from kiwisolver import Variable as ConstraintsVariable

from .linear_symbolic import LinearSymbolic


class ConstraintsNamespace(object):
    """ A class which acts as a namespace for casuarius constraint variables.

    The constraint variables are created on an as-needed basis, this
    allows components to define new constraints and build layouts
    with them, without having to specifically update this client code.

    """
    def __init__(self, name, owner):
        """ Initialize a ConstraintsNamespace.

        Parameters
        ----------
        name : str
            A name to use in the label for the constraint variables in
            this namespace.
        owner : str
            The owner id to use in the label for the constraint variables
            in this namespace.
        """
        self._name = name
        self._owner = owner
        self._constraints = {}

    def __getattr__(self, name):
        """ Returns a casuarius constraint variable for the given name,
        unless the name is already in the instance dictionary.

        Parameters
        ----------
        name : str
            The name of the constraint variable to return.
        """
        try:
            return super(ConstraintsNamespace, self).__getattr__(name)
        except AttributeError:
            pass

        constraints = self._constraints
        if name in constraints:
            res = constraints[name]
        else:
            label = '{0}|{1}|{2}'.format(self._name, self._owner, name)
            res = constraints[name] = ConstraintsVariable(label)
        return res

    def __setattr__(self, name, value):
        """ Adds a casuarius constraint variable to the constraints dictionary.

        Parameters
        ----------
        name : str
            The name of the constraint variable to set.
        value : LinearSymbolic
            The casuarius variable to add to the constraints dictionary.
        """
        if isinstance(value, LinearSymbolic):
            self._constraints[name] = value
        else:
            super(ConstraintsNamespace, self).__setattr__(name, value)
