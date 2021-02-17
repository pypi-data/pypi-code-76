from .MargoBlock import MargoBlock
from ..utils.get_preamble_source import get_preamble_source


class MargoPythonCellPreambleBlock(MargoBlock):
    """A helper to process just the Margo preamble (if any) of a Python cell.
    Instead of using MargoBlock directly, which requires the source string to
    only be valid Margo, this will extract the preamble from the cell contents.
    """

    def __init__(self, source: str):

        """
        :param source: The entire source of a Python cell
        """

        preamble_source = get_preamble_source(source)
        super().__init__(preamble_source)
