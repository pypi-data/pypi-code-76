# -*- coding: utf-8 -*-
from .api import APIClient
from .resources import (
    AgentResource,
    PartnerResource,
    TeamResource,
    ItineraryResource,
    ItemResource,
    ActivityResource,
    ActivityHistoryResource,
    ScheduleResource,
    ScheduleItemResource,
    MessageResource,
)


class UmovmeCenter(object):

    def __init__(self, api_key):
        self._http_client = APIClient(api_key)
        self.partner = PartnerResource(self._http_client)
        self.agent = AgentResource(self._http_client)
        self.team = TeamResource(self._http_client)
        self.itinerary = ItineraryResource(self._http_client)
        self.item = ItemResource(self._http_client)
        self.activity = ActivityResource(self._http_client)
        self.activity_history = ActivityHistoryResource(self._http_client)
        self.schedule = ScheduleResource(self._http_client)
        self.schedule_item = ScheduleItemResource(self._http_client)
        self.message = MessageResource(self._http_client)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __contains__(self, key):
        return key in self.__dict__

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)

