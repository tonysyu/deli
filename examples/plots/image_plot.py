from skimage import data

from deli.demo_utils.traits_view import TraitsView
from deli.graph import Graph
from deli.artist.image_artist import ImageArtist


class Demo(TraitsView):

    def setup_graph(self):
        graph = Graph()
        artist = ImageArtist(data=data.lena())
        graph.add_artist(artist)
        return graph


if __name__ == '__main__':
    demo = Demo()
    demo.show()
