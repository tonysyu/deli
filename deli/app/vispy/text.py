# -*- coding: utf-8 -*-
from __future__ import division

import sys

import numpy as np

from vispy.gloo import (set_state, IndexBuffer, VertexBuffer, set_viewport,
                        get_parameter)
from vispy.gloo.wrappers import _check_valid
from vispy.ext.six import string_types
from vispy.color import Color
from vispy.scene.visuals.text.text import FontManager

from .element import GLElement


# Note that initializing the font manager is very costly.
FONT_MANAGER = FontManager()
ANCHOR_Y_ENUM = ('top', 'center', 'middle', 'baseline', 'bottom')
ANCHOR_X_ENUM = ('left', 'center', 'right')
BLEND_FUNC = ('src_alpha', 'one_minus_src_alpha')

def rect_extents_to_corners(x0, y0, x1, y1):
    return [[x0, y0], [x0, y1], [x1, y1], [x1, y0]]


def _text_to_vbo(text, font, anchor_x, anchor_y, lowres_size):
    """Convert text characters to vertex buffer object."""
    # XXX: This function may benefit from a LRU cache.

    text_vtype = np.dtype([('a_position', 'f4', 2),
                           ('a_texcoord', 'f4', 2)])
    vertices = np.zeros(len(text) * 4, dtype=text_vtype)
    prev = None
    width = height = ascender = descender = 0
    ratio, slop = 1. / font.ratio, font.slop
    x_off = -slop
    # Need to make sure we have a unicode string here (Py2.7 mis-interprets
    # characters like "•" otherwise)
    if sys.version[0] == '2' and isinstance(text, str):
        text = text.decode('utf-8')
    # Need to store the original viewport, because the font[char] will
    # trigger SDF rendering, which changes our viewport
    orig_viewport = get_parameter('viewport')

    positions = []
    texcoords = []
    # XXX: Iterating over characters in Python is a really bad idea.
    for char in text:
        glyph = font[char]
        kerning = glyph['kerning'].get(prev, 0.) * ratio
        x0 = x_off + glyph['offset'][0] * ratio + kerning
        y0 = glyph['offset'][1] * ratio + slop
        x1 = x0 + glyph['size'][0]
        y1 = y0 - glyph['size'][1]
        u0, v0, u1, v1 = glyph['texcoords']
        positions.extend(rect_extents_to_corners(x0, y0, x1, y1))
        texcoords.extend(rect_extents_to_corners(u0, v0, u1, v1))
        x_move = glyph['advance'] * ratio + kerning
        x_off += x_move
        width += x_move
        ascender = max(ascender, y0 - slop)
        descender = min(descender, y1 + slop)
        height = max(height, glyph['size'][1] - 2*slop)
        prev = char
    vertices['a_position'] = positions
    vertices['a_texcoord'] = texcoords

    # Also analyse chars with large ascender and descender, otherwise the
    # vertical alignment can be very inconsistent
    for char in 'hy':
        glyph = font[char]
        y0 = glyph['offset'][1] * ratio + slop
        y1 = y0 - glyph['size'][1]
        ascender = max(ascender, y0 - slop)
        descender = min(descender, y1 + slop)
        height = max(height, glyph['size'][1] - 2*slop)

    set_viewport(*orig_viewport)

    # Tight bounding box (loose would be width, font.height /.asc / .desc)
    width -= glyph['advance'] * ratio - (glyph['size'][0] - 2*slop)
    dx = dy = 0

    if anchor_y == 'top':
        dy = -ascender
    elif anchor_y in ('center', 'middle'):
        dy = -(height / 2 + descender)
    elif anchor_y == 'bottom':
        dy = -descender

    if anchor_x == 'right':
        dx = -width
    elif anchor_x == 'center':
        dx = -width / 2.

    vertices['a_position'] += (dx, dy)
    vertices['a_position'] /= lowres_size
    return VertexBuffer(vertices)


class TextElement(GLElement):
    """Visual that displays text

    Parameters
    ----------
    text : str
        Text to display.
    color : instance of Color
        Color to use.
    bold : bool
        Bold face.
    italic : bool
        Italic face.
    face : str
        Font face to use.
    font_size : float
        Point size to use.
    pos : tuple
        Position (x, y) of the text.
    rotation : float
        Rotation (in degrees) of the text clockwise.
    anchor_x : str
        Horizontal text anchor.
    anchor_y : str
        Vertical text anchor.
    parent : instance of Entity
        The parent of the Text visual.
    """

    VERTEX_SHADER = """
        uniform mat4 u_model;
        uniform mat4 u_view;
        uniform mat4 u_projection;
        uniform float u_antialias;
        uniform float u_size;

        uniform vec2 u_pos;  // anchor position
        uniform vec2 u_scale;  // to scale to pixel units
        uniform float u_rotation;  // rotation in rad

        attribute vec2 a_position; // in point units
        attribute vec2 a_texcoord;

        varying vec2 v_texcoord;

        void main(void) {
            vec4 pos = u_projection * u_view * u_model * vec4(u_pos, 0.0, 1.0);
            mat2 rot = mat2(cos(u_rotation), -sin(u_rotation),
                            sin(u_rotation), cos(u_rotation));
            gl_Position = pos + vec4(rot * a_position * u_scale, 0., 0.);
            v_texcoord = a_texcoord;
        }
        """

    FRAGMENT_SHADER = """
        // Adapted from glumpy with permission
        const float M_SQRT1_2 = 0.707106781186547524400844362104849039;
        const float kernel_bias  = -0.234377;
        const float kernel_scale = 1.241974;

        uniform sampler2D u_font_atlas;
        uniform vec2 u_font_atlas_shape;
        uniform vec4 u_color;
        uniform float u_npix;
        uniform sampler2D u_kernel;

        varying vec2 v_texcoord;
        const float center = 0.5;

        // CatRom (bicubic) interpolation code
        vec4 filter1D_radius2(sampler2D kernel, float index, float x,
                              vec4 c0, vec4 c1, vec4 c2, vec4 c3) {
            float w, w_sum = 0.0;
            vec4 r = vec4(0.0,0.0,0.0,0.0);
            w = texture2D(kernel, vec2(0.500000+(x/2.0),index) ).r;
            w = w*kernel_scale + kernel_bias;
            r += c0 * w;
            w = texture2D(kernel, vec2(0.500000-(x/2.0),index) ).r;
            w = w*kernel_scale + kernel_bias;
            r += c2 * w;
            w = texture2D(kernel, vec2(0.000000+(x/2.0),index) ).r;
            w = w*kernel_scale + kernel_bias;
            r += c1 * w;
            w = texture2D(kernel, vec2(1.000000-(x/2.0),index) ).r;
            w = w*kernel_scale + kernel_bias;
            r += c3 * w;
            return r;
        }

        vec4 filter2D_radius2(sampler2D texture, sampler2D kernel, float index,
                              vec2 uv, vec2 pixel) {
            vec2 texel = uv/pixel - vec2(0.0,0.0) ;
            vec2 f = fract(texel);
            texel = (texel-fract(texel)+vec2(0.001,0.001))*pixel;
            vec4 t0 = filter1D_radius2(kernel, index, f.x,
                texture2D( texture, texel + vec2(-1,-1)*pixel),
                texture2D( texture, texel + vec2(0,-1)*pixel),
                texture2D( texture, texel + vec2(1,-1)*pixel),
                texture2D( texture, texel + vec2(2,-1)*pixel));
            vec4 t1 = filter1D_radius2(kernel, index, f.x,
                texture2D( texture, texel + vec2(-1,0)*pixel),
                texture2D( texture, texel + vec2(0,0)*pixel),
                texture2D( texture, texel + vec2(1,0)*pixel),
                texture2D( texture, texel + vec2(2,0)*pixel));
            vec4 t2 = filter1D_radius2(kernel, index, f.x,
                texture2D( texture, texel + vec2(-1,1)*pixel),
                texture2D( texture, texel + vec2(0,1)*pixel),
                texture2D( texture, texel + vec2(1,1)*pixel),
                texture2D( texture, texel + vec2(2,1)*pixel));
            vec4 t3 = filter1D_radius2(kernel, index, f.x,
                texture2D( texture, texel + vec2(-1,2)*pixel),
                texture2D( texture, texel + vec2(0,2)*pixel),
                texture2D( texture, texel + vec2(1,2)*pixel),
                texture2D( texture, texel + vec2(2,2)*pixel));
            return filter1D_radius2(kernel, index, f.y, t0, t1, t2, t3);
        }

        vec4 CatRom(sampler2D texture, vec2 shape, vec2 uv) {
            return filter2D_radius2(texture, u_kernel, 0.468750,
                                    uv, 1.0/shape);
        }

        float contour(in float d, in float w)
        {
            return smoothstep(center - w, center + w, d);
        }

        float sample(sampler2D texture, vec2 uv, float w)
        {
            return contour(texture2D(texture, uv).r, w);
        }

        void main(void) {
            vec4 color = u_color;
            vec2 uv = v_texcoord.xy;
            vec4 rgb;

            // Use interpolation at high font sizes
            if(u_npix >= 50.0)
                rgb = CatRom(u_font_atlas, u_font_atlas_shape, uv);
            else
                rgb = texture2D(u_font_atlas, uv);
            float distance = rgb.r;

            // GLSL's fwidth = abs(dFdx(uv)) + abs(dFdy(uv))
            float width = 0.5 * fwidth(distance);  // sharpens a bit

            // Regular SDF
            float alpha = contour(distance, width);

            if (u_npix < 30.) {
                // Supersample, 4 extra points
                // Half of 1/sqrt2; you can play with this
                float dscale = 0.5 * M_SQRT1_2;
                vec2 duv = dscale * (dFdx(v_texcoord) + dFdy(v_texcoord));
                vec4 box = vec4(v_texcoord-duv, v_texcoord+duv);
                float asum = sample(u_font_atlas, box.xy, width)
                           + sample(u_font_atlas, box.zw, width)
                           + sample(u_font_atlas, box.xw, width)
                           + sample(u_font_atlas, box.zy, width);
                // weighted average, with 4 extra points having 0.5 weight
                // each, so 1 + 0.5*4 = 3 is the divisor
                alpha = (alpha + 0.5 * asum) / 3.0;
            }

            gl_FragColor = vec4(color.rgb, color.a * alpha);
        }
        """

    def __init__(self, text='', color='black', bold=False, italic=False,
                 face='OpenSans', font_size=12, pos=(0, 0), rotation=0.,
                 anchor_x='center', anchor_y='center', font_manager=None):

        super(TextElement, self).__init__(self.VERTEX_SHADER,
                                          self.FRAGMENT_SHADER)
        # Check input
        _check_valid('anchor_y', anchor_y, ANCHOR_Y_ENUM)
        _check_valid('anchor_x', anchor_x, ANCHOR_X_ENUM)

        # Init font handling stuff
        # _font_manager is a temporary solution to use global mananger
        self._font_manager = font_manager or FONT_MANAGER
        self._font = self._font_manager.get_font(face, bold, italic)
        self._vertices = None
        self._anchors = (anchor_x, anchor_y)
        # Init text properties
        self.color = color
        self.text = text
        self.font_size = font_size
        self.pos = pos
        self.rotation = rotation

    def update(self, state, text):
        super(TextElement, self).update(state)
        self.text = text
        self.color = state.line_color

    @property
    def text(self):
        """The text string"""
        return self._text

    @text.setter
    def text(self, text):
        assert isinstance(text, string_types)
        self._text = text
        self._vertices = None

    @property
    def font_size(self):
        """ The font size (in points) of the text
        """
        return self._font_size

    @font_size.setter
    def font_size(self, size):
        self._font_size = max(0.0, float(size))

    @property
    def color(self):
        """ The color of the text
        """
        return self._color

    @color.setter
    def color(self, color):
        self._color = Color(color)

    @property
    def rotation(self):
        """ The rotation of the text (clockwise, in degrees)
        """
        return self._rotation * 180. / np.pi

    @rotation.setter
    def rotation(self, rotation):
        self._rotation = float(rotation) * np.pi / 180.

    @property
    def pos(self):
        """ The position of the text anchor in the local coordinate frame
        """
        return self._pos

    @pos.setter
    def pos(self, pos):
        pos = [float(p) for p in pos]
        assert len(pos) == 2
        self._pos = tuple(pos)

    def draw(self, projection_size):
        width, height = projection_size
        px_scale = 2.0/width, 2.0/height

        if len(self.text) == 0:
            return

        if self._vertices is None:
            self._vertices = _text_to_vbo(self._text, self._font,
                                          self._anchors[0], self._anchors[1],
                                          self._font._lowres_size)
            idx = (np.array([0, 1, 2, 0, 2, 3], np.uint32) +
                   np.arange(0, 4*len(self._text), 4,
                             dtype=np.uint32)[:, np.newaxis])
            self._ib = IndexBuffer(idx.ravel())

        ps = (self._font_size / 72.) * 92.
        self._program['u_npix'] = ps
        self._program['u_font_atlas_shape'] = self._font._atlas.shape[:2]
        self._program['u_kernel'] = self._font._kernel
        self._program['u_scale'] = ps * px_scale[0], ps * px_scale[1]
        self._program['u_rotation'] = self._rotation
        self._program['u_pos'] = self._pos
        self._program['u_color'] = self._color.rgba
        self._program['u_font_atlas'] = self._font._atlas
        self._program.bind(self._vertices)
        set_state(blend=True, depth_test=False, blend_func=BLEND_FUNC)

        with self._draw_context():
            self._program.draw('triangles', self._ib)
