from textwrap import wrap

__name__ = "PrettyTextTestRunner.textTable"
__module__ = "PrettyTextTestRunner"
__author__ = "Rob MacKinnon <rome@villagertechnolgies.com>"
__license__ = "MIT"

class TextTable(object):
    """ @abstract Easily build a text formated table
        @parmas props [dict] Table descriptor dict
        @example Table Descriptor
            {
                "titles": ["column title", ... ],
                "colWidths": [x, ... ],  # In characters
                "colJustify": ["right"|"center"|"left", ... ],
                "padding": 1,  # In characters
                "indent": 5,   # Indent entire text block by `x` characters
                "margins": {"top":0, "bottom": 0, "left": 0, "right": 0},
                "border": "solid"|"columnDelimit"
            }
    """

    def __init__(self, props: dict= {}):
        _emptyMargins = {
            "top": 0,
            "left": 0,
            "right": 0,
            "bottom": 0
        }
        _defaultJustify = "center"
        _defaultBorder = "solid"

        if "colWidths" not in props:
            raise KeyError("`colWidths` key is required for table description.")

        if "titles" in props:
            self.columnTitles = props["titles"]
        else:
            self.columnTitles = [""] * len(props["colWidths"])

        if "colJustify" in props:
            self.columnJustify = props["colJustify"]
        else:
            self.columnJustify = [_defaultJustify] * len(props["colWidths"])

        self.columnWidths = props["colWidths"]
        self.padding = props["padding"] if "padding" in props else 0
        self.margins = props["margins"] if "margins" in props else _emptyMargins
        self.indent = props["indent"] if "indent" in props else 0
        self.border = props["border"] if "border" in props else _defaultBorder
        self.__heading__ = []
        self.__table__ = []

    @property
    def hr(self):
        """ @abstract Add a horizontal rule across table."""
        if self.border == "solid":
            return " " * self.indent + "-" * (sum(self.columnWidths) + len(self.columnWidths) + 1)
        elif self.border == "columnDelimit":
            return " " * self.indent + " " + " ".join(["-"*_ for _ in self.columnWidths])
        return " " * self.indent

    def __generateCell(self, colIdx: int=0, content: str="",
                       single: bool=False) -> list:
        """ @abstract Format content for table cell.
            @params colIdx [int] Column index.
            @params content [str] Text for cell, can be multi-lined.
            @params single [bool] #Optional flag to denote text is a single line.
            @returns [list] of formatted strings
        """
        _lines = []
        _contentwidth = self.columnWidths[colIdx] - (2 * self.padding) 
        if self.margins["top"] > 0 and not header:
            _lines.extend(["" for _ in range(0, self.margins["top"])])

        try:
            if len(content) > 0:
                _lines.extend(wrap(content, _contentwidth))
        except TypeError:
            return _lines

        if self.margins["bottom"] > 0  and not single:
            _lines.extend(["" for _ in range(0, self.margins["bottom"])])

        if len(_lines) > 0:
            #Adjust column width to largest line value
            try:
                _maxWidth = max([len(_val) for _val in _lines])
            except ValueError:
                return _lines

            if _maxWidth > _contentwidth:
                self.columnWidths[colIdx] += _maxWidth - self.columnWidths[colIdx]

        return _lines

    def appendRow(self, cells: list=[], single: bool=False):
        """ @abstract Append a row of cells to the table.
            @params cells [list] List of cell content.
        """
        _row = []
        _row.extend([self.__generateCell(_idx, _val, single) for _idx, _val in enumerate(cells)])
        self.__table__.append(_row)

    def generateRow(self, columns: list=None) -> list:
        """ @abstract Create a formated table cell from formatted cells
            @params columns [list] Formated column content
            @returns [list] List of complete formatted rows
        """
        _lines = []
        # compute maximum line length
        _maxLen = max(*[len(_) for _ in columns])

        _border = "|" if self.border == "solid" else " "

        # pad other columns to max length
        for _rowIdx in range(0, _maxLen):
            _line = " " * self.indent
            for _colIdx in range(0, len(columns)):
                _col = columns[_colIdx]
                _justify = self.columnJustify[_colIdx]
                _colWidth = self.columnWidths[_colIdx]
                _maxContWidth = _colWidth - (2*self.padding)

                if _rowIdx < len(_col):
                    _content = _col[_rowIdx].lstrip(" ")
                else:
                    _content = " " * _maxContWidth

                _padLeft = 0
                _padRidge = 0
                if _justify == "center":
                    _padLeft = ((_maxContWidth - len(_content)) // 2) + self.padding
                    _padRight = _padLeft

                elif _justify == "left":
                    _padLeft = self.padding
                    _padRight = _maxContWidth - len(_content) + self.padding

                elif _justify == "right":
                    _padRight = self.padding
                    _padLeft = _maxContWidth - len(_content) + self.padding
                else:
                    _padLeft = 0
                    _padRidge = 0

                _content = " " * _padLeft + _content + " " * _padRight

                # import pdb; pdb.set_trace()  # breakpoint 4e0ee8d8 //
                if len(_content) < _colWidth:
                    _content += " "*(_colWidth - len(_content))
                _line += _border + _content
            _line += _border
            _lines.append(_line)
        return _lines

    def generateHeader(self) -> list:
        """ @abstract Generate the table header row """
        _header = [self.__generateCell(_idx, _val, True) for _idx, _val in enumerate(self.columnTitles)]
        return self.generateRow(_header)

    def drawHeader(self):
        """ @abstract Generate and draw the table header row """
        _header = [self.__generateCell(_idx, _val) for _idx, _val in enumerate(self.columnTitles)]
        print("\n".join(self.generateHeader()))

    def generateBody(self) -> list:
        """ @abstract Generate the table body
            @returns [list] Rows of string
        """
        _body = []
        for _r in self.__table__:
            _body.extend(self.generateRow(_r))
        return _body

    def drawBody(self):
        """ @abstract Generate and draw the table body """
        print("\n".join(self.generateBody()))

    def generateHR(self) -> list:
        """ @abstract Generate table horizontal break
            @returns [list] Rows of string
        """
        return [self.hr]

    # def drawFooter(self):
    # """ @abstract Generate and draw the table footer """
    #     print("".join(self.generateFooter()))

    def generate(self) -> list:
        """ @abstract Generate the entire table
            @returns [list] Rows of string
        """
        _output = []
        if self.border == "solid":
            _output.extend(self.generateHR())
        _output.extend(self.generateHeader())
        _output.extend(self.generateHR())
        _output.extend(self.generateBody())
        if self.border == "solid":
            _output.extend(self.generateHR())
        return _output

    def draw(self):
        """ @abstract Generate and draw the entire table """
        print("\n".join(self.generate()))
