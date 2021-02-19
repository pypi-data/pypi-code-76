"""WELDS section."""
from .ordered_attrib import ET
from .base import DistItem, Section as InfotechSection, to_int
from . import reverse_orient, XmlFormat


class Item(DistItem):  # pylint: disable=too-many-instance-attributes
    """Weld item from <WELDS> xml section.

    <WLD
      IDTYPEOBJ="2097791" ODOMETER="0"
      NUM_TUBE="1" DL_TUBE="752" THICK="19.5" PSH1="11.6" PSH2="" REM=""
    />
    """

    xml_node_name = 'WLD'
    field_number = 'NUM_TUBE'
    field_length = 'DL_TUBE'
    field_thick = 'THICK'
    field_hor1 = 'PSH1'
    field_hor2 = 'PSH2'

    # IUST fields
    field_iust_type = 'IUST_TYPE'
    field_iust_geo = 'IUST_GEO'
    field_iust_oval = 'IUST_OVAL'
    field_iust_radius = 'IUST_RADIUS'
    field_iust_isolation = 'IUST_ISOLATION'
    field_iust_manufacturer = 'IUST_MANUFACTURER'
    field_iust_steel_class = 'IUST_STEEL_CLASS'
    field_iust_koef_press = 'IUST_KOEF_PRESS'
    field_iust_koef_pipe = 'IUST_KOEF_PIPE'
    field_iust_koef_mater = 'IUST_KOEF_MATER'
    field_iust_steel_mark = 'IUST_STEEL_MARK'
    field_iust_ballast = 'IUST_BALLAST'
    field_iust_pipe_category = 'IUST_PIPE_CATEGORY'
    field_iust_prod_method = 'IUST_PROD_METHOD'
    field_iust_prod_standart = 'IUST_PROD_STANDART'
    field_iust_prod_country = 'IUST_PROD_COUNTRY'
    field_iust_cover_type = 'IUST_COVER_TYPE'

    def __init__(self, xml_format=XmlFormat.Infotech):
        """Weld section item with given format."""
        DistItem.__init__(self)

        self.xml_format = xml_format
        self.number = ''
        self.length = ''
        self.thick = ''
        self.hor1 = ''
        self.hor2 = ''

        self.iust_type = ''
        self.iust_geo = ''
        self.iust_oval = ''
        self.iust_radius = ''
        self.iust_isolation = ''
        self.iust_manufacturer = ''
        self.iust_steel_class = ''
        self.iust_koef_press = ''
        self.iust_koef_pipe = ''
        self.iust_koef_mater = ''
        self.iust_steel_mark = ''
        self.iust_ballast = ''
        self.iust_pipe_category = ''
        self.iust_prod_method = ''
        self.iust_prod_standart = ''
        self.iust_prod_country = ''
        self.iust_cover_type = ''

    @classmethod
    def from_xml(cls, xml_item, xml_format=XmlFormat.Infotech):
        """Create weld item from existing xml element."""
        obj = cls(xml_format=xml_format)
        obj.fill_from_xml(xml_item)

        obj.number = xml_item.attrib[Item.field_number]
        obj.length = to_int(xml_item.attrib[Item.field_length])
        obj.thick = xml_item.attrib[Item.field_thick]
        obj.hor1 = xml_item.attrib[Item.field_hor1]
        obj.hor2 = xml_item.attrib[Item.field_hor2]

        if obj.xml_format == XmlFormat.Iust:
            obj.iust_type = xml_item.attrib.get(Item.field_iust_type, '')
            obj.iust_geo = xml_item.attrib.get(Item.field_iust_geo, '')
            obj.iust_oval = xml_item.attrib.get(Item.field_iust_oval, '')
            obj.iust_radius = xml_item.attrib.get(Item.field_iust_radius, '')
            obj.iust_isolation = xml_item.attrib.get(Item.field_iust_isolation, '')
            obj.iust_manufacturer = xml_item.attrib.get(Item.field_iust_manufacturer, '')
            obj.iust_steel_class = xml_item.attrib.get(Item.field_iust_steel_class, '')
            obj.iust_koef_press = xml_item.attrib.get(Item.field_iust_koef_press, '')
            obj.iust_koef_pipe = xml_item.attrib.get(Item.field_iust_koef_pipe, '')
            obj.iust_koef_mater = xml_item.attrib.get(Item.field_iust_koef_mater, '')
            obj.iust_steel_mark = xml_item.attrib.get(Item.field_iust_steel_mark, '')
            obj.iust_ballast = xml_item.attrib.get(Item.field_iust_ballast, '')
            obj.iust_pipe_category = xml_item.attrib.get(Item.field_iust_pipe_category, '')
            obj.iust_prod_method = xml_item.attrib.get(Item.field_iust_prod_method, '')
            obj.iust_prod_standart = xml_item.attrib.get(Item.field_iust_prod_standart, '')
            obj.iust_prod_country = xml_item.attrib.get(Item.field_iust_prod_country, '')
            obj.iust_cover_type = xml_item.attrib.get(Item.field_iust_cover_type, '')

        return obj

    def end(self):
        """Return distance for end of tube."""
        return self.dist + self.length

    def as_csv_row(self, infotech, with_navigation=False):
        """Return list of field values for csv string."""
        columns = [
          self.number,
          "{}".format(self.length),
          self.thick.replace('.', ','),
          self.hor1.replace('.', ','),
          self.hor2.replace('.', ','),
        ]
        base_columns = DistItem.as_csv_row(self, infotech, with_navigation=with_navigation)

        return base_columns[:2] + columns + base_columns[2:]

    def reverse(self, total_length, object_index):
        """Reverse weld."""
        self.dist = total_length - (self.dist + self.length)
        self.number = "{}".format(object_index)
        self.hor1 = reverse_orient(self.hor1)
        self.hor2 = reverse_orient(self.hor2)

    def add_xml_child(self, parent_node):
        """Create and add xmml node of weld to parent xml node."""
        node = ET.SubElement(parent_node, Item.xml_node_name)
        DistItem.base_xml(self, node)
        node.set(Item.field_number, self.number)
        node.set(Item.field_length, "{}".format(self.length))
        node.set(Item.field_thick, self.thick)
        node.set(Item.field_hor1, self.hor1)
        node.set(Item.field_hor2, self.hor2)

        if self.xml_format == XmlFormat.Iust:
            node.set(Item.field_iust_type, self.iust_type)
            node.set(Item.field_iust_geo, self.iust_geo)
            node.set(Item.field_iust_oval, self.iust_oval)
            node.set(Item.field_iust_radius, self.iust_radius)
            node.set(Item.field_iust_isolation, self.iust_isolation)
            node.set(Item.field_iust_manufacturer, self.iust_manufacturer)
            node.set(Item.field_iust_steel_class, self.iust_steel_class)
            node.set(Item.field_iust_koef_press, self.iust_koef_press)
            node.set(Item.field_iust_koef_pipe, self.iust_koef_pipe)
            node.set(Item.field_iust_koef_mater, self.iust_koef_mater)
            node.set(Item.field_iust_steel_mark, self.iust_steel_mark)
            node.set(Item.field_iust_ballast, self.iust_ballast)
            node.set(Item.field_iust_pipe_category, self.iust_pipe_category)
            node.set(Item.field_iust_prod_method, self.iust_prod_method)
            node.set(Item.field_iust_prod_standart, self.iust_prod_standart)
            node.set(Item.field_iust_prod_country, self.iust_prod_country)
            node.set(Item.field_iust_cover_type, self.iust_cover_type)

        return node


class Section(InfotechSection):
    """<WELDS> xml section."""

    tag = 'WELDS'

    def __init__(self, infotech):
        """Weld section of infotech object."""
        InfotechSection.__init__(self, infotech, Item, Section.tag)

        self.item_attributes = DistItem.dist_attribs + [
          Item.field_number,
          Item.field_length,
          Item.field_thick,
          Item.field_hor1,
          Item.field_hor2,
          DistItem.field_comment,
        ] + DistItem.coords_attribs

        if infotech.xml_format == XmlFormat.Iust:
            self.item_attributes += [
              Item.field_iust_type,
              Item.field_iust_geo,
              Item.field_iust_oval,
              Item.field_iust_radius,
              Item.field_iust_isolation,
              Item.field_iust_manufacturer,
              Item.field_iust_steel_class,
              Item.field_iust_koef_press,
              Item.field_iust_koef_pipe,
              Item.field_iust_koef_mater,
              Item.field_iust_steel_mark,
              Item.field_iust_ballast,
              Item.field_iust_pipe_category,
              Item.field_iust_prod_method,
              Item.field_iust_prod_standart,
              Item.field_iust_prod_country,
              Item.field_iust_cover_type,
            ]

    def as_csv(self, with_navigation=False):
        """Dump weld section content as csv string."""
        column_titles = [
          'Name', 'Distance', 'Tube number', 'Tube length', 'Thick', 'Weld1', 'Weld2', 'Comment'
        ]
        return InfotechSection.as_csv_body(self, 'Welds table', column_titles, with_navigation=with_navigation)

    def add_tube(self, objtype, tube_dist, tube_length):
        """Add new tube with given type, dist and length to thr end of record."""
        item = Item()

        item.objtype = objtype
        item.dist = tube_dist
        item.comment = ''

        item.number = ''
        item.length = tube_length
        item.thick = self.items[-1].thick
        item.hor1 = ''
        item.hor2 = ''

        self._items.append(item)
