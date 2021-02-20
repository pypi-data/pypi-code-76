from visualife.core.shapes import arrow
from visualife.core.styles import get_color
from visualife.widget import TooltipWidget
from browser import document,html


class SequenceFeaturesBar:

    def __init__(self, viewport, sequence_ids=[], seq_len=0,**kwargs):
        """Draws a sequence features widget.

        This widget displays a sequence or sequences, representing them by a row of featured regions.
        Each region as well as each sequence is identified by a name

        :param viewport: where to draw the widget
        :param sequence_ids: a list of IDs for displayed sequences; sequences can also be added with ``add_sequence()`` method
        :param kwargs: see below

        :Keyword Arguments:
            * *arrow_fill* (``string`` or ``ColorBase``) --
              provides color to fill an arrow; arrow border will be made darker than the given fill
        """
        self.__sequence_ids = {}
        self.__seq_len = seq_len
        self.__seq_annotations = {}
        self.__viewport = viewport
        self.__region_kwargs = {}
        # graphics settings
        self.__margin_x = 10
        self.__arrow_width = 100
        self.__arrow_height = 25
        self.__seq_height = 25
        document <=html.DIV(id="container")
        self.__tooltip = TooltipWidget("sfb-tooltip","container","",150,20)
        for si in sequence_ids:
            self.add_sequence(si ,**kwargs)

    def add_sequence(self, seq_name,**kwargs):
        """Adds a new row to this widget.

        Each row represents a protein / nucleic sequence. Annotations for this sequence may be added with
        :meth:`add_to_region` method
        :param seq_name: (``string``) name of a new sequence, it will be displayed by this widget. It's
            also used to identify this sequence in :meth:`add_to_region` method
        :param kwargs: drawing parameters
        """
        desc =  kwargs.get("description",seq_name)
        self.__sequence_ids[seq_name]=desc
        self.__seq_annotations[seq_name] = {}

    def show_tooltip(self,evt):
        """Shows tooltip with description of event target annotation"""
        tokens = evt.target.id.split("-")
        self.__tooltip.tooltip_text="%s %s-%s"%(tokens[-3],tokens[-2],tokens[-1])
        self.__tooltip.show(evt.clientX, evt.clientY)

    def __calculate_regions(self,regions):
        reg_start_lenght = []
        begin = self.__margin_x*2 + self.__arrow_width
        full_len = self.__viewport.get_width()-begin
        #print(regions)
        for reg,spans in regions.items():
         #   print(spans)
            for span in spans:
                start = span[0]
                leng = span[1]-span[0]
                draw_len = full_len*leng/self.__seq_len
                draw_start = begin+full_len*start/self.__seq_len
                reg_start_lenght.append((reg,span[0],span[1],draw_start,draw_len))

        return reg_start_lenght

    def draw(self):
        """Draws whole widget"""

        n = 0
    
        arrow_center_x = self.__arrow_width/2.0 +self.__margin_x
        for si in self.__sequence_ids:
            n += 1
            y_step = n * self.__seq_height
            #parms = self.__seq_kwargs[si]
            parms={}
            fill = get_color(parms.get("arrow_fill","white"))
            strk = fill.create_darker(0.3) if "arrow_fill" in parms else "black"
            arrow(self.__viewport, "arrow-%s" % si, self.__arrow_width, self.__arrow_height, self.__arrow_height, 0,
                  **dict(cx=70, cy=y_step, fill=fill, stroke=strk, stroke_width=parms.get("stroke_width", 1)))
            arrow_center_y = y_step - self.__arrow_height/2.0
            self.__viewport.text("label-%s" % si, arrow_center_x, arrow_center_y, self.__sequence_ids[si])
            start_and_len = self.__calculate_regions(self.__seq_annotations[si])
            begin = self.__margin_x*2 + self.__arrow_width
            full_len = self.__viewport.get_width()-begin
            self.__viewport.rect("rect-%s" % n, begin, y_step-self.__arrow_height, full_len, self.__seq_height,fill="whitesmoke",stroke="lightgrey")

            for reg,start,leng,draw_start,draw_len in start_and_len:
                self.__viewport.rect("rect-%s-%d-%d" % (reg,start,leng), draw_start, y_step-self.__arrow_height, draw_len, self.__seq_height,**(self.__region_kwargs[reg]),Class="region")


        self.__viewport.close()
        for rect in document.select("rect"):
            if rect.attrs.get("class","")=="region":
                rect.bind("mousemove",self.show_tooltip)
                rect.bind("mouseout",self.__tooltip.hide)


    def add_to_region(self, sequence_name, region_name, if_show_region=True, **kwargs):
        """Adds parts of sequence to the region_name of given sequence"""
        if region_name not in self.__region_kwargs:
            self.__region_kwargs[region_name]=kwargs
        if "first_pos" in kwargs:
            pos_from = kwargs["first_pos"]
            pos_to = kwargs.get("last_pos", pos_from + 1)
        elif "last_pos" in kwargs:
            pos_to = kwargs["last_pos"]
            pos_from = kwargs.get("first_pos", pos_to - 1)
        if sequence_name not in self.__seq_annotations:
            self.__seq_annotations[sequence_name]={}
        if region_name not in self.__seq_annotations[sequence_name]:
            self.__seq_annotations[sequence_name][region_name]=[]
        self.__seq_annotations[sequence_name][region_name].append((pos_from,pos_to))
            
    def delete_region(self, sequence_name, region_name):
        """Deletes region for the given sequence"""
        self.__seq_annotations[sequence_name][region_name]=[]

    def delete_regions(self):
        pass
        