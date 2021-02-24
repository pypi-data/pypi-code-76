# ./binding.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2020-05-26 14:44:49.433897 by PyXB version 1.2.6 using Python 3.8.2.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:a1a46e5a-9f0b-11ea-b81e-38c986523fcd')

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


# Atomic simple type: Ext
class Ext (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Ext')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 21, 1)
    _Documentation = None
Ext._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'Ext', Ext)
_module_typeBindings.Ext = Ext

# Atomic simple type: VersionNumber
class VersionNumber (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'VersionNumber')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 153, 1)
    _Documentation = None
VersionNumber._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'VersionNumber', VersionNumber)
_module_typeBindings.VersionNumber = VersionNumber

# Atomic simple type: Modified
class Modified (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Modified')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 156, 1)
    _Documentation = None
Modified._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'Modified', Modified)
_module_typeBindings.Modified = Modified

# Atomic simple type: ID
class ID (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ID')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 197, 1)
    _Documentation = None
ID._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'ID', ID)
_module_typeBindings.ID = ID

# Complex type Document with content type ELEMENT_ONLY
class Document_ (pyxb.binding.basis.complexTypeDefinition):
    """Complex type Document with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Document')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 3, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Ext uses Python identifier Ext
    __Ext = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Ext'), 'Ext', '__AbsentNamespace0_Document__Ext', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 5, 3), )

    
    Ext = property(__Ext.value, __Ext.set, None, None)

    
    # Element Properties uses Python identifier Properties
    __Properties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Properties'), 'Properties', '__AbsentNamespace0_Document__Properties', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 6, 3), )

    
    Properties = property(__Properties.value, __Properties.set, None, None)

    
    # Element BaseVersion uses Python identifier BaseVersion
    __BaseVersion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'BaseVersion'), 'BaseVersion', '__AbsentNamespace0_Document__BaseVersion', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 7, 3), )

    
    BaseVersion = property(__BaseVersion.value, __BaseVersion.set, None, None)

    
    # Element VersionNumber uses Python identifier VersionNumber
    __VersionNumber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'VersionNumber'), 'VersionNumber', '__AbsentNamespace0_Document__VersionNumber', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 8, 3), )

    
    VersionNumber = property(__VersionNumber.value, __VersionNumber.set, None, None)

    
    # Element Modified uses Python identifier Modified
    __Modified = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Modified'), 'Modified', '__AbsentNamespace0_Document__Modified', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 9, 3), )

    
    Modified = property(__Modified.value, __Modified.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'version'), 'version', '__AbsentNamespace0_Document__version', pyxb.binding.datatypes.string)
    __version._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 11, 2)
    __version._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 11, 2)
    
    version = property(__version.value, __version.set, None, None)

    _ElementMap.update({
        __Ext.name() : __Ext,
        __Properties.name() : __Properties,
        __BaseVersion.name() : __BaseVersion,
        __VersionNumber.name() : __VersionNumber,
        __Modified.name() : __Modified
    })
    _AttributeMap.update({
        __version.name() : __version
    })
_module_typeBindings.Document_ = Document_
Namespace.addCategoryObject('typeBinding', 'Document', Document_)


# Complex type BaseVersion with content type ELEMENT_ONLY
class BaseVersion (pyxb.binding.basis.complexTypeDefinition):
    """Complex type BaseVersion with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'BaseVersion')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 13, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element VersionNumber uses Python identifier VersionNumber
    __VersionNumber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'VersionNumber'), 'VersionNumber', '__AbsentNamespace0_BaseVersion_VersionNumber', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 15, 3), )

    
    VersionNumber = property(__VersionNumber.value, __VersionNumber.set, None, None)

    
    # Element Modified uses Python identifier Modified
    __Modified = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Modified'), 'Modified', '__AbsentNamespace0_BaseVersion_Modified', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 16, 3), )

    
    Modified = property(__Modified.value, __Modified.set, None, None)

    
    # Element Ext uses Python identifier Ext
    __Ext = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Ext'), 'Ext', '__AbsentNamespace0_BaseVersion_Ext', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 17, 3), )

    
    Ext = property(__Ext.value, __Ext.set, None, None)

    
    # Element Properties uses Python identifier Properties
    __Properties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Properties'), 'Properties', '__AbsentNamespace0_BaseVersion_Properties', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 18, 3), )

    
    Properties = property(__Properties.value, __Properties.set, None, None)

    _ElementMap.update({
        __VersionNumber.name() : __VersionNumber,
        __Modified.name() : __Modified,
        __Ext.name() : __Ext,
        __Properties.name() : __Properties
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.BaseVersion = BaseVersion
Namespace.addCategoryObject('typeBinding', 'BaseVersion', BaseVersion)


# Complex type Properties with content type ELEMENT_ONLY
class Properties (pyxb.binding.basis.complexTypeDefinition):
    """Complex type Properties with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Properties')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 24, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element isExpanded uses Python identifier isExpanded
    __isExpanded = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'isExpanded'), 'isExpanded', '__AbsentNamespace0_Properties_isExpanded', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 26, 3), )

    
    isExpanded = property(__isExpanded.value, __isExpanded.set, None, None)

    
    # Element isGroup uses Python identifier isGroup
    __isGroup = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'isGroup'), 'isGroup', '__AbsentNamespace0_Properties_isGroup', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 27, 3), )

    
    isGroup = property(__isGroup.value, __isGroup.set, None, None)

    
    # Element title uses Python identifier title
    __title = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'title'), 'title', '__AbsentNamespace0_Properties_title', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 28, 3), )

    
    title = property(__title.value, __title.set, None, None)

    
    # Element password uses Python identifier password
    __password = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'password'), 'password', '__AbsentNamespace0_Properties_password', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 29, 3), )

    
    password = property(__password.value, __password.set, None, None)

    
    # Element markColor uses Python identifier markColor
    __markColor = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'markColor'), 'markColor', '__AbsentNamespace0_Properties_markColor', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 30, 3), )

    
    markColor = property(__markColor.value, __markColor.set, None, None)

    
    # Element note uses Python identifier note
    __note = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'note'), 'note', '__AbsentNamespace0_Properties_note', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 31, 3), )

    
    note = property(__note.value, __note.set, None, None)

    
    # Element context uses Python identifier context
    __context = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'context'), 'context', '__AbsentNamespace0_Properties_context', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 32, 3), )

    
    context = property(__context.value, __context.set, None, None)

    
    # Element fontSize uses Python identifier fontSize
    __fontSize = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'fontSize'), 'fontSize', '__AbsentNamespace0_Properties_fontSize', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 33, 3), )

    
    fontSize = property(__fontSize.value, __fontSize.set, None, None)

    
    # Element defaultFontStyle uses Python identifier defaultFontStyle
    __defaultFontStyle = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'defaultFontStyle'), 'defaultFontStyle', '__AbsentNamespace0_Properties_defaultFontStyle', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 34, 3), )

    
    defaultFontStyle = property(__defaultFontStyle.value, __defaultFontStyle.set, None, None)

    
    # Element defaultColor uses Python identifier defaultColor
    __defaultColor = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'defaultColor'), 'defaultColor', '__AbsentNamespace0_Properties_defaultColor', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 35, 3), )

    
    defaultColor = property(__defaultColor.value, __defaultColor.set, None, None)

    
    # Element numerationStyle uses Python identifier numerationStyle
    __numerationStyle = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'numerationStyle'), 'numerationStyle', '__AbsentNamespace0_Properties_numerationStyle', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 36, 3), )

    
    numerationStyle = property(__numerationStyle.value, __numerationStyle.set, None, None)

    
    # Element lastModificationTime uses Python identifier lastModificationTime
    __lastModificationTime = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'lastModificationTime'), 'lastModificationTime', '__AbsentNamespace0_Properties_lastModificationTime', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 37, 3), )

    
    lastModificationTime = property(__lastModificationTime.value, __lastModificationTime.set, None, None)

    
    # Element showCheckBox uses Python identifier showCheckBox
    __showCheckBox = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'showCheckBox'), 'showCheckBox', '__AbsentNamespace0_Properties_showCheckBox', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 38, 3), )

    
    showCheckBox = property(__showCheckBox.value, __showCheckBox.set, None, None)

    
    # Element hideCheckedEnements uses Python identifier hideCheckedEnements
    __hideCheckedEnements = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'hideCheckedEnements'), 'hideCheckedEnements', '__AbsentNamespace0_Properties_hideCheckedEnements', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 39, 3), )

    
    hideCheckedEnements = property(__hideCheckedEnements.value, __hideCheckedEnements.set, None, None)

    
    # Element hideUncheckedEnements uses Python identifier hideUncheckedEnements
    __hideUncheckedEnements = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'hideUncheckedEnements'), 'hideUncheckedEnements', '__AbsentNamespace0_Properties_hideUncheckedEnements', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 40, 3), )

    
    hideUncheckedEnements = property(__hideUncheckedEnements.value, __hideUncheckedEnements.set, None, None)

    
    # Element resizebleLineForTextSize uses Python identifier resizebleLineForTextSize
    __resizebleLineForTextSize = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'resizebleLineForTextSize'), 'resizebleLineForTextSize', '__AbsentNamespace0_Properties_resizebleLineForTextSize', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 41, 3), )

    
    resizebleLineForTextSize = property(__resizebleLineForTextSize.value, __resizebleLineForTextSize.set, None, None)

    
    # Element showNotesOnlyForSelectedRow uses Python identifier showNotesOnlyForSelectedRow
    __showNotesOnlyForSelectedRow = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'showNotesOnlyForSelectedRow'), 'showNotesOnlyForSelectedRow', '__AbsentNamespace0_Properties_showNotesOnlyForSelectedRow', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 42, 3), )

    
    showNotesOnlyForSelectedRow = property(__showNotesOnlyForSelectedRow.value, __showNotesOnlyForSelectedRow.set, None, None)

    
    # Element readOnly uses Python identifier readOnly
    __readOnly = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'readOnly'), 'readOnly', '__AbsentNamespace0_Properties_readOnly', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 43, 3), )

    
    readOnly = property(__readOnly.value, __readOnly.set, None, None)

    
    # Element ID uses Python identifier ID
    __ID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__AbsentNamespace0_Properties_ID', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 44, 3), )

    
    ID = property(__ID.value, __ID.set, None, None)

    
    # Element ChildItems uses Python identifier ChildItems
    __ChildItems = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ChildItems'), 'ChildItems', '__AbsentNamespace0_Properties_ChildItems', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 45, 3), )

    
    ChildItems = property(__ChildItems.value, __ChildItems.set, None, None)

    
    # Attribute className uses Python identifier className
    __className = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'className'), 'className', '__AbsentNamespace0_Properties_className', pyxb.binding.datatypes.NCName, required=True)
    __className._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 47, 2)
    __className._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 47, 2)
    
    className = property(__className.value, __className.set, None, None)

    _ElementMap.update({
        __isExpanded.name() : __isExpanded,
        __isGroup.name() : __isGroup,
        __title.name() : __title,
        __password.name() : __password,
        __markColor.name() : __markColor,
        __note.name() : __note,
        __context.name() : __context,
        __fontSize.name() : __fontSize,
        __defaultFontStyle.name() : __defaultFontStyle,
        __defaultColor.name() : __defaultColor,
        __numerationStyle.name() : __numerationStyle,
        __lastModificationTime.name() : __lastModificationTime,
        __showCheckBox.name() : __showCheckBox,
        __hideCheckedEnements.name() : __hideCheckedEnements,
        __hideUncheckedEnements.name() : __hideUncheckedEnements,
        __resizebleLineForTextSize.name() : __resizebleLineForTextSize,
        __showNotesOnlyForSelectedRow.name() : __showNotesOnlyForSelectedRow,
        __readOnly.name() : __readOnly,
        __ID.name() : __ID,
        __ChildItems.name() : __ChildItems
    })
    _AttributeMap.update({
        __className.name() : __className
    })
_module_typeBindings.Properties = Properties
Namespace.addCategoryObject('typeBinding', 'Properties', Properties)


# Complex type password with content type MIXED
class password (pyxb.binding.basis.complexTypeDefinition):
    """Complex type password with content type MIXED"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_MIXED
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'password')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 49, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute className uses Python identifier className
    __className = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'className'), 'className', '__AbsentNamespace0_password_className', pyxb.binding.datatypes.NCName, required=True)
    __className._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 50, 2)
    __className._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 50, 2)
    
    className = property(__className.value, __className.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __className.name() : __className
    })
_module_typeBindings.password = password
Namespace.addCategoryObject('typeBinding', 'password', password)


# Complex type markColor with content type SIMPLE
class markColor (pyxb.binding.basis.complexTypeDefinition):
    """Complex type markColor with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.integer
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'markColor')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 52, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.integer
    
    # Attribute className uses Python identifier className
    __className = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'className'), 'className', '__AbsentNamespace0_markColor_className', pyxb.binding.datatypes.NCName, required=True)
    __className._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 55, 4)
    __className._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 55, 4)
    
    className = property(__className.value, __className.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __className.name() : __className
    })
_module_typeBindings.markColor = markColor
Namespace.addCategoryObject('typeBinding', 'markColor', markColor)


# Complex type note with content type MIXED
class note (pyxb.binding.basis.complexTypeDefinition):
    """Complex type note with content type MIXED"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_MIXED
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'note')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 59, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute className uses Python identifier className
    __className = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'className'), 'className', '__AbsentNamespace0_note_className', pyxb.binding.datatypes.NCName, required=True)
    __className._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 60, 2)
    __className._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 60, 2)
    
    className = property(__className.value, __className.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __className.name() : __className
    })
_module_typeBindings.note = note
Namespace.addCategoryObject('typeBinding', 'note', note)


# Complex type context with content type ELEMENT_ONLY
class context (pyxb.binding.basis.complexTypeDefinition):
    """Complex type context with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'context')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 62, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element isExpanded uses Python identifier isExpanded
    __isExpanded = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'isExpanded'), 'isExpanded', '__AbsentNamespace0_context_isExpanded', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 64, 3), )

    
    isExpanded = property(__isExpanded.value, __isExpanded.set, None, None)

    
    # Element isGroup uses Python identifier isGroup
    __isGroup = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'isGroup'), 'isGroup', '__AbsentNamespace0_context_isGroup', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 65, 3), )

    
    isGroup = property(__isGroup.value, __isGroup.set, None, None)

    
    # Element title uses Python identifier title
    __title = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'title'), 'title', '__AbsentNamespace0_context_title', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 66, 3), )

    
    title = property(__title.value, __title.set, None, None)

    
    # Element completionState uses Python identifier completionState
    __completionState = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'completionState'), 'completionState', '__AbsentNamespace0_context_completionState', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 67, 3), )

    
    completionState = property(__completionState.value, __completionState.set, None, None)

    
    # Element color uses Python identifier color
    __color = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'color'), 'color', '__AbsentNamespace0_context_color', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 68, 3), )

    
    color = property(__color.value, __color.set, None, None)

    
    # Element fontStyle uses Python identifier fontStyle
    __fontStyle = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'fontStyle'), 'fontStyle', '__AbsentNamespace0_context_fontStyle', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 69, 3), )

    
    fontStyle = property(__fontStyle.value, __fontStyle.set, None, None)

    
    # Element ID uses Python identifier ID
    __ID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__AbsentNamespace0_context_ID', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 70, 3), )

    
    ID = property(__ID.value, __ID.set, None, None)

    
    # Element ChildItems uses Python identifier ChildItems
    __ChildItems = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ChildItems'), 'ChildItems', '__AbsentNamespace0_context_ChildItems', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 71, 3), )

    
    ChildItems = property(__ChildItems.value, __ChildItems.set, None, None)

    
    # Element ChildItem uses Python identifier ChildItem
    __ChildItem = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ChildItem'), 'ChildItem', '__AbsentNamespace0_context_ChildItem', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 72, 3), )

    
    ChildItem = property(__ChildItem.value, __ChildItem.set, None, None)

    
    # Attribute className uses Python identifier className
    __className = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'className'), 'className', '__AbsentNamespace0_context_className', pyxb.binding.datatypes.NCName, required=True)
    __className._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 74, 2)
    __className._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 74, 2)
    
    className = property(__className.value, __className.set, None, None)

    _ElementMap.update({
        __isExpanded.name() : __isExpanded,
        __isGroup.name() : __isGroup,
        __title.name() : __title,
        __completionState.name() : __completionState,
        __color.name() : __color,
        __fontStyle.name() : __fontStyle,
        __ID.name() : __ID,
        __ChildItems.name() : __ChildItems,
        __ChildItem.name() : __ChildItem
    })
    _AttributeMap.update({
        __className.name() : __className
    })
_module_typeBindings.context = context
Namespace.addCategoryObject('typeBinding', 'context', context)


# Complex type fontSize with content type SIMPLE
class fontSize (pyxb.binding.basis.complexTypeDefinition):
    """Complex type fontSize with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.integer
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'fontSize')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 76, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.integer
    
    # Attribute className uses Python identifier className
    __className = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'className'), 'className', '__AbsentNamespace0_fontSize_className', pyxb.binding.datatypes.NCName, required=True)
    __className._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 79, 4)
    __className._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 79, 4)
    
    className = property(__className.value, __className.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __className.name() : __className
    })
_module_typeBindings.fontSize = fontSize
Namespace.addCategoryObject('typeBinding', 'fontSize', fontSize)


# Complex type defaultFontStyle with content type SIMPLE
class defaultFontStyle (pyxb.binding.basis.complexTypeDefinition):
    """Complex type defaultFontStyle with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.integer
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'defaultFontStyle')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 83, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.integer
    
    # Attribute className uses Python identifier className
    __className = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'className'), 'className', '__AbsentNamespace0_defaultFontStyle_className', pyxb.binding.datatypes.NCName, required=True)
    __className._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 86, 4)
    __className._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 86, 4)
    
    className = property(__className.value, __className.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __className.name() : __className
    })
_module_typeBindings.defaultFontStyle = defaultFontStyle
Namespace.addCategoryObject('typeBinding', 'defaultFontStyle', defaultFontStyle)


# Complex type defaultColor with content type SIMPLE
class defaultColor (pyxb.binding.basis.complexTypeDefinition):
    """Complex type defaultColor with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.integer
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'defaultColor')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 90, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.integer
    
    # Attribute className uses Python identifier className
    __className = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'className'), 'className', '__AbsentNamespace0_defaultColor_className', pyxb.binding.datatypes.NCName, required=True)
    __className._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 93, 4)
    __className._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 93, 4)
    
    className = property(__className.value, __className.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __className.name() : __className
    })
_module_typeBindings.defaultColor = defaultColor
Namespace.addCategoryObject('typeBinding', 'defaultColor', defaultColor)


# Complex type numerationStyle with content type SIMPLE
class numerationStyle (pyxb.binding.basis.complexTypeDefinition):
    """Complex type numerationStyle with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.integer
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'numerationStyle')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 97, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.integer
    
    # Attribute className uses Python identifier className
    __className = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'className'), 'className', '__AbsentNamespace0_numerationStyle_className', pyxb.binding.datatypes.NCName, required=True)
    __className._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 100, 4)
    __className._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 100, 4)
    
    className = property(__className.value, __className.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __className.name() : __className
    })
_module_typeBindings.numerationStyle = numerationStyle
Namespace.addCategoryObject('typeBinding', 'numerationStyle', numerationStyle)


# Complex type lastModificationTime with content type SIMPLE
class lastModificationTime (pyxb.binding.basis.complexTypeDefinition):
    """Complex type lastModificationTime with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.float
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'lastModificationTime')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 104, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.float
    
    # Attribute className uses Python identifier className
    __className = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'className'), 'className', '__AbsentNamespace0_lastModificationTime_className', pyxb.binding.datatypes.NCName, required=True)
    __className._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 107, 4)
    __className._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 107, 4)
    
    className = property(__className.value, __className.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __className.name() : __className
    })
_module_typeBindings.lastModificationTime = lastModificationTime
Namespace.addCategoryObject('typeBinding', 'lastModificationTime', lastModificationTime)


# Complex type showCheckBox with content type SIMPLE
class showCheckBox (pyxb.binding.basis.complexTypeDefinition):
    """Complex type showCheckBox with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.integer
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'showCheckBox')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 111, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.integer
    
    # Attribute className uses Python identifier className
    __className = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'className'), 'className', '__AbsentNamespace0_showCheckBox_className', pyxb.binding.datatypes.NCName, required=True)
    __className._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 114, 4)
    __className._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 114, 4)
    
    className = property(__className.value, __className.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __className.name() : __className
    })
_module_typeBindings.showCheckBox = showCheckBox
Namespace.addCategoryObject('typeBinding', 'showCheckBox', showCheckBox)


# Complex type hideCheckedEnements with content type SIMPLE
class hideCheckedEnements (pyxb.binding.basis.complexTypeDefinition):
    """Complex type hideCheckedEnements with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.integer
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'hideCheckedEnements')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 118, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.integer
    
    # Attribute className uses Python identifier className
    __className = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'className'), 'className', '__AbsentNamespace0_hideCheckedEnements_className', pyxb.binding.datatypes.NCName, required=True)
    __className._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 121, 4)
    __className._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 121, 4)
    
    className = property(__className.value, __className.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __className.name() : __className
    })
_module_typeBindings.hideCheckedEnements = hideCheckedEnements
Namespace.addCategoryObject('typeBinding', 'hideCheckedEnements', hideCheckedEnements)


# Complex type hideUncheckedEnements with content type SIMPLE
class hideUncheckedEnements (pyxb.binding.basis.complexTypeDefinition):
    """Complex type hideUncheckedEnements with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.integer
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'hideUncheckedEnements')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 125, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.integer
    
    # Attribute className uses Python identifier className
    __className = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'className'), 'className', '__AbsentNamespace0_hideUncheckedEnements_className', pyxb.binding.datatypes.NCName, required=True)
    __className._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 128, 4)
    __className._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 128, 4)
    
    className = property(__className.value, __className.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __className.name() : __className
    })
_module_typeBindings.hideUncheckedEnements = hideUncheckedEnements
Namespace.addCategoryObject('typeBinding', 'hideUncheckedEnements', hideUncheckedEnements)


# Complex type resizebleLineForTextSize with content type SIMPLE
class resizebleLineForTextSize (pyxb.binding.basis.complexTypeDefinition):
    """Complex type resizebleLineForTextSize with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.integer
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'resizebleLineForTextSize')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 132, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.integer
    
    # Attribute className uses Python identifier className
    __className = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'className'), 'className', '__AbsentNamespace0_resizebleLineForTextSize_className', pyxb.binding.datatypes.NCName, required=True)
    __className._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 135, 4)
    __className._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 135, 4)
    
    className = property(__className.value, __className.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __className.name() : __className
    })
_module_typeBindings.resizebleLineForTextSize = resizebleLineForTextSize
Namespace.addCategoryObject('typeBinding', 'resizebleLineForTextSize', resizebleLineForTextSize)


# Complex type showNotesOnlyForSelectedRow with content type SIMPLE
class showNotesOnlyForSelectedRow (pyxb.binding.basis.complexTypeDefinition):
    """Complex type showNotesOnlyForSelectedRow with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.integer
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'showNotesOnlyForSelectedRow')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 139, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.integer
    
    # Attribute className uses Python identifier className
    __className = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'className'), 'className', '__AbsentNamespace0_showNotesOnlyForSelectedRow_className', pyxb.binding.datatypes.NCName, required=True)
    __className._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 142, 4)
    __className._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 142, 4)
    
    className = property(__className.value, __className.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __className.name() : __className
    })
_module_typeBindings.showNotesOnlyForSelectedRow = showNotesOnlyForSelectedRow
Namespace.addCategoryObject('typeBinding', 'showNotesOnlyForSelectedRow', showNotesOnlyForSelectedRow)


# Complex type readOnly with content type SIMPLE
class readOnly (pyxb.binding.basis.complexTypeDefinition):
    """Complex type readOnly with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.integer
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'readOnly')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 146, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.integer
    
    # Attribute className uses Python identifier className
    __className = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'className'), 'className', '__AbsentNamespace0_readOnly_className', pyxb.binding.datatypes.NCName, required=True)
    __className._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 149, 4)
    __className._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 149, 4)
    
    className = property(__className.value, __className.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __className.name() : __className
    })
_module_typeBindings.readOnly = readOnly
Namespace.addCategoryObject('typeBinding', 'readOnly', readOnly)


# Complex type isExpanded with content type SIMPLE
class isExpanded (pyxb.binding.basis.complexTypeDefinition):
    """Complex type isExpanded with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.integer
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'isExpanded')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 159, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.integer
    
    # Attribute className uses Python identifier className
    __className = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'className'), 'className', '__AbsentNamespace0_isExpanded_className', pyxb.binding.datatypes.NCName, required=True)
    __className._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 162, 4)
    __className._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 162, 4)
    
    className = property(__className.value, __className.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __className.name() : __className
    })
_module_typeBindings.isExpanded = isExpanded
Namespace.addCategoryObject('typeBinding', 'isExpanded', isExpanded)


# Complex type isGroup with content type SIMPLE
class isGroup (pyxb.binding.basis.complexTypeDefinition):
    """Complex type isGroup with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.integer
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'isGroup')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 166, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.integer
    
    # Attribute className uses Python identifier className
    __className = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'className'), 'className', '__AbsentNamespace0_isGroup_className', pyxb.binding.datatypes.NCName, required=True)
    __className._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 169, 4)
    __className._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 169, 4)
    
    className = property(__className.value, __className.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __className.name() : __className
    })
_module_typeBindings.isGroup = isGroup
Namespace.addCategoryObject('typeBinding', 'isGroup', isGroup)


# Complex type title with content type MIXED
class title (pyxb.binding.basis.complexTypeDefinition):
    """Complex type title with content type MIXED"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_MIXED
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'title')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 173, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute className uses Python identifier className
    __className = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'className'), 'className', '__AbsentNamespace0_title_className', pyxb.binding.datatypes.NCName, required=True)
    __className._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 174, 2)
    __className._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 174, 2)
    
    className = property(__className.value, __className.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __className.name() : __className
    })
_module_typeBindings.title = title
Namespace.addCategoryObject('typeBinding', 'title', title)


# Complex type completionState with content type SIMPLE
class completionState (pyxb.binding.basis.complexTypeDefinition):
    """Complex type completionState with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.integer
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'completionState')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 176, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.integer
    
    # Attribute className uses Python identifier className
    __className = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'className'), 'className', '__AbsentNamespace0_completionState_className', pyxb.binding.datatypes.NCName, required=True)
    __className._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 179, 4)
    __className._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 179, 4)
    
    className = property(__className.value, __className.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __className.name() : __className
    })
_module_typeBindings.completionState = completionState
Namespace.addCategoryObject('typeBinding', 'completionState', completionState)


# Complex type color with content type SIMPLE
class color (pyxb.binding.basis.complexTypeDefinition):
    """Complex type color with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.integer
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'color')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 183, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.integer
    
    # Attribute className uses Python identifier className
    __className = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'className'), 'className', '__AbsentNamespace0_color_className', pyxb.binding.datatypes.NCName, required=True)
    __className._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 186, 4)
    __className._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 186, 4)
    
    className = property(__className.value, __className.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __className.name() : __className
    })
_module_typeBindings.color = color
Namespace.addCategoryObject('typeBinding', 'color', color)


# Complex type fontStyle with content type SIMPLE
class fontStyle (pyxb.binding.basis.complexTypeDefinition):
    """Complex type fontStyle with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.integer
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'fontStyle')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 190, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.integer
    
    # Attribute className uses Python identifier className
    __className = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'className'), 'className', '__AbsentNamespace0_fontStyle_className', pyxb.binding.datatypes.NCName, required=True)
    __className._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 193, 4)
    __className._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 193, 4)
    
    className = property(__className.value, __className.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __className.name() : __className
    })
_module_typeBindings.fontStyle = fontStyle
Namespace.addCategoryObject('typeBinding', 'fontStyle', fontStyle)


# Complex type ChildItems with content type ELEMENT_ONLY
class ChildItems (pyxb.binding.basis.complexTypeDefinition):
    """Complex type ChildItems with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ChildItems')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 200, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ID uses Python identifier ID
    __ID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__AbsentNamespace0_ChildItems_ID', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 202, 3), )

    
    ID = property(__ID.value, __ID.set, None, None)

    _ElementMap.update({
        __ID.name() : __ID
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.ChildItems = ChildItems
Namespace.addCategoryObject('typeBinding', 'ChildItems', ChildItems)


# Complex type ChildItem with content type ELEMENT_ONLY
class ChildItem (pyxb.binding.basis.complexTypeDefinition):
    """Complex type ChildItem with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ChildItem')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 205, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ChildItem uses Python identifier ChildItem
    __ChildItem = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ChildItem'), 'ChildItem', '__AbsentNamespace0_ChildItem_ChildItem', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 207, 3), )

    
    ChildItem = property(__ChildItem.value, __ChildItem.set, None, None)

    
    # Element ChildItems uses Python identifier ChildItems
    __ChildItems = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ChildItems'), 'ChildItems', '__AbsentNamespace0_ChildItem_ChildItems', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 208, 3), )

    
    ChildItems = property(__ChildItems.value, __ChildItems.set, None, None)

    
    # Element ID uses Python identifier ID
    __ID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__AbsentNamespace0_ChildItem_ID', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 209, 3), )

    
    ID = property(__ID.value, __ID.set, None, None)

    
    # Element color uses Python identifier color
    __color = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'color'), 'color', '__AbsentNamespace0_ChildItem_color', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 210, 3), )

    
    color = property(__color.value, __color.set, None, None)

    
    # Element completionState uses Python identifier completionState
    __completionState = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'completionState'), 'completionState', '__AbsentNamespace0_ChildItem_completionState', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 211, 3), )

    
    completionState = property(__completionState.value, __completionState.set, None, None)

    
    # Element fontStyle uses Python identifier fontStyle
    __fontStyle = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'fontStyle'), 'fontStyle', '__AbsentNamespace0_ChildItem_fontStyle', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 212, 3), )

    
    fontStyle = property(__fontStyle.value, __fontStyle.set, None, None)

    
    # Element isExpanded uses Python identifier isExpanded
    __isExpanded = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'isExpanded'), 'isExpanded', '__AbsentNamespace0_ChildItem_isExpanded', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 213, 3), )

    
    isExpanded = property(__isExpanded.value, __isExpanded.set, None, None)

    
    # Element isGroup uses Python identifier isGroup
    __isGroup = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'isGroup'), 'isGroup', '__AbsentNamespace0_ChildItem_isGroup', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 214, 3), )

    
    isGroup = property(__isGroup.value, __isGroup.set, None, None)

    
    # Element title uses Python identifier title
    __title = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'title'), 'title', '__AbsentNamespace0_ChildItem_title', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 215, 3), )

    
    title = property(__title.value, __title.set, None, None)

    
    # Element notes uses Python identifier notes
    __notes = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'notes'), 'notes', '__AbsentNamespace0_ChildItem_notes', True, pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 216, 3), )

    
    notes = property(__notes.value, __notes.set, None, None)

    
    # Attribute className uses Python identifier className
    __className = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'className'), 'className', '__AbsentNamespace0_ChildItem_className', pyxb.binding.datatypes.NCName, required=True)
    __className._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 218, 2)
    __className._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 218, 2)
    
    className = property(__className.value, __className.set, None, None)

    _ElementMap.update({
        __ChildItem.name() : __ChildItem,
        __ChildItems.name() : __ChildItems,
        __ID.name() : __ID,
        __color.name() : __color,
        __completionState.name() : __completionState,
        __fontStyle.name() : __fontStyle,
        __isExpanded.name() : __isExpanded,
        __isGroup.name() : __isGroup,
        __title.name() : __title,
        __notes.name() : __notes
    })
    _AttributeMap.update({
        __className.name() : __className
    })
_module_typeBindings.ChildItem = ChildItem
Namespace.addCategoryObject('typeBinding', 'ChildItem', ChildItem)


# Complex type notes with content type MIXED
class notes (pyxb.binding.basis.complexTypeDefinition):
    """Complex type notes with content type MIXED"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_MIXED
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'notes')
    _XSDLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 220, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute className uses Python identifier className
    __className = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'className'), 'className', '__AbsentNamespace0_notes_className', pyxb.binding.datatypes.NCName, required=True)
    __className._DeclarationLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 221, 2)
    __className._UseLocation = pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 221, 2)
    
    className = property(__className.value, __className.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __className.name() : __className
    })
_module_typeBindings.notes = notes
Namespace.addCategoryObject('typeBinding', 'notes', notes)


Document = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Document'), Document_, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 223, 1))
Namespace.addCategoryObject('elementBinding', Document.name().localName(), Document)



Document_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Ext'), Ext, scope=Document_, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 5, 3)))

Document_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Properties'), Properties, scope=Document_, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 6, 3)))

Document_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'BaseVersion'), BaseVersion, scope=Document_, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 7, 3)))

Document_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'VersionNumber'), VersionNumber, scope=Document_, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 8, 3)))

Document_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Modified'), Modified, scope=Document_, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 9, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 4, 2))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Document_._UseForTag(pyxb.namespace.ExpandedName(None, 'Ext')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 5, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Document_._UseForTag(pyxb.namespace.ExpandedName(None, 'Properties')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 6, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Document_._UseForTag(pyxb.namespace.ExpandedName(None, 'BaseVersion')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 7, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Document_._UseForTag(pyxb.namespace.ExpandedName(None, 'VersionNumber')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 8, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Document_._UseForTag(pyxb.namespace.ExpandedName(None, 'Modified')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 9, 3))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Document_._Automaton = _BuildAutomaton()




BaseVersion._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'VersionNumber'), VersionNumber, scope=BaseVersion, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 15, 3)))

BaseVersion._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Modified'), Modified, scope=BaseVersion, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 16, 3)))

BaseVersion._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Ext'), Ext, scope=BaseVersion, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 17, 3)))

BaseVersion._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Properties'), Properties, scope=BaseVersion, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 18, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 14, 2))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(BaseVersion._UseForTag(pyxb.namespace.ExpandedName(None, 'VersionNumber')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 15, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(BaseVersion._UseForTag(pyxb.namespace.ExpandedName(None, 'Modified')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 16, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(BaseVersion._UseForTag(pyxb.namespace.ExpandedName(None, 'Ext')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 17, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(BaseVersion._UseForTag(pyxb.namespace.ExpandedName(None, 'Properties')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 18, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
BaseVersion._Automaton = _BuildAutomaton_()




Properties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'isExpanded'), isExpanded, scope=Properties, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 26, 3)))

Properties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'isGroup'), isGroup, scope=Properties, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 27, 3)))

Properties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'title'), title, scope=Properties, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 28, 3)))

Properties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'password'), password, scope=Properties, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 29, 3)))

Properties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'markColor'), markColor, scope=Properties, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 30, 3)))

Properties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'note'), note, scope=Properties, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 31, 3)))

Properties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'context'), context, scope=Properties, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 32, 3)))

Properties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'fontSize'), fontSize, scope=Properties, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 33, 3)))

Properties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'defaultFontStyle'), defaultFontStyle, scope=Properties, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 34, 3)))

Properties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'defaultColor'), defaultColor, scope=Properties, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 35, 3)))

Properties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'numerationStyle'), numerationStyle, scope=Properties, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 36, 3)))

Properties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'lastModificationTime'), lastModificationTime, scope=Properties, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 37, 3)))

Properties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'showCheckBox'), showCheckBox, scope=Properties, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 38, 3)))

Properties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'hideCheckedEnements'), hideCheckedEnements, scope=Properties, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 39, 3)))

Properties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'hideUncheckedEnements'), hideUncheckedEnements, scope=Properties, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 40, 3)))

Properties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'resizebleLineForTextSize'), resizebleLineForTextSize, scope=Properties, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 41, 3)))

Properties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'showNotesOnlyForSelectedRow'), showNotesOnlyForSelectedRow, scope=Properties, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 42, 3)))

Properties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'readOnly'), readOnly, scope=Properties, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 43, 3)))

Properties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ID'), ID, scope=Properties, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 44, 3)))

Properties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ChildItems'), ChildItems, scope=Properties, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 45, 3)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 25, 2))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Properties._UseForTag(pyxb.namespace.ExpandedName(None, 'isExpanded')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 26, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Properties._UseForTag(pyxb.namespace.ExpandedName(None, 'isGroup')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 27, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Properties._UseForTag(pyxb.namespace.ExpandedName(None, 'title')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 28, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Properties._UseForTag(pyxb.namespace.ExpandedName(None, 'password')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 29, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Properties._UseForTag(pyxb.namespace.ExpandedName(None, 'markColor')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 30, 3))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Properties._UseForTag(pyxb.namespace.ExpandedName(None, 'note')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 31, 3))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Properties._UseForTag(pyxb.namespace.ExpandedName(None, 'context')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 32, 3))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Properties._UseForTag(pyxb.namespace.ExpandedName(None, 'fontSize')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 33, 3))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Properties._UseForTag(pyxb.namespace.ExpandedName(None, 'defaultFontStyle')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 34, 3))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Properties._UseForTag(pyxb.namespace.ExpandedName(None, 'defaultColor')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 35, 3))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Properties._UseForTag(pyxb.namespace.ExpandedName(None, 'numerationStyle')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 36, 3))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Properties._UseForTag(pyxb.namespace.ExpandedName(None, 'lastModificationTime')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 37, 3))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Properties._UseForTag(pyxb.namespace.ExpandedName(None, 'showCheckBox')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 38, 3))
    st_12 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Properties._UseForTag(pyxb.namespace.ExpandedName(None, 'hideCheckedEnements')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 39, 3))
    st_13 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Properties._UseForTag(pyxb.namespace.ExpandedName(None, 'hideUncheckedEnements')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 40, 3))
    st_14 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Properties._UseForTag(pyxb.namespace.ExpandedName(None, 'resizebleLineForTextSize')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 41, 3))
    st_15 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Properties._UseForTag(pyxb.namespace.ExpandedName(None, 'showNotesOnlyForSelectedRow')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 42, 3))
    st_16 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Properties._UseForTag(pyxb.namespace.ExpandedName(None, 'readOnly')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 43, 3))
    st_17 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Properties._UseForTag(pyxb.namespace.ExpandedName(None, 'ID')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 44, 3))
    st_18 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Properties._UseForTag(pyxb.namespace.ExpandedName(None, 'ChildItems')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 45, 3))
    st_19 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_17._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_18._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_19._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Properties._Automaton = _BuildAutomaton_2()




def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    return fac.Automaton(states, counters, True, containing_state=None)
password._Automaton = _BuildAutomaton_3()




def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    return fac.Automaton(states, counters, True, containing_state=None)
note._Automaton = _BuildAutomaton_4()




context._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'isExpanded'), isExpanded, scope=context, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 64, 3)))

context._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'isGroup'), isGroup, scope=context, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 65, 3)))

context._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'title'), title, scope=context, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 66, 3)))

context._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'completionState'), completionState, scope=context, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 67, 3)))

context._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'color'), color, scope=context, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 68, 3)))

context._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'fontStyle'), fontStyle, scope=context, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 69, 3)))

context._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ID'), ID, scope=context, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 70, 3)))

context._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ChildItems'), ChildItems, scope=context, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 71, 3)))

context._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ChildItem'), ChildItem, scope=context, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 72, 3)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 63, 2))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(context._UseForTag(pyxb.namespace.ExpandedName(None, 'isExpanded')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 64, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(context._UseForTag(pyxb.namespace.ExpandedName(None, 'isGroup')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 65, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(context._UseForTag(pyxb.namespace.ExpandedName(None, 'title')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 66, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(context._UseForTag(pyxb.namespace.ExpandedName(None, 'completionState')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 67, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(context._UseForTag(pyxb.namespace.ExpandedName(None, 'color')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 68, 3))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(context._UseForTag(pyxb.namespace.ExpandedName(None, 'fontStyle')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 69, 3))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(context._UseForTag(pyxb.namespace.ExpandedName(None, 'ID')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 70, 3))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(context._UseForTag(pyxb.namespace.ExpandedName(None, 'ChildItems')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 71, 3))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(context._UseForTag(pyxb.namespace.ExpandedName(None, 'ChildItem')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 72, 3))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_8._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
context._Automaton = _BuildAutomaton_5()




def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    return fac.Automaton(states, counters, True, containing_state=None)
title._Automaton = _BuildAutomaton_6()




ChildItems._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ID'), ID, scope=ChildItems, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 202, 3)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 201, 2))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 202, 3))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(ChildItems._UseForTag(pyxb.namespace.ExpandedName(None, 'ID')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 202, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
ChildItems._Automaton = _BuildAutomaton_7()




ChildItem._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ChildItem'), ChildItem, scope=ChildItem, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 207, 3)))

ChildItem._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ChildItems'), ChildItems, scope=ChildItem, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 208, 3)))

ChildItem._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ID'), ID, scope=ChildItem, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 209, 3)))

ChildItem._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'color'), color, scope=ChildItem, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 210, 3)))

ChildItem._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'completionState'), completionState, scope=ChildItem, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 211, 3)))

ChildItem._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'fontStyle'), fontStyle, scope=ChildItem, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 212, 3)))

ChildItem._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'isExpanded'), isExpanded, scope=ChildItem, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 213, 3)))

ChildItem._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'isGroup'), isGroup, scope=ChildItem, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 214, 3)))

ChildItem._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'title'), title, scope=ChildItem, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 215, 3)))

ChildItem._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'notes'), notes, scope=ChildItem, location=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 216, 3)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 206, 2))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ChildItem._UseForTag(pyxb.namespace.ExpandedName(None, 'ChildItem')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 207, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ChildItem._UseForTag(pyxb.namespace.ExpandedName(None, 'ChildItems')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 208, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ChildItem._UseForTag(pyxb.namespace.ExpandedName(None, 'ID')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 209, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ChildItem._UseForTag(pyxb.namespace.ExpandedName(None, 'color')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 210, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ChildItem._UseForTag(pyxb.namespace.ExpandedName(None, 'completionState')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 211, 3))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ChildItem._UseForTag(pyxb.namespace.ExpandedName(None, 'fontStyle')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 212, 3))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ChildItem._UseForTag(pyxb.namespace.ExpandedName(None, 'isExpanded')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 213, 3))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ChildItem._UseForTag(pyxb.namespace.ExpandedName(None, 'isGroup')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 214, 3))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ChildItem._UseForTag(pyxb.namespace.ExpandedName(None, 'title')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 215, 3))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ChildItem._UseForTag(pyxb.namespace.ExpandedName(None, 'notes')), pyxb.utils.utility.Location('/Users/dave/git/github.com/Public/Swapsies/xsd/cod.types.xsd', 216, 3))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_9._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
ChildItem._Automaton = _BuildAutomaton_8()




def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    return fac.Automaton(states, counters, True, containing_state=None)
notes._Automaton = _BuildAutomaton_9()

