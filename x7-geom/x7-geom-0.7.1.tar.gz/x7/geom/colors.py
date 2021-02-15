from .typing import *
from .transform import Transform

TRANSPARENT = (0, 0, 0, 0)
NOCOLOR = 'NoColor'
Color = Union[str, Number, Tuple]
OptColor = Optional[Color]

__all__ = [
    'TRANSPARENT', 'NOCOLOR', 'Color', 'OptColor',
    'Colors', 'ColorsByShape',
    'Brush', 'Pen', 'PenBrush', 'PensByShape',
]


def _nocolor(color):
    return None if color == NOCOLOR else color


class Colors(object):
    def __init__(self, outline: OptColor = 'black', fill: OptColor = None):
        self.outline = _nocolor(outline)
        self.fill = _nocolor(fill)

    @property
    def filled(self):
        return bool(self.fill)

    def __repr__(self):
        return 'Colors(%s, %s)' % (self.outline, self.fill)


class Brush(object):
    """Brush describes how to fill an object"""
    def __init__(self, color: Color):
        self.color = color

    def __eq__(self, other):
        return type(self) is type(other) and self.color == other.color

    def __str__(self):
        return 'Brush(%s)' % str(self.color)

    def __repr__(self):
        return 'Brush(%s)' % repr(self.color)


class Pen(object):
    """
        Pen describes how to stroke an object:
            * Width == 0 => thinnest possible line (1 pixel)
            * Width > 0 => width in pixels
            * Width < 0 => width will be scaled by xform
    """
    def __init__(self, brush: Union[Brush, Color], width: float = 0.0):
        self.brush = brush if isinstance(brush, Brush) else Brush(brush)
        self.width = width

    def __eq__(self, other):
        return type(self) is type(other) and self.brush == other.brush and self.width == other.width

    def __str__(self):
        return 'Pen(%s, %s)' % (self.brush.color, self.width)

    def __repr__(self):
        return 'Pen(%r, %r)' % (self.brush.color, self.width)

    def replace(self, brush=None, width=None):
        return Pen(brush or self.brush, width if width is not None else self.width)


class PenBrush(object):
    """PenBrush describes both how to stroke and fill an object"""
    def __init__(self, pen: Union[None, Pen, Color, tuple], brush: Union[None, Brush, Color] = None):
        if isinstance(pen, Pen) or pen is None:
            self.pen = pen
        elif isinstance(pen, tuple) and len(pen) == 2:
            self.pen = Pen(*pen)        # (color, width)
        else:
            self.pen = Pen(pen)         # color
        if isinstance(brush, Brush) or brush is None:
            self.brush = brush
        else:
            self.brush = Brush(brush)  # color

    def __eq__(self, other):
        return type(self) is type(other) and self.pen == other.pen and self.brush == other.brush

    @property
    def filled(self):
        return bool(self.brush)

    @property
    def stroked(self):
        return bool(self.pen)

    @property
    def fill_color(self):
        return self.brush.color if self.brush else None

    @property
    def stroke_color(self):
        return self.pen.brush.color if self.pen else None

    def stroke_width(self, xform: Transform):
        if self.pen:
            if self.pen.width > 0:
                return self.pen.width
            else:
                return xform.transform_width(-self.pen.width)

    def __str__(self):
        if not self.pen:
            pen = None
        elif self.pen.width == 1:
            pen = self.pen.brush.color
        else:
            pen = '(%s, %s)' % (self.pen.brush.color, self.pen.width)
        return 'PenBrush(%s, %s)' % (pen, self.brush.color if self.brush else self.brush)

    def __repr__(self):
        return 'PenBrush(%r, %r)' % (self.pen, self.brush)

    def replace(self, pen=None, width=None, brush=None):
        if pen and width is not None:
            raise ValueError("specify pen or width not both")
        if width is not None and self.pen:
            pen = Pen(self.pen.brush, width)
        return PenBrush(pen or self.pen, brush or self.brush)


class ColorsByShape(object):
    """
        Shapes have the following color attributes:
            - edge - draw edge only, no fill
            - filled - fill only, no edge
            - clear - filled with TRANSPARENT, no edge
            - edge_filled - fill with opaque, then edge
            - edge_clear - fill with TRANSPARENT, then edge
    """

    def __init__(self, edge=Colors(), filled=Colors(), clear=Colors(), edge_filled=Colors(), edge_clear=Colors()):
        self.edge = edge
        self.filled = filled
        self.clear = clear
        self.edge_filled = edge_filled
        self.edge_clear = edge_clear

    @staticmethod
    def keys():
        return 'edge', 'filled', 'clear', 'edge_filled', 'edge_clear'

    def __str__(self):
        return 'ColorsByShape(%s)' % ','.join(str(self[k]) for k in self.keys())

    def __repr__(self):
        return str(self)

    def __getitem__(self, shape_kind):
        if shape_kind in self.keys():
            return getattr(self, shape_kind)
        else:
            raise ValueError('Unknown shape kind: %s, expected one of %s' % (shape_kind, ', '.join(self.keys())))

    @staticmethod
    def make(draft=True, color: Color = 'white', fill: Color = TRANSPARENT, transparent: Color = TRANSPARENT):
        """
            Generate the colors for different types of shapes, using a standard mapping:
                1. Non-closed shapes: thin line in draft, fat line in prod
                2. Filled shapes: thin outline in draft, filled in prod
                3. Edged, closed shapes: thin outline in draft, fat outline in prod
                4. Edged, filled shapes: thin outline in draft, filled & fat outline in prod
                4a. Edged, transparent: like #4, but filled with transparent

        :param draft:		True for draft images
        :param color:		Color to be used for lines and normal fill
        :param fill:		Color to be used for filling edged shapes
        :param transparent:	 Color to be used for transparent fills
        :return:
        """

        if draft:
            return ColorsByShape(
                edge=Colors(color, None),
                filled=Colors(color, None),
                clear=Colors(color, None),
                edge_filled=Colors(color, None),
                edge_clear=Colors(color, None),
            )
        else:
            return ColorsByShape(
                edge=Colors(color, None),
                filled=Colors(None, color),
                clear=Colors(None, transparent),
                edge_filled=Colors(color, fill),
                edge_clear=Colors(color, transparent),
            )


class PensByShape(object):
    """
        Shapes have the following color attributes:
            - edge - draw edge only, no fill
            - filled - fill only, no edge
            - clear - filled with TRANSPARENT, no edge
            - edge_filled - fill with opaque, then edge
            - edge_clear - fill with TRANSPARENT, then edge
    """

    def __init__(self, edge=None, filled=None, clear=None, edge_filled=None, edge_clear=None):
        default = PenBrush(Pen('black', 1), None)
        self.edge = edge or default
        self.filled = filled or default
        self.clear = clear or default
        self.edge_filled = edge_filled or default
        self.edge_clear = edge_clear or default

    @staticmethod
    def keys():
        return 'edge', 'filled', 'clear', 'edge_filled', 'edge_clear'

    def __str__(self):
        return 'PensByShape(%s)' % ','.join(str(self[k]) for k in self.keys())

    def __repr__(self):
        return 'PensByShape(%s)' % ', '.join('%s=%r' % (k, self[k]) for k in self.keys())

    def __getitem__(self, shape_kind) -> PenBrush:
        if shape_kind in self.keys():
            return getattr(self, shape_kind)
        else:
            raise ValueError('Unknown shape kind: %s, expected one of %s' % (shape_kind, ', '.join(self.keys())))

    def replace_width(self, width):
        return PensByShape(**dict((k, self[k].replace(width=width)) for k in self.keys()))

    @staticmethod
    def make(
            draft=True, color: Color = 'white', fill: Color = TRANSPARENT,
            transparent: Color = TRANSPARENT, width=0.0):
        """
            Generate the colors for different types of shapes, using a standard mapping:
                1. Non-closed shapes: thin line in draft, fat line in prod
                2. Filled shapes: thin outline in draft, filled in prod
                3. Edged, closed shapes: thin outline in draft, fat outline in prod
                4. Edged, filled shapes: thin outline in draft, filled & fat outline in prod
                4a. Edged, transparent: like #4, but filled with transparent

        :param draft:		True for draft images
        :param color:		Color to be used for lines and normal fill
        :param fill:		Color to be used for filling edged shapes
        :param transparent:	 Color to be used for transparent fills
        :param width:       Width for all production pens
        :return:
        """

        if draft:
            pen = PenBrush((color, 0.0), None)
            return PensByShape(
                edge=pen,
                filled=pen,
                clear=pen,
                edge_filled=pen,
                edge_clear=pen,
            )
        else:
            edge_pen = Pen(color, width)
            return PensByShape(
                edge=PenBrush(edge_pen, None),
                filled=PenBrush(None, color),
                clear=PenBrush(None, transparent),
                edge_filled=PenBrush(edge_pen, fill),
                edge_clear=PenBrush(edge_pen, transparent),
            )
