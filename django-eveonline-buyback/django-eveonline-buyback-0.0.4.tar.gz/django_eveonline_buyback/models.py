# models.py
from django.db import models
from django_eveonline_connector.models import EveEntity
from django_singleton_admin.models import DjangoSingleton


class BuybackSettings(DjangoSingleton):
    ancient_coordinates_database_price = models.FloatField(default=1500000)
    neural_network_analyzer_price = models.FloatField(default=200000)
    sleeper_data_library_price = models.FloatField(default=500000)
    sleeper_drone_ai_nexus_price = models.FloatField(default=5000000)
    blue_loot_buyback_rate = models.FloatField(default=0.9)
    general_buyback_rate = models.FloatField(default=0.85)
    contract_entity = models.ForeignKey(
        EveEntity, null=True, blank=True, on_delete=models.SET_NULL)

    @staticmethod
    def get_instance():
        return BuybackSettings.objects.get_or_create(pk=1)[0]

    def __str__(self):
        return "Buyback Settings"
