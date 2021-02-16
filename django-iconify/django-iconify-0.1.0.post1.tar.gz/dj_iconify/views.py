"""Iconify API endpoints as views.

Documentation: https://docs.iconify.design/sources/api/queries.html
"""
import json
import os
import re

from django.http import Http404, HttpRequest, HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.views.generic import View

from .conf import JSON_ROOT
from .types import IconifyJSON


class BaseJSONView(View):
    """Base view that wraps JSON and JSONP responses.

    It relies on the following query parameters:

      callback - name of the JavaScript callback function to call via JSONP
      pretty - 1 or true to pretty-print JSON (default is condensed)

    The URL route has to pass an argument called format_ containing js or json
    to determine the output format.
    """

    default_callback: str = "Console.log"

    def get_data(self, request: HttpRequest) -> dict:
        """Generate a dictionary contianing the data to return."""
        raise NotImplementedError("You must implement this method in your view.")

    def get(self, request: HttpRequest, format_: str = "json", *args, **kwargs) -> HttpResponse:
        """Get the JSON or JSONP response containing the data from the get_data method."""
        # For JSONP, the callback name has to be passed
        if format_ == "js":
            callback = request.GET.get("callback", self.default_callback)

        # Client can request pretty-printing of JSON
        if request.GET.get("pretty", "0").lower() in ("1", "true"):
            indent = 2
        else:
            indent = None

        # Call main function implemented by children
        data = self.get_data(request, *args, **kwargs)

        # Get result JSON and form response
        res = json.dumps(data, indent=indent, sort_keys=True)
        if format_ == "js":
            # Format is JSONP
            res = f"{callback}({res})"
            return HttpResponse(res, content_type="application/javascript")
        else:
            # Format is plain JSON
            return HttpResponse(res, content_type="application/json")


class ConfigView(View):
    """Get JavaScript snippet to conifugre Iconify for our API.

    This sets the API base URL to the endpoint determined by Django's reverse
    URL mapper.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        # Guess the base URL by reverse-mapping the URL for a fake icon set
        rev = reverse("iconify_json", kwargs={"collection": "prefix", "format_": "js"})
        # Iconify SVG Framework expects placeholders {prefix} and {icons} in API URL
        api_pattern = rev[:-9] + "{prefix}.js?icons={icons}"

        # Put together configuration as dict and output as JSON
        config = {
            "defaultAPI": api_pattern,
        }
        config_json = json.dumps(config)
        return HttpResponse(f"var IconifyConfig = {config_json}", content_type="text/javascript")


class CollectionView(BaseJSONView):
    """Retrieve the meta-data for a single collection."""

    def get_data(self, request: HttpRequest) -> dict:
        # Collection name is passed in the prefix query parameter
        collection = request.GET.get("prefix", None)
        if collection is None or not re.match(r"[A-Za-z0-9-]+", collection):
            return HttpResponseBadRequest("You must provide a valid prefix name.")

        # Load icon set through Iconify types
        collection_file = os.path.join(JSON_ROOT, "json", f"{collection}.json")
        try:
            icon_set = IconifyJSON.from_file(collection_file)
        except FileNotFoundError as exc:
            raise Http404(f"Icon collection {collection} not found") from exc

        # Return the info member, which holds the data we want
        return icon_set.info.as_dict()


class CollectionsView(BaseJSONView):
    """Retrieve the available collections with meta-data."""

    def get_data(self, request: HttpRequest) -> dict:
        # Read the pre-compiled collections list and return it verbatim
        # FIXME Consider using type models to generate from sources
        collections_path = os.path.join(JSON_ROOT, "collections.json")
        with open(collections_path, "r") as collections_file:
            data = json.load(collections_file)
        return data


class IconifyJSONView(BaseJSONView):
    """Serve the Iconify icon data retrieval API."""

    default_callback: str = "SimpleSVG._loaderCallback"

    def get_data(self, request: HttpRequest, collection: str) -> dict:
        # Icon names are passed as comma-separated list
        icons = request.GET.get("icons", None)
        if icons is not None:
            icons = icons.split(",")

        # Load icon set through Iconify types
        collection_file = os.path.join(JSON_ROOT, "json", f"{collection}.json")
        try:
            icon_set = IconifyJSON.from_file(collection_file, only=icons)
        except FileNotFoundError as exc:
            raise Http404(f"Icon collection {collection} not found") from exc

        return icon_set.as_dict()


class IconifySVGView(View):
    """Serve the Iconify SVG retrieval API.

    It serves a single icon as SVG, allowing some transformations.
    """

    def get(self, request: HttpRequest, collection: str, name: str) -> HttpResponse:
        # General retrieval parameters
        download = request.GET.get("download", "0").lower() in ("1", "true")
        box = request.GET.get("box", "0").lower() in ("1", "true")

        # SVG manipulation parameters
        color = request.GET.get("color", None)
        width = request.GET.get("width", None)
        height = request.GET.get("height", None)
        rotate = request.GET.get("rotate", None)
        flip = request.GET.get("flip", None)

        # Load icon set through Iconify types
        collection_file = os.path.join(JSON_ROOT, "json", f"{collection}.json")
        try:
            icon_set = IconifyJSON.from_file(collection_file, only=[name])
        except FileNotFoundError as exc:
            raise Http404(f"Icon collection {collection} not found") from exc

        # Generate SVG from icon
        icon = icon_set.icons[name]
        icon_svg = icon.as_svg(
            color=color, width=width, height=height, rotate=rotate, flip=flip, box=box
        )

        # Form response
        res = HttpResponse(icon_svg, content_type="image/svg+xml")
        if download:
            res["Content-Disposition"] = f"attachment; filename={name}.svg"
        return res
