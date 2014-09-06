from traits.api import HasStrictTraits, Property


class BaseArtist(HasStrictTraits):

    label = Property

    def _get_label(self):
        return self.__class__.__name__
