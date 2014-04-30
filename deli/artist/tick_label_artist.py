from .label_artist import LabelArtist
from ..utils.traits import Alias


class XTickLabelArtist(LabelArtist):

    y_origin = 'top'

    offset = Alias('y_offset')


class YTickLabelArtist(LabelArtist):

    x_origin = 'right'

    offset = Alias('x_offset')
