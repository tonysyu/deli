from .label_stylus import LabelStylus
from ..utils.traits import Alias


class XTickLabelStylus(LabelStylus):

    y_origin = 'top'

    offset = Alias('y_offset')


class YTickLabelStylus(LabelStylus):

    x_origin = 'right'

    offset = Alias('x_offset')
