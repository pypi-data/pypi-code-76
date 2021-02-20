import math
from browser import document, html,aio,ajax
from visualife.core.styles import *
from visualife.data import kd_hydrophobicity
from visualife.widget import SequenceViewer
from visualife.utils.html_utils import MenuWidget, run_async_func
from visualife.core.Plot import Plot
from visualife.core.HtmlViewport import HtmlViewport


class MSAViewer:

    def __init__(self, element_id, msa_header="", msa=None,**kwargs):
        """Displays a Multiple Sequence Alignment (MSA)

                A basic example of the widget is given below:

        .. raw:: html

          <div id="show_msa"></div>
          <script type="text/python">
            from visualife.widget import MSAViewer

            msa = [ {"description" : "Crambin", "sequence": "TTCCPSIVARSNFNVCRLPGTPEALCATYTGCIIIPGATCPGDYAN"},
            {"description" : "Thionin", "sequence": "-SCCPTTAARNTYNVCRLPGTPRPVCASLSGCIIISGTRCPPNYPR"},
            {"description" : "Viscotoxin", "sequence": "-SCCPNTTGRNIYNTCRFGGGSREVCASLSGCKIISASTCP-SYPD"}]

            msa = MSAViewer("show_msa","crambin homologs", msa=msa)
            msa.add_to_region("sel1", 1, first_pos=4, last_pos=8)
            msa.region_tooltip("sel1","first region")
          </script>

        It has been created by the following code:

        .. code-block:: Python

            from visualife.widget import MSAViewer

            msa = [ {"description" : "Crambin", "sequence": "TTCCPSIVARSNFNVCRLPGTPEALCATYTGCIIIPGATCPGDYAN"},
            {"description" : "Thionin", "sequence": "-SCCPTTAARNTYNVCRLPGTPRPVCASLSGCIIISGTRCPPNYPR"},
            {"description" : "Viscotoxin", "sequence": "-SCCPNTTGRNIYNTCRFGGGSREVCASLSGCKIISASTCP-SYPD"}]

            msa = MSAViewer("show_msa","crambin homologs", msa=msa)
            msa.add_to_region("sel1", 1, first_pos=4, last_pos=8)
            msa.region_tooltip("sel1","first region")

        :param element_id: id of div element where you want to display your MSA
        :param msa_header: header text will be display on top of MSA
        :param msa: list of dictionaries; each dictionary is another sequence; eg. {"description":"2gb1","sequence":"AGTPTACAGA"}

        :Keyword Arguments:
            * *if_bars* (``bool``) --
              if ``True`` bars will appeare under every part of MSA
            * *bars_function* (``string``) --
              name of a function that bars shows
            * *n_columns_of_ten* (``int``) --
              when the widget displays sequence, it puts a space after every 10 residues; by default there are
              50 residues in every line, divided in five 10-residues blocks; say ``n_columns_of_ten=4`` to display
              only 40 residues per line  or to  ``n_columns_of_ten=8`` if you like to have 80 residues per line
            * *show_blockwise* (``bool``) --
              if ``True``, a sequence will be displayed in blocks of 10 residues, separated by a space (``True`` by default);
              otherwise, each row of this widget will be a contiguous line of amino acid or nucleotide symbols
        """
        self.__msa = []  # --- id, seq, long_desc
        self.__max_name_len = 10  # --- the length of the longest sequence name
        self.__max_sequence_len = 80  # --- the number of sequence residues shown in a single panel
        self.__if_numerated = True
        self.__sequences_split_to_columns = []  # --- Each inner list contains sequence fragments for a single panel
        self.__element_id = element_id
        self.__subwidgets = []
        self.__msa_header = msa_header
        self.__bars_dict = {"identity":self.identity_fraction, "entropy":self.shannon_entropy, 
            "hydrophobicity":self.hydrophobicity}
        
        document[element_id].style.textAlign="left"
        if msa:
            self.load_msa(msa,**kwargs)

    def load_msa(self, msa_as_json, msa_header="", fix_terminal_gaps=True,**kwargs):
        """Loads MSA data into this widget.

        Input sequences should be provided in JSON data structure, see read_fasta() method for details
        :param msa_as_json: input sequences
        :param msa_header: a string displayed at the top of the MSA widget to describe it
        """
        self.__add_bars = kwargs.get("if_bars",True)
        self.__bars_function = kwargs.get("bars_function","identity")
        self.__n_columns_of_ten = kwargs.get("n_columns_of_ten",5)
        self.__max_sequence_len = 10*self.__n_columns_of_ten
        self.__blockwise = kwargs.get("show_blockwise",True)

        self.__msa_header = msa_header
        for seq_dic in msa_as_json:
            t = ["", "", ""]
            if "sequence" in seq_dic:
                t[1] = seq_dic["sequence"]
            else:
                continue
            t[2] = seq_dic.get("description", "")
            t[0] = seq_dic.get("id", t[2][0:15])

            self.__msa.append(t)

        if fix_terminal_gaps:
            longest = 0
            for seq in self.__msa:
                longest = max(longest, len(seq[1]))
            for seq in self.__msa:
                seq[1] += "-" * (longest - len(seq[1]))
        n_sect = self.__count_sections()
        self.__sequences_split_to_columns = []
        for i_section in range(n_sect):
            section = []
            for seq in self.__msa:
                section.append(self.__sequence_fragment(seq[1], i_section))
            self.__sequences_split_to_columns.append(section)
        self.__create_widget()

    @property
    def secondary_structure(self):
        """Protein / nucleotide secondary structure - for coloring purposes only

        :getter: returns the secondary structure
        :setter: sets secondary structure string for this sequence
        :type: string
        """
        s = ""
        for w in self.__subwidgets:
            s += w.secondary_structure
        return s

    @secondary_structure.setter
    def secondary_structure(self, hec_string):
        m = self.__max_sequence_len
        substr = [hec_string[i:i + m] for i in range(0, len(hec_string), m)]
        i = 0
        for w in self.__subwidgets:
            print(substr[i])
            w.secondary_structure = substr[i]
            i += 1

    @property
    def msa_header(self):
        """Header line for this MSA

        :getter: returns the header line displayed by the widget
        :setter: sets the new header line string
        :type: string
        """
        return self.__msa_header

    @msa_header.setter
    def msa_header(self, new_header):
        self.__msa_header = new_header
        document["header-subwidget-0-" + self.__element_id].innerHTML = ">" + new_header

    def add_to_region(self, region_name, which_sequence, if_show_region=True, **kwargs):
        """
        Add a block of amino acids/nucleotides to a sequence region

        This method calls :meth:`SequenceViewer.add_to_region` method of an appropriate
        :class:`SequenceViewer` panel of this widget.
        :param region_name: name of this sequence region
        :param which_sequence: (``integer``) index of a sequence to mark a region; use ``0`` (the default)
            to mark a region on all sequences shown by this widget
        :param if_show_region: if True, the sequence region will be made visible after this change
        :param kwargs: see :meth:`SequenceViewer.add_to_region` documentation
        """

        for w in self.__subwidgets:
            kwargs["show_in_legend"] = False if w != self.__subwidgets[-1] else True
            w.add_to_region(region_name, which_sequence, if_show_region=if_show_region, **kwargs)

    def region_tooltip(self, region_name, tooltip):
        """ Sets a text that will show up in a tooltip

        The given text will be displayed in a tooltip box when a user hoovers the given sequence region
        with a mouse pointer. Use empty string to clear a tooltip

        :param region_name: name of a sequence region that needs a tooltip
        :param tooltip: tooltip text
        """
        for subw in self.__subwidgets:
            subw.region_tooltip(region_name, tooltip)

    def aa_composition(self, i_column):
        """ Returns amino acid composition of a given column of this alignment.

        :param i_column: index of an alignment column (from 0)
        :return: a dictionary with single-letter characters as keys and integer counts as avalues
        """
        aa = {k: 0 for k in
              ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'Y', 'V', 'W', 'X',
               '-']}
        for s in self.__msa:
            aa[s[1][i_column]] += 1
        return aa

    def identity_fraction(self, i_column):
        """ Computes sequence identity fraction at a given position for the most probable residue
        :param i_column: index of an alignment column (from 0)
        :return: a two-tuple of the most probable residue code and the fraction of sequences it has been observed
            in that column
        """
        best = 'A'
        best_cnt = 0
        sum = 0
        aa = self.aa_composition(i_column)
        for k, v in aa.items():
            if v > best_cnt:
                best_cnt = v
                best = k
            sum += v
        return best, best_cnt / float(sum)

    def hydrophobicity(self, i_column):
        """ Computes average hydrophobicity at a given position for the most probable residue

        :param i_column: index of an alignment column (from 0)
        :return: average hydrophobicity according to  Kyte & Doolittle scale
        """
        avg = 0
        cnt = 0
        for k, v in self.aa_composition(i_column).items():
            if k != '-':
                avg += kd_hydrophobicity[k] * v
                cnt += v
        return avg / cnt if cnt != 0 else 0

    def shannon_entropy(self, i_column):
        """ Computes Shannon entropy for a given column of this alignment.

        :param i_column: index of an alignment column (from 0)
        :return: information entropy value in the range of [0,1]
        """
        sum = 0.0
        total = 0.0
        for k, v in self.aa_composition(i_column).items():
            if k != '-' and v > 0: total += v
        for k, v in self.aa_composition(i_column).items():
            if k != '-' and v > 0:
                v /= total
                sum -= v * math.log(v)
        return sum

    def colors_by_scheme(self, color_scheme, which_sequence=0, **kwargs):
        """Returns a vector of colors to color this MSA.

        This method calculates color schemes based on MSA composition rather than on a single amino acid type.
        To color residues by chemical type, use method from :class:`SequenceViewer` class

        :param color_scheme: a color scheme name; known schemes are listed below
        :param which_sequence: a sequence to be used as a reference;
        :param kwargs: see below

        :Known color schemes:
          * *secondary* -- color by secondary structure which must be provided by a :meth:`secondary_structure` setter
          * *identity* -- color scale based on the sequence identity (conservation) of a given MSA column
          * *entropy* -- color scale based on the Shanon entropy of a given MSA column
          * *hydrophobicity* -- color scale based on the average hydrophobicity of a given MSA column
          * *mutations* -- color amino acids that are very unlikely in a given MSA column

        :Keyword Arguments:
            * *palette_name* (``string``) --
              name of a color palette used to convert values into colors
            * *neutral_color* (``string``) --
              a color to be used when no color can be assigned; a typical choice is
              ``"black"`` to color letters and ``"white"`` for background

        :return: ``list[str]`` list of ``n_res`` colors, where  ``n_res`` is the length of the selected sequence
          if a given ``color_scheme`` is incorrect, an emtpy list is returned
        """

        n = len(self.__msa[which_sequence][1])
        neutral_color = kwargs.get("neutral_color", "white")
        if color_scheme == 'secondary':
            return SequenceViewer.secondary_structure_colors(self.secondary_structure, neutral_color)
        elif color_scheme == 'identity':
            palette = colormap_by_name(kwargs.get("palette_name", "pinks"), 0, 1)
            return [str(palette.color(self.identity_fraction(i)[1])) for i in range(n)]
        elif color_scheme == 'entropy':
            palette = colormap_by_name(kwargs.get("palette_name", "pinks"), 0, 1)
            return [str(palette.color(self.shannon_entropy(i))) for i in range(n)]
        elif color_scheme == "hydrophobicity":
            palette = colormap_by_name(kwargs.get("palette_name", "pinks"), -4.5, 4.5)
            return [str(palette.color(self.hydrophobicity(i))) for i in range(n)]
        elif color_scheme == "mutations":
            aa_cnts = []
            most_popular = []
            for i_column in range(n):
                aa_cnts.append(self.aa_composition(i_column))  # amino acid composition of a column
                m = [0, 0]  # most popular aa in that column
                for aa, cnt in aa_cnts[-1].items():
                    if cnt > m[0]: m[0], m[1] = cnt, aa
                most_popular.append(m)
            conserved_column = len(self.__msa) * 0.9  # arbitrary choice: conserved cols have 90% of the same AA
            all_clrs = []
            for seq in self.__msa:
                clrs = []
                seq = seq[1]
                for i_column in range(len(seq)):
                    if most_popular[i_column][0] >= conserved_column and seq[i_column] != most_popular[i_column][1]:
                        clrs.append("red")
                    else:
                        clrs.append(neutral_color)
                all_clrs.append(clrs)
            return all_clrs
        else:
            return []

    def color_sequences(self, color_scheme, **kwargs):
        """Color letters of this MSA

        :param color_scheme: either a color scheme name or a list of colors separately for each sequence:
           - (``string``) -- a color scheme name the available color schemes are listed in :meth:`colors_by_scheme`
             method documentation
           - (``list[list[float]]``) -- list of values to be converted to colors with a given palette
           - (``list[list[string]]``) -- list of colors to be used directly to color this MSA
        :param kwargs: see below

        :Keyword Arguments:
            * *palette_name* (``string``) --
              name of a color palette used to convert values into colors
            * *neutral_color* (``string``) --
              a color to be used when no color can be assigned; black is used by default
        """
        if "neutral_color" not in kwargs: kwargs["neutral_color"] = "black"
        self.__color(color_scheme, "color_sequence", **kwargs)

    def color_background(self, color_scheme, **kwargs):
        """Color letter background of this MSA

        :param color_scheme: either a color scheme name or a list of colors separately for each sequence:
           - (``string``) -- a color scheme name the available color schemes are listed in :meth:`colors_by_scheme`
             method documentation
           - (``list[float]``) -- list of values to be converted to colors with a given palette;
             the same color will be used for a given column
           - (``list[list[float]]``) -- list of values to be converted to colors with a given palette
           - (``list[list[string]]``) -- list of colors to be used directly to color this MSA
        :param kwargs: see below

        :Keyword Arguments:
            * *palette_name* (``string``) --
              name of a color palette used to convert values into colors
            * *neutral_color* (``string``) --
              a color to be used when no color can be assigned; white is used by default
        """
        if "neutral_color" not in kwargs: kwargs["neutral_color"] = "white"
        self.__color(color_scheme, "color_background", **kwargs)

    def __color(self, color_scheme, function, **kwargs):

        # The first case is a 2D array of real values or 2D array of color names
        # these values can come from any source, in particular can be returned by colors_by_scheme() method
        plt = kwargs.get("palette_name","pinks")
        if isinstance(color_scheme, list) and isinstance(color_scheme[0], list):
            palette = colormap_by_name(plt, 0, 5)
            first = 0
            for w in self.__subwidgets:
                sub_seq = w.sequence()
                i_seq = 0
                clrs = []
                for ss in sub_seq:
                    last = min(len(ss) + first, len(color_scheme[i_seq]))
                    for i_pos in range(first, last):
                        if isinstance(color_scheme[i_seq][i_pos], str):
                            clrs.append(color_scheme[i_seq][i_pos])
                        else:
                            clrs.append(str(palette.color(color_scheme[i_seq][i_pos])))
                    i_seq += 1
                getattr(w, function)(clrs)
                first += len(ss)
        elif isinstance(color_scheme, list):  # A 1D list of colors: they are the same for each sequence
            i = 0
            for w in self.__subwidgets:
                getattr(w, function)(color_scheme[i:(i + self.__max_sequence_len)])
                i += self.__max_sequence_len
        elif isinstance(color_scheme, str):     # a color scheme name; either handled by an MSA or by a SequenceViewer
            if color_scheme in ["secondary", "identity", "entropy", "hydrophobicity", "mutations"]:
                if "neutral_color" not in kwargs: kwargs["neutral_color"] = "white"
                self.__color(self.colors_by_scheme(color_scheme), function, **kwargs)
            for w in self.__subwidgets:
                getattr(w, function)(color_scheme)
        else:
            print("Unknown color scheme!")

    def __count_sections(self):
        max_len = 0
        for seq in self.__msa:
            max_len = max(max_len, len(seq[1]))
        return math.ceil(max_len / self.__max_sequence_len)

    def __sequence_fragment(self, the_sequence, which_section):

        nmax = len(self.__msa[0][1])

        if which_section * self.__max_sequence_len < nmax:
            seq_fragment = the_sequence[
                           which_section * self.__max_sequence_len: (which_section + 1) * self.__max_sequence_len]
        else:
            seq_fragment = the_sequence[which_section * self.__max_sequence_len: nmax]

        return seq_fragment

    def __color_sequence_event(self, evt):
        what = evt.target.id
        print("sequence colored by", what)
        self.color_sequences(what)

    def __color_background_event(self, evt):
        what = evt.target.id
        print("background colored by", what)
        self.color_background(what)

    def __change_bars_event(self, evt):
        what = evt.target.id
        print("bars function is", what)
        self.change_bars(what)

    def __ruler_text(self, number, first):
        two_template = "....:...%d|"
        three_template = "....:..%d|"
        four_template = "....:.%d|"
        if number * 10 + first - 1 < 100:
            return two_template % (number * 10 + first - 1)
        if number * 10 + first - 1 < 1000:
            return three_template % (number * 10 + first - 1)
        if number * 10 + first - 1 < 10000:
            return four_template % (number * 10 + first - 1)

    def __change_one_bars(self, what, i,spaces):
        bars_id = ("bars-%d-" % i) + self.__element_id
        ruler_id = ("ruler-%d-" % i) + self.__element_id
        drawing = HtmlViewport(document[bars_id], 0, 0, document[ruler_id].width, 20)
        pl = Plot(drawing, 0, 500, 0, 20, 0.0, 63.0, 0.0, 1.0, axes_definition="UBLR")
        data = []
        data_x = []

        for c in range(max(spaces + 3, 9)):
            data.append(0)
            data_x.append(c)
        cnt = 0
        for cc in range(c, self.__n_columns_of_ten * 10 + c + cnt):
            if cc - c >= len(self.__sequences_split_to_columns[i][0]):
                break
            data.append(self.__bars_dict[what](cc - c)[1] if isinstance(self.__bars_dict[what](cc - c), tuple) else
                        self.__bars_dict[what](cc - c))
            data_x.append(cc + cnt)
            if (cc + 1 - c) % 10 == 0 and self.__blockwise:
                data_x.append(cc + 1)
                data.append(0)
                cnt += 1

        pl.bars(data_x, data, width=0.5, adjust_range="y")
        pl.draw(axes=False)
        drawing.close()

    def change_bars(self,what):

        for i in range(len(self.__sequences_split_to_columns)):
            bars_id = ("bars-%d-" % i) + self.__element_id
            ruler_id = ("ruler-%d-" % i) + self.__element_id
            if bars_id in document:
                document[bars_id].innerHTML=""
            self.__change_one_bars(what,i)

    def async_viewer(self,res):
        #adding ruler 
        i=self.__i
        first=self.__first

        div_id = ("subwidget-%d-" % i) + self.__element_id
        ruler_id = ("ruler-%d-" % i) + self.__element_id
        #print(self.__msa)
        spaces_len = len (self.__msa[0][0][:15])
        for j in range(len(self.__msa)):
            if len(self.__msa[j][0][:15])>spaces_len:
                spaces_len=len(self.__msa[j][0][:15])
        ruler_text = "&nbsp;"* max(spaces_len+2,8)
        #ruler_text =""
        for r in range(self.__n_columns_of_ten):
            ruler_text+=self.__ruler_text(r+1,first)
            if (r+1)*10>len(self.__sequences_split_to_columns[i][0]): break
        # adding SequenceViewer
        document[self.__element_id] <= html.DIV('', id=div_id)
        seq_viewer = SequenceViewer(div_id, self.__msa_header, self.__sequences_split_to_columns[i],
            first_residue_id=first,show_blockwise=self.__blockwise ,show_menu=False, show_header=(True if i == 0 else False),
            if_add_style=(True if i == 0 else False),n_columns_of_ten=self.__n_columns_of_ten)
        #wid = numbers_div.width
        #print("HHH ",wid)

        #ruler = html.DIV()
        ruler  = html.DIV(ruler_text, id=ruler_id,Class="SequenceViewer-fasta",style={"textAlign":"left"})
        #ruler_placeholder = html.DIV("&nbsp;",id="ruler_placeholder",Class="SequenceViewer-numbers",style={"width":"%dpx"%wid})
        #ruler <= ruler_placeholder
        #ruler <= ruler_fasta
        document[div_id].children[0].insertBefore(ruler,document["top-row-subwidget-%d-show_msa"%i].nextSibling)
        self.__subwidgets.append(seq_viewer)
        # --- Now we change the width of a SequenceViewer: it assumes 40px for the left columns of sequence numbers
        # --- MSAViewer stores sequence IDs in that column, 150px wide. Therefore 90px must be added
        w = document["SequenceViewer-" + div_id].style.width
        w = document["header-" + div_id].style.width
        w = int(w.replace("px", "")) + 90
        document["SequenceViewer-" + div_id].style.width = str(w) + "px"
        document["SequenceViewer-" + div_id].style.maxWidth = str(w) + "px"
        document[self.__element_id].style.width = str(w) + "px"
        document[self.__element_id].style.maxWidth = str(w) + "px"
        numbers_div = document["numbers-" + seq_viewer.element_id]
        numbers_div.style.width = "150px"
        numbers_div.innerHTML = ""
        for seq in self.__msa:
            numbers_div <= html.SPAN(seq[0][:15]) + html.BR()
        
        #adding bars 

        if self.__add_bars:
            bars_id = ("bars-%d-" % i) + self.__element_id
            bars = html.SPAN("", id=bars_id,Class="SequenceViewer-fasta",style={"width":document[ruler_id].width,"height":20})
            if "legend-box-subwidget-%d-show_msa"%i in document:
                document[div_id].children[0].insertBefore(bars,document["legend-box-subwidget-%d-show_msa"%i])
            else: document[div_id] <=bars
            self.__change_one_bars(self.__bars_function,i,spaces_len)
        

        if self.__i == 0:
            self.menu = MenuWidget("menu-" + "subwidget-0-" + self.__element_id,
             {"color letters": {
                 "clear": self.__color_sequence_event,
                 "secondary": self.__color_sequence_event,
                 "clustal": self.__color_sequence_event,
                 "maeditor": self.__color_sequence_event,
                 "identity": self.__color_sequence_event,
                 "hydrophobicity": self.__color_sequence_event,
                 "entropy": self.__color_sequence_event,
                 "mutations": self.__color_sequence_event
             },
                 "color background": {
                     "clear": self.__color_background_event,
                     "secondary": self.__color_background_event,
                     "clustal": self.__color_background_event,
                     "maeditor": self.__color_background_event,
                     "identity": self.__color_background_event,
                     "hydrophobicity": self.__color_background_event,
                     "entropy": self.__color_background_event,
                     "mutations": self.__color_background_event
                 },
                 "bars function": {
                     "identity": self.__change_bars_event,
                     "hydrophobicity": self.__change_bars_event,
                     "entropy": self.__change_bars_event
                 }
             },
             width=150)
            
        self.__first += len(self.__sequences_split_to_columns[self.__i][0])
        self.__i+=1

    def __create_widget(self):
        document[self.__element_id].innerHTML = ""
        self.__first = 1
        self.__i = 0

        for i in range(len(self.__sequences_split_to_columns)):            
            run_async_func(self.async_viewer)


        
