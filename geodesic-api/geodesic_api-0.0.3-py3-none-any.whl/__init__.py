__version__ = '0.0.3'

from geodesic.oauth import AuthManager
from geodesic.stac import Item, Feature, FeatureCollection
from geodesic.raster import Raster, RasterCollection
from geodesic.datasets import Dataset, DatasetList

__all__ = [
    "authenticate",
    "Item",
    "Feature",
    "FeatureCollection",
    "Raster",
    "RasterCollection",
    "Dataset",
    "DatasetList",
]


def authenticate():
    auth = AuthManager()
    auth.authenticate()
