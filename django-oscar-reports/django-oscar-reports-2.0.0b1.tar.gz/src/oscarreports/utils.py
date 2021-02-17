from oscar.apps.dashboard.reports import utils
from django.core.exceptions import ImproperlyConfigured


class GeneratorRepository(utils.GeneratorRepository):

    @classmethod
    def register(cls, ReportGeneratorSubclass):
        if ReportGeneratorSubclass in cls.generators:
            raise ImproperlyConfigured('The class %s is already registered' % ReportGeneratorSubclass)
        cls.generators.append(ReportGeneratorSubclass)
