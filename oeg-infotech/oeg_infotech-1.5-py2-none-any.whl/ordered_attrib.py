"""Ordered attrib patch for py2.

https://stackoverflow.com/questions/2741480/can-elementtree-be-told-to-preserve-the-order-of-attributes
"""
import xml.etree.ElementTree as ET


def get_items(elem):
    """Sort attribs by given order, if set."""
    if not hasattr(elem, 'ordered_attributes'):
        return sorted(elem.items())

    items = dict(elem.items())
    return [(attr, items[attr]) for attr in elem.ordered_attributes if attr in items]


def _serialize_xml(write, elem, encoding, qnames, namespaces, short_empty_elements=None):
    """Monkey patch for dump ordered attributes for xml element."""
    tag = elem.tag
    text = elem.text
    if tag is ET.Comment:
        write("<!--%s-->" % ET._encode(text, encoding))
    elif tag is ET.ProcessingInstruction:
        write("<?%s?>" % ET._encode(text, encoding))
    else:
        tag = qnames[tag]
        if tag is None:
            if text:
                write(ET._escape_cdata(text, encoding))
            for e in elem:
                _serialize_xml(write, e, encoding, qnames, None)
        else:
            write("<" + tag)
            items = get_items(elem)
            if items or namespaces:
                if namespaces:
                    for v, k in sorted(namespaces.items(),
                                       key=lambda x: x[1]):  # sort on prefix
                        if k:
                            k = ":" + k
                        write(" xmlns%s=\"%s\"" % (
                            k.encode(encoding),
                            ET._escape_attrib(v, encoding)
                            ))
                for k, v in items:
                    if isinstance(k, ET.QName):
                        k = k.text
                    if isinstance(v, ET.QName):
                        v = qnames[v.text]
                    else:
                        v = ET._escape_attrib(v, encoding)
                    write(" %s=\"%s\"" % (qnames[k], v))
            if text or len(elem):
                write(">")
                if text:
                    write(ET._escape_cdata(text, encoding))
                for e in elem:
                    _serialize_xml(write, e, encoding, qnames, None)
                write("</" + tag + ">")
            else:
                write(" />")
    if elem.tail:
        write(ET._escape_cdata(elem.tail, encoding))


ET._serialize_xml = _serialize_xml
ET._serialize["xml"] = _serialize_xml  # dump root elem
