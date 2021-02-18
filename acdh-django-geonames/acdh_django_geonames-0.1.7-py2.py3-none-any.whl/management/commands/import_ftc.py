from django.core.management.base import BaseCommand

from acdh_geonames_utils.acdh_geonames_utils import feature_codes_df

from gn_places.import_utils import import_feature_codes


class Command(BaseCommand):
    help = "Import geonames feature codes as SkosConcepts"

    def add_arguments(self, parser):
        parser.add_argument(
            '--lang',
            default="en",
            help="The language code of the features"
        )

    def handle(self, *args, **kwargs):
        lang = kwargs.get('lang', )
        df = feature_codes_df(lang=lang)
        import_feature_codes(df)
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully imported {len(df)} concepts')
        )
