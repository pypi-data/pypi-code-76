from browser import document, html
from visualife.core.styles import *
from visualife.utils.html_utils import create_tooltip, MenuWidget


class SequenceViewer:

    __style = """
.SequenceViewer-numbers {
    font-family: monospace;
    font-size: 13px;
    display: inline-block;
    text-align: right;
    padding-right: 5px;
    border-right: 1px solid LightGray;
    width: 40px;
}

.SequenceViewer-fasta {
    font-family: monospace;
    font-size: 13px;
    display: inline-block;
    padding-left: 5px;
    box-sizing: border-box;
    text-align: left;
    white-space: nowrap;
    cursor: pointer;
}

.SequenceViewer-top_row {
    overflow: visible;
    padding-left: 45px;
    text-align: left;
    font-family: monospace;
    font-size: 13px;
    height: 20px;
    display: flex;
    flex-direction: row;
    align-content: space-between;
}

.SequenceViewer-legend_item {
    display: inline;
    font: Arial;
    font-size: 15px;
    cursor: pointer;
}

.SequenceViewer-legend_item:disabled {
    color: gray;
}

.SequenceViewer-sequence-box { overflow: visible; }

.SequenceViewer-menu {
    width: 20px;
    height: 20px;
    right: 0px;
    cursor: context-menu;
}
    """

    def __init__(self, element_id, sequence_name="", sequence="", **kwargs):
        """Creates a widget that displays an amino acid or a nucleotide sequence

        A basic example of the widget is given below:

        .. raw:: html

          <div id="show_sequence"></div>
          <script type="text/python">
            from visualife.widget import SequenceViewer

            seq = SequenceViewer("show_sequence","4fia A","GRVLQDVFLDWAKKYGPVVRVNVFHKTSVIVTSPESVKKFLMSTKYNKDSKMYRALQTVFGERLFGQGLVSECNYERWHKQRRVIDLAFSRSSLVSLMETFNEKAEQLVEILEAKADGQTPVSMQDMLTYTAMDILAKAAFGMETSMLLGAQKPLSQAVKLMLEGITASRNTKRKQLREVRESIRFLRQVGRDWVQRRREALKRGEEVPADILTQILKAEEGAQDDEGLLDNFVTFFIAGHETSANHLAFTVMELSRQPEIVARLQAEVDEVIGSKRYLDFEDLGRLQYLSQVLKESLRLYPPAWGTFRLLEEETLIDGVRVPGNTPLLFSTYVMGRMDTYFEDPLTFNPDRFGPGAPKPRFTYFPFSLGHRSCIGQQFAQMEVKVVMAKLLQRLEFRLVPGQRFGLQEQATLKPLDPVLCTLRPR")
            seq.add_to_region("sel1", first_pos=40, last_pos=80)
            seq.region_tooltip("sel1","first region")
          </script>

        It has been created by the following code:

        .. code-block:: Python

            from visualife.widget import SequenceViewer

            seq = SequenceViewer("show_sequence","4fia A","GRVLQDVFLDWAKKYGPVVRVNVFHKTSVIVTSPESVKKFLMSTKYNKDSKMYRALQTVFGERLFGQGLVSECNYERWHKQRRVIDLAFSRSSLVSLMETFNEKAEQLVEILEAKADGQTPVSMQDMLTYTAMDILAKAAFGMETSMLLGAQKPLSQAVKLMLEGITASRNTKRKQLREVRESIRFLRQVGRDWVQRRREALKRGEEVPADILTQILKAEEGAQDDEGLLDNFVTFFIAGHETSANHLAFTVMELSRQPEIVARLQAEVDEVIGSKRYLDFEDLGRLQYLSQVLKESLRLYPPAWGTFRLLEEETLIDGVRVPGNTPLLFSTYVMGRMDTYFEDPLTFNPDRFGPGAPKPRFTYFPFSLGHRSCIGQQFAQMEVKVVMAKLLQRLEFRLVPGQRFGLQEQATLKPLDPVLCTLRPR")
            seq.add_to_region("sel1", first_pos=40, last_pos=80)
            seq.region_tooltip("sel1","first region")

        SequenceViewer allows also loading more than one sequence; multiple sequences must be provided as a list

        .. raw:: html

          <div id="show_sequence2"></div>
          <script type="text/python">
            from visualife.widget import SequenceViewer

            seq = ["GQSSLALHKVIMVGSGGVGKSALTLQFMYDEFVEDYEPTKADSYRKKVVLDGEEVQIDILDTAGLEDYAAIRDNYFRSGEGFLLVFSITEHESFTATAEFREQILRVKAEEDKIPLLVVGNKSDLEERRQVPVEEARSKAEEWGVQYVETSAKTRANVDKVFFDLMREIRTKKMSENK",
                "GSETQAGIKEEIRRQEFLLNSLHRDLQGGIKDLSKEERLWEVQRILTALKRKLREA"]
            in_chain_A = [16,18,48,49,50,51,52,65,67,74,75,77,78,81,82,84,85]
            in_chain_B = [409,413,416,417,421,426,427,429,430,433,434,437,440,444]
            seq = SequenceViewer("show_sequence2", "2kwi A, B", seq, first_residue_id=[8, 391])
            for ires in in_chain_A:
                seq.add_to_region("sel1", 1, first_pos=ires, last_pos=ires, by_residue_id=True)
            seq.region_tooltip("sel1","chain A interacting with chain B")
            for ires in in_chain_B:
                seq.add_to_region("sel2", 2, first_pos=ires, last_pos=ires, by_residue_id=True)
            seq.region_tooltip("sel2","chain B interacting with chain A")
          </script>

        It has been created by the following code:

        .. code-block:: Python

            from visualife.widget import SequenceViewer

            seq = ["GQSSLALHKVIMVGSGGVGKSALTLQFMYDEFVEDYEPTKADSYRKKVVLDGEEVQIDILDTAGLEDYAAIRDNYFRSGEGFLLVFSITEHESFTATAEFREQILRVKAEEDKIPLLVVGNKSDLEERRQVPVEEARSKAEEWGVQYVETSAKTRANVDKVFFDLMREIRTKKMSENK",
                "GSETQAGIKEEIRRQEFLLNSLHRDLQGGIKDLSKEERLWEVQRILTALKRKLREA"]
            in_chain_A = [16,18,48,49,50,51,52,65,67,74,75,77,78,81,82,84,85]
            in_chain_B = [409,413,416,417,421,426,427,429,430,433,434,437,440,444]
            seq = SequenceViewer("show_sequence2", "2kwi A, B", seq, first_residue_id=[8, 391])
            for ires in in_chain_A:
                seq.add_to_region("sel1", 1, first_pos=ires, last_pos=ires, by_residue_id=True)
            seq.region_tooltip("sel1","chain A interacting with chain B")
            for ires in in_chain_B:
                seq.add_to_region("sel2", 2, first_pos=ires, last_pos=ires, by_residue_id=True)
            seq.region_tooltip("sel2","chain B interacting with chain A")

        :param element_id: ID of a html DIV element that will contain this SequenceViewer instance
        :param sequence_name: name of the sequence to be shown
        :param sequence: the sequence itself (one-letter string, FASTA-style without header)
        :param kwargs: see below

        :Keyword Arguments:
            * *palette_name* (``string``) --
              name of a color palette used to mark sequence regions (one color per region)
            * *sequence_colors* (``dict``) --
              name of a color scheme that is used to color a sequence. The available
              color schemes are defined in ``core/styles.py``. Each style is just a dictionary that provides
              a color (either by its name or hex) for every letter that may be found in sequence
            * *n_columns_of_ten* (``int``) --
              when the widget displays sequence, it puts a space after every 10 residues; by default there are
              50 residues in every line, divided in five 10-residues blocks; say ``n_columns_of_ten=4`` to display
              only 40 residues per line  or to  ``n_columns_of_ten=8`` if you like to have 80 residues per line
            * *onclick* (``function``) --
              provide a function that will be called at ``onclick`` event; the function must accept
              sole ``event`` object argument
            * *first_residue_id* (``int`` or ``list[int]``) --
              integer index of the very first residue in the given sequence (1 by default); if more than one sequence
              has been provided, user should provide also a list with first residue IDs
            * *region_cmap* (``ColorMap`` or ``string``) --
              defines a color map that will be used to color letters within a single residue range - in the case
              where user provides a real value for each letter of a range
            * *show_menu* (``bool``) --
              if ``True``, a drop-down menu will be shown for that widget (``True`` by default)
            * *show_header* (``bool``) --
              if ``True``, a header line will be shown for that widget (``True`` by default)
            * *show_blockwise* (``bool``) --
              if ``True``, a sequence will be displayed in blocks of 10 residues, separated by a space (``True`` by default);
              otherwise, each row of this widget will be a contiguous line of amino acid or nucleotide symbols
        """

        self.__element_id = element_id
        self.__sequence_name = sequence_name
        self.__sequence = sequence
        self.__secondary_structure = ""
        self.__selecting_allowed = kwargs.get("selecting_allowed", False)
        frst = kwargs.get("first_residue_id", [1])
        self.__first_residue_id = list(frst) if type(frst) in [list, tuple] else [frst]
        self.__chars_in_block = 10
        self.__show_blockwise = kwargs.get("show_blockwise", True)
        # --- for each region name stores a list of chunk, each chunk is a two-tuple: (begin, end)
        # --- Begin and end of each chunk (both inclusive) start from 0!
        self.__selections = {}
        self.__selection_colors = {}
        self.__show_menu = kwargs.get("show_menu", True)
        self.__show_header = kwargs.get("show_header", True)
        self.__selection_tooltips = {}
        # --- palette for categorical features (yes/no)
        self.__selections_palette_name = kwargs.get("palette_name", "pastel1")
        self.__selections_palette = known_color_scales[self.__selections_palette_name]
        # --- palette for continuous features (double values)
        self.__selection_cmap = colormap_by_name(kwargs.get("region_cmap", "blues"), 0.0, 1.0)
        self.__regions_shown = {}
        self.click_on_sequence_callback = self.__click_letter_default
        self.click_on_legend_callback = self.__click_on_legend_default

        self.__blocks_in_line = kwargs.get("n_columns_of_ten", 5)
        width = int(86 * self.__blocks_in_line + 10)
        if_add_style = kwargs.get("if_add_style",True)
        if if_add_style: document <= html.STYLE(SequenceViewer.__style)

        max_width_style = {'width': '%spx' % str(width+50), 'max-width': '%spx' % str(width+50)}
        d1 = html.DIV('', Class="SequenceViewer-sequence-box", id="SequenceViewer-"+element_id, style=max_width_style)

        width_style = {'width': '%spx' % str(width-5), 'max-width': '%spx' % str(width-5)}
        d2 = html.DIV('', Class="SequenceViewer-top_row", id="top-row-" + element_id, style=width_style)

        d2 <= html.DIV('', id="header-" + element_id, style={"width": "%dpx" % (width-40)})
        d2 <= html.DIV('', Class="SequenceViewer-menu", id="menu-" + element_id)
        d1 <= d2
        if not self.__show_header:
            d2.style.visibility = "hidden"

        d3 = html.DIV('', style={'display': 'flex', 'flex-direction': 'row'})
        d3 <= html.DIV('', Class="SequenceViewer-numbers", id="numbers-"+element_id)
        width_style = {'width': '%spx' % str(width), 'max-width': '%spx' % str(width)}
        d3 <= html.DIV('', Class="SequenceViewer-fasta", id="fasta-"+element_id, style=width_style)
        d1 <= d3
        d1 <= html.DIV('', id="legend-box-" + element_id, style={'display': 'flex', 'flex-direction': 'row',
                    'width': '%spx' % str(width+50), 'max-width': '%spx' % str(width+50), 'flex-wrap':'wrap',
                    'padding-top':'10px'})
        document[element_id] <= d1

        if self.__show_menu:
            self.__menu = MenuWidget("menu-" + element_id,
                    {"color scheme": {
                        "clear": self.__color_sequence_event,
                        "secondary": self.__color_sequence_event,
                        "clustal": self.__color_sequence_event,
                        "maeditor": self.__color_sequence_event},
                     },
                    width=150)

        self.sequence_name = sequence_name
        if len(sequence) > 0:
            self.load_sequence(sequence)

        if "sequence_colors" in kwargs:
            self.color_sequence(kwargs["sequence_colors"])

    @property
    def element_id(self):
        """Provides ID of the page element that holds this widget (parent element)

        :return: ID of the parent HTML element
        """
        return self.__element_id

    @property
    def menu(self):
        """Provides menu for this object

        :return: MenuWidget object
        """
        return self.__menu

    def region_legend_id(self, region_name):
        """Returns the ID of a legion legend element

        :param region_name: (``string``) a region name, assigned at ``add_to_region()`` call
        :return: ID of the DOM element that holds legend for that sequence region
        """
        return "legend-box-" + self.__element_id + "-" + region_name

    @property
    def sequence_name(self):
        """Name of the sequence displayed by this viewer.

        :getter: returns the sequence name
        :setter: sets a new name for this sequence;  if the header line has been hidden, will be made visible
        :type: string
        """
        return self.__sequence_name

    @sequence_name.setter
    def sequence_name(self, name):
        self.__sequence_name = name
        if self.__sequence_name != "":
            document["header-" + self.__element_id].innerHTML = "&gt; "+self.__sequence_name

    @property
    def show_header(self):
        """Whether this widget shows a sequence header line or not

        :getter: returns ``True`` when the sequence header line is displayed
        :setter: switch on or off this sequence header line
        :type: boolean
        """
        return self.__show_header

    @show_header.setter
    def show_header(self, if_show):
        self.__show_header = if_show
        if if_show:
            document["header-" + self.element_id].style.visibility = "visible"
        else:
            document["header-" + self.element_id].style.visibility = "hidden"

    def count_sequences(self):
        """Number of  sequences displayed by this viewer.

        :return: (``int``) number of sequences
        """
        return self.__sequence

    def sequence(self):
        """Protein / nucleotide sequence displayed by this viewer.

        Total number of sequences can be checked by :meth:`count_sequences`
        :param index: (``int``) the index of the sequence (from 0)
        :return: (``str``) a sequence
        """
        return self.__sequence

    @property
    def secondary_structure(self):
        """Protein / nucleotide secondary structure - for coloring purposes only

        :getter: returns the secondary structure
        :setter: sets secondary structure string for this sequence
        :type: string
        """
        return self.__secondary_structure

    @secondary_structure.setter
    def secondary_structure(self, hec_string):
        self.__secondary_structure = hec_string

    def first_residue_id(self, which_sequence):
        """Index of the very first residue in a given sequence

        :param which_sequence: (``int``) index of a sequence
        :return: (``int``) ID of the very first residue of that sequence
        """
        return self.__first_residue_id[which_sequence]

    @property
    def click_on_legend_callback(self):
        """procedure called when a user clicks on a region's label

        :getter: returns the callback procedure
        :setter: sets the new callback procedure for ``onclick`` event
        :type: function
        """
        return self.__click_on_legend_callback

    @click_on_legend_callback.setter
    def click_on_legend_callback(self, callback):
        self.__click_on_legend_callback = callback

    @property
    def click_on_sequence_callback(self):
        """procedure called when a user clicks on a sequence's letter

        :getter: returns the callback procedure
        :setter: sets the new callback procedure for ``onclick`` event
        :type: function
        """
        return self.__onclick_callback

    @click_on_sequence_callback.setter
    def click_on_sequence_callback(self, callback):
        self.__onclick_callback = callback

    @property
    def regions_palette(self):
        """A name of color palette used to color marked regions.

        To display more than one regions, use one of the categorical palettes defined in styles.known_color_scales,
        such as ``"tableau10"``, ``"pastel1"`` or ``"accent"``. To color residues by a real-valued property, use
        a continuous color scale such as ``"violet_red"``

        :getter: returns the  name of color palette used to color selected regions
        :setter: sets the new palette
        :type: string
        """
        return self.__selections_palette_name

    @regions_palette.setter
    def regions_palette(self, palette_name):
        if palette_name in known_color_scales:
            self.__selections_palette_name = palette_name
        self.__selections_palette = known_color_scales[self.__selections_palette_name]

    @property
    def region_cmap(self):
        """A color map used to color a single sequence region according to real values

         :getter: returns the ``ColorMap`` object
         :setter: sets the new color map, either by its name or an object by itself
         :type: ``string`` or ``ColorMap`` object
         """
        return self.__selection_cmap

    @region_cmap.setter
    def region_cmap(self, cmap):
        if isinstance(cmap, str):
            self.__selection_cmap = colormap_by_name(cmap, 0.0, 1.0)
        else:
            self.__selection_cmap = cmap

    @property
    def sequence_blocks_in_line(self):
        """ Returns the number of 10-residues long blocks of a sequence that are printed in a single line

        :return: number of sequence blocks in a line
        """
        return self.__blocks_in_line

    def add_to_region(self, region_name, which_sequence=0, if_show_region=True, **kwargs):
        """Add a block of amino acids/nucleotides to a sequence region

        This method updates an existing region. If the given region name has not been used so far,
        a new region will be created

        :param region_name: name of this sequence region
        :param which_sequence: (``integer``) index of a sequence to mark a region; use ``0`` (the default)
            to mark a region on all sequences shown by this widget
        :param if_show_region: if True, the sequence region will be made visible after this change
        :param kwargs: see below

        :Keyword Arguments:
            * *color* (``string``, ``ColorBase``, ``int`` or ``list[float]``) --
              provides color for this region:
                - directly as ColorBase object
                - by color name as ``string``
                - by index of a color in the palette defined by ``regions_palette()``
                - by real values: color map will be used to color the region
              color is assigned only to newly created blocks; extending a block doesn't change its color
            * *tooltip* -- a tooltip text will be shown when mouse cursor is over the region (*mouseover* event)
            * *by_residue_id* (``bool``) -- by default is ``False``; when set to ``True``, ``pos_from`` and ``pos_to``
              will be considered residue IDs rather than indexes from 1
            * *show_in_legend* (``bool``) -- if ``True``, the region will be also listed in a legend box
            * *first_pos* (``int``) -- first residue included in this region, numbers start from 1;
              if no *last_pos* is provided, *last_pos* will be set to ``first_pos``
            * *last_pos* (``int``) -- last residue included in this region, numbers start from 1;
              if no *first_pos* is provided, *first_pos* will be set to ``last_pos``
            * *sequence* (``string``) -- a string that is a sequence fragment of this sequence
        :return: None
        """
        if_legend = kwargs.get("show_in_legend", True)
        if region_name not in self.__selections:
            if "color" in kwargs:
                self.__selection_colors[region_name] = kwargs["color"]
            else:
                self.__selection_colors[region_name] = len(self.__selections)
            self.__selections[region_name] = []
            if region_name+"-tooltip" not in document:
                document <= create_tooltip(region_name+"-tooltip", "", 200, 10)
            if if_legend:
                legend_div = html.DIV("", Class="SequenceViewer-legend_item", id=self.region_legend_id(region_name))
                clr = self.__selection_colors[region_name]
                if isinstance(clr, int):
                    legend_div <= html.SPAN("&#9679;", style={'color': self.__selections_palette[clr%len(self.__selections_palette)],
                                                               'padding': '0px 10px 0px 20px'})
                elif isinstance(clr, float):
                    legend_div <= html.SPAN("&#9679;", style={'color': self.__selection_cmap(clr),
                                                               'padding': '0px 10px 0px 20px'})
                elif isinstance(clr, list):
                    clr_left = str(self.__selection_cmap.color((self.__selection_cmap.min_value)))
                    legend_div <= html.SPAN("&#9679;", style={'color': clr_left,
                                                               'padding': '0px 10px 0px 20px'})
                    clr_right = str(self.__selection_cmap.color((self.__selection_cmap.max_value)))
                    legend_div <= html.SPAN("&#9679;", style={'color': clr_right,
                                                                'padding': '0px 10px 0px 20px'})
                else:
                    legend_div <= html.SPAN("&#9679;", style={'color': clr,
                                                              'padding': '0px 10px 0px 0px'})
                legend_div <= html.DIV(kwargs.get("tooltip", ""),
                                       id="legend-box-" + self.__element_id + "-" + region_name + "-text", style={'display': 'inline'})
                document["legend-box-" + self.__element_id] <= legend_div
                legend_div.bind("click", self.__click_legend_dispatch)

        if "sequence" in kwargs:
            pos = self.__sequence[which_sequence].find(kwargs["sequence"])
            if pos > -1:
                pos_from = pos + 1
                pos_to = pos_from + len(kwargs["sequence"])
        elif "first_pos" in kwargs:
            pos_from = kwargs["first_pos"]
            pos_to = kwargs.get("last_pos", pos_from + 1)
        elif "last_pos" in kwargs:
            pos_to = kwargs["last_pos"]
            pos_from = kwargs.get("first_pos", pos_to - 1)
        else:
            return

        n_first = len(self.__first_residue_id)
        if which_sequence > 0:
            first = -self.__first_residue_id[(which_sequence - 1) % n_first] if "by_residue_id" in kwargs else -1
            self.__selections[region_name].append((which_sequence, pos_from+first, pos_to+first))
        else:
            first = -self.__first_residue_id[0] if "by_residue_id" in kwargs else -1
            self.__selections[region_name].append((0, pos_from + first, pos_to + first))

        if "tooltip" in kwargs:
            self.region_tooltip(region_name, kwargs["tooltip"])
        if if_show_region: self.show_region(region_name)

    def delete_region(self, region_name):
        """Permanently removes a sequence region

        If you just want to hide a region, use ``hide_region()`` instead
        :param region_name: name of a sequence region to be deleted
        :return: None
        """
        for d in [self.__selections, self.__selection_colors, self.__selection_tooltips]:
            if region_name in d:
                del(d[region_name])

    def delete_regions(self):
        """Permanently removes all regions defined for a sequence

        :return: None
        """
        for name in list(self.__selections.keys()): self.delete_region(name)

    def show_region(self, region_name):
        """Activates a given region

        :param region_name: name of a sequence region to be made visible
        :return: None
        """
        if region_name not in self.__selections: return

        self.__regions_shown[region_name] = True
        if isinstance(self.__selection_colors[region_name], int):
            color = [self.__selections_palette[self.__selection_colors[region_name]%len(self.__selections_palette)]]
        elif isinstance(self.__selection_colors[region_name], list):
            color = []
            for f in self.__selection_colors[region_name]:
                color.append(self.__selection_cmap.color(f))
        else:
            color = [self.__selection_colors[region_name]]
        id_str = "ch-" + self.__element_id + "-"
        for chunk in self.__selections[region_name]:
            if chunk[0] == 0:
                i_max = max(1, chunk[1] + 1)
                for i in range(i_max, min(chunk[2] + 2, len(self.__sequence[0]) + 1)):  # Here self.__sequence[0] assumes all sequences to be of the same length
                    i_str = '-' + str(i)
                    i_color = str(color[i % len(color)])
                    for i_seq in range(1, len(self.__sequence) + 1):
                        el = document[id_str + str(i_seq) + i_str]
                        el.style.backgroundColor = i_color
                        el.class_name += " "+region_name+"-tipcls"
            else:
                for i in range(max(1, chunk[1] + 1), min(chunk[2] + 2, len(self.__sequence[chunk[0] - 1]) + 1)):
                    el = document[id_str + str(chunk[0]) + '-' + str(i)]
                    el.style.backgroundColor = str(color[i % len(color)])
                    el.class_name += " "+region_name+"-tipcls"

    def hide_region(self, region_name):
        """Deactivates a given sequence region

        This method does not remove any region, it just clears the color
        :param region_name: name of a sequence region to be made cleared off
        :return: None
        """

        if region_name not in self.__selections: return

        self.__regions_shown[region_name] = False
        id_str = "ch-" + self.__element_id + "-"
        for chunk in self.__selections[region_name]:
            for i in range(chunk[0] + 1, min(chunk[1] + 2, len(self.__sequence)+1)):
                document[id_str + str(i)].style.backgroundColor = "#FFFFFF"

    def flip_region(self, region_name):
        """ Flips region visibility.

         Visible region will be hidden while a hidden region will be shown
        :param region_name:  name of a sequence region
        """
        if region_name not in self.__selections: return
        if not self.__regions_shown[region_name]: self.show_region(region_name)
        else: self.hide_region(region_name)

    def region_tooltip(self, region_name, tooltip):
        """ Sets a text that will show up in a tooltip

        The given text will be displayed in a tooltip box when a user hoovers the given sequence region
        with a mouse pointer. Use empty string to clear a tooltip

        :param region_name: name of a sequence region that needs a tooltip
        :param tooltip: tooltip text
        """

        self.__selection_tooltips[region_name] = tooltip
        document[region_name+"-tooltip"].innerHTML = tooltip
        el_id = "legend-box-" + self.__element_id + "-" + region_name + "-text"
        if el_id in document:
            document[el_id].innerHTML = tooltip

    def region_for_name(self, region_name):
        """ Returns a sequence region registered under a given name.

        :param region_name: (``string``) region name
        :return: a list of residue ranges (from, to) - both inclusive from 0, e.g. ``[(0,5),(7,20)]``
        """
        return self.__selections[region_name]

    def region_for_position(self, pos):
        """ Returns a sequence region a given residue belongs to.

        :param pos: (``int``) residue position from 1
        :return: a region name and  a list of ranges as in ``region_for_name()`` or None if a given residue
          doesn't belong to any region
        """
        for name, region in self.__selections.items():
            for chunk in region:
                if pos >= chunk[1] and pos <= chunk[2]:
                    return name, region
        return None, None

    def which_region_in_legend(self, evt):
        """Returns the sequence region corresponding to a legend item user clicked on.

        :param evt: event object passed by a browser, that holds the clicked element
        :return: tuple of two: sequence region name and the residues' range as a list of lists of int
        """
        for name, region in self.__selections.items():
            if evt.target.id.find(name) > -1 : return name, region
        return None, None

    @staticmethod
    def secondary_structure_colors(hec_string, default_color="black"):
        color_scheme = known_sequence_scales["hec_secondary"]
        return [color_scheme.get(c, default_color) for c in hec_string]

    def color_sequence(self, color_scheme,**kwargs):
        """Colors characters in this sequence

        The color of each character, which by default is black, will be set according to a requested color scheme

        :param color_scheme: a color scheme to be used (see below):

          - ``list[string]`` - list of colors (names of hex-strings) - the colors will be assigned to letters
            by one one; the list is cycled, so the colors can re-appear periodically
          - "secondary": by secondary structure: helices, strands and loops (coil) will be red, blue and gray, respectively;
            this scheme requires secondary structure string to be set (secondary_structure property)
          - "clear": all letters will be turned back to black
          - "clustal": letters will be coloured by amino acid code (ClustalW scheme)
          - "maeditor": coloured by amino acid code (Multiple Alignment Editor program scheme)
        """
        if isinstance(color_scheme,list):
            if not isinstance(color_scheme[0],str):
                palette = kwargs.get("palette_name","pinks")
                map = colormap_by_name(palette, min(color_scheme)+0.001, max(color_scheme))
                map.left_color="white"
                colors=[str(map.color(i)) for i in color_scheme]
                self.__color_span(colors, "color", "black")
                return
        self.__color_span(color_scheme, "color", "black")

    def color_background(self, color_scheme,**kwargs):
        """Colors letter background in this sequence

        The background color for each character, which by default is white, will be set according to a requested color scheme

        :param color_scheme: a color scheme to be used (see below):

          - ``list[string]`` - list of colors (names of hex-strings) - the colors will be assigned to letters
            by one one; the list is cycled, so the colors can re-appear periodically
          - secondary: by secondary structure: helices, strands and loops (coil) will be red, blue and gray, respectively;
            this scheme requires secondary structure string to be set (secondary_structure property)
          - clear: background will be set back to white
          - clustal: coloured by amino acid code (ClustalX scheme)
          - maeditor: coloured by amino acid code (Multiple Alignment Editor program scheme)
        """
        if isinstance(color_scheme,list):
            if not isinstance(color_scheme[0],str):
                palette = kwargs.get("palette_name","pinks")

                map = colormap_by_name(palette, min(color_scheme)+0.001, max(color_scheme))
                map.left_color="white"

                colors=[str(map.color(i)) for i in color_scheme]
                self.__color_span(colors, "backgroundColor", "white")
                return
        
        self.__color_span(color_scheme, "backgroundColor", "white")

    def load_sequence(self, fasta_sequence):
        """ Replaces the sequence displayed by this object with a new one

        :param fasta_sequence: a new sequence to be loaded (one-letter code)
        :return: None
        """

        n = self.__chars_in_block
        document["numbers-" + self.element_id].innerHTML = ""
        document["fasta-" + self.element_id].innerHTML = ""
        document["legend-box-" + self.__element_id].innerHTML = ""
        i_char, i_seq = 0, 0
        id_str = "ch-" + self.__element_id + "-"
        n_first = len(self.__first_residue_id)          # --- cycle index of the first residue
        # ---if it's not a list, make a list of size 1
        self.__sequence = fasta_sequence if isinstance(fasta_sequence, list) else [fasta_sequence]
        f = html.DIV()
        fasta_text = ""
        dn = html.DIV()
        for fasta_sequence in self.__sequence:                 # --- for every sequence
            i_row, i_char = 0, 0
            # --- split a fasta sequence into blocks of self.__chars_in_block, by default 10
            subseq = [fasta_sequence[i:i + n] for i in range(0, len(fasta_sequence), n)]
            # --- The number of lines required to print the blocks
            n_total_rows = int(len(subseq)/self.__blocks_in_line)

            i_seq += 1
            
            i_block_in_subseq = 0
            for block in subseq:            # --- process blocks one by one
                for ch in block:
                    i_char += 1
                    #f<= html.SPAN(ch, id=id_str + str(i_seq) + '-' + str(i_char))
                    fasta_text += "<span id=%s>%s</span>"%(id_str + str(i_seq) + '-' + str(i_char),ch)

                    #document["fasta-" + self.element_id] <= html.SPAN(ch, id=id_str + str(i_seq) + '-' + str(i_char))
                if self.__show_blockwise:
                    #document["fasta-"+self.element_id] <= html.SPAN(" ")
                    #f <= html.SPAN(" ")
                    fasta_text += "<span> </span>"
                i_block_in_subseq += 1
                is_very_last_block = (n_total_rows == i_row) and (i_seq == len(self.__sequence))
                is_line_full_of_blocks = i_block_in_subseq % self.__blocks_in_line == 0 and len(block) == self.__chars_in_block and not is_very_last_block
                is_sequence_end = i_block_in_subseq == len(subseq)
                if is_line_full_of_blocks or is_sequence_end:
                    ir = i_row * self.__chars_in_block * self.__blocks_in_line + self.__first_residue_id[(i_seq-1)%n_first]
                    dn <= html.SPAN(str(ir)) + html.BR()
                    
                    #document["numbers-" + self.element_id] <= html.SPAN(str(ir)) + html.BR()
                    #document["fasta-" + self.element_id] <= html.BR()
                    #f <= html.BR()
                    fasta_text += "<br>" 

                    i_row += 1
        document["numbers-" + self.element_id] <= dn
        #document["fasta-" + self.element_id] <= f
        document["fasta-" + self.element_id].innerHTML = fasta_text 

        for c in document["fasta-" + self.element_id].children:
            c.bind("click", self.__click_letter_dispatch)
            c.bind("mouseover", self.__show_tooltip)
            c.bind("mouseout", self.__hide_tooltips)

    def __color_span(self, color_scheme_name, style_name, default_color):
        """Assign color to every SPAN element of this widget.

        Depending on this method's parameters, either ``color`` or ``backgroundColor`` can be assigned.

        :param color_scheme_name: list of colors or a color scheme name; colors from a list are cycled
        :param style_name: CSS element property to set the color; either ``color`` or ``backgroundColor``
        :param default_color: e.g. ``white`` (in the case of background) or ``black`` in the case of text
        :return: ``None``
        """

        fasta_seq = document["fasta-" + self.element_id]
        if isinstance(color_scheme_name, ColorMap):
            ii = 0
            for span in fasta_seq.getElementsByTagName("span"):
                if span.hasAttribute('id'):
                    span.style[style_name] = color_scheme_name.get(ch, default_color)
                    ii += 1
            return

        if isinstance(color_scheme_name, list):
            ii = 0
            for span in fasta_seq.getElementsByTagName("span"):
                if span.hasAttribute('id'):
                    span.style[style_name] = color_scheme_name[ii % len(color_scheme_name)]
                    ii += 1
            return

        if color_scheme_name == "none" or color_scheme_name == "clear":
            for span in fasta_seq.getElementsByTagName("span"):
                if span.hasAttribute('id'):
                    span.style[style_name] = default_color
            return

        if color_scheme_name == "secondary" and len(self.secondary_structure) == len(self.sequence):
            self.__color_span(SequenceViewer.secondary_structure_colors(self.secondary_structure, default_color),
                              style_name, default_color)
            return

        if color_scheme_name in known_sequence_scales:
            color_scheme = known_sequence_scales[color_scheme_name]
            for span in fasta_seq.getElementsByTagName("span"):
                if span.hasAttribute('id'):
                    ch = span.innerHTML
                    span.style[style_name] = color_scheme.get(ch, default_color)

    def __click_letter_default(self, evt):

        if not self.__selecting_allowed: return

        aa = document["fasta-" + self.__element_id].children
        pos = self.__locate_letter(evt.target)
        if aa[pos].style.backgroundColor == "rgb(255, 255, 0)":
            aa[pos].style.backgroundColor = "#FFFFFF"
        else:
            aa[pos].style.backgroundColor = "rgb(255, 255, 0)"

    def __click_on_legend_default(self, evt):

        name, _ = self.which_region_in_legend(evt)
        if name: self.flip_region(name)

    def __click_letter_dispatch(self, evt):
        return self.click_on_sequence_callback(evt)

    def __click_legend_dispatch(self, evt):
        return self.click_on_legend_callback(evt)

    def __locate_letter(self, obj):
        i = 0
        for o in document["fasta-" + self.__element_id].children:
            if o == obj: return i
            i += 1
        return None

    def __show_tooltip(self, evt):

        class_name = evt.target.class_name
        if len(class_name) < 2: return
        for tip_name in self.__selection_tooltips:
            if class_name.find(tip_name) > -1 :
                if len(self.__selection_tooltips[tip_name]) > 0:
                    document[tip_name + "-tooltip"].style.visibility = 'visible'
                    document[tip_name + "-tooltip"].style.top = str(evt.clientY + 20) + 'px'
                    document[tip_name + "-tooltip"].style.left = str(evt.clientX + 20) + 'px'

    def __hide_tooltips(self, evt):

        for tip_name in self.__selection_tooltips:
            document[tip_name + "-tooltip"].style.visibility = 'hidden'

    def __color_sequence_event(self, evt):
        what = evt.target.id
        print("coloring by", what)
        self.color_sequence(what)

    def __color_background_event(self, evt):
        what = evt.target.id
        print("coloring background by", what)
        self.color_background(what)
