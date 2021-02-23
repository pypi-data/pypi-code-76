class TwilioActivity:
    def __init__(self, friendly_name: str, availability: bool, default: bool = False):
        self.__friendly_name = friendly_name
        self.__availability = availability
        self.__default = default

    @property
    def friendly_name(self):
        return self.__friendly_name

    @property
    def availability(self):
        return self.__availability

    @property
    def default(self):
        return self.__default
