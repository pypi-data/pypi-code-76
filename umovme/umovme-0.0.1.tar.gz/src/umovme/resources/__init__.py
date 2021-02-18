from .base import ListResource


class PartnerResource(ListResource):

    resource_name = 'serviceLocal'


class AgentResource(ListResource):

    resource_name = 'agent'


class TeamResource(ListResource):

    resource_name = 'team'


class ItineraryResource(ListResource):
    resource_name = 'itinerary'


class ItemResource(ListResource):
    resource_name = 'item'


class ActivityResource(ListResource):
    resource_name = 'activity'


class ScheduleResource(ListResource):
    resource_name = 'schedule'


class MessageResource(ListResource):
    resource_name = 'message'


class ActivityHistoryResource(ListResource):
    resource_name = 'activityHistory'


class ScheduleItemResource(ListResource):
    resource_name = 'scheduleItem'




