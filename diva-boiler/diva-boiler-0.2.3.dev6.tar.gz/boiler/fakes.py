from typing import List

from factory import Factory, Faker, lazy_attribute, SubFactory

from boiler import definitions, models

MAX_FRAME = 30 * 60 * 5


class BoxFactory(Factory):
    class Meta:
        model = models.Box

    left: int = Faker('random_int', min=0, max=1070)
    top: int = Faker('random_int', min=0, max=750)

    @lazy_attribute
    def right(self) -> int:
        return 1080

    @lazy_attribute
    def bottom(self) -> int:
        return 760


class DetectionFactory(Factory):
    class Meta:
        model = models.Detection

    frame: int = Faker('random_int', min=0, max=MAX_FRAME)
    box: models.Box = SubFactory(BoxFactory)
    keyframe: bool = Faker('random_element', elements=[True, False])


class ActorFactory(Factory):
    class Meta:
        model = models.Actor

    actor_id: int = Faker('random_int', min=0, max=10000)
    actor_type: str = Faker('random_element', elements=definitions.ActorType)
    begin: int = Faker('random_int', min=0, max=MAX_FRAME - 10)

    @lazy_attribute
    def end(self) -> int:
        return MAX_FRAME

    @lazy_attribute
    def detections(self) -> List[models.Detection]:
        return [
            DetectionFactory(frame=self.begin, keyframe=True),
            DetectionFactory(frame=self.end, keyframe=True),
        ]


class ActivityFactory(Factory):
    class Meta:
        model = models.Activity

    activity_id: int = Faker('random_int', min=0, max=10000)
    activity_type: definitions.ActivityType = Faker(
        'random_element', elements=definitions.ActivityType
    )
    begin: int = Faker('random_int', min=0, max=MAX_FRAME - 10)

    @lazy_attribute
    def end(self) -> int:
        return MAX_FRAME

    @lazy_attribute
    def actors(self) -> List[models.Actor]:
        return [
            ActorFactory(),
            ActorFactory(),
        ]
