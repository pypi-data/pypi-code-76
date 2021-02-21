
from farmos_ext.farmobj import FarmObj
from farmos_ext.term import Season


class Plan(FarmObj):
    pass


class CropPlan(Plan):

    @property
    def notes(self) -> str:
        return self.attr('notes', str)

    @property
    def season(self) -> Season:
        return self.attr('season', Season)


class GrazingPlan(Plan):

    @property
    def field_days_bulk_feeding(self) -> int:
        return self.attr('field_days_bulk_feeding', int)

    @property
    def field_days_of_drought_reserve(self) -> int:
        return self.attr('field_days_of_drought_reserve', int)

    @property
    def field_expected_rotations(self) -> int:
        return self.attr('field_expected_rotations', int)

    @property
    def grazing_factors(self) -> str:
        return self.attr('grazing_factors', str)

    @property
    def field_grazing_growing_season(self) -> bool:
        return self.attr('field_grazing_growing_season', bool)

    @property
    def date_range(self):
        pass
