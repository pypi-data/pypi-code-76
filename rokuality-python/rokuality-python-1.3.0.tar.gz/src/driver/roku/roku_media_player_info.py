
class RokuMediaPlayerInfo():

    speed = None
    runtime = None
    container = None
    captions = None
    video = None
    audio = None
    drm = None
    video_res = None
    position = None
    segment_type = None
    media_sequence = None
    time = None
    bitrate = None
    state = None
    error = None
    duration = None
    live = None
    target = None
    max = None
    current = None

    def __init__(self, json):
        value_obj = json['value']
        new_stream_obj = value_obj['NewStream']
        format_obj = value_obj['Format']
        stream_segment_obj = value_obj['StreamSegment']
        buffering_obj = value_obj['Buffering']

        self.speed = new_stream_obj['Speed']
        self.runtime = value_obj['Runtime']
        self.container = format_obj['Container']
        self.captions = format_obj['Captions']
        self.video = format_obj['Video']
        self. audio = format_obj['Audio']
        self.drm = format_obj['Drm']
        self.video_res = format_obj['VideoRes']
        self.position = value_obj['Position']
        self.segment_type = stream_segment_obj['SegmentType']
        self.media_sequence = stream_segment_obj['MediaSequence']
        self.time = stream_segment_obj['Time']
        self.bitrate = stream_segment_obj['Bitrate']
        self.state = value_obj['State']
        self.error = value_obj['Error']
        self.duration = value_obj['Duration']
        self.live = value_obj['IsLive']
        self.target = buffering_obj['Target']
        self.max = buffering_obj['Max']
        self.current = buffering_obj['Current']

    def get_speed(self):
        return self.speed

    def get_runtime(self):
        return self.runtime

    def get_container(self):
        return self.container

    def get_captions(self):
        return self.captions

    def get_video(self):
        return self.video

    def get_audio(self):
        return self.audio

    def get_drm(self):
        return self.drm

    def get_video_resolution(self):
        return self.vide_res

    def get_position(self):
        return self.position

    def get_segment_type(self):
        return self.segment_type

    def get_media_sequence(self):
        return self.media_sequence

    def get_time(self):
        return self.time

    def get_bitrate(self):
        return self.bitrate

    def get_state(self):
        return self.state

    def is_error(self):
        return self.__parse_boolean(self.error)

    def get_duration(self):
        return self.duration

    def is_live(self):
        return self.__parse_boolean(self.live)

    def get_target(self):
        return self.target

    def get_max(self):
        return self.max

    def get_current(self):
        return self.current

    def __parse_boolean(self, value):
        return value == 'true'
