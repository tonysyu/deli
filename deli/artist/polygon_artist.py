from .base_patch_artist import BasePatchArtist


class PolygonArtist(BasePatchArtist):
    """ A Flyweight object for drawing filled polygons.
    """

    def draw(self, gc, vertices):
        with gc:
            if self.fill_color is not 'none':
                gc.set_fill_color(self.fill_color_)
                gc.lines(vertices)
                gc.fill_path()
            if self.edge_color is not 'none':
                gc.set_stroke_color(self.edge_color_)
                gc.lines(vertices)
                gc.close_path()
                gc.stroke_path()
