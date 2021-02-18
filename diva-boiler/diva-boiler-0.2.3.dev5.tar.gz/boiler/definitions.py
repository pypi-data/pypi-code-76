import enum
from typing import Type, TypeVar


T = TypeVar('T', bound='StrEnum')


# This is needed to get mypy to validate enum's correctly.  By default,
# enum's have value type Any, which means that it is never validated.
class StrEnum(enum.Enum):
    @property
    def value(self) -> str:
        return super(StrEnum, self).value

    @classmethod
    def from_string(cls: Type[T], value: str) -> T:
        return cls(value.lower())


class ActorType(StrEnum):
    BAG = 'bag'
    BIKE = 'bicycle'
    OTHER = 'other'
    PERSON = 'person'
    QUEUE = 'queue'
    RECEPTACLE = 'receptacle'
    VEHICLE = 'vehicle'

    @classmethod
    def from_string(cls, value: str) -> 'ActorType':
        value = value.lower()
        if value == 'bike':
            value = 'bicycle'
        return cls(value)


actor_codes = {
    ActorType.BAG: 'b',
    ActorType.BIKE: 'k',
    ActorType.OTHER: 'o',
    ActorType.PERSON: 'p',
    ActorType.QUEUE: 'q',
    ActorType.RECEPTACLE: 'o',  # https://gitlab.com/diva-mturk/stumpf-diva/issues/32#note_285508683
    ActorType.VEHICLE: 'v',
}


class CurrentActivityType(StrEnum):
    HAND_INTERACTS_WITH_PERSON = 'hand_interacts_with_person'
    PERSON_ABANDONS_PACKAGE = 'person_abandons_package'
    PERSON_ASCENDS_STAIRS = 'person_ascends_stairs'
    PERSON_CARRIES_HEAVY_OBJECT = 'person_carries_heavy_object'
    PERSON_CLOSES_FACILITY_DOOR = 'person_closes_facility_door'
    PERSON_CLOSES_TRUNK = 'person_closes_trunk'
    PERSON_CLOSES_VEHICLE_DOOR = 'person_closes_vehicle_door'
    PERSON_DESCENDS_STAIRS = 'person_descends_stairs'
    PERSON_DISCARDS_TRASH = 'person_discards_trash'
    PERSON_DOFFS_JACKET = 'person_doffs_jacket'
    PERSON_DONS_JACKET = 'person_dons_jacket'
    PERSON_DRINKS = 'person_drinks'
    PERSON_EMBRACES_PERSON = 'person_embraces_person'
    PERSON_ENTERS_SCENE_THROUGH_STRUCTURE = 'person_enters_scene_through_structure'
    PERSON_ENTERS_VEHICLE = 'person_enters_vehicle'
    PERSON_EXITS_SCENE_THROUGH_STRUCTURE = 'person_exits_scene_through_structure'
    PERSON_EXITS_VEHICLE = 'person_exits_vehicle'
    PERSON_INTERACTS_WITH_LAPTOP = 'person_interacts_with_laptop'
    PERSON_LEADS_ANIMAL = 'person_leads_animal'
    PERSON_LOADS_VEHICLE = 'person_loads_vehicle'
    PERSON_OPENS_FACILITY_DOOR = 'person_opens_facility_door'
    PERSON_OPENS_TRUNK = 'person_opens_trunk'
    PERSON_OPENS_VEHICLE_DOOR = 'person_opens_vehicle_door'
    PERSON_PICKS_UP_OBJECT = 'person_picks_up_object'
    PERSON_PULLS_OBJECT = 'person_pulls_object'
    PERSON_PURCHASES = 'person_purchases'
    PERSON_PUSHES_OBJECT = 'person_pushes_object'
    PERSON_PUTS_DOWN_OBJECT = 'person_puts_down_object'
    PERSON_READS_DOCUMENT = 'person_reads_document'
    PERSON_RIDES_BICYCLE = 'person_rides_bicycle'
    PERSON_RUMMAGES_IN_PARCEL = 'person_rummages_in_parcel'
    PERSON_SITS_DOWN = 'person_sits_down'
    PERSON_STANDS_UP = 'person_stands_up'
    PERSON_STEALS_OBJECT = 'person_steals_object'
    PERSON_TALKS_ON_PHONE = 'person_talks_on_phone'
    PERSON_TALKS_TO_PERSON = 'person_talks_to_person'
    PERSON_TEXTS_ON_PHONE = 'person_texts_on_phone'
    PERSON_TRANSFERS_OBJECT = 'person_transfers_object'
    PERSON_UNLOADS_VEHICLE = 'person_unloads_vehicle'
    VEHICLE_DROPS_OFF_PERSON = 'vehicle_drops_off_person'
    VEHICLE_MAKES_U_TURN = 'vehicle_makes_u_turn'
    VEHICLE_PICKS_UP_PERSON = 'vehicle_picks_up_person'
    VEHICLE_REVERSES = 'vehicle_reverses'
    VEHICLE_STARTS = 'vehicle_starts'
    VEHICLE_STOPS = 'vehicle_stops'
    VEHICLE_TURNS_LEFT = 'vehicle_turns_left'
    VEHICLE_TURNS_RIGHT = 'vehicle_turns_right'


class ActivityType(StrEnum):
    # cannot extend the previous enum class:
    # https://docs.python.org/3/library/enum.html#restricted-enum-subclassing
    HAND_INTERACTS_WITH_PERSON = 'hand_interacts_with_person'
    PERSON_ABANDONS_PACKAGE = 'person_abandons_package'
    PERSON_ASCENDS_STAIRS = 'person_ascends_stairs'
    PERSON_CARRIES_HEAVY_OBJECT = 'person_carries_heavy_object'
    PERSON_CLOSES_FACILITY_DOOR = 'person_closes_facility_door'
    PERSON_CLOSES_TRUNK = 'person_closes_trunk'
    PERSON_CLOSES_VEHICLE_DOOR = 'person_closes_vehicle_door'
    PERSON_DESCENDS_STAIRS = 'person_descends_stairs'
    PERSON_DISCARDS_TRASH = 'person_discards_trash'
    PERSON_DOFFS_JACKET = 'person_doffs_jacket'
    PERSON_DONS_JACKET = 'person_dons_jacket'
    PERSON_DRINKS = 'person_drinks'
    PERSON_EMBRACES_PERSON = 'person_embraces_person'
    PERSON_ENTERS_SCENE_THROUGH_STRUCTURE = 'person_enters_scene_through_structure'
    PERSON_ENTERS_VEHICLE = 'person_enters_vehicle'
    PERSON_EXITS_SCENE_THROUGH_STRUCTURE = 'person_exits_scene_through_structure'
    PERSON_EXITS_VEHICLE = 'person_exits_vehicle'
    PERSON_INTERACTS_WITH_LAPTOP = 'person_interacts_with_laptop'
    PERSON_LEADS_ANIMAL = 'person_leads_animal'
    PERSON_LOADS_VEHICLE = 'person_loads_vehicle'
    PERSON_OPENS_FACILITY_DOOR = 'person_opens_facility_door'
    PERSON_OPENS_TRUNK = 'person_opens_trunk'
    PERSON_OPENS_VEHICLE_DOOR = 'person_opens_vehicle_door'
    PERSON_PICKS_UP_OBJECT = 'person_picks_up_object'
    PERSON_PULLS_OBJECT = 'person_pulls_object'
    PERSON_PURCHASES = 'person_purchases'
    PERSON_PUSHES_OBJECT = 'person_pushes_object'
    PERSON_PUTS_DOWN_OBJECT = 'person_puts_down_object'
    PERSON_READS_DOCUMENT = 'person_reads_document'
    PERSON_RIDES_BICYCLE = 'person_rides_bicycle'
    PERSON_RUMMAGES_IN_PARCEL = 'person_rummages_in_parcel'
    PERSON_SITS_DOWN = 'person_sits_down'
    PERSON_STANDS_UP = 'person_stands_up'
    PERSON_STEALS_OBJECT = 'person_steals_object'
    PERSON_TALKS_ON_PHONE = 'person_talks_on_phone'
    PERSON_TALKS_TO_PERSON = 'person_talks_to_person'
    PERSON_TEXTS_ON_PHONE = 'person_texts_on_phone'
    PERSON_TRANSFERS_OBJECT = 'person_transfers_object'
    PERSON_UNLOADS_VEHICLE = 'person_unloads_vehicle'
    VEHICLE_DROPS_OFF_PERSON = 'vehicle_drops_off_person'
    VEHICLE_MAKES_U_TURN = 'vehicle_makes_u_turn'
    VEHICLE_PICKS_UP_PERSON = 'vehicle_picks_up_person'
    VEHICLE_REVERSES = 'vehicle_reverses'
    VEHICLE_STARTS = 'vehicle_starts'
    VEHICLE_STOPS = 'vehicle_stops'
    VEHICLE_TURNS_LEFT = 'vehicle_turns_left'
    VEHICLE_TURNS_RIGHT = 'vehicle_turns_right'

    # activities used in the past but no longer allowed
    CARRY_IN_HANDS = 'carry_in_hands'
    CARRY_ON_BACK = 'carry_on_back'
    CASING_FACILITY = 'casing_facility'
    JOINING_QUEUE = 'joining_queue'
    VEHICLE_MOVING = 'vehicle_moving'


# activity validations are described as regular expressions
# individual actors are encoded as single characters (mapping below)
# words separated by | must be internally sorted in alphabetical order
# because candidates will be sorted before testing to avoid using regex
# lookaround.
#
# for example:
#   `bop` is a valid spec, but `pob` is not.
#   `(kpv|bo)` is valid because each individual word is sorted.
activity_spec = {
    ActivityType.HAND_INTERACTS_WITH_PERSON: 'p{2,}',
    ActivityType.PERSON_ASCENDS_STAIRS: 'p',
    ActivityType.PERSON_ABANDONS_PACKAGE: '(bp|op)',
    ActivityType.PERSON_CARRIES_HEAVY_OBJECT: '(bp+|o+p+|p{2,})',
    ActivityType.PERSON_CLOSES_FACILITY_DOOR: 'p',
    ActivityType.PERSON_CLOSES_TRUNK: 'p?v',
    ActivityType.PERSON_CLOSES_VEHICLE_DOOR: 'p?v',
    ActivityType.PERSON_DESCENDS_STAIRS: 'p',
    ActivityType.PERSON_DISCARDS_TRASH: 'b*o*p',
    ActivityType.PERSON_DONS_JACKET: 'p',
    ActivityType.PERSON_DOFFS_JACKET: 'p',
    ActivityType.PERSON_DRINKS: 'o*p',
    ActivityType.PERSON_EMBRACES_PERSON: 'p{2,}',
    ActivityType.PERSON_ENTERS_SCENE_THROUGH_STRUCTURE: 'p',
    ActivityType.PERSON_ENTERS_VEHICLE: 'pv',
    ActivityType.PERSON_EXITS_SCENE_THROUGH_STRUCTURE: 'p',
    ActivityType.PERSON_EXITS_VEHICLE: 'pv',
    ActivityType.PERSON_INTERACTS_WITH_LAPTOP: 'p',
    ActivityType.PERSON_LEADS_ANIMAL: 'o*p',
    ActivityType.PERSON_LOADS_VEHICLE: '(o*pv|b*pv)',
    ActivityType.PERSON_OPENS_FACILITY_DOOR: 'p',
    ActivityType.PERSON_OPENS_TRUNK: 'p?v',
    ActivityType.PERSON_OPENS_VEHICLE_DOOR: 'pv',
    ActivityType.PERSON_PICKS_UP_OBJECT: '(bp|op+)',
    ActivityType.PERSON_PULLS_OBJECT: '(bp|op+)',
    ActivityType.PERSON_PUSHES_OBJECT: '(bp|op+)',
    ActivityType.PERSON_PURCHASES: 'p+',
    ActivityType.PERSON_READS_DOCUMENT: 'p',
    ActivityType.PERSON_RIDES_BICYCLE: 'kp',
    ActivityType.PERSON_RUMMAGES_IN_PARCEL: '(op|bp)',
    ActivityType.PERSON_SITS_DOWN: 'p',
    ActivityType.PERSON_STANDS_UP: 'p',
    ActivityType.PERSON_STEALS_OBJECT: '(bo*p|o+p)',
    ActivityType.PERSON_TALKS_ON_PHONE: 'p',
    ActivityType.PERSON_TALKS_TO_PERSON: 'p{2,}',
    ActivityType.PERSON_TEXTS_ON_PHONE: 'p',
    ActivityType.PERSON_TRANSFERS_OBJECT: '(o*p{2}|b*p{2}|o*pv|b*pv)',
    ActivityType.PERSON_UNLOADS_VEHICLE: '(o*pv|b*pv)',
    ActivityType.VEHICLE_DROPS_OFF_PERSON: 'p+v',
    ActivityType.VEHICLE_MAKES_U_TURN: 'v',
    ActivityType.VEHICLE_PICKS_UP_PERSON: 'p+v',
    ActivityType.VEHICLE_REVERSES: 'v',
    ActivityType.VEHICLE_STARTS: 'v',
    ActivityType.VEHICLE_STOPS: 'v',
    ActivityType.VEHICLE_TURNS_LEFT: 'v',
    ActivityType.VEHICLE_TURNS_RIGHT: 'v',
}

all_activity_codes = {
    3: ActivityType.PERSON_STANDS_UP,
    4: ActivityType.PERSON_SITS_DOWN,
    7: ActivityType.PERSON_TALKS_ON_PHONE,
    8: ActivityType.PERSON_READS_DOCUMENT,
    9: ActivityType.PERSON_TEXTS_ON_PHONE,
    10: ActivityType.VEHICLE_STOPS,
    11: ActivityType.VEHICLE_STARTS,
    12: ActivityType.VEHICLE_TURNS_LEFT,
    13: ActivityType.VEHICLE_TURNS_RIGHT,
    14: ActivityType.VEHICLE_MAKES_U_TURN,
    15: ActivityType.PERSON_TRANSFERS_OBJECT,
    16: ActivityType.PERSON_PICKS_UP_OBJECT,
    17: ActivityType.PERSON_PUTS_DOWN_OBJECT,
    18: ActivityType.PERSON_CARRIES_HEAVY_OBJECT,
    19: ActivityType.HAND_INTERACTS_WITH_PERSON,
    20: ActivityType.PERSON_EMBRACES_PERSON,
    21: ActivityType.PERSON_OPENS_FACILITY_DOOR,
    22: ActivityType.PERSON_CLOSES_FACILITY_DOOR,
    23: ActivityType.PERSON_ENTERS_SCENE_THROUGH_STRUCTURE,
    24: ActivityType.PERSON_EXITS_SCENE_THROUGH_STRUCTURE,
    25: ActivityType.PERSON_OPENS_VEHICLE_DOOR,
    26: ActivityType.PERSON_CLOSES_VEHICLE_DOOR,
    27: ActivityType.PERSON_ENTERS_VEHICLE,
    28: ActivityType.PERSON_EXITS_VEHICLE,
    29: ActivityType.PERSON_OPENS_TRUNK,
    30: ActivityType.PERSON_CLOSES_TRUNK,
    31: ActivityType.PERSON_LOADS_VEHICLE,
    32: ActivityType.PERSON_UNLOADS_VEHICLE,
    33: ActivityType.VEHICLE_PICKS_UP_PERSON,
    34: ActivityType.VEHICLE_DROPS_OFF_PERSON,
    35: ActivityType.PERSON_TALKS_TO_PERSON,
    37: ActivityType.PERSON_RIDES_BICYCLE,
    38: ActivityType.PERSON_PURCHASES,
    39: ActivityType.PERSON_INTERACTS_WITH_LAPTOP,
    40: ActivityType.PERSON_ABANDONS_PACKAGE,
    42: ActivityType.PERSON_LEADS_ANIMAL,
    43: ActivityType.PERSON_STEALS_OBJECT,
    44: ActivityType.VEHICLE_REVERSES,
    45: ActivityType.PERSON_ASCENDS_STAIRS,
    46: ActivityType.PERSON_DESCENDS_STAIRS,
    47: ActivityType.PERSON_PUSHES_OBJECT,
    48: ActivityType.PERSON_PULLS_OBJECT,
    49: ActivityType.PERSON_DONS_JACKET,
    50: ActivityType.PERSON_DOFFS_JACKET,
    51: ActivityType.PERSON_RUMMAGES_IN_PARCEL,
    52: ActivityType.PERSON_DISCARDS_TRASH,
    53: ActivityType.PERSON_DRINKS,
}


class ActivityPipelineStatuses(StrEnum):
    UNAUDITED = 'unaudited'
    AUDITED = 'audited'
    GLADIATOR_1 = 'gladiator_1'
    REFINER_1 = 'refiner_1'
    GLADIATOR_2 = 'gladiator_2'
    REFINER_2 = 'refiner_2'
    GLADIATOR_3 = 'gladiator_3'
    JANITOR = 'janitor'
    NOT_GOOD = 'not_good'
    GOOD = 'good'


class AnnotationVendors(StrEnum):
    IMERIT = 'imerit'
    KITWARE = 'kitware'


class CameraLocation(StrEnum):
    ADMIN = 'admin'
    BUS = 'bus'
    SCHOOL = 'school'
    HOSPITAL = 'hospital'


class DataCollects(StrEnum):
    M1 = 'm1'
    M2 = 'm2'


class ReleaseBatches(StrEnum):
    SEQUESTERED = 'sequestered'
    MEVA = 'meva'
    TESTING = 'testing'
    PUBLIC = 'public'


class CameraTypes(StrEnum):
    VISIBLE = 'eo'
    INFRARED = 'ir'


class VideoPipelineStatuses(StrEnum):
    ANNOTATION = 'annotation'
    AUDIT = 'audit'
    GUNRUNNER = 'gunrunner'


class Scenarios(StrEnum):
    BASKETBALL = 'basketball'
    CONFERENCE = 'conference'
    CONTROL = 'control'
    DEBATE_TEAM = 'debate team'
    DENSE_SUBWAY = 'dense subway'
    FOOTRACE = 'footrace'
    PANEL_DEBATE = 'panel debate'
    POLITICAL_DEBATE = 'political debate'
    POLITICAL_RALLY = 'political rally'
    THREAT = 'threat'
    TRAVEL = 'travel'
