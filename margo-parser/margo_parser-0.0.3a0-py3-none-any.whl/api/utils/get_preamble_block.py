from .get_preamble_source import get_preamble_source
from ..classes.MargoBlock import MargoBlock


def get_preamble_block(cell_source: str, cell_type="code") -> MargoBlock:
    return MargoBlock(get_preamble_source(cell_source, cell_type=cell_type))
