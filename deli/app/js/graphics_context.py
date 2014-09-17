import numpy as np


class GraphicsContext(object):

    def __init__(self, array_or_size, pix_format="bgra32",
                 interpolation="nearest", bottom_up=1):
        """ When specifying size, it must be a two element tuple.

        Array input is always treated as an image.

        This class handles the polymorphism of the underlying template classes
        for individual pixel formats.
        """
        pass

    def __del__(self, destroy=None):
        pass

    def bottom_up(self, *args):
        pass

    def width(self, *args):
        pass

    def height(self, *args):
        pass

    def stride(self, *args):
        pass

    def format(self):
        pass

    def get_image_interpolation(self):
        pass

    def set_image_interpolation(self,interp):
        pass

    def set_stroke_color(self,color):
        pass

    def get_stroke_color(self, *args):
        pass

    def set_line_width(self, *args):
        pass

    def set_line_join(self, *args):
        pass

    def set_line_cap(self, *args):
        pass

    def set_line_dash(self, *args):
        pass

    def set_blend_mode(self, *args):
        pass

    def get_blend_mode(self, *args):
        pass

    def set_fill_color(self,color):
        pass

    def get_fill_color(self, *args):
        pass

    def set_alpha(self, *args):
        pass

    def get_alpha(self, *args):
        pass

    def set_antialias(self, *args):
        pass

    def get_antialias(self, *args):
        pass

    def set_miter_limit(self, *args):
        pass

    def set_flatness(self, *args):
        pass

    def set_text_position(self, *args):
        pass

    def get_text_position(self, *args):
        pass

    def show_text_simple(self, *args):
        pass

    def show_text_at_point(self, text, dx, dy):
        pass

    def show_text(self, text, point = None):
        pass

    def get_text_extent(self, text):
        pass

    def is_font_initialized(self, *args):
        pass

    def set_text_matrix(self, matrix):
        pass

    def get_text_matrix(self, *args):
        pass

    def set_character_spacing(self, *args):
        pass

    def get_character_spacing(self, *args):
        pass

    def set_text_drawing_mode(self, *args):
        pass

    def get_full_text_extent(self, text):
        pass

    def set_font(self, font):
        pass

    def set_font_size(self, size):
        pass

    def get_font(self, *args):
        pass

    def save_state(self, *args):
        pass

    def restore_state(self, *args):
        pass

    def translate_ctm(self, *args):
        pass

    def rotate_ctm(self, *args):
        pass

    def scale_ctm(self, *args):
        pass

    def concat_ctm(self, m):
        if isinstance(m, tuple):
            _agg.GraphicsContextArray_concat_ctm(self, _AffineMatrix(*m))
        else:
            _agg.GraphicsContextArray_concat_ctm(self, m)

    def set_ctm(self, m):
        if isinstance(m, tuple):
            _agg.GraphicsContextArray_set_ctm(self, _AffineMatrix(*m))
        else:
            _agg.GraphicsContextArray_set_ctm(self, m)


    def get_ctm(self):
        return _agg.GraphicsContextArray_get_ctm(self)

    def get_freetype_text_matrix(self, *args):
        pass

    def flush(self, *args):
        pass

    def synchronize(self, *args):
        pass

    def begin_page(self, *args):
        pass

    def end_page(self, *args):
        pass

    def begin_path(self, *args):
        pass

    def move_to(self, *args):
        pass

    def line_to(self, *args):
        pass

    def curve_to(self, *args):
        pass

    def quad_curve_to(self, *args):
        pass

    def arc(self, *args):
        pass

    def arc_to(self, *args):
        pass

    def close_path(self, *args):
        pass

    def add_path(self, *args):
        pass

    def lines(self, *args):
        pass

    def line_set(self, *args):
        pass

    def rect(self, *args):
        pass

    def rects(self, *args):
        pass

    def _get_path(self, *args):
        pass

    def clip(self, *args):
        pass

    def even_odd_clip(self, *args):
        pass

    def get_num_clip_regions(self, *args):
        pass

    def get_clip_region(self, *args):
        pass

    def clip_to_rect(self, *args):
        pass

    def clear_clip_path(self, *args):
        pass

    def clear(self, *args):
        pass

    def stroke_path(self, *args):
        pass

    def fill_path(self, *args):
        pass

    def eof_fill_path(self, *args):
        pass

    def draw_path(self, *args):
        pass

    def draw_rect(self, *args):
        pass

    def draw_image(self, img, rect=None, force_copy=False):
        if isinstance(img, np.ndarray):
            # The C++ implementation only handles other
            # GraphicsContexts, so create one.
            if img.shape[-1] == 3:
                pix_format = 'rgb24'
            else:
                pix_format = 'rgba32'
            img = GraphicsContextArray(img, pix_format=pix_format)
        if rect is None:
            rect = np.array((0,0,img.width(),img.height()),float)
        return _agg.GraphicsContextArray_draw_image(self,img,rect,force_copy)

    def draw_marker_at_points(self, pts, size, kiva_marker_type):
        marker = kiva_marker_to_agg.get(kiva_marker_type, None)
        if marker is None:
            success = 0
        elif kiva_marker_type in (CIRCLE_MARKER,):
            # The kiva circle marker is rather jagged so lets
            # use our own
            path_func, mode = substitute_markers[kiva_marker_type]
            path = self.get_empty_path()
            path_func(path, size)
            success = _agg.GraphicsContextArray_draw_path_at_points(self, pts, path, mode)
        else:
            args = (self,pts,int(size),marker)
            success = _agg.GraphicsContextArray_draw_marker_at_points(self, pts,
                            int(size), marker)
        return success

    def draw_path_at_points(self, *args):
        pass

    def convert_pixel_format(self,pix_format,inplace=0):
        """ Convert gc from one pixel format to another.

            !! This used to be done in C++ code, but difficult-to-find
            !! memory bugs pushed toward a simpler solution.
            !! HACK
            !! Now we just draw into a new gc and assume its underlying C++
            !! object. We must be careful not to add any attributes in the
            !! Python GraphicsContextArray constructor other than the bmp_array.
            !! if we do, we need to copy them here also.
        """
        # make sure it uses sub-class if needed
        new_img = self.__class__((self.width(),self.height()),
                                  pix_format=pix_format,
                                  interpolation=self.get_image_interpolation(),
                                  bottom_up = self.bottom_up())
        new_img.draw_image(self)

        if inplace:
            """
            # swap internals with new_self -- it will dealloc our (now unused) C++
            # object and we'll acquire its new one.  We also get a ref to his bmp_array
            """
            old_this = self.this
            self.this = new_img.this
            new_img.this = old_this
            self.bmp_array = new_img.bmp_array
            return self
        else:
            return new_img

    def get_empty_path(self):
        pass

    def save(self, filename, file_format=None, pil_options=None):
        pass

    #----------------------------------------------------------------
    # context manager interface
    #----------------------------------------------------------------

    def __enter__(self):
        self.save_state()

    def __exit__(self, type, value, traceback):
        self.restore_state()

    def linear_gradient(self, *args):
        pass

    def radial_gradient(self, *args):
        pass
