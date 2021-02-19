"""LINEOBJS section."""
from .ordered_attrib import ET
from .base import Section as InfotechSection, DistItem
from .codes import Feature
from . import XmlFormat


REVERTED = {
  Feature.WATER_START: Feature.WATER_END,
  Feature.WATER_END: Feature.WATER_START,

  Feature.METALL_CASE_START: Feature.METALL_CASE_END,
  Feature.METALL_CASE_END: Feature.METALL_CASE_START,

  Feature.KOMPOS_CASE_START: Feature.KOMPOS_CASE_END,
  Feature.KOMPOS_CASE_END: Feature.KOMPOS_CASE_START,

  Feature.CASE_START: Feature.CASE_END,
  Feature.CASE_END: Feature.CASE_START,

  Feature.PRIGRUZ_START: Feature.PRIGRUZ_END,
  Feature.PRIGRUZ_END: Feature.PRIGRUZ_START,

  Feature.TURN_START: Feature.TURN_END,
  Feature.TURN_END: Feature.TURN_START,

  Feature.TURN_SEGM_START: Feature.TURN_SEGM_END,
  Feature.TURN_SEGM_END: Feature.TURN_SEGM_START,
}


class Item(DistItem):
    """Object item from <LINEOBJS> xml section.

    <PLOBJ
      IDTYPEOBJ="990006537229" ODOMETER="0" NAME_MARKER="M1" L_LCH="" REM=""
    />
    """

    xml_node_name = 'PLOBJ'
    field_name_marker = 'NAME_MARKER'
    field_piketag_km = 'L_LCH'

    # IUST fields
    field_iust_type = 'IUST_TYPE'

    def __init__(self, xml_format=XmlFormat.Infotech):
        """Lineobj section item with given format."""
        DistItem.__init__(self)
        self.xml_format = xml_format

        self.marker_name = ''
        self.piketag_km = ''

        self.iust_type = ''

    @classmethod
    def from_xml(cls, xml_item, xml_format=XmlFormat.Infotech):
        """Create lineobj item from existing xml element."""
        obj = cls(xml_format=xml_format)
        obj.fill_from_xml(xml_item)

        if obj.xml_format == XmlFormat.Iust:
            obj.iust_type = xml_item.attrib.get(Item.field_iust_type, '')

        obj.marker_name = xml_item.attrib[Item.field_name_marker]
        obj.piketag_km = xml_item.attrib[Item.field_piketag_km]

        return obj

    def as_csv_row(self, infotech, with_navigation=False):
        """Return list of lineobj field values for csv string."""
        columns = [self.marker_name, self.piketag_km]
        base_columns = DistItem.as_csv_row(self, infotech, with_navigation=with_navigation)

        return base_columns[:2] + columns + base_columns[2:]

    def add_xml_child(self, parent_node):
        """Create and add lineobj xml node of object to parent xml node."""
        node = ET.SubElement(parent_node, Item.xml_node_name)
        DistItem.base_xml(self, node)

        if self.xml_format == XmlFormat.Iust:
            node.set(Item.field_iust_type, self.iust_type)

        node.set(Item.field_name_marker, self.marker_name)
        node.set(Item.field_piketag_km, self.piketag_km)

        return node

    def reverse(self, total_length, object_index):
        """Reverse line object."""
        DistItem.reverse(self, total_length, object_index)
        if self.objtype in REVERTED:
            self.objtype = REVERTED[self.objtype]


class Section(InfotechSection):
    """<LINEOBJS> xml section."""

    tag = 'LINEOBJS'

    def __init__(self, infotech):
        """Lineobj section of infotech object."""
        InfotechSection.__init__(self, infotech, Item, Section.tag)

        self.item_attributes = DistItem.dist_attribs + [
          Item.field_name_marker,
          Item.field_piketag_km,
          DistItem.field_comment,
        ] + DistItem.coords_attribs

        if infotech.xml_format == XmlFormat.Iust:
            self.item_attributes.append(Item.field_iust_type)

    def as_csv(self, with_navigation=False):
        """Dump lineobj section content as csv string."""
        column_titles = [
          'Name', 'Distance', 'Marker', 'Piketag', 'Comment'
        ]
        return InfotechSection.as_csv_body(self, 'Line objects table', column_titles, with_navigation=with_navigation)
