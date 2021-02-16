import enum


class BaseEnum(enum.Enum):
    def __str__(self):
        return str(self.value)

    @classmethod
    def to_list(cls) -> list:
        return [*map(str, cls)]


class ColorsNormal(BaseEnum):
    """
    Colours with name references for the values
    Colours from: https://e360-bootstrap-styleguide-staging.internal.imsglobal.com/docs/1.7-beta/utilities/colors/#data-visualization-colors
    """
    PURPLE = "#9e54b0"
    BLUE = "#005ff1"
    ORANGE = "#ff9300"
    RED = "#df216d"
    GREEN = "#00c221"
    NAVY = "#10558a"
