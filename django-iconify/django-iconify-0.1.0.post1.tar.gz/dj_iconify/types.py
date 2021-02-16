"""Iconify data types used in API.

Documentation: https://docs.iconify.design/types/
"""
from typing import Collection, Dict, List, Optional, Sequence, Union
from typing.io import TextIO
import json

from .util import split_css_unit


class IconifyOptional:
    """Mixin containing optional attributes all other types can contain."""

    left: Optional[int] = None
    top: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None

    rotate: Optional[int] = None
    h_flip: Optional[bool] = None
    v_flip: Optional[bool] = None

    def _as_dict_optional(self) -> dict:
        res = {}
        if self.left is not None:
            res["left"] = self.left
        if self.top is not None:
            res["top"] = self.top
        if self.width is not None:
            res["width"] = self.width
        if self.height is not None:
            res["height"] = self.height
        if self.rotate is not None:
            res["rotate"] = self.rotate
        if self.h_flip is not None:
            res["hFlip"] = self.h_flip
        if self.v_flip is not None:
            res["vFlip"] = self.v_flip
        return res

    def _from_dict_optional(self, src: dict) -> None:
        self.left = src.get("left", None)
        self.top = src.get("top", None)
        self.width = src.get("width", None)
        self.height = src.get("height", None)
        self.rotate = src.get("rotate", None)
        self.h_flip = src.get("hFlip", None)
        self.v_flip = src.get("vFlip", None)


class IconifyIcon(IconifyOptional):
    """Single icon as loaded from Iconify JSON data.

    Documentation: https://docs.iconify.design/types/iconify-icon.html
    """

    _collection: Optional["IconifyJSON"]
    _name: str
    body: str

    @classmethod
    def from_dict(
        cls, name: str, src: dict, collection: Optional["IconifyJSON"] = None
    ) -> "IconifyIcon":
        self = cls()
        self.body = src["body"]
        self._name = name
        self._from_dict_optional(src)
        self._collection = collection
        return self

    def as_dict(self) -> dict:
        res = {
            "body": self.body,
        }
        res.update(self._as_dict_optional())
        return res

    def get_width(self):
        """Get the width of the icon.

        If the icon has an explicit width, it is returned.
        If not, the width set in the collection is returned, or the default of 16.
        """
        if self.width:
            return self.width
        elif self._collection and self._collection.width:
            return self._collection.height
        else:
            return 16

    def get_height(self):
        """Get the height of the icon.

        If the icon has an explicit height, it is returned.
        If not, the height set in the collection is returned, or the default of 16.
        """
        if self.height:
            return self.height
        elif self._collection and self._collection.height:
            return self._collection.height
        else:
            return 16

    def as_svg(
        self,
        color: Optional[str] = None,
        width: Optional[str] = None,
        height: Optional[str] = None,
        rotate: Optional[str] = None,
        flip: Optional[Union[str, Sequence]] = None,
        box: bool = False,
    ) -> str:
        """Generate a full SVG of this icon.

        Some transformations can be applied by passing arguments:

          width, height - Scale the icon; if only one is set and the other is not
              (or set to 'auto'), the other is calculated, preserving aspect ratio.
              Suffixes (i.e. CSS units) are allowed
          rotate - Either a degress value with 'deg' suffix, or a number from 0 to 4
              expressing the number of 90 degreee rotations
          flip - horizontal, vertical, or both values with comma
          box - Include a transparent box spanning the whole viewbox

        Documentation: https://docs.iconify.design/types/iconify-icon.html
        """
        # Original dimensions, the viewbox we use later
        orig_width, orig_height = self.get_width(), self.get_height()

        if width and (height is None or height.lower() == "auto"):
            # Width given, determine height automatically
            value, unit = split_css_unit(width)
            height = str(value / (orig_width / orig_height)) + unit
        elif height and (width is None or width.lower() == "auto"):
            # Height given, determine width automatically
            value, unit = split_css_unit(height)
            width = str(value / (orig_height / orig_width)) + unit
        elif width is None and height is None:
            # Neither width nor height given, default to browser text size
            width, height = "1em", "1em"
        # Build attributes to inject into <svg> element
        svg_dim_attrs = f'width="{width}" height="{height}"'

        # SVG root element (copied bluntly from example output on api.iconify.design)
        head = (
            '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f"{svg_dim_attrs} "
            'preserveAspectRatio="xMidYMid meet" '
            f'viewBox="0 0 {orig_width} {orig_height}" '
            'style="-ms-transform: rotate(360deg); -webkit-transform: rotate(360deg); transform: rotate(360deg);">'
        )
        foot = "</svg>"

        # Build up all transformations, which are added as an SVG group (<g> element)
        transform = []
        if rotate is not None:
            # Rotation will be around center of viewbox
            center_x, center_y = int(orig_width / 2), int(orig_height / 2)
            if rotate.isnumeric():
                # Plain number, calculate degrees in 90deg steps
                deg = int(rotate) * 90
            elif rotate.endswith("deg"):
                deg = int(rotate[:-3])
            transform.append(f"rotate({deg} {center_x} {center_y})")
        if flip is not None:
            if isinstance(flip, str):
                # Split flip attribute if passed verbatim from request
                flip = flip.split(",")
            # Seed with no-op values
            translate_x, translate_y = 0, 0
            scale_x, scale_y = 1, 1
            if "horizontal" in flip:
                # Flip around X axis
                translate_x = orig_width
                scale_x = -1
            if "vertical" in flip:
                # Flip around Y axis
                translate_y = orig_height
                scale_y = -1
            # Build transform functions for <g> attribute
            transform.append(f"translate({translate_x} {translate_y})")
            transform.append(f"scale({scale_x} {scale_y})")
        if transform:
            # Generate a <g> attribute if any transformations were generated
            transform = " ".join(transform)
            g = f'<g transform="{transform}">', "</g>"
        else:
            # use dummy empty strings to make string building easier further down
            g = "", ""

        # Body from icon data
        body = self.body
        if color is not None:
            # Color is replaced anywhere it appears as attribute value
            # FIXME Find a better way to repalce only color values safely
            body = body.replace('"currentColor"', f'"{color}"')

        if box:
            # Add a transparent box spanning the whole viewbox for browsers that do not support viewbox
            box = f'<rect x="0" y="0" width="{orig_width}" height="{orig_height}" fill="rgba(0, 0, 0, 0)" />'
        else:
            # Dummy empty string for easier string building further down
            box = ""

        # Construct final SVG data
        svg = f"{head}{g[0]}{body}{g[1]}{box}{foot}"
        return svg


class IconifyAlias(IconifyOptional):
    """Alias for an icon.

    Documentation: https://docs.iconify.design/types/iconify-alias.html
    """

    _collection: Optional["IconifyJSON"]
    parent: str

    def get_icon(self):
        """Get the real icon by retrieving it from the parent collection, if any."""
        if self._collection:
            return self._collection.get_icon(self.parent)

    @classmethod
    def from_dict(cls, src: dict, collection: Optional["IconifyJSON"] = None) -> "IconifyAlias":
        self = cls()
        self.parent = src["parent"]
        self._from_dict_optional(src)
        self._collection = collection
        return self

    def as_dict(self) -> dict:
        res = {
            "parent": self.parent,
        }
        res.update(self._as_dict_optional())
        return res


class IconifyInfo(IconifyOptional):
    """Meta information on a colelction.

    No documentation; guessed from the JSON data provided by Iconify.
    """

    name: str
    author: Dict[str, str]  # FIXME turn intoreal object
    license_: Dict[str, str]  # FIXME turn into real object
    samples: Optional[List[IconifyIcon]]
    category: str
    palette: bool

    @property
    def total(self):
        """Determine icon count from parent collection."""
        if self._collection:
            return len(self._collection.icons)

    @classmethod
    def from_dict(cls, src: dict, collection: Optional["IconifyJSON"] = None) -> "IconifyInfo":
        self = cls()
        self.name = src.get("name", None)
        self.category = src.get("category", None)
        self.palette = src.get("palette", None)
        self.author = src.get("author", None)
        self.license_ = src.get("license", None)
        self.samples = [collection.get_icon(name) for name in src.get("samples", [])] or None
        self._from_dict_optional(src)
        self._collection = collection
        return self

    def as_dict(self) -> dict:
        res = {}
        if self.name is not None:
            res["name"] = self.name
        if self.category is not None:
            res["category"] = self.category
        if self.palette is not None:
            res["palette"] = self.palette
        if self.author is not None:
            res["author"] = self.author
        if self.license_ is not None:
            res["license"] = self.license_
        if self.total is not None:
            res["total"] = self.total
        if self.samples is not None:
            res["samples"] = [icon._name for icon in self.samples if icon is not None]
        if self._collection is not None:
            res["uncategorized"] = list(self._collection.icons.keys())
        res.update(self._as_dict_optional())
        return res


class IconifyJSON(IconifyOptional):
    """One collection as a whole.

    Documentation: https://docs.iconify.design/types/iconify-json.html
    """

    prefix: str
    icons: Dict[str, IconifyIcon]
    aliases: Optional[Dict[str, IconifyAlias]]
    info: Optional[IconifyInfo]
    not_found: List[str]

    def get_icon(self, name: str):
        """Get an icon by name.

        First, tries to find a real icon with the name. If none is found, tries
        to resolve the name from aliases.
        """
        if name in self.icons.keys():
            return self.icons[name]
        elif name in self.aliases.keys():
            return self.aliases[name].get_icon()

    @classmethod
    def from_dict(
        cls, collection: Optional[dict] = None, only: Optional[Collection[str]] = None
    ) -> "IconifyJSON":
        """Construct collection from a dictionary (probably from JSON, originally).

        If the only parameter is passed a sequence or set, only icons and aliases with
        these names are loaded (and real icons for aliases).
        """
        if collection is None:
            # Load from a dummy empty collection
            collection = {}
        if only is None:
            # Construct a list of all names from source collection
            only = set(collection["icons"].keys())
            if "aliases" in collection:
                only |= set(collection["aliases"].keys())

        self = cls()

        self.prefix = collection["prefix"]
        self.icons, self.aliases = {}, {}
        self.not_found = []
        for name in only:
            # Try to find a real icon with the name
            icon_dict = collection["icons"].get(name, None)
            if icon_dict:
                self.icons[name] = IconifyIcon.from_dict(name, icon_dict, collection=self)
                continue

            # If we got here, try finding an alias with the name
            alias_dict = collection["aliases"].get(name, None)
            if alias_dict:
                self.aliases[name] = IconifyAlias.from_dict(alias_dict, collection=self)
                # Make sure we also get the real icon to resolve the alias
                self.icons[alias_dict["parent"]] = IconifyIcon.from_dict(
                    alias_dict["parent"], collection["icons"][alias_dict["parent"]], collection=self
                )
                continue

            # If we got here, track the we did not find the icon
            # Undocumented, but the original API server seems to return this field in its
            # response instead of throwing a 404 error or so
            self.not_found.append(name)

        if "info" in collection:
            self.info = IconifyInfo.from_dict(collection["info"], self)

        self._from_dict_optional(collection)

        return self

    @classmethod
    def from_file(cls, src_file: Union[str, TextIO] = None, **kwargs) -> "IconifyJSON":
        """Construct collection by reading a JSON file and calling from_dict."""
        if isinstance(src_file, str):
            with open(src_file, "r") as in_file:
                src = json.load(in_file)
        else:
            src = json.load(src_file)

        return cls.from_dict(src, **kwargs)

    def as_dict(self, include_info: bool = False) -> dict:
        res = {
            "prefix": self.prefix,
            "icons": {name: icon.as_dict() for name, icon in self.icons.items()},
            "aliases": {name: alias.as_dict() for name, alias in self.aliases.items()},
        }
        if self.not_found:
            res["not_found"] = self.not_found
        if self.info and include_info:
            res["info"] = self.info.as_dict()
        res.update(self._as_dict_optional())
        return res
