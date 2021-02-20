#! /usr/bin/env python

from math import fabs


class ColorBase:
  """Represents an abstract color.

  The actual meaning of this color depend on implementation in the derived classes
  """

  def __init__(__self__, *args):
    """Creates an instance of a color from given components

    :param c1: represents first component of this color
    :type c1: ``integer``
    :param c2: represents second component of this color
    :type c2: ``integer``
    :param c3: represents third component of this color
    :type c3: ``integer``
    :param alpha: represents transparency of this color
    :type alpha: ``integer``
    """
    alpha = 0
    if len(args) > 1:
      if len(args)>3:
        alpha = args[3]
      __self__.set(args[0], args[1], args[2], alpha)
    else:
      c1,c2,c3 = hex_to_rgb(args[0])
      __self__.set(c1,c2,c3, alpha)

  def deepcopy(self):
    """Returns a deep copy of this color
    """
    return ColorBase(self.c1, self.c2, self.c3, self.alpha)

  def set(__self__, c1, c2, c3, alpha=0):
    """
    Sets new values for components of this color.

    The color's components must be given as integers from [0,255] range

    :param c1:
      sets first component of this color
    :type c1: ``integer``
    :param c2:
      sets second component of this color
    :type c2: ``integer``
    :param c3:
      sets third component of this color
    :type c3: ``integer``
    :param alpha:
      sets transparency of this color
    :type alpha: ``integer``
    """
    if c1 <= 1 and c2 <= 1 and c3 <= 1:
      c1 = int(c1 * 255)
      c2 = int(c2 * 255)
      c3 = int(c3 * 255)
      alpha = int(alpha * 255)
    __self__.c1 = c1
    __self__.c2 = c2
    __self__.c3 = c3
    __self__._alpha = alpha

  @property
  def alpha(self):
    """alpha value

       :getter: returns actual alpha value
       :setter: sets new alpha value
       :type: ``integer``
    """
    return self._alpha

  @alpha.setter
  def alpha(self, a):
    self._alpha = a

  @staticmethod
  def clamp(val, minimum=0, maximum=255):
    """Clamps color value to the given range, by default to [0,255]

    if val is between minimum and maximum returns val
    if val is less than minimum returns minimum
    if is over maximum returns maximum 
    """
    if val < minimum: return minimum
    if val > maximum: return maximum

    return val

  def shade(__self__, factor):
    """Creates color changed with factor

       :param factor:
         value to change the color shade
       :type factor: ``float``
    """
    __self__.c1 = __self__.clamp(__self__.c1 * factor) if __self__.c1 > 0 else int(255*(factor-1))
    __self__.c2 = __self__.clamp(__self__.c2 * factor) if __self__.c2 > 0 else int(255*(factor-1))
    __self__.c3 = __self__.clamp(__self__.c3 * factor) if __self__.c3 > 0 else int(255*(factor-1))
    return __self__

  def create_darker(__self__, factor=0.1):
    """Creates darker color with given factor 

       :param factor:
         value to change the color to darker (default is 0.1)
       :type factor: ``float``
    """
    return ColorBase(__self__.c1, __self__.c2, __self__.c3, __self__.alpha).shade(1.0 - factor)

  def create_lighter(__self__, factor=0.1):
    """Creates lighter color with given factor

       :param factor:
         value to change the color to lighter (default is 0.1)
       :type factor: ``float``
    """
    return ColorBase(__self__.c1, __self__.c2, __self__.c3, __self__.alpha).shade(1.0 + factor)

  def mix(__self__, fraction, another_color):
    """ Mix this color with another color

    :param fraction:
       value to shift the color to another color
    :type fraction: ``float``
    :param another_color:
       color that is mix with a current color
    :type another_color: ``string``

    After this call this color retains (1-fraction) of this color and shifts by fraction value towards the new color
    """

    __self__.c1 = (1 - fraction) * __self__.c1 + fraction * another_color.c1
    __self__.c2 = (1 - fraction) * __self__.c2 + fraction * another_color.c2
    __self__.c3 = (1 - fraction) * __self__.c3 + fraction * another_color.c3

    return __self__

  def mixed_copy(__self__, fraction, another_color):
    """
    Mix this color with another color and returns result as a new color object

    :param fraction:
      value to shift the color to another color
    :type fraction: ``float``
    :param another_color:
      color that is mix with a current color
    :type another_color: ``string``

    The newly created color retains (1-fraction) of this color and shifts by fraction value towards the new color
    """
    new = ColorBase(__self__.c1, __self__.c2, __self__.c3, __self__._alpha)

    return new.mix(fraction, another_color)

  def __str__(__self__):
    """Returns a HEX-string representing this color

    The color's components must be given as integers from [0,255] range
    """

    return "#%02X%02X%02X" % (int(__self__.c1), int(__self__.c2), int(__self__.c3))


class ColorRGB(ColorBase):
  """Represents a color in RGB format
  """

  def to_rgb(__self__):
    """Returns RGB color
    """
    return __self__


def hex_to_rgb(hex_string):
  """Convert HEX string to RGB format

  :param hex_string:
    string in a HEX format
  :type hex_string: ``string``

  """
  hex_string = hex_string.lstrip('#')
  lv = len(hex_string)
  return tuple(int(hex_string[i:i + int(lv / 3)], 16) for i in range(0, lv, int(lv / 3)))


def mix_colors_by_hex(hex_color1, fraction, hex_color2):
    """
    Creates a color that is a mixture of two colors.

    Works as  ColorBase.mixed_copy() but without creating a ColorBase object in meantime. Use this method
    to make a mixed color if you have a pair of hex strings rather that ColorBase objects

    :param hex_color1: the first color to be mixed
    :param fraction: fraction of the first color
    :param hex_color2:  the second color to be mixed
    :return: a hex string representing the mixed color
    """
    h1 = hex_color1.lstrip('#')
    h2 = hex_color2.lstrip('#')

    lv = len(h1)
    ll = int(lv / 3)
    red = fraction * int(h1[0: ll], 16) + (1-fraction) * int(h2[0: ll], 16)
    grn = fraction * int(h1[ll: 2*ll], 16) + (1-fraction) * int(h2[ll: 2*ll], 16)
    blu = fraction * int(h1[2*ll: 3*ll], 16) + (1-fraction) * int(h2[2*ll: 3*ll], 16)

    return "#%02X%02X%02X" % (int(red), int(grn), int(blu))


named_colors = {}


def color_by_name(name):
  """Contains a Python dictionary which holds HEX string and color name as a key-value pairs

     Colors taken from:
     https://www.w3schools.com/colors/colors_names.asp

     :param name:
       name of a color to get as a HEX format
     :type name: ``string``
     :return: a deep copy of color

  """

  if len(named_colors) == 0:
    for i in [("#F0F8FF", "AliceBlue"), ("#FAEBD7", "AntiqueWhite"), ("#00FFFF", "Aqua"), ("#7FFFD4", "Aquamarine"),
              ("#F0FFFF", "Azure"), ("#F5F5DC", "Beige"), ("#FFE4C4", "Bisque"), ("#000000", "Black"),
              ("#FFEBCD", "BlanchedAlmond"), ("#0000FF", "Blue"), ("#8A2BE2", "BlueViolet"), ("#A52A2A", "Brown"),
              ("#DEB887", "BurlyWood"), ("#5F9EA0", "CadetBlue"), ("#7FFF00", "Chartreuse"), ("#D2691E", "Chocolate"),
              ("#FF7F50", "Coral"), ("#6495ED", "CornflowerBlue"), ("#FFF8DC", "Cornsilk"), ("#DC143C", "Crimson"),
              ("#00FFFF", "Cyan"), ("#00008B", "DarkBlue"), ("#008B8B", "DarkCyan"), ("#B8860B", "DarkGoldenRod"),
              ("#A9A9A9", "DarkGray"), ("#A9A9A9", "DarkGrey"), ("#006400", "DarkGreen"), ("#BDB76B", "DarkKhaki"),
              ("#8B008B", "DarkMagenta"), ("#556B2F", "DarkOliveGreen"), ("#FF8C00", "DarkOrange"),
              ("#9932CC", "DarkOrchid"), ("#8B0000", "DarkRed"), ("#E9967A", "DarkSalmon"), ("#8FBC8F", "DarkSeaGreen"),
              ("#483D8B", "DarkSlateBlue"), ("#2F4F4F", "DarkSlateGray"), ("#2F4F4F", "DarkSlateGrey"),
              ("#00CED1", "DarkTurquoise"), ("#9400D3", "DarkViolet"), ("#FF1493", "DeepPink"),
              ("#00BFFF", "DeepSkyBlue"), ("#696969", "DimGray"), ("#696969", "DimGrey"), ("#1E90FF", "DodgerBlue"),
              ("#B22222", "FireBrick"), ("#FFFAF0", "FloralWhite"), ("#228B22", "ForestGreen"), ("#FF00FF", "Fuchsia"),
              ("#DCDCDC", "Gainsboro"), ("#F8F8FF", "GhostWhite"), ("#FFD700", "Gold"), ("#DAA520", "GoldenRod"),
              ("#808080", "Gray"), ("#808080", "Grey"), ("#008000", "Green"), ("#ADFF2F", "GreenYellow"),
              ("#F0FFF0", "HoneyDew"), ("#FF69B4", "HotPink"), ("#CD5C5C", "Chestnut"),("#4B0082","Indigo"), ("#FFFFF0", "Ivory"),
              ("#F0E68C", "Khaki"), ("#E6E6FA", "Lavender"), ("#FFF0F5", "LavenderBlush"), ("#7CFC00", "LawnGreen"),
              ("#FFFACD", "LemonChiffon"), ("#ADD8E6", "LightBlue"), ("#F08080", "LightCoral"),
              ("#E0FFFF", "LightCyan"), ("#FAFAD2", "LightGoldenRodYellow"), ("#D3D3D3", "LightGray"),
              ("#D3D3D3", "LightGrey"), ("#90EE90", "LightGreen"), ("#FFB6C1", "LightPink"), ("#FFA07A", "LightSalmon"),
              ("#20B2AA", "LightSeaGreen"), ("#87CEFA", "LightSkyBlue"), ("#778899", "LightSlateGray"),
              ("#778899", "LightSlateGrey"), ("#B0C4DE", "LightSteelBlue"), ("#FFFFE0", "LightYellow"),
              ("#00FF00", "Lime"), ("#32CD32", "LimeGreen"), ("#FAF0E6", "Linen"), ("#FF00FF", "Magenta"),
              ("#800000", "Maroon"), ("#66CDAA", "MediumAquaMarine"), ("#0000CD", "MediumBlue"),
              ("#BA55D3", "MediumOrchid"), ("#9370DB", "MediumPurple"), ("#3CB371", "MediumSeaGreen"),
              ("#7B68EE", "MediumSlateBlue"), ("#00FA9A", "MediumSpringGreen"), ("#48D1CC", "MediumTurquoise"),
              ("#C71585", "MediumVioletRed"), ("#191970", "MidnightBlue"), ("#F5FFFA", "MintCream"),
              ("#FFE4E1", "MistyRose"), ("#FFE4B5", "Moccasin"), ("#FFDEAD", "NavajoWhite"), ("#000080", "Navy"),
              ("#FDF5E6", "OldLace"), ("#808000", "Olive"), ("#6B8E23", "OliveDrab"), ("#FFA500", "Orange"),
              ("#FF4500", "OrangeRed"), ("#DA70D6", "Orchid"), ("#EEE8AA", "PaleGoldenRod"), ("#98FB98", "PaleGreen"),
              ("#AFEEEE", "PaleTurquoise"), ("#DB7093", "PaleVioletRed"), ("#FFEFD5", "PapayaWhip"),
              ("#FFDAB9", "PeachPuff"), ("#CD853F", "Peru"), ("#FFC0CB", "Pink"), ("#DDA0DD", "Plum"),
              ("#B0E0E6", "PowderBlue"), ("#800080", "Purple"), ("#663399", "RebeccaPurple"), ("#FF0000", "Red"),
              ("#BC8F8F", "RosyBrown"), ("#4169E1", "RoyalBlue"), ("#8B4513", "SaddleBrown"), ("#FA8072", "Salmon"),
              ("#F4A460", "SandyBrown"), ("#2E8B57", "SeaGreen"), ("#FFF5EE", "SeaShell"), ("#A0522D", "Sienna"),
              ("#C0C0C0", "Silver"), ("#87CEEB", "SkyBlue"), ("#6A5ACD", "SlateBlue"), ("#708090", "SlateGray"),
              ("#708090", "SlateGrey"), ("#FFFAFA", "Snow"), ("#00FF7F", "SpringGreen"), ("#4682B4", "SteelBlue"),
              ("#D2B48C", "Tan"), ("#008080", "Teal"), ("#D8BFD8", "Thistle"), ("#FF6347", "Tomato"),
              ("#40E0D0", "Turquoise"), ("#EE82EE", "Violet"), ("#F5DEB3", "Wheat"), ("#FFFFFF", "White"),
              ("#F5F5F5", "WhiteSmoke"), ("#FFFF00", "Yellow"), ("#9ACD32", "YellowGreen"),
              ("#89B3E2", "ClustalXBlue"), ("#59B93D", "ClustalXGreen"), ("#DC9C5B", "ClustalXOrange"),
              ("#CDCB42", "ClustalXYellow"), ("#B53A25", "ClustalXRed"), ("#BD59C6", "ClustalXMagenta"), ("#E28683","ClustalXPink"),
              ("#77dd88", "MAELightGreen"), ("#99ee66", "MAEGreen"), ("#55bb33", "MAEDarkGreen"),
              ("#66bbff", "MAEBlue"), ("#9999ff", "MAELilac"), ("#5555ff", "MAEDarkBlue"), ("#ffcc77", "MAEOrange"),
              ("#eeaaaa", "MAEPink"), ("#ff4455", "MAERed")
              ]:
      rgb = hex_to_rgb(i[0])
      named_colors[i[1]] = ColorRGB(rgb[0], rgb[1], rgb[2])
      named_colors[i[1].lower()] = ColorRGB(rgb[0], rgb[1], rgb[2])
  return named_colors[name].deepcopy()

#+ Default colors used for plotting; one color for each data set
default_plotting_colors = ["#1f77b4", "#ff7f0e","#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e3ffc2", "#7f7f7f", "#bcbd22", "#17becf"]


def get_color(color):
    """Returns a color corresponding to the given argument

    :param color: new  color
    :type color: color name as ``string``, color hex as ``string`` or ``ColorBase`` object
    :return: an object representing a color
    """

    if isinstance(color, str):
        if color[0] == '#' :
            rgb = hex_to_rgb(color)
            return ColorRGB(rgb[0], rgb[1], rgb[2])
        elif color.startswith("rgb("):
            tokens = color[4:-1].replace(",", " ").split()
            return ColorRGB(int(tokens[0]), int(tokens[1]), int(tokens[2]))
        else:
            return color_by_name(color)
    else:
        return color


class ColorHSV(ColorBase):
  """Represents a color in HSV format
  """
  def to_rgb(__self__):
    """Converts HSV format to RGB
    """
    rgb = ColorRGB()
    if __self__.c2 == 0: rgb.set(__self__.c3, __self__.c3, __self__.c3, __self__.a)
    h = __self__.c1 / 255.0
    s = __self__.c2 / 255.0
    v = __self__.c3 / 255.0
    i = int(h * 6.)
    f = (h * 6.) - i;
    p, q, t = int(255 * (v * (1. - s))), int(255 * (v * (1. - s * f))), int(255 * (v * (1. - s * (1. - f))));
    v *= 255;
    i %= 6
    if i == 0: rgb.set(v, t, p, __self__.a / 255)
    if i == 1: rgb.set(q, v, p, __self__.a / 255)
    if i == 2: rgb.set(p, v, t, __self__.a / 255)
    if i == 3: rgb.set(p, q, v, __self__.a / 255)
    if i == 4: rgb.set(t, p, v, __self__.a / 255)
    if i == 5: rgb.set(v, p, q, __self__.a / 255)
    return rgb


class ColorMap:
    """
    A class that converts real values into a color

    """

    def __init__(self, stops, **kwargs):
        """ Creates a color map of given stops

        :param stops:
          values and colors that defines stops in ColorMap object
        :type stops: ``list`` of ``(float, color)`` tuples
        :param kwargs:
            see below

        :Keyword Arguments ``(**kwargs)``:
            * *left_color* (``color``) --
              a color assigned to values lover than the first stop color; by default the leftmost color is used
            * *right_color* (``color``) --
              a color assigned to values higher than the last stop color; by default the rightmost color is used
        """
        self.stop_values = []
        self.stop_colors = []
        self.__left_color = kwargs.get("left_color", None)
        self.__right_color = kwargs.get("right_color", None)
        for v, c in stops:
            if isinstance(c, str):
                self.stop_colors.append(color_by_name(c))
            else:
                self.stop_colors.append(c)
            self.stop_values.append(v)

    @property
    def min_value(self):
        """ Returns the minimum value of this color scale. All values lower than this one will be painted
        with self.left_color color

        :return: minimum value of this color scale
        """
        return self.stop_values[0]

    @property
    def max_value(self):
        """ Returns the maximum value of this color scale. All values higher than this one will be painted
        with self.right_color color

        :return: maximum value of this color scale
        """
        return self.stop_values[-1]

    @property
    def left_color(self):
        """Returns a color assigned to values lover than the first stop color"""
        return self.__left_color

    @left_color.setter
    def left_color(self, new_color):
        self.__left_color = new_color

    @property
    def right_color(self):
        """Returns a color assigned to values lover than the last stop color"""
        return self.__right_color

    @right_color.setter
    def right_color(self, new_color):
        self.__right_color = new_color

    def color(self, val):
        """Returns a color for given value

        :param val:
          value for a color
        :type val: ``float``
        """
        if val < self.stop_values[0]:
            return self.__left_color if self.__left_color else self.stop_colors[0]
        if val > self.stop_values[-1]:
            return self.__right_color if self.__right_color else self.stop_colors[-1]
        for i in range(1, len(self.stop_values)):
            if val >= self.stop_values[i - 1] and val <= self.stop_values[i]:
                return self.stop_colors[i - 1].mixed_copy(
                    (val - self.stop_values[i - 1]) / (self.stop_values[i] - self.stop_values[i - 1]), self.stop_colors[i])

# violet_red and yellow_green come from Joelle Snaith, see https://www.joellesnaith.com/tesco-data-visualisation/
known_color_scales = {"reds" : ['#ffffe0','#ffd59b','#ffa474','#f47461','#db4551','#b81b34','#8b0000'],
		"blues" : ['#eff3ff','#c6dbef','#9ecae1','#6baed6','#4292c6','#2171b5','#084594'],
		"greens" : ['#edf8e9','#c7e9c0','#a1d99b','#74c476','#41ab5d','#238b45','#005a32'],
		"greys" : ['#f7f7f7','#d9d9d9','#bdbdbd','#969696','#737373','#525252','#252525'],
		"purples" : ['#f2f0f7','#dadaeb','#bcbddc','#9e9ac8','#807dba','#6a51a3','#4a1486'],
		"pinks" : ['#feebe2','#fcc5c0','#fa9fb5','#f768a1','#dd3497','#ae017e','#7a0177'],
		"magma" : ['#FCFFB2','#FCDF96','#FBC17D','#FBA368','#FA8657','#F66B4D','#ED504A','#E03B50','#C92D59','#B02363',
			    '#981D69','#81176D','#6B116F','#57096E','#43006A','#300060','#1E0848','#110B2D','#080616','#000005'],
		"viridis" : ['#440154','#481567','#482677','#453781','#404788','#39568C','#33638D','#2D708E','#287D8E','#238A8D',
			     '#1F968B','#20A387','#29AF7F','#3CBB75','#55C667','#73D055','#95D840','#B8DE29','#DCE319','#FDE725'],
        "pastel1" : ["#fbb4ae","#b3cde3","#ccebc5","#decbe4","#fed9a6","#ffffcc","#e5d8bd","#fddaec","#f2f2f2"],
        "accent" : ["#7fc97f","#beaed4","#fdc086","#ffff99","#386cb0","#f0027f","#bf5b17","#666666"],
        "paired" : ["#a6cee3","#1f78b4","#b2df8a","#33a02c","#fb9a99","#e31a1c","#fdbf6f","#ff7f00","#cab2d6","#6a3d9a","#ffff99","#b15928"],
        "tableau10" : ["#4e79a7","#f28e2c","#e15759","#76b7b2","#59a14f","#edc949","#af7aa1","#ff9da7","#9c755f","#bab0ab"],
        "violet_red" : ["#77216f", "#7b3f88", "#7f5ea1", "#837dbb", "#a76a8f", "#cb5763", "#ef4438"],
        "yellow_green" : ["#cddc37", "#88c452", "#44ad6d", "#009688", "#007f8f", "#006997", "#00539f"],
        "spectral": ['#9e0142','#a70b44','#af1446','#b71d48','#c02749','#c7304a','#ce384b','#d5414b','#db494a','#e1514a','#e65949','#ea6149','#ee6a49','#f1724a','#f47b4d','#f68550','#f88e53','#f99858','#fba15d','#fcaa62','#fcb368','#fdbc6e','#fdc474','#fecc7b','#fed382','#feda89','#fee090','#fee698','#feeb9f','#fef0a5','#fdf3aa','#fcf6ae','#faf8b0','#f8f9b0','#f5faae','#f2f9ab','#edf8a7','#e8f6a4','#e2f3a1','#dbf19f','#d4ee9f','#cbea9f','#c3e79f','#b9e3a0','#b0dfa1','#a6dba3','#9bd7a3','#91d3a4','#87cea5','#7dc9a6','#73c3a7','#69bda9','#60b6ab','#57aeae','#50a6b0','#499db2','#4595b4','#428cb5','#4283b4','#447ab3','#4771b0','#4c68ad','#525fa9','#5956a5'],
        "purple_orange": ['#2d004b','#330655','#390c5e','#3f1367','#461a70','#4c2279','#522a81','#593388','#603d8f','#664796','#6d529c','#745da2','#7c68a8','#8372ae','#8a7cb4','#9286b9','#998fbf','#a198c5','#a8a0ca','#afa8cf','#b6b0d4','#bcb8d9','#c3c0dd','#c9c7e1','#cfcee4','#d4d4e7','#dadaea','#dfdfed','#e4e4ee','#e8e8ef','#ecebef','#f0eded','#f3eeea','#f6eee4','#f8eddd','#faead5','#fbe7cc','#fce3c1','#fddeb6','#fdd9aa','#fdd49e','#fdce92','#fcc885','#fbc178','#faba6c','#f7b35f','#f4ab52','#f1a346','#ed9b3b','#e89430','#e38c27','#dd841f','#d77d18','#d17613','#ca6f0f','#c3680c','#bc620a','#b55c09','#ad5708','#a55208','#9d4c07','#954807','#8d4308','#853e08'],
        "red_blue": ['#67001f','#730421','#7e0823','#8a0c25','#941127','#9f172a','#a81d2d','#b12531','#b82e35','#bf373a','#c6413f','#cc4c45','#d1574b','#d66252','#db6d59','#e07861','#e58369','#e98d71','#ed977a','#f0a183','#f3ab8d','#f5b497','#f7bda1','#f9c5ab','#faccb5','#fad3bf','#fbdac8','#fae0d1','#fae5d8','#f9e9e0','#f7ece6','#f4eeeb','#f1efee','#edf0f1','#e9eff2','#e3edf2','#ddeaf2','#d6e7f0','#cfe4ef','#c7e0ed','#bedbea','#b5d7e8','#abd1e5','#a1cce2','#96c6df','#8bc0db','#80b9d7','#74b2d4','#69aad0','#5ea3cc','#549bc8','#4b94c4','#428cc0','#3b85bc','#347eb7','#2e76b2','#296fad','#2467a6','#1f609e','#1a5895','#164f8b','#114781','#0d3f75','#08366a'],
        "red_yellow_blue":['#a50026','#ad0826','#b50f26','#bc1727','#c41f28','#cb2729','#d12f2b','#d7382d','#dd4030','#e24a33','#e75337','#eb5d3c','#ee6640','#f17044','#f47a49','#f6844e','#f88e53','#f99858','#fba15d','#fcaa63','#fcb369','#fdbc70','#fdc477','#fecc7e','#fed385','#feda8c','#fee094','#fee69b','#feeba3','#fef0aa','#fdf3b2','#fbf6ba','#f9f8c2','#f7f9ca','#f3f9d2','#eff8da','#eaf6e1','#e4f4e7','#def1eb','#d7eeee','#d0ebef','#c8e7ef','#c0e3ee','#b8deec','#b0d9e9','#a7d4e6','#9fcee3','#96c8e0','#8ec1dc','#86bad8','#7db3d4','#75abd0','#6da3cc','#669bc8','#5f92c3','#5889bf','#5180ba','#4c77b5','#466eb1','#4264ac','#3e5ba7','#3a51a2','#37479e','#333d99'],
        "pink_yellow_green": ['#8e0152','#970559','#9f0960','#a70e66','#af146d','#b71b74','#be237b','#c42c83','#c9378a','#ce4391','#d34f99','#d75ca0','#da69a8','#de75af','#e181b6','#e48cbd','#e796c4','#eaa0ca','#eda9d0','#f0b1d6','#f2bada','#f4c1df','#f6c8e3','#f8cfe6','#f9d5e9','#fadaec','#fadfee','#fae4f0','#fae8f1','#f9ecf2','#f8eff2','#f7f1f1','#f5f3ef','#f3f4ec','#f1f5e7','#eef5e2','#ebf5dc','#e7f4d5','#e2f2cc','#ddf1c3','#d7eeb9','#d1ecaf','#cae8a4','#c3e599','#bbe18e','#b3dc83','#abd878','#a2d26d','#9acd62','#91c759','#89c150','#80bb47','#78b540','#70af39','#68a833','#60a12e','#599b2a','#529426','#4b8d23','#448621','#3e7f1f','#38781d','#31711b','#2b691a']
    }

categorical_palettes = ["pastel1", "accent", "paired", "tableau10"]
continuous_palettes = ["violet_red", "blues", "greens", "greys", "purples", "pinks", "magma", "viridis", "yellow_green",
                       "spectral", "purple_orange", "red_blue", "red_yellow_blue", "pink_yellow_green"]

def colormap_by_name(scale_name, min_val, max_val, if_reversed=False):
  """Sets the real values for colors for given color map
  Returns ColorMap object

  :param scale_name:
    name of a color scale
  :type scale_name: ``string``
  :param min_val:
     minimum value of a scale
  :type min_val: ``integer``
  :param max_val:
    maximum value of a scale
  :type max_val: ``integer``
  :param if_reversed:
    if True, the colors will be used in the reversed order
  :type if_reversed: ``boolean``

  """
  arg = []
  if scale_name in known_color_scales :
    if if_reversed:
        known_color_scales[scale_name].reverse()
    for i in range(0,len(known_color_scales[scale_name])):
      v = (max_val-min_val)/(len(known_color_scales[scale_name])-1)*i+min_val
      rgb = hex_to_rgb(known_color_scales[scale_name][i])
      arg.append( (v,ColorRGB(rgb[0],rgb[1],rgb[2])) )
    if if_reversed:
        known_color_scales[scale_name].reverse()

  return ColorMap(arg)


def get_font_size(x):
    """Return a size from a real value argument

    This function is used by plotting methods to convert a computed real value to nicely looking font

    :param x: a real value that will be rounded to a nearest font size
    :return: font size (``integer``)
    """

    sizes = [4, 8, 12, 16, 20, 24]

    for i in sizes:
        if fabs(x) <= i: return i - 1
    return sizes[-1]


def create_style(**kwargs):
    """Creates a string encoding a style of a SVG element

    Style parameters are retrieved from a given kwargs object.

    If ``"darker`` or ``"lighter"`` words are used as ``stroke``, a darker or a lighter variant of the fill color
    will be used as a stroke color. This works only when the fill color has been explicitly specified

    :param kwargs:
      style parameters; recognized keys are: 'fill_opacity', 'gradient', 'fill', 'stroke', 'stroke_width',
      'stroke_dasharray', 'stroke_linejoin', 'stroke_linecap', 'text_anchor', 'font_weight',
      'font_size', 'style', 'cursor' and 'opacity'
    :type kwargs: ``map``

    """
    style_str = "style='"
    if 'style' in kwargs : style_str += kwargs["style"]
    if 'gradient' in kwargs: style_str += " fill:url(#%s);" % kwargs['gradient']
    else:
      if 'fill' in kwargs: style_str += " fill:%s ;" % kwargs['fill']

    if 'stroke' in kwargs:
        if kwargs['stroke'] == "darker" and 'fill' in kwargs:
            col = get_color(kwargs['fill']).create_darker(0.3)
            style_str += " stroke:%s;" % str(col)
        elif kwargs['stroke'] == "lighter" and 'fill' in kwargs:
            col = get_color(kwargs['fill']).create_lighter(0.2)
            style_str += " stroke:%s;" % str(col)
        else:
            style_str += " stroke:%s;" % kwargs['stroke']
    if 'stroke_width' in kwargs: style_str += " stroke-width:%s;" % kwargs['stroke_width']
    if 'opacity' in kwargs: style_str += " opacity:%.2f;" % kwargs['opacity']
    if 'stroke_dasharray' in kwargs: style_str += " stroke-dasharray:%.1f;" % kwargs['stroke_dasharray']
    if 'font_size' in kwargs : style_str += "font-size:%.1fpx;" % kwargs['font_size']
    if 'font_family' in kwargs : style_str += "font-family:%s;" % kwargs['font_family']
    if 'font_weight' in kwargs : style_str += "font-weight: %s;" % kwargs['font_weight'] 
    if 'text_anchor' in kwargs : style_str += "text-anchor:%s;" % kwargs['text_anchor'] 
    if 'stroke_linecap' in kwargs: style_str += ": stroke-linecap:%s;" % kwargs['stroke_linecap']
    if 'stroke_linejoin' in kwargs : style_str += "stroke-linejoin:%s;"% kwargs['stroke_linejoin']
    if 'fill_opacity' in kwargs: style_str += " fill-opacity:%s;" % kwargs['fill_opacity']
    if 'cursor' in kwargs: style_str += " cursor:%s; " % kwargs['cursor']

    style_str +="'"
    return style_str


default_drawing_style = """
    stroke:black;
    """

default_text_style = """stroke-width:0;
    font-size: 10px;
    font-family:sans-serif;
    font-weight:normal;
    text-anchor:middle;
    """

atom_colors = {"H": ColorRGB(128, 128, 128), "C": "#050505", "CA": "#050505", "S": "#FFC832", "P": "#FFA500",
               "N": "#87CEEB", "FE": "#C0C0C0", "O": "red", "NA": "#A0A0A0", "MG": "#000080", "CU": "#e96b39", "ZN": "#C0C0C0", "MO": "#20B2AA", "SE": "Orange"}


__mlg = str(color_by_name("MAELightGreen"))
__mg = str(color_by_name("MAEGreen"))
__mdg = str(color_by_name("MAEDarkGreen"))
__mb = str(color_by_name("MAEBlue"))
__ml = str(color_by_name("MAELilac"))
__mdb = str(color_by_name("MAEDarkBlue"))
__mo = str(color_by_name("MAEOrange"))
__mp = str(color_by_name("MAEPink"))
__mr = str(color_by_name("MAERed"))


__b = str(color_by_name("ClustalXBlue"))
__r = str(color_by_name("ClustalXRed"))
__o = str(color_by_name("ClustalXOrange"))
__y = str(color_by_name("ClustalXYellow"))
__g = str(color_by_name("ClustalXGreen"))
__m = str(color_by_name("ClustalXMagenta"))
__p = str(color_by_name("ClustalXPink"))
known_sequence_scales = {
    "hec_secondary": {'H': "red", "E": "blue", "C": "gray", "L": "gray", "gap": "gray"},
    "clustal": {
        "A": __b, "I": __b, "L": __b, "M": __b, "F": __b, "W": __b, "V": __b, "K": __r,
        "R": __r, "D": __m, "E": __m, "N": __g, "Q": __g, "S": __g, "T": __g,
        "C": __p, "G": __o, "P": __y, "H": "white", "Y": "white", "-": "grey", "_": "grey"
    },
    "maeditor": {
        "A": __mlg, "I": __mb, "L": __mb, "M": __mb, "F": __ml, "W": __ml, "V": __mb, "K": __mo,
        "R": __mo, "D": __mdg, "E": __mdg, "N": __mdg, "Q": __mdg, "S": __mr, "T": __mr,
        "C": __mg, "G": __mlg, "P": __mp, "H": __mdb, "Y": __ml, "-": "grey", "_": "grey"
    }
}
