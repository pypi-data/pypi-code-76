from browser import document, html


class TableWidget:

    __style = """
        div.table-body {
            width: 500px;
            height: 200px;
            overflow-y: scroll;
            display: block;
            border-bottom: 2px solid #00cccc;
            font-size: inherit;
        }

        div.table-body table {
            width: 100%;
            height: 100%;
            border-collapse: collapse;
            width: 100%;
            font-size: 1em;
        }

        div.table-body table tr:nth-child(odd) { background: #f4f4f4; }

        div.table-body table tbody tr:hover { background: #ddd; }

        div.table-body td {
            height: 20px; 
            text-align: center;
            padding: 0 0 0 0;
        }

        div.table-header { height: 30px; }
        
        div.table-header table { overflow: scroll; height: inherit; border: none;}
        
        div.table-header table th {
            cursor: pointer;
            background: #00cccc;
            color: #fff;
            height: inherit;
        }

        div.table-header table th div {
            display: inline-flex;
            flex-direction: row;
        }
        .up { 
            position:absolute;
            top:0px;
            left:0px
        }
        
        .down { 
            position:absolute;
            top:10px;
            left:0px
        }
        div.table-header {
            width: 500px;
            height: 30px;
            /* overflow-y: scroll; */
            display: block;
        }

        div.table-header table {
            width: 100%;
            height: 100%;
            border: 1px solid #ccc;
            border-collapse: collapse;
        }

        div.table-footer {
            width: 500px;
            height: 30px;
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            background: #00cccc;
            color: #fff;
        }
        div.table-footer-left div.table-footer-right {
            width: 50px;
        }        
        div.table-footer-center {
            width: 250px;
            display: flex;
            flex-direction: row;
            justify-content: space-between;
        }
        div.table-footer-center span {
            font-size: 12px;
            display: table-cell;
            vertical-align: middle;
          }
    """

    def __init__(self, table_id,  parent_id, **kwargs):
        """Creates a new table

        :param table_id: ID of a *<TABLE>* html  element
        :param parent_id: ID of the outer HTML element this table should be inserted
        :param kwargs: see below

        :Keyword Arguments:
            * *columns* (``list(dict)``) --
              provides a list of dictionaries that defines columns of this table. Each dictionary defines a single
                  column and must provide at least the two keys: ``title`` and ``field_id``
            * *data* (``list(list)``) --
              provides rows of data to be shown in the table; any ``data[i]`` element should be a list holding
              a row  of data for this table
            * *width* (``int``) --
              table width - in pixels (300 pixels by default)
            * *height* (``int``) --
              height of the full table, including its header - in pixels (500 pixels by default)
            * *header_height* (``int``) --
              height of the table  header - in pixels
            * *rows_per_page* (``int``) --
              the number of rows to be shown on a single page in that table (100 by default)
            * *cell_callback* (``function``) --
              callback routine called when a table cell is clicked. This method will replace the default behavior
              which is selecting table's rows by click / shift-click
            * *highlight_color* (``string``) --
              color that will be used to mark rows of this table as selected
        """
        self.__table_id = table_id
        self.__parent_id = parent_id
        self.__columns = kwargs.get("columns", [])
        self.__sort_inverse = {}
        self.__data = kwargs.get("data", [])
        self.__cell_callback = kwargs.get("cell_callback", [self.__select_table_row])
        self.__sort_callback = [self.__sort_by_column]
        self.__page_callback = [self.__go_to_page]
        self.__rows_per_page = kwargs.get("rows_per_page", 100)
        self.__current_page = 0
        self.__selected_rows = []
        self.__highlight_color = kwargs.get("highlight_color", "lightgrey")
        self.__table_width = document[parent_id].clientWidth

        document <= html.STYLE(TableWidget.__style)
        document <= html.LINK(rel="stylesheet",
                              href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css")

        hh = kwargs.get("header_height", 30)
        wh = kwargs.get("width", 500)

        # ---------- Create a table that holds the header (only)
        header_div = html.DIV(id=table_id+"-div-header", Class="table-header",
                              style={"height": "%dpx" % hh, "width": "%dpx" % wh})
        header_tbl = html.TABLE(id=table_id+"-header")
        header_div <= header_tbl
        self.__thead = html.THEAD(id=self.__table_id + "-THEAD")
        header_tbl <= self.__thead

        # ---------- Create the actual table that holds data
        dh = kwargs.get("height", 500) - hh
        body_div = html.DIV(id=table_id+"-div-table", Class="table-body",
                            style={"height": "%dpx" % dh, "width": "%dpx" % wh})
        body_tbl = html.TABLE(id=table_id+"-body")
        body_div <= body_tbl
        self.__tbody = html.TBODY(id=self.__table_id + "-TBODY")
        body_tbl <= self.__tbody

        # ---------- Create a DIV to hold navigation footer
        footer_div = html.DIV(id=table_id+"-div-footer", Class="table-footer",
                              style={"height": "%dpx" % hh, "width": "%dpx" % wh})
        footer_div <= html.DIV(id=table_id+"-div-footer-left", Class="table-footer-left",
                               style={"padding-left":"10px"})
        footer_cntr = html.DIV(id=table_id + "-div-footer-center", Class="table-footer-center")
        footer_cntr <= html.SPAN(id=table_id+"fast-backward", Class="fa fa-fast-backward")
        footer_cntr <= html.SPAN(id=table_id+"backward",Class="fa fa-backward")
        footer_cntr <= html.SPAN( "page")
        footer_cntr <= html.INPUT(id=table_id + "-div-footer-input", type="text", size="4", maxlength="7", value="1")
        footer_cntr <= html.SPAN("of", id=table_id + "-div-footer-counter")

        footer_cntr <= html.SPAN(id=table_id+"forward", Class="fa fa-forward")
        footer_cntr <= html.SPAN(id=table_id+"fast-forward", Class="fa fa-fast-forward")
        footer_div <= footer_cntr
        footer_div <= html.DIV(id=table_id + "-div-footer-right", Class="table-footer-right",
                               style={"padding-right":"10px"})

        # ---------- Pack the DIVs into the component
        document[parent_id] <= header_div
        document[parent_id] <= body_div
        document[parent_id] <= footer_div

        # ---------- Bind events
        document[table_id + "-div-table"].bind("scroll", self.__scroll_table)

        document[table_id + "forward"].bind("click", self.__dispatch_page_event)
        document[table_id + "backward"].bind("click", self.__dispatch_page_event)
        document[table_id + "fast-forward"].bind("click", self.__dispatch_page_event)
        document[table_id + "fast-backward"].bind("click", self.__dispatch_page_event)

        if len(self.__columns) > 0:
            self.__create_header()
            self.__create_table_rows()

        if len(self.__data) > 0:
            self.__current_page = 1
            self.show_table(1)
            document[table_id + "-div-footer-counter"].innerHTML = "of %d" % self.count_pages()

    @property
    def current_page(self):
        """ Provides index of the page of data that is currently displayed by this table browser

        :return: page index from 1 to ``self.count_pages()``, inclusive
        """
        return self.__current_page

    @property
    def rows_per_page(self):
        """ says how many rows are displayed in this table

        :return: number of rows displayed by this table on the screen
        """
        return self.__rows_per_page

    def add_column(self, **kwargs):
        """ Adds a new column to this table

        :param kwargs: dictionary of properties for that column, see below

        :Keyword Arguments:
            * *title* (``string``) --
              text displayed in the header of this column
            * *field_id* (``string``) --
              ID string for that  column
            * *format* (``string``) --
              formatting string for that column, that will be used to convert variable into a string
            * *width* (``string``) --
              CSS string to define the width of this column. Can be like ``"100px"`` or ``"20%"``
            * *sorter* (``string``) --
              method used to sort this column, use one of the following: ``"string"``, ``"int"`` or ``"float"``;
              use ``"None"`` to prohibit sorting by this column

        :return: None
        """
        if TableWidget.__check_column(kwargs):
            self.__columns.append(kwargs)

    def add_data_rows(self, data_rows):
        """ Add data rows to this table.
        This method doesn't add table rows - the newly added data will not be visible until ``show_table()`` is called

        :param data_rows: data row (``list``) or data rows (``list[list]``) to be added
        :return: None
        """

        if not isinstance(data_rows[0], list):
            data_rows = [data_rows]

        for data_row in data_rows:
            if len(data_row) >= len(self.__columns):
                self.__data.append(data_row)
            else:
                print("Too few data elements in a table row:", data_row)
                return False

        document[self.__table_id + "-div-footer-counter"].innerHTML = "of %d" % self.count_pages()

    def clear_data(self):
        """Clears all data of this table.

        All data entries will be removed both from internal data structure and from the HTML table.
        New content may be added with ``add_data_rows()`` method

        :return: None
        """
        self.__tbody.clear()
        self.__data = []

    @property
    def data(self):
        """Returns original data that that is displayed by this table.
        If this table was sorted by a user, the returned data is in the new order

        :return: original data displayed by this table
        """
        return self.__data

    def replace_data(self, new_data):
        """replaces the data presented by this table with new content; the current data will be lost

        :param new_data: (``list(list)``)  rows of data to be shown in the table; number of data columns should match
            with the number of columns of this table
        :return: None
        """
        self.__data = new_data
        document[self.__table_id + "-div-footer-counter"].innerHTML = "of %d" % self.count_pages()

    def get_column_data(self, which_column, which_page=1):
        """Returns data from a column of this table

        :param which_column: (``string`` or ``int``) points to a column of this table: either its name or index from 0
        :param which_page: index that *counts from 1* which points to a table page; use ``which_page=0``
            to get the whole column (from all pages)
        :return: ``list`` of data from a requested column
        """
        out = []
        if isinstance(which_column, str):
            i_col = 0
            for column in self.__columns:
                if which_column.find(column.get("field_id")) >= 0:
                    which_column = i_col
                    break
                i_col += 1
        if which_page == 0:
            row_from = 0
            row_to = len(self.__data)
        else:
            row_from = (which_page - 1) * self.__rows_per_page
            row_to = min(which_page * self.__rows_per_page, len(self.__data))
        for i in range(row_from, row_to):
            out.append(self.__data[i][which_column])

        return out

    def show_table(self, which_page):
        """Loads a requested page of data into this table

        :param which_page: index of a page (counting from 1) to be displayed by this table
        :return: None
        """
        row_from = (which_page - 1) * self.__rows_per_page
        row_to = min(which_page * self.__rows_per_page, len(self.__data))
        document[self.__table_id + "-div-footer-left"].innerHTML = "%d rows" % len(self.__data)
        document[self.__table_id + "-div-footer-right"].innerHTML = "showing rows from %d to %s" % (row_from+1, row_to)
        document[self.__table_id + "-div-footer-input"].value = which_page
        current_row_id = (self.__current_page - 1) * self.__rows_per_page
        for i in range(row_from, row_to):
            current_id = self.__table_id + "-TR-%d" % current_row_id
            j = 0
            for td in document[current_id].children:
                column = self.__columns[j]
                data = self.__data[i][j]
                td.innerHTML = column["format"] % data if "format" in column and not isinstance(data, str) else data
                td.id = "%s-TD-%d-%d" % (self.__table_id, i, j)
                j += 1
            if i in self.__selected_rows:
                document[current_id].style.background = self.__highlight_color
            else:
                document[current_id].style.background = ''
            document[current_id].id = self.__table_id + "-TR-%d" % i
            current_row_id += 1
        for i in range(row_to-row_from, self.__rows_per_page):
            current_id = self.__table_id + "-TR-%d" % current_row_id
            for td in document[current_id].children: td.innerHTML = ""
            document[current_id].style.background = ''              # --- unselect empty rows even if they are selected
            document[current_id].id = self.__table_id + "-TR-%d" % (i+row_from)
            current_row_id += 1
        self.__current_page = which_page

    def select_row(self, which_row, if_select=True):
        """ Selects (or un-selects) a given row of this table

        :param which_row: index of *data row* to be selected. *Note* that ``which_row`` must not be a table row index
        :param if_select: if ``True`` (the default), the given row will be selected,
            if ``False``, the row will be un-selected by this call
        :return: the resulting state of  ``which_row`` row of data: ``True`` when selected, ``False`` otherwise.
        *Note* that the returned value doesn't tell if this call was successful. E.g. when an attempt was made to select
            an already selected row, it returns ``True`` (the row is selected) even though the call didn't change it's state
        """
        row_id = self.__table_id + "-TR-%d" % which_row
        if which_row in self.__selected_rows:
            if not if_select:
                self.__selected_rows.remove(which_row)
                document[row_id].style.background = ''
                return False
            else:
                document[row_id].style.background = self.__highlight_color
                return True
        else:
            if if_select:
                self.__selected_rows.append(which_row)
                row_from = (self.current_page - 1) * self.__rows_per_page
                row_to = min(self.current_page * self.__rows_per_page, len(self.__data))
                if which_row >= row_from and which_row < row_to:
                    self.show_table(self.current_page)
                document[row_id].style.background = self.__highlight_color
                return True
            else:
                document[row_id].style.background = ''
                return False

    @property
    def selected_rows(self):
        """Provides a list indexes that point to all data rows that are selected"""
        return self.__selected_rows

    def unselect_all_rows(self):
        """Unselects all rows that are selected"""
        self.__selected_rows = []

    def count_pages(self):
        """ Returns the number of pages the data takes in this table

        :return: the number of pages of this table
        """
        return len(self.__data) // self.__rows_per_page + (1 if len(self.__data) % self.__rows_per_page > 0 else 0)

    def add_cell_callback(self, callback_function):
        """ Adds an additional callback function that will be called upon a click on a table's cell

        The new ``callback_function`` will be called after the already registered callbacks. If you want to
        replace old callbacks with a new one, call  ``clear_cell_callback()`` first

        :param callback_function: callback function object, which must take a single argument: click event
        :return: ``None``
        """
        self.__cell_callback.append(callback_function)

    def add_sort_callback(self, callback_function):
        """ Adds an additional callback function that will be called when this table is sorted by a column

        The new ``callback_function`` will be called *after* sorting this table; it can be used e.g. to notify that
        the table content has been altered

        :param callback_function: callback function object, which must take a single argument: click event
        :return: ``None``
        """
        self.__sort_callback.append(callback_function)

    def add_page_callback(self, callback_function):
        """ Adds an additional callback function that will be called when user changes a page of this table

        :param callback_function: callback function object, which must take a single argument: click event
        :return: ``None``
        """
        self.__page_callback.append(callback_function)

    def clear_cell_callback(self):
        """Removes all callback routines assigned to click on a cell events

        :return: ``None``
        """
        self.__cell_callback = []

    def get_data_row(self, element_id):
        """ Returns a row of data that corresponds to a given ID of a TD or TR page element.
        This method can be used to decode ID of a table element that was clicked by a user into the actual data
         stored in this table

        :param element_id: (``string``) ID of an element of a HTML page that displays this table
        :return: row of table's data or ``None`` if the ID was incorrect
        """
        row_column = self.__process_id(element_id)
        if not row_column: return None
        return self.data[row_column[0]]

    def get_data_value(self, element_id):
        """ Returns a data value that corresponds to a given ID of a TD page element.
        This method can be used to decode ID of a table element that was clicked by a user into the actual data
         stored in this table

        :param element_id: (``string``) ID of an element of a HTML page that displays this table
        :return: row of table's data or ``None`` if the ID was incorrect
        """
        row_column = self.__process_id(element_id)
        if not row_column: return None
        return self.data[row_column[0]][row_column[1]]

    def __process_id(self, element_id):
        """ Process ID of a TD or TR page element to find which data row/cell it points to

        :param element_id: element ID must comply to the format:
            - for TR element: ``%s-TR-%d`` where the two fields are: table ID and row number
            - for TD element: ``%s-TD-%d-%d`` where the two fields are: table ID, row number, column number
        :return:
            - ``None`` in the case of incorrect format
            - ``[int]`` (list of a single element) in the case of table row ID, which holds data index of the row
            - ``[int, int]`` (list of two elements) in the case of table data ID, which holds data index of the row and column
        """
        tokens = element_id.split('-')
        if len(tokens) < 2:
            print("Incorrect element ID!")
            return None
        if tokens[0] != self.__table_id:
            print("Element ID points to another table! This table ID is: %s, received: %s" % (self.__table_id, tokens[0]))
            return None
        if tokens[1] == "TR": return [int(tokens[2])]
        if tokens[1] == "TD": return [int(tokens[2]), int(tokens[3])]
        print("Incorrect element ID! Expected TD or TR element ID")
        return None

    def __create_header(self):
        tr = html.TR(id=self.__table_id+"-THEAD-TR")
        document[self.__table_id+"-THEAD"] <= tr
        j = 0
        for col in self.__columns:
            id_prefix = self.__table_id + "-" + col.get("field_id")
            j += 1
            style = {}              # --- a style for that TH element, created based on column's properties
            if "width" in col:      # --- set up width of that column
                style["width"] = col["width"]
            if "min_width" in col: style["min-width"] = col["min_width"]
            if len(style) > 0:
                th = html.TH(id=id_prefix+"-TH", style=style)
            else:
                th = html.TH(id=id_prefix+"-TH")
            th_content = html.DIV(col.get("title"), id=id_prefix + "-DIV")
            th <= th_content

            group = html.DIV(id=self.__table_id + "-sort-arrows",
                             style={"position": "relative", "min-width": "20px", "width": "20px"})
            up = html.SPAN(id=self.__table_id + "-%s-up" % col.get("field_id"),
                           Class="fa fa-caret-up up", style={"font-size": "120%", "opacity": "0.5"})
            down = html.SPAN(id=self.__table_id + "-%s-down" % col.get("field_id"),
                             Class="fa fa-caret-down down", style={"font-size": "120%", "opacity": "0.5"})
            up.bind("click", self.__dispatch_sort_event)
            down.bind("click", self.__dispatch_sort_event)
            th.bind("click", self.__dispatch_sort_event)
            group <= up
            group <= down
            th_content <= group
            tr <= th
        self.__thead <= tr

    def __create_table_rows(self):

        widths = []
        for column in self.__columns:
            id = self.__table_id + "-" + column.get("field_id") + "-TH"
            widths.append(column["width"] if "width" in column else str(document[id].offsetWidth)+"px")
        n_col = len(self.__columns)
        for i in range(self.__rows_per_page):
            tr = html.TR(id=self.__table_id + "-TR-%d" % i)     # , style={'width': '100%'}
            self.__tbody <= tr
            for j in range(n_col):
                id = "%s-TD-%d-%d" % (self.__table_id, i, j)
                tr <= html.TD(id=id, style={"width": widths[j],"min-width": widths[j]})
        for td in self.__tbody.select('td'):
            td.bind('click', self.__cell_callback_handler)

    def __select_table_row(self, evt):
        """ Default callback method fired when a user clicks on a table's cell

        The method selects the row of a clicked cell, i.e.:
          - the data row ID is added to the list of selected rows
          - the respective table row is highlighted

        :param evt: JavaScript event object
        :return: None
        """
        row, col = self.__process_id(evt.target.id)
        self.select_row(row, (row not in self.__selected_rows))

    def __dispatch_sort_event(self, evt):
        for f in self.__sort_callback: f(evt)

    def __dispatch_page_event(self, evt):
        for f in self.__page_callback: f(evt)

    def __sort_by_column(self, evt):
        """ Default callback method fired when a user clicks on a table's column (column header)

        The method sorts the whole table by the given column. A relevant sorting method,
        that has been provided by a user, will be used for sorting.

        :param evt: JavaScript event object
        :return: None
        """
        id = evt.target.id
        self.unselect_all_rows()
        print("sort called:", id)
        i_col = 0
        for column in self.__columns:
            if id.find(column.get("field_id")) >= 0:
                self.__clear_all_sorting_arrows()
                sorter_name = column.get("sorter", "")
                if sorter_name == "" or sorter_name == "string":
                    sorter = lambda row: str(row[i_col])
                elif sorter_name == "int":
                    sorter = lambda row: int(row[i_col])
                elif sorter_name == "float":
                    sorter = lambda row: float(row[i_col])
                elif not sorter_name:
                    return
                if id.find("up") >= 0: reverse = False              # --- if "up" button was clicked, sort ascending
                elif id.find("down") >= 0: reverse = True           # --- if "down" button was clicked, sort descending
                else: reverse = self.__sort_inverse.get(id, False)  # --- otherwise reverse previous order
                self.__data.sort(key=sorter, reverse=reverse)
                self.__sort_inverse[id] = not reverse
                self.show_table(1)
                if reverse:
                    document[self.__table_id + "-%s-down" % column.get("field_id")].style.opacity = 1.0
                else:
                    document[self.__table_id + "-%s-up" % column.get("field_id")].style.opacity = 1.0
            i_col += 1

    def __clear_all_sorting_arrows(self):
        for column in self.__columns:
            document[self.__table_id + "-%s-down" % column.get("field_id")].style.opacity = 0.5
            document[self.__table_id + "-%s-up" % column.get("field_id")].style.opacity = 0.5

    def __go_to_page(self, evt):
        """Callback function to handle page navigation"""

        if evt.target.id.find("fast-forward") >= 0:
            self.show_table(self.count_pages())
        elif evt.target.id.find("fast-backward") >= 0:
            self.show_table(1)
        elif evt.target.id.find("backward") >= 0:
            self.show_table(max(self.current_page - 1, 1))
        elif evt.target.id.find("forward") >= 0:
            self.show_table(min(self.current_page + 1, self.count_pages()))

    def __scroll_table(self, evt):
        print(evt.target.id)
        print(evt.target.scrollLeft)
        document[self.__table_id+"-header"].scrollLeft = evt.target.scrollLeft
        print(document[self.__table_id+"-header"].id)
        print(document[self.__table_id+"-header"].scrollLeft)

    @staticmethod
    def __check_column(**kwargs):
        for key in ["title", "field_id"]:
            if key not in kwargs:
                print("Table column is missing its mandatory key:",key)
                return False
        return True

    def __cell_callback_handler(self, evt):
        if self.__cell_callback:
            for c in self.__cell_callback: c(evt)
