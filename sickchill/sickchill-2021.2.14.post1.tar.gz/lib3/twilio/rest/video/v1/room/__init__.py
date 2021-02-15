# coding=utf-8
r"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base import deserialize
from twilio.base import serialize
from twilio.base import values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.page import Page
from twilio.rest.video.v1.room.recording import RoomRecordingList
from twilio.rest.video.v1.room.room_participant import ParticipantList


class RoomList(ListResource):

    def __init__(self, version):
        """
        Initialize the RoomList

        :param Version version: Version that contains the resource

        :returns: twilio.rest.video.v1.room.RoomList
        :rtype: twilio.rest.video.v1.room.RoomList
        """
        super(RoomList, self).__init__(version)

        # Path Solution
        self._solution = {}
        self._uri = '/Rooms'.format(**self._solution)

    def create(self, enable_turn=values.unset, type=values.unset,
               unique_name=values.unset, status_callback=values.unset,
               status_callback_method=values.unset, max_participants=values.unset,
               record_participants_on_connect=values.unset,
               video_codecs=values.unset, media_region=values.unset):
        """
        Create the RoomInstance

        :param bool enable_turn: Enable Twilio's Network Traversal TURN service
        :param RoomInstance.RoomType type: The type of room
        :param unicode unique_name: An application-defined string that uniquely identifies the resource
        :param unicode status_callback: The URL to send status information to your application
        :param unicode status_callback_method: The HTTP method we should use to call status_callback
        :param unicode max_participants: The maximum number of concurrent Participants allowed in the room
        :param bool record_participants_on_connect: Whether to start recording when Participants connect
        :param RoomInstance.VideoCodec video_codecs: An array of the video codecs that are supported when publishing a track in the room
        :param unicode media_region: The region for the media server in Group Rooms

        :returns: The created RoomInstance
        :rtype: twilio.rest.video.v1.room.RoomInstance
        """
        data = values.of({
            'EnableTurn': enable_turn,
            'Type': type,
            'UniqueName': unique_name,
            'StatusCallback': status_callback,
            'StatusCallbackMethod': status_callback_method,
            'MaxParticipants': max_participants,
            'RecordParticipantsOnConnect': record_participants_on_connect,
            'VideoCodecs': serialize.map(video_codecs, lambda e: e),
            'MediaRegion': media_region,
        })

        payload = self._version.create(method='POST', uri=self._uri, data=data, )

        return RoomInstance(self._version, payload, )

    def stream(self, status=values.unset, unique_name=values.unset,
               date_created_after=values.unset, date_created_before=values.unset,
               limit=None, page_size=None):
        """
        Streams RoomInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param RoomInstance.RoomStatus status: Read only the rooms with this status
        :param unicode unique_name: Read only rooms with this unique_name
        :param datetime date_created_after: Read only rooms that started on or after this date, given as YYYY-MM-DD
        :param datetime date_created_before: Read only rooms that started before this date, given as YYYY-MM-DD
        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.video.v1.room.RoomInstance]
        """
        limits = self._version.read_limits(limit, page_size)

        page = self.page(
            status=status,
            unique_name=unique_name,
            date_created_after=date_created_after,
            date_created_before=date_created_before,
            page_size=limits['page_size'],
        )

        return self._version.stream(page, limits['limit'])

    def list(self, status=values.unset, unique_name=values.unset,
             date_created_after=values.unset, date_created_before=values.unset,
             limit=None, page_size=None):
        """
        Lists RoomInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param RoomInstance.RoomStatus status: Read only the rooms with this status
        :param unicode unique_name: Read only rooms with this unique_name
        :param datetime date_created_after: Read only rooms that started on or after this date, given as YYYY-MM-DD
        :param datetime date_created_before: Read only rooms that started before this date, given as YYYY-MM-DD
        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.video.v1.room.RoomInstance]
        """
        return list(self.stream(
            status=status,
            unique_name=unique_name,
            date_created_after=date_created_after,
            date_created_before=date_created_before,
            limit=limit,
            page_size=page_size,
        ))

    def page(self, status=values.unset, unique_name=values.unset,
             date_created_after=values.unset, date_created_before=values.unset,
             page_token=values.unset, page_number=values.unset,
             page_size=values.unset):
        """
        Retrieve a single page of RoomInstance records from the API.
        Request is executed immediately

        :param RoomInstance.RoomStatus status: Read only the rooms with this status
        :param unicode unique_name: Read only rooms with this unique_name
        :param datetime date_created_after: Read only rooms that started on or after this date, given as YYYY-MM-DD
        :param datetime date_created_before: Read only rooms that started before this date, given as YYYY-MM-DD
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50

        :returns: Page of RoomInstance
        :rtype: twilio.rest.video.v1.room.RoomPage
        """
        data = values.of({
            'Status': status,
            'UniqueName': unique_name,
            'DateCreatedAfter': serialize.iso8601_datetime(date_created_after),
            'DateCreatedBefore': serialize.iso8601_datetime(date_created_before),
            'PageToken': page_token,
            'Page': page_number,
            'PageSize': page_size,
        })

        response = self._version.page(method='GET', uri=self._uri, params=data, )

        return RoomPage(self._version, response, self._solution)

    def get_page(self, target_url):
        """
        Retrieve a specific page of RoomInstance records from the API.
        Request is executed immediately

        :param str target_url: API-generated URL for the requested results page

        :returns: Page of RoomInstance
        :rtype: twilio.rest.video.v1.room.RoomPage
        """
        response = self._version.domain.twilio.request(
            'GET',
            target_url,
        )

        return RoomPage(self._version, response, self._solution)

    def get(self, sid):
        """
        Constructs a RoomContext

        :param sid: The SID that identifies the resource to fetch

        :returns: twilio.rest.video.v1.room.RoomContext
        :rtype: twilio.rest.video.v1.room.RoomContext
        """
        return RoomContext(self._version, sid=sid, )

    def __call__(self, sid):
        """
        Constructs a RoomContext

        :param sid: The SID that identifies the resource to fetch

        :returns: twilio.rest.video.v1.room.RoomContext
        :rtype: twilio.rest.video.v1.room.RoomContext
        """
        return RoomContext(self._version, sid=sid, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Video.V1.RoomList>'


class RoomPage(Page):

    def __init__(self, version, response, solution):
        """
        Initialize the RoomPage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API

        :returns: twilio.rest.video.v1.room.RoomPage
        :rtype: twilio.rest.video.v1.room.RoomPage
        """
        super(RoomPage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of RoomInstance

        :param dict payload: Payload response from the API

        :returns: twilio.rest.video.v1.room.RoomInstance
        :rtype: twilio.rest.video.v1.room.RoomInstance
        """
        return RoomInstance(self._version, payload, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Video.V1.RoomPage>'


class RoomContext(InstanceContext):

    def __init__(self, version, sid):
        """
        Initialize the RoomContext

        :param Version version: Version that contains the resource
        :param sid: The SID that identifies the resource to fetch

        :returns: twilio.rest.video.v1.room.RoomContext
        :rtype: twilio.rest.video.v1.room.RoomContext
        """
        super(RoomContext, self).__init__(version)

        # Path Solution
        self._solution = {'sid': sid, }
        self._uri = '/Rooms/{sid}'.format(**self._solution)

        # Dependents
        self._recordings = None
        self._participants = None

    def fetch(self):
        """
        Fetch the RoomInstance

        :returns: The fetched RoomInstance
        :rtype: twilio.rest.video.v1.room.RoomInstance
        """
        payload = self._version.fetch(method='GET', uri=self._uri, )

        return RoomInstance(self._version, payload, sid=self._solution['sid'], )

    def update(self, status):
        """
        Update the RoomInstance

        :param RoomInstance.RoomStatus status: The new status of the resource

        :returns: The updated RoomInstance
        :rtype: twilio.rest.video.v1.room.RoomInstance
        """
        data = values.of({'Status': status, })

        payload = self._version.update(method='POST', uri=self._uri, data=data, )

        return RoomInstance(self._version, payload, sid=self._solution['sid'], )

    @property
    def recordings(self):
        """
        Access the recordings

        :returns: twilio.rest.video.v1.room.recording.RoomRecordingList
        :rtype: twilio.rest.video.v1.room.recording.RoomRecordingList
        """
        if self._recordings is None:
            self._recordings = RoomRecordingList(self._version, room_sid=self._solution['sid'], )
        return self._recordings

    @property
    def participants(self):
        """
        Access the participants

        :returns: twilio.rest.video.v1.room.room_participant.ParticipantList
        :rtype: twilio.rest.video.v1.room.room_participant.ParticipantList
        """
        if self._participants is None:
            self._participants = ParticipantList(self._version, room_sid=self._solution['sid'], )
        return self._participants

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Video.V1.RoomContext {}>'.format(context)


class RoomInstance(InstanceResource):

    class RoomStatus(object):
        IN_PROGRESS = "in-progress"
        COMPLETED = "completed"
        FAILED = "failed"

    class RoomType(object):
        PEER_TO_PEER_BASIC = "peer-to-peer-basic"
        PEER_TO_PEER = "peer-to-peer"
        GROUP = "group"
        GROUP_SMALL = "group-small"

    class VideoCodec(object):
        VP8 = "VP8"
        H264 = "H264"

    def __init__(self, version, payload, sid=None):
        """
        Initialize the RoomInstance

        :returns: twilio.rest.video.v1.room.RoomInstance
        :rtype: twilio.rest.video.v1.room.RoomInstance
        """
        super(RoomInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'sid': payload.get('sid'),
            'status': payload.get('status'),
            'date_created': deserialize.iso8601_datetime(payload.get('date_created')),
            'date_updated': deserialize.iso8601_datetime(payload.get('date_updated')),
            'account_sid': payload.get('account_sid'),
            'enable_turn': payload.get('enable_turn'),
            'unique_name': payload.get('unique_name'),
            'status_callback': payload.get('status_callback'),
            'status_callback_method': payload.get('status_callback_method'),
            'end_time': deserialize.iso8601_datetime(payload.get('end_time')),
            'duration': deserialize.integer(payload.get('duration')),
            'type': payload.get('type'),
            'max_participants': deserialize.integer(payload.get('max_participants')),
            'record_participants_on_connect': payload.get('record_participants_on_connect'),
            'video_codecs': payload.get('video_codecs'),
            'media_region': payload.get('media_region'),
            'url': payload.get('url'),
            'links': payload.get('links'),
        }

        # Context
        self._context = None
        self._solution = {'sid': sid or self._properties['sid'], }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context

        :returns: RoomContext for this RoomInstance
        :rtype: twilio.rest.video.v1.room.RoomContext
        """
        if self._context is None:
            self._context = RoomContext(self._version, sid=self._solution['sid'], )
        return self._context

    @property
    def sid(self):
        """
        :returns: The unique string that identifies the resource
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def status(self):
        """
        :returns: The status of the room
        :rtype: RoomInstance.RoomStatus
        """
        return self._properties['status']

    @property
    def date_created(self):
        """
        :returns: The ISO 8601 date and time in GMT when the resource was created
        :rtype: datetime
        """
        return self._properties['date_created']

    @property
    def date_updated(self):
        """
        :returns: The ISO 8601 date and time in GMT when the resource was last updated
        :rtype: datetime
        """
        return self._properties['date_updated']

    @property
    def account_sid(self):
        """
        :returns: The SID of the Account that created the resource
        :rtype: unicode
        """
        return self._properties['account_sid']

    @property
    def enable_turn(self):
        """
        :returns: Enable Twilio's Network Traversal TURN service
        :rtype: bool
        """
        return self._properties['enable_turn']

    @property
    def unique_name(self):
        """
        :returns: An application-defined string that uniquely identifies the resource
        :rtype: unicode
        """
        return self._properties['unique_name']

    @property
    def status_callback(self):
        """
        :returns: The URL to send status information to your application
        :rtype: unicode
        """
        return self._properties['status_callback']

    @property
    def status_callback_method(self):
        """
        :returns: The HTTP method we use to call status_callback
        :rtype: unicode
        """
        return self._properties['status_callback_method']

    @property
    def end_time(self):
        """
        :returns: The UTC end time of the room in UTC ISO 8601 format
        :rtype: datetime
        """
        return self._properties['end_time']

    @property
    def duration(self):
        """
        :returns: The duration of the room in seconds
        :rtype: unicode
        """
        return self._properties['duration']

    @property
    def type(self):
        """
        :returns: The type of room
        :rtype: RoomInstance.RoomType
        """
        return self._properties['type']

    @property
    def max_participants(self):
        """
        :returns: The maximum number of concurrent Participants allowed in the room
        :rtype: unicode
        """
        return self._properties['max_participants']

    @property
    def record_participants_on_connect(self):
        """
        :returns: Whether to start recording when Participants connect
        :rtype: bool
        """
        return self._properties['record_participants_on_connect']

    @property
    def video_codecs(self):
        """
        :returns: An array of the video codecs that are supported when publishing a track in the room
        :rtype: RoomInstance.VideoCodec
        """
        return self._properties['video_codecs']

    @property
    def media_region(self):
        """
        :returns: The region for the media server in Group Rooms
        :rtype: unicode
        """
        return self._properties['media_region']

    @property
    def url(self):
        """
        :returns: The absolute URL of the resource
        :rtype: unicode
        """
        return self._properties['url']

    @property
    def links(self):
        """
        :returns: The URLs of related resources
        :rtype: unicode
        """
        return self._properties['links']

    def fetch(self):
        """
        Fetch the RoomInstance

        :returns: The fetched RoomInstance
        :rtype: twilio.rest.video.v1.room.RoomInstance
        """
        return self._proxy.fetch()

    def update(self, status):
        """
        Update the RoomInstance

        :param RoomInstance.RoomStatus status: The new status of the resource

        :returns: The updated RoomInstance
        :rtype: twilio.rest.video.v1.room.RoomInstance
        """
        return self._proxy.update(status, )

    @property
    def recordings(self):
        """
        Access the recordings

        :returns: twilio.rest.video.v1.room.recording.RoomRecordingList
        :rtype: twilio.rest.video.v1.room.recording.RoomRecordingList
        """
        return self._proxy.recordings

    @property
    def participants(self):
        """
        Access the participants

        :returns: twilio.rest.video.v1.room.room_participant.ParticipantList
        :rtype: twilio.rest.video.v1.room.room_participant.ParticipantList
        """
        return self._proxy.participants

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Video.V1.RoomInstance {}>'.format(context)
