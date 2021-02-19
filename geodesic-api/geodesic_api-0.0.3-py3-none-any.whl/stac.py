try:
    import arcgis
except ImportError:
    arcgis = None
try:
    import pandas as pd
except ImportError:
    pd = None

try:
    import geopandas as gpd
except ImportError:
    gpd = None

import hashlib
import json

from collections import defaultdict
# from datetime import datetime

from geodesic.client import get_client
from geodesic.raster import Raster
from shapely.geometry import shape
# from shapely.geometry.base import BaseGeometry
from dateutil.parser import parse
from typing import List


class Feature(dict):
    """Feature representation.

    Args:
        obj: Dictionary representation of a feature

    """

    def __init__(self, obj=None):
        if isinstance(obj, dict):
            self.update(obj)

        self._geometry = None

    @property
    def geometry(self):
        if self._geometry is not None:
            return self._geometry

        self._geometry = shape(self["geometry"])
        return self._geometry

    @geometry.setter
    def geometry(self, g):
        if isinstance(g, dict):
            self["geometry"] = g
            return
        try:
            self["geometry"] = g.__geo_interface__
            try:
                self["bbox"] = g.bounds
            except AttributeError:
                try:
                    self["bbox"] = g.extent
                except Exception:
                    pass
            return
        except AttributeError:
            raise ValueError("unknown geometry object")

    def set_property(self, k, v):
        self.properties[k] = v

    @property
    def properties(self):
        props = self.get("properties", {})
        self.properties = props
        return props

    @properties.setter
    def properties(self, v):
        self["properties"] = v

    @property
    def links(self):
        links = self.get("links", [])
        self.links = links
        return links

    @links.setter
    def links(self, v):
        self["links"] = v

    def _repr_svg_(self):
        return self.geometry._repr_svg_()


class FeatureCollection(dict):
    def __init__(self, obj=None, dataset=None, query=None):
        # From GeoJSON
        if isinstance(obj, dict):
            self.update(obj)
        self._gdf = None
        self._sedf = None

        self._is_stac = False
        self.dataset = dataset
        self.query = query
        if self.dataset is not None:
            self._ds_type = self.dataset.type
            self._ds_subtype = self.dataset.subtype

        self._provenance = None

    @property
    def features(self):
        if self._is_stac:
            return [Item(f, dataset=self.dataset) for f in self["features"]]
        else:
            return [Feature(f) for f in self["features"]]

    @property
    def gdf(self):
        if gpd is None:
            raise ValueError("this method requires geopandas (not installed)")
        if self._gdf is not None:
            return self._gdf
        df = pd.DataFrame(self["features"])
        geo = [shape(g) for g in df.geometry]
        self._gdf = gpd.GeoDataFrame(df, geometry=geo, crs="EPSG:4326")
        return self._gdf

    @property
    def sedf(self):
        if pd is None:
            raise ValueError("this method requires pandas (not installed)")
        if self._sedf is not None:
            return self._sedf
        df = pd.DataFrame(self["features"])
        geo = [arcgis.geometry.Geometry.from_shapely(shape(g)) for g in df.geometry]
        df.spatial.set_geometry(geo)
        self._sedf = df
        return self._sedf

    @property
    def __geo_interface__(self):
        return dict(self)

    @property
    def _next_link(self):
        links = self.get("links", [])

        for link in links:
            if link.get("rel", None) == "next":
                return link.get("href")

    def get_all(self):
        features = self.get("features", [])
        self["features"] = features
        client = get_client()
        next_uri = self._next_link
        while next_uri is not None:

            res = client.get(next_uri)
            if len(res["features"]) == 0:
                return

            features.extend(res["features"])
            next_uri = self._next_link

    @property
    def query_hash(self):
        if self.query is None:
            return ""
        st = json.dumps(self.query)
        return hashlib.sha256(st.encode()).hexdigest()

    @property
    def provenance(self):
        """
        Returns the data provenance, if available, for this object.

        Returns:
            provenance - a dictionary representing a json provenance object

        Example:
            >>> provenance = feature_collection.get_provenance()
            >>> provenance
            {
                "query_hash": "234809s7dfsouj9s8j3f9s3j8o4ij2o3ij4",
                "query": {
                    ...
                },
                "provenance":{
                    "landsat-8-l1": [
                        {
                            "pfs:commit": "79swa87f9s8d7f987234jlsdfkljsld"
                            "pfs:path": "LC80120322021032LGN00.json"
                        }, {
                            ...
                        }
                    ],
                    "srtm-gl1": [
                        {
                            ...
                        }
                    ]
                }
            }


        """
        if self._provenance is not None:
            return self._provenance

        prov = defaultdict(list)
        for feature in self.features:
            try:
                pfs = feature.pfs
            except AttributeError:
                continue

            repo = pfs.pop("pfs:repo")
            if repo is None:
                continue

            prov[repo].append(pfs)

        self._provenance = {
            "id": self.query_hash,
            "query": self.query,
            "provenance": prov,
        }
        return self._provenance


class Item(Feature):
    """Class representing a STAC item.

    Implements additional STAC properties on top of a :class:`geodesic.stac.feature`

    Args:
        obj: A python object representing a STAC item.
        dataset: The dataset object this Item belongs to.

    """

    def __init__(self, obj=None, dataset=None):
        super().__init__(obj)
        if dataset is not None:
            self.item_type = dataset.subtype
            self.dataset = dataset

    def _repr_html_(self):
        assets = self.get("assets", {})
        if "thumbnail" in assets:
            href = assets["thumbnail"]["href"]
            width = 500
            if href == "https://seerai.space/images/Logo.svg":
                width = 100

            return f'<img src="{href}" style="width: {width}px;"></img>'
        else:
            try:
                return self._repr_svg_()
            except Exception:
                href = "https://seerai.space/images/Logo.svg"
                width = 100
                return f'<img src="{href}" style="width: {width}px;"></img>'

    @property
    def datetime(self):
        dt = self.properties.get("datetime", None)
        if dt is None:
            return
        try:
            return parse(dt)
        # datetime could be a list
        except TypeError:
            return map(parse, dt)

    @datetime.setter
    def datetime(self, v):
        if isinstance(v, (list, tuple)):
            try:
                self.set_property("datetime", [d.isoformat() for d in v])
            except AttributeError:
                self.set_property("datetime", v)
        else:
            try:
                self.set_property("datetime", v.isoformat())
            except AttributeError:
                self.set_property("datetime", v)

    @property
    def pfs(self):
        """Get information about this item from PFS

        If this item was produced by running in a Pachyderm pipeline, all of the relevant Pachyderm
        info will be stored in here. This allows the provenance of an item to be traced.
        """
        return {
            "pfs:repo": self.properties.get("pfs:repo", None),
            "pfs:commit": self.properties.get("pfs:commit", None),
            "pfs:path": self.properties.get("pfs:path", None),
        }

    def set_pfs(self, repo=None, commit=None, path=None):
        self.set_property("pfs:repo", repo)
        self.set_property("pfs:commit", commit)
        self.set_property("pfs:path", path)

    def set_asset(self, k, a):
        assets = self.assets
        assets[k] = dict(a)

    def get_asset(self, k):
        return self.assets[k]

    @property
    def raster(self):
        if self.item_type != "raster":
            raise ValueError(
                "item must be of raster type, is: '{0}'".format(self.item_type)
            )
        return Raster(self, dataset=self.dataset)

    @property
    def assets(self):
        assets = self.get("assets", {})
        assets = {k: Asset(v) for k, v in assets.items()}
        self.assets = assets
        return assets

    @assets.setter
    def assets(self, assets):
        self["assets"] = assets

    @staticmethod
    def new(dataset=None):
        return Item(
            obj={
                "type": "Feature",
                "id": None,
                "geometry": None,
                "bbox": None,
                "collection": None,
                "stac_extensions": [],
                "properties": {},
                "assets": {},
                "links": [],
            },
            dataset=dataset,
        )

    @property
    def id(self):
        return self["id"]

    @id.setter
    def id(self, id):
        if not isinstance(id, str):
            raise ValueError("id must be a string")
        self["id"] = id

    @property
    def collection(self):
        return self["collection"]

    @collection.setter
    def collection(self, c):
        self["collection"] = c

    @property
    def stac_extensions(self):
        return self["stac_extensions"]

    @stac_extensions.setter
    def stac_extensions(self, e):
        self["stac_extensions"] = e


class Asset(dict):
    @property
    def href(self) -> str:
        return self["href"]

    @href.setter
    def href(self, v):
        self["href"] = v

    @property
    def title(self) -> str:
        return self["title"]

    @title.setter
    def title(self, v):
        self["title"] = v

    @property
    def description(self):
        return self["description"]

    @description.setter
    def description(self, v):
        self["description"] = vars

    @property
    def type(self):
        return self["type"]

    @type.setter
    def type(self, v):
        self["type"] = v

    @property
    def roles(self) -> List[str]:
        roles = self.get("roles", [])
        self["roles"] = roles
        return roles

    @roles.setter
    def roles(self, v):
        self["roles"] = v

    def has_role(self, role: str):
        for r in self.roles:
            if role == r:
                return True
        return False

    @staticmethod
    def new():
        return Asset(
            {
                "href": None,
                "title": None,
                "type": None,
                "description": None,
                "roles": [],
            }
        )
