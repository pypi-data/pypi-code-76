import math
import json
from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder

from tqdm import tqdm
from acdh_geonames_utils.acdh_geonames_utils import download_to_df
from gn_places.config import field_mapping
from gn_places.models import GeoNamesPlace


class Command(BaseCommand):
    help = "Import Places from geonames.org by country_code"

    def add_arguments(self, parser):
        parser.add_argument(
            '--country_code',
            default="AL",
            help="The country code of the places to import"
        )

    def handle(self, *args, **kwargs):
        country_code = kwargs.get('country_code', )
        df = download_to_df(country_code=country_code)
        fm = field_mapping(GeoNamesPlace)
        for i, row in tqdm(df.iterrows(), total=len(df)):
            pl, _ = GeoNamesPlace.objects.get_or_create(gn_id=row['geonameid'])
            row_data = f"{json.dumps(row.to_dict(), cls=DjangoJSONEncoder)}"
            pl.orig_data_csv = row_data
            for key, value in fm.items():
                if 'related' not in f"{value['field_type']}":
                    object_value = row[key]
                    if isinstance(object_value, (int, float)):
                        if not math.isnan(object_value):
                            setattr(pl, value['field_name'], row[key])
                    else:
                        setattr(pl, value['field_name'], row[key])
            pl.save()
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully imported {len(df)} places')
        )
