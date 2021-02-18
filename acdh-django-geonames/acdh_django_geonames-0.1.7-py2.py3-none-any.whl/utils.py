from django.core.exceptions import ObjectDoesNotExist

from acdh_geonames_utils.gn_client import gn_as_object
from acdh_geonames_utils.utils import extract_id
from gn_places.models import GeoNamesPlace


def gn_get_or_create(gn_id):
    clean_gn_id = extract_id(gn_id)
    try:
        item = GeoNamesPlace.objects.get(gn_id=clean_gn_id)
        print('already exists')
        return item
    except ObjectDoesNotExist:
        print('create new object')
        gn_obj = gn_as_object(clean_gn_id)
        item = GeoNamesPlace.objects.create(
            gn_id=gn_obj['geonameid']
        )
        item.gn_name = gn_obj['name']
        item.gn_lat = gn_obj['latitude']
        item.gn_long = gn_obj['longitude']
        item.gn_feature_class = gn_obj['feature class']
        item.gn_feature_code = gn_obj['feature code']
        item.gn_country_code = gn_obj['country code']
        item.save()
    return item
