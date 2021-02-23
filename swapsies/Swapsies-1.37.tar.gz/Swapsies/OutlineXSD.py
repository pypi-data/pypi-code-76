# ./binding.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2020-06-19 16:18:58.998406 by PyXB version 1.2.6 using Python 3.8.2.final.0
# Namespace AbsentNamespace0

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six
# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:c2f8caa0-b1f4-11ea-b5cf-80e65012546e')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.CreateAbsentNamespace()
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Atomic simple type: RFC822Date
class RFC822Date (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'RFC822Date')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 68, 4)
    _Documentation = None
RFC822Date._CF_pattern = pyxb.binding.facets.CF_pattern()
RFC822Date._CF_pattern.addPattern(pattern='((Mon|Tue|Wed|Thu|Fri|Sat|Sun),\\s*)?\\d\\d?\\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\\s+\\d\\d(\\d\\d)?\\s+\\d\\d:\\d\\d(:\\d\\d)?\\s+([+\\-]?\\d\\d\\d\\d|[A-Z]{2,3})')
RFC822Date._InitializeFacetMap(RFC822Date._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'RFC822Date', RFC822Date)
_module_typeBindings.RFC822Date = RFC822Date

# Atomic simple type: EmailAddress
class EmailAddress (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'EmailAddress')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 74, 4)
    _Documentation = None
EmailAddress._CF_pattern = pyxb.binding.facets.CF_pattern()
EmailAddress._CF_pattern.addPattern(pattern='[a-zA-Z0-9_\\-][a-zA-Z0-9_.\\-]*@[a-zA-Z0-9_\\-][a-zA-Z0-9_.\\-]*')
EmailAddress._InitializeFacetMap(EmailAddress._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'EmailAddress', EmailAddress)
_module_typeBindings.EmailAddress = EmailAddress

# Atomic simple type: Unknown
class Unknown (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Unknown')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 84, 4)
    _Documentation = None
Unknown._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=Unknown, enum_prefix=None)
Unknown.unknown = Unknown._CF_enumeration.addEnumeration(unicode_value='unknown', tag='unknown')
Unknown._InitializeFacetMap(Unknown._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'Unknown', Unknown)
_module_typeBindings.Unknown = Unknown

# Atomic simple type: Version
class Version (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Version')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 90, 4)
    _Documentation = None
Version._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=Version, enum_prefix=None)
Version.n1_0 = Version._CF_enumeration.addEnumeration(unicode_value='1.0', tag='n1_0')
Version.n2_0 = Version._CF_enumeration.addEnumeration(unicode_value='2.0', tag='n2_0')
Version._InitializeFacetMap(Version._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'Version', Version)
_module_typeBindings.Version = Version

# Union simple type: Language
# superclasses pyxb.binding.datatypes.anySimpleType
class Language (pyxb.binding.basis.STD_union):

    """Simple type that is a union of pyxb.binding.datatypes.language, Unknown."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Language')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 80, 4)
    _Documentation = None

    _MemberTypes = ( pyxb.binding.datatypes.language, Unknown, )
Language._CF_pattern = pyxb.binding.facets.CF_pattern()
Language._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=Language)
Language.unknown = 'unknown'                      # originally Unknown.unknown
Language._InitializeFacetMap(Language._CF_pattern,
   Language._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'Language', Language)
_module_typeBindings.Language = Language

# Complex type Body with content type ELEMENT_ONLY
class Body (pyxb.binding.basis.complexTypeDefinition):
    """Complex type Body with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Body')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 25, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element outline uses Python identifier outline
    __outline = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'outline'), 'outline', '__AbsentNamespace0_Body_outline', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 27, 12), )

    
    outline = property(__outline.value, __outline.set, None, None)

    _ElementMap.update({
        __outline.name() : __outline
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Body = Body
Namespace.addCategoryObject('typeBinding', 'Body', Body)


# Complex type Head with content type ELEMENT_ONLY
class Head (pyxb.binding.basis.complexTypeDefinition):
    """Complex type Head with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Head')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 31, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element title uses Python identifier title
    __title = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'title'), 'title', '__AbsentNamespace0_Head_title', False, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 33, 12), )

    
    title = property(__title.value, __title.set, None, None)

    
    # Element dateCreated uses Python identifier dateCreated
    __dateCreated = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'dateCreated'), 'dateCreated', '__AbsentNamespace0_Head_dateCreated', False, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 34, 12), )

    
    dateCreated = property(__dateCreated.value, __dateCreated.set, None, None)

    
    # Element dateModified uses Python identifier dateModified
    __dateModified = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'dateModified'), 'dateModified', '__AbsentNamespace0_Head_dateModified', False, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 35, 12), )

    
    dateModified = property(__dateModified.value, __dateModified.set, None, None)

    
    # Element ownerName uses Python identifier ownerName
    __ownerName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ownerName'), 'ownerName', '__AbsentNamespace0_Head_ownerName', False, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 36, 12), )

    
    ownerName = property(__ownerName.value, __ownerName.set, None, None)

    
    # Element ownerEmail uses Python identifier ownerEmail
    __ownerEmail = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ownerEmail'), 'ownerEmail', '__AbsentNamespace0_Head_ownerEmail', False, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 37, 12), )

    
    ownerEmail = property(__ownerEmail.value, __ownerEmail.set, None, None)

    
    # Element ownerId uses Python identifier ownerId
    __ownerId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ownerId'), 'ownerId', '__AbsentNamespace0_Head_ownerId', False, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 38, 12), )

    
    ownerId = property(__ownerId.value, __ownerId.set, None, None)

    
    # Element docs uses Python identifier docs
    __docs = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'docs'), 'docs', '__AbsentNamespace0_Head_docs', False, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 39, 12), )

    
    docs = property(__docs.value, __docs.set, None, None)

    
    # Element expansionState uses Python identifier expansionState
    __expansionState = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'expansionState'), 'expansionState', '__AbsentNamespace0_Head_expansionState', False, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 40, 12), )

    
    expansionState = property(__expansionState.value, __expansionState.set, None, None)

    
    # Element vertScrollState uses Python identifier vertScrollState
    __vertScrollState = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'vertScrollState'), 'vertScrollState', '__AbsentNamespace0_Head_vertScrollState', False, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 41, 12), )

    
    vertScrollState = property(__vertScrollState.value, __vertScrollState.set, None, None)

    
    # Element windowTop uses Python identifier windowTop
    __windowTop = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'windowTop'), 'windowTop', '__AbsentNamespace0_Head_windowTop', False, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 42, 12), )

    
    windowTop = property(__windowTop.value, __windowTop.set, None, None)

    
    # Element windowLeft uses Python identifier windowLeft
    __windowLeft = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'windowLeft'), 'windowLeft', '__AbsentNamespace0_Head_windowLeft', False, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 43, 12), )

    
    windowLeft = property(__windowLeft.value, __windowLeft.set, None, None)

    
    # Element windowBottom uses Python identifier windowBottom
    __windowBottom = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'windowBottom'), 'windowBottom', '__AbsentNamespace0_Head_windowBottom', False, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 44, 12), )

    
    windowBottom = property(__windowBottom.value, __windowBottom.set, None, None)

    
    # Element windowRight uses Python identifier windowRight
    __windowRight = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'windowRight'), 'windowRight', '__AbsentNamespace0_Head_windowRight', False, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 45, 12), )

    
    windowRight = property(__windowRight.value, __windowRight.set, None, None)

    _ElementMap.update({
        __title.name() : __title,
        __dateCreated.name() : __dateCreated,
        __dateModified.name() : __dateModified,
        __ownerName.name() : __ownerName,
        __ownerEmail.name() : __ownerEmail,
        __ownerId.name() : __ownerId,
        __docs.name() : __docs,
        __expansionState.name() : __expansionState,
        __vertScrollState.name() : __vertScrollState,
        __windowTop.name() : __windowTop,
        __windowLeft.name() : __windowLeft,
        __windowBottom.name() : __windowBottom,
        __windowRight.name() : __windowRight
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Head = Head
Namespace.addCategoryObject('typeBinding', 'Head', Head)


# Complex type OPML with content type ELEMENT_ONLY
class OPML (pyxb.binding.basis.complexTypeDefinition):
    """Complex type OPML with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'OPML')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 17, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element head uses Python identifier head
    __head = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'head'), 'head', '__AbsentNamespace0_OPML_head', False, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 19, 12), )

    
    head = property(__head.value, __head.set, None, None)

    
    # Element body uses Python identifier body
    __body = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'body'), 'body', '__AbsentNamespace0_OPML_body', False, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 20, 12), )

    
    body = property(__body.value, __body.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'version'), 'version', '__AbsentNamespace0_OPML_version', _module_typeBindings.Version, required=True)
    __version._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 22, 8)
    __version._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 22, 8)
    
    version = property(__version.value, __version.set, None, None)

    _ElementMap.update({
        __head.name() : __head,
        __body.name() : __body
    })
    _AttributeMap.update({
        __version.name() : __version
    })
_module_typeBindings.OPML = OPML
Namespace.addCategoryObject('typeBinding', 'OPML', OPML)


# Complex type Outline with content type ELEMENT_ONLY
class Outline (pyxb.binding.basis.complexTypeDefinition):
    """Complex type Outline with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Outline')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 49, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element outline uses Python identifier outline
    __outline = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'outline'), 'outline', '__AbsentNamespace0_Outline_outline', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 51, 12), )

    
    outline = property(__outline.value, __outline.set, None, None)

    
    # Attribute text uses Python identifier text
    __text = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'text'), 'text', '__AbsentNamespace0_Outline_text', pyxb.binding.datatypes.string, required=True)
    __text._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 53, 8)
    __text._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 53, 8)
    
    text = property(__text.value, __text.set, None, None)

    
    # Attribute isComment uses Python identifier isComment
    __isComment = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isComment'), 'isComment', '__AbsentNamespace0_Outline_isComment', pyxb.binding.datatypes.boolean, unicode_default='false')
    __isComment._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 54, 8)
    __isComment._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 54, 8)
    
    isComment = property(__isComment.value, __isComment.set, None, None)

    
    # Attribute isBreakpoint uses Python identifier isBreakpoint
    __isBreakpoint = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isBreakpoint'), 'isBreakpoint', '__AbsentNamespace0_Outline_isBreakpoint', pyxb.binding.datatypes.boolean, unicode_default='false')
    __isBreakpoint._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 55, 8)
    __isBreakpoint._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 55, 8)
    
    isBreakpoint = property(__isBreakpoint.value, __isBreakpoint.set, None, None)

    
    # Attribute created uses Python identifier created
    __created = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'created'), 'created', '__AbsentNamespace0_Outline_created', _module_typeBindings.RFC822Date)
    __created._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 56, 8)
    __created._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 56, 8)
    
    created = property(__created.value, __created.set, None, None)

    
    # Attribute category uses Python identifier category
    __category = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'category'), 'category', '__AbsentNamespace0_Outline_category', pyxb.binding.datatypes.string)
    __category._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 57, 8)
    __category._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 57, 8)
    
    category = property(__category.value, __category.set, None, None)

    
    # Attribute description uses Python identifier description
    __description = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'description'), 'description', '__AbsentNamespace0_Outline_description', pyxb.binding.datatypes.string)
    __description._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 58, 8)
    __description._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 58, 8)
    
    description = property(__description.value, __description.set, None, None)

    
    # Attribute url uses Python identifier url
    __url = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'url'), 'url', '__AbsentNamespace0_Outline_url', pyxb.binding.datatypes.anyURI)
    __url._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 59, 8)
    __url._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 59, 8)
    
    url = property(__url.value, __url.set, None, None)

    
    # Attribute htmlUrl uses Python identifier htmlUrl
    __htmlUrl = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'htmlUrl'), 'htmlUrl', '__AbsentNamespace0_Outline_htmlUrl', pyxb.binding.datatypes.anyURI)
    __htmlUrl._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 60, 8)
    __htmlUrl._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 60, 8)
    
    htmlUrl = property(__htmlUrl.value, __htmlUrl.set, None, None)

    
    # Attribute xmlUrl uses Python identifier xmlUrl
    __xmlUrl = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'xmlUrl'), 'xmlUrl', '__AbsentNamespace0_Outline_xmlUrl', pyxb.binding.datatypes.anyURI)
    __xmlUrl._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 61, 8)
    __xmlUrl._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 61, 8)
    
    xmlUrl = property(__xmlUrl.value, __xmlUrl.set, None, None)

    
    # Attribute title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'title'), 'title', '__AbsentNamespace0_Outline_title', pyxb.binding.datatypes.string)
    __title._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 62, 8)
    __title._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 62, 8)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'version'), 'version', '__AbsentNamespace0_Outline_version', pyxb.binding.datatypes.string)
    __version._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 63, 8)
    __version._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 63, 8)
    
    version = property(__version.value, __version.set, None, None)

    
    # Attribute language uses Python identifier language
    __language = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'language'), 'language', '__AbsentNamespace0_Outline_language', _module_typeBindings.Language)
    __language._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 64, 8)
    __language._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 64, 8)
    
    language = property(__language.value, __language.set, None, None)

    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__AbsentNamespace0_Outline_type', pyxb.binding.datatypes.string)
    __type._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 65, 8)
    __type._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 65, 8)
    
    type = property(__type.value, __type.set, None, None)

    _ElementMap.update({
        __outline.name() : __outline
    })
    _AttributeMap.update({
        __text.name() : __text,
        __isComment.name() : __isComment,
        __isBreakpoint.name() : __isBreakpoint,
        __created.name() : __created,
        __category.name() : __category,
        __description.name() : __description,
        __url.name() : __url,
        __htmlUrl.name() : __htmlUrl,
        __xmlUrl.name() : __xmlUrl,
        __title.name() : __title,
        __version.name() : __version,
        __language.name() : __language,
        __type.name() : __type
    })
_module_typeBindings.Outline = Outline
Namespace.addCategoryObject('typeBinding', 'Outline', Outline)


opml = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'opml'), OPML, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 15, 4))
Namespace.addCategoryObject('elementBinding', opml.name().localName(), opml)



Body._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'outline'), Outline, scope=Body, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 27, 12)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Body._UseForTag(pyxb.namespace.ExpandedName(None, 'outline')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 27, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Body._Automaton = _BuildAutomaton()




Head._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'title'), pyxb.binding.datatypes.string, scope=Head, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 33, 12)))

Head._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'dateCreated'), RFC822Date, scope=Head, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 34, 12)))

Head._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'dateModified'), RFC822Date, scope=Head, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 35, 12)))

Head._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ownerName'), pyxb.binding.datatypes.string, scope=Head, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 36, 12)))

Head._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ownerEmail'), EmailAddress, scope=Head, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 37, 12)))

Head._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ownerId'), pyxb.binding.datatypes.anyURI, scope=Head, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 38, 12)))

Head._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'docs'), pyxb.binding.datatypes.anyURI, scope=Head, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 39, 12)))

Head._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'expansionState'), pyxb.binding.datatypes.string, scope=Head, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 40, 12)))

Head._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'vertScrollState'), pyxb.binding.datatypes.positiveInteger, scope=Head, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 41, 12)))

Head._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'windowTop'), pyxb.binding.datatypes.integer, scope=Head, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 42, 12)))

Head._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'windowLeft'), pyxb.binding.datatypes.integer, scope=Head, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 43, 12)))

Head._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'windowBottom'), pyxb.binding.datatypes.integer, scope=Head, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 44, 12)))

Head._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'windowRight'), pyxb.binding.datatypes.integer, scope=Head, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 45, 12)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 33, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 34, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 35, 12))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 36, 12))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 37, 12))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 38, 12))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 39, 12))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 40, 12))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 41, 12))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 42, 12))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 43, 12))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 44, 12))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 45, 12))
    counters.add(cc_12)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Head._UseForTag(pyxb.namespace.ExpandedName(None, 'title')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 33, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Head._UseForTag(pyxb.namespace.ExpandedName(None, 'dateCreated')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 34, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(Head._UseForTag(pyxb.namespace.ExpandedName(None, 'dateModified')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 35, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(Head._UseForTag(pyxb.namespace.ExpandedName(None, 'ownerName')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 36, 12))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(Head._UseForTag(pyxb.namespace.ExpandedName(None, 'ownerEmail')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 37, 12))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(Head._UseForTag(pyxb.namespace.ExpandedName(None, 'ownerId')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 38, 12))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(Head._UseForTag(pyxb.namespace.ExpandedName(None, 'docs')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 39, 12))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(Head._UseForTag(pyxb.namespace.ExpandedName(None, 'expansionState')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 40, 12))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(Head._UseForTag(pyxb.namespace.ExpandedName(None, 'vertScrollState')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 41, 12))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(Head._UseForTag(pyxb.namespace.ExpandedName(None, 'windowTop')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 42, 12))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(Head._UseForTag(pyxb.namespace.ExpandedName(None, 'windowLeft')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 43, 12))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(Head._UseForTag(pyxb.namespace.ExpandedName(None, 'windowBottom')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 44, 12))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(Head._UseForTag(pyxb.namespace.ExpandedName(None, 'windowRight')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 45, 12))
    st_12 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_11, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_12, True) ]))
    st_12._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Head._Automaton = _BuildAutomaton_()




OPML._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'head'), Head, scope=OPML, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 19, 12)))

OPML._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'body'), Body, scope=OPML, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 20, 12)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(OPML._UseForTag(pyxb.namespace.ExpandedName(None, 'head')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 19, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(OPML._UseForTag(pyxb.namespace.ExpandedName(None, 'body')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 20, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
OPML._Automaton = _BuildAutomaton_2()




Outline._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'outline'), Outline, scope=Outline, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 51, 12)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 51, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Outline._UseForTag(pyxb.namespace.ExpandedName(None, 'outline')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/opml.xsd', 51, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Outline._Automaton = _BuildAutomaton_3()

