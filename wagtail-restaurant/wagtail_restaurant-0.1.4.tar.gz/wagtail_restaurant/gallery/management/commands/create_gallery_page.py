from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType

from apps.home.models import HomePage
from ...models import GalleryPage

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            home_page = HomePage.objects.first()
            gallery_content_type = ContentType.objects.get_for_model(GalleryPage)
            
            gallery_page= GalleryPage(  title="GALERIE",
                                        draft_title="GALERIE",
                                        slug='galerie',
                                        content_type=gallery_content_type,
                                        show_in_menus=True,
                                     )

            home_page.add_child(instance=gallery_page)
            # self.stdout.write(self.style.SUCCESS(gallery_content_type.app_label))
        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))
            return
        self.stdout.write(self.style.SUCCESS('  ✓  ') + 'Successfully Gallery Page created')
        return