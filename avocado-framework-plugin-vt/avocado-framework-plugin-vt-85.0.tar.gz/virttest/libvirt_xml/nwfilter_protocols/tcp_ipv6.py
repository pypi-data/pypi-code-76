"""
tcp-ipv6 protocl support class(es)

http://libvirt.org/formatnwfilter.html#nwfelemsRulesProtoTCP-ipv6
"""

from virttest.libvirt_xml import accessors, xcepts
from virttest.libvirt_xml.nwfilter_protocols import base


class Tcp_ipv6(base.TypedDeviceBase):

    """
    Create new Tcp_ipv6 xml instances

    Properties:
        attrs: ``libvirt_xml.nwfilter_protocols.Tcp_ipv6.Attr`` instance
    """

    __slots__ = ('attrs',)

    def __init__(self, type_name='file', virsh_instance=base.base.virsh):
        accessors.XMLElementNest('attrs', self, parent_xpath='/',
                                 tag_name='tcp_ipv6', subclass=self.Attr,
                                 subclass_dargs={
                                     'virsh_instance': virsh_instance})
        super(Tcp_ipv6, self).__init__(protocol_tag='tcp-ipv6',
                                       type_name=type_name,
                                       virsh_instance=virsh_instance)

    def new_attr(self, **dargs):
        """
        Return a new Attr instance and set properties from dargs

        :param dargs: dict of attributes
        :return: new Attr instance
        """
        new_one = self.Attr(virsh_instance=self.virsh)
        for key, value in list(dargs.items()):
            setattr(new_one, key, value)
        return new_one

    def get_attr(self):
        """
        Return tcp-ipv6 attribute dict

        :return: None if no tcp-ipv6 in xml, dict of tcp-ipv6's attributes.
        """
        try:
            tcp_node = self.xmltreefile.reroot('/tcp-ipv6')
        except KeyError as detail:
            raise xcepts.LibvirtXMLError(detail)
        node = tcp_node.getroot()
        tcp_attr = dict(list(node.items()))

        return tcp_attr

    class Attr(base.base.LibvirtXMLBase):

        """
        Tcp_ipv6 attribute XML class

        Properties:

        srcmacaddr: string, MAC address of sender
        srcipaddr: string, Source IP address
        srcipmask: string, Mask applied to source IP address
        dstipaddr: string, Destination IP address
        dstipmask: string, Mask applied to destination IP address
        srcipfrom: string, Start of range of source IP address
        srcipto: string, End of range of source IP address
        dstipfrom: string, Start of range of destination IP address
        dstipto: string, End of range of destination IP address
        srcportstart: string, Start of range of valid source ports; requires protocol
        srcportend: string, End of range of valid source ports; requires protocol
        dstportstart: string, Start of range of valid destination ports; requires protocol
        dstportend: string, End of range of valid destination ports; requires protocol
        comment: string, text with max. 256 characters
        state: string, comma separated list of NEW,ESTABLISHED,RELATED, INVALID or NONE
        flags: string, TCP-only: format of mask/flags with mask and flags each being a comma separated list of SYN,ACK,URG,PSH,FIN,RST or NONE or ALL
        ipset: The name of an IPSet managed outside of libvirt
        ipsetflags: flags for the IPSet; requires ipset attribute
        """

        __slots__ = ('srcmacaddr', 'srcipaddr', 'srcipmask', 'dstipaddr',
                     'dstipmask', 'srcipfrom', 'srcipto', 'dstipfrom',
                     'dstipto', 'srcportstart', 'srcportend', 'dstportstart',
                     'dstportend', 'dscp', 'comment', 'state', 'flags',
                     'ipset', 'ipsetflags')

        def __init__(self, virsh_instance=base.base.virsh):
            accessors.XMLAttribute('srcmacaddr', self, parent_xpath='/',
                                   tag_name='tcp-ipv6', attribute='srcmacaddr')
            accessors.XMLAttribute('srcipaddr', self, parent_xpath='/',
                                   tag_name='tcp-ipv6', attribute='srcipaddr')
            accessors.XMLAttribute('srcipmask', self, parent_xpath='/',
                                   tag_name='tcp-ipv6', attribute='srcipmask')
            accessors.XMLAttribute('dstipaddr', self, parent_xpath='/',
                                   tag_name='tcp-ipv6', attribute='dstipaddr')
            accessors.XMLAttribute('dstipmask', self, parent_xpath='/',
                                   tag_name='tcp-ipv6', attribute='dstipmask')
            accessors.XMLAttribute('srcipfrom', self, parent_xpath='/',
                                   tag_name='tcp-ipv6', attribute='srcipfrom')
            accessors.XMLAttribute('srcipto', self, parent_xpath='/',
                                   tag_name='tcp-ipv6', attribute='srcipto')
            accessors.XMLAttribute('dstipfrom', self, parent_xpath='/',
                                   tag_name='tcp-ipv6', attribute='dstipfrom')
            accessors.XMLAttribute('dstipto', self, parent_xpath='/',
                                   tag_name='tcp-ipv6', attribute='dstipto')
            accessors.XMLAttribute('srcportstart', self, parent_xpath='/',
                                   tag_name='tcp-ipv6',
                                   attribute='srcportstart')
            accessors.XMLAttribute('srcportend', self, parent_xpath='/',
                                   tag_name='tcp-ipv6', attribute='srcportend')
            accessors.XMLAttribute('dstportstart', self, parent_xpath='/',
                                   tag_name='tcp-ipv6',
                                   attribute='dstportstart')
            accessors.XMLAttribute('dstportend', self, parent_xpath='/',
                                   tag_name='tcp-ipv6', attribute='dstportend')
            accessors.XMLAttribute('dscp', self, parent_xpath='/',
                                   tag_name='tcp-ipv6', attribute='dscp')
            accessors.XMLAttribute('comment', self, parent_xpath='/',
                                   tag_name='tcp-ipv6', attribute='comment')
            accessors.XMLAttribute('state', self, parent_xpath='/',
                                   tag_name='tcp-ipv6', attribute='state')
            accessors.XMLAttribute('flags', self, parent_xpath='/',
                                   tag_name='tcp-ipv6', attribute='flags')
            accessors.XMLAttribute('ipset', self, parent_xpath='/',
                                   tag_name='tcp-ipv6', attribute='ipset')
            accessors.XMLAttribute('ipsetflags', self, parent_xpath='/',
                                   tag_name='tcp-ipv6', attribute='ipsetflags')

            super(self.__class__, self).__init__(virsh_instance=virsh_instance)
            self.xml = '<tcp-ipv6/>'
