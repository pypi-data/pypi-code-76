"""


The  Rotterdam  Exchange  Format  Initiative  (REFI),  responsible  for  the  interoperability  standard
described  in  this  document,  originated  in  September  2016  as  a  result  of  the  KWALON  Conference:
Reflecting on the Future of QDA Software, held at Erasmus University Rotterdam. Software developers
attending  the  conference  agreed  to  work  together  in  developing  an  exchange  format,  thus  en

[PDF](https://www.qdasoftware.org/wp-content/uploads/2019/09/REFI-QDA-1-5.pdf)


"""
import typing,uuid,re,platform,inspect,logging,pathlib
import lxml.etree as etree
from portableqda import __version__

__all__ = ["log","etree"] #infrastructure
__all__ +=["CATEGORY_SEP","ENCODING"]  #format
__all__ +=["codebookCls","codeCls","setCls"] #interface

def _trace(self, message, *args, **kws):
    if self.isEnabledFor(logging.DEBUG - 1):
        self._log(logging.DEBUG - 1, message, args, **kws)  # pylint: disable=W0212

logging.addLevelName(logging.DEBUG - 1, "TRACE")
logging.Logger.trace = _trace  # type: ignore

logger = logging.getLogger
log = logger(__name__)

parser = etree.XMLParser()

CATEGORY_SEP = "::"
ENCODING = "utf-8"
CODEBOOK_UNPOPULATED=b"""<?xml version="1.0" encoding="UTF-8"?>
            <CodeBook xmlns="urn:QDA-XML:codebook:1.0" xmlns:qda="urn:QDA-XML:codebook:1.0"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="urn:QDA-XML:codebook:1.0 http://schema.qdasoftware.org/versions/Codebook/v1.0/Codebook.xsd"><Codes/><Sets/></CodeBook>"""
TAG_DESC="Description"
TAG_CODE="Code" #expected container is TAG_CODE+"s", "Codes"
TAG_SET="Set" #expected container is TAG_SET+"s"
TAG_SET_MEMBERCODE = "MemberCode"
CODES_ID = 0 #order of the container in the codebook
SETS_ID = 1 #order of the container in the codebook

# GUIDType, The schema can be accessed online at http://schema.qdasoftware.org/versions/Codebook/v1.0/Codebook.xsd
guidRe=re.compile("([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})|(\{[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\})")
# RGBType, The schema can be accessed online at http://schema.qdasoftware.org/versions/Codebook/v1.0/Codebook.xsd
colorRe=re.compile("#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})")

LOCAL_NAMESPACE = uuid.uuid3(uuid.NAMESPACE_DNS,platform.node()*2)

class elementCls:
    pass

def valid_guid(guid=None,name=None):
    result=guid
    if guid is None or not re.match(guidRe,guid):
        if name is None:
            import time
            name = time.strftime("%s", time.gmtime())
        result = str(uuid.uuid5(LOCAL_NAMESPACE, name)).upper()
    return result

def valid_color(color=None):
    result=color
    if color is None or not re.match(colorRe,color):
        result = "#000000"
    return result

class codeSetDict(typing.MutableMapping):
    """defaultDict with type validation upon item creation

    based on: https://stackoverflow.com/questions/3387691/how-to-perfectly-override-a-dict
    """
    def __init__(self, memberTypes: list):
        if isinstance(memberTypes, typing.Sequence):
            self._memberTypes = memberTypes
        else:
            raise ValueError("ERR: a sequence containing types has to be passed as argument to 'memberTypes'")
        self._store = dict()
        #keys = self._store.keys # not needed, using __iter__ ?

    def __getitem__(self, key):
        return self._store.setdefault(key, None)

    def __setitem__(self, key, value):
        """
        Raises ValueError when type of 'value' not in _memberTypes


        :param key: as in dict
        :param value: as in dict
        :return: nothing
        """
        if not type(value) in self._memberTypes:
            raise  ValueError("type of argument ({}) not in memberTypes ({})".
                              format(type(value),
                                     self._memberTypes))
        self._store[key] = value

    def __delitem__(self, key):
        del self._store[key]

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def allowType(self,memberCandidateType):
        #return type(memberCandidate) in self._memberTypes
        return memberCandidateType in self._memberTypes

    def __repr__(self):
        return self._store.__repr__()

class codebookCls():
    def __init__(self,input=None,output=None):
        """
        REFI-QDA codebook object, as per https://www.qdasoftware.org/codebook-exchange/, retrieved jan/2020, cited 
        as [REFI-QDA21].  
        If not otherwise stated, [REFI-QDA21] standard applies to attributes and member objects throughout the module.

        :param input: name of a file-like object o stream URL, possibly fully qualified. optional, can be override when calling  or readQdcStrem()
        :param output: name of a file-like object o stream URL, if not fully qualified uses home directory . read-only. defaults to standard output.
        :param origin: string as per [REFI-QDA21]
        """
        self.__input=input
        self.originDict = dict(origin="portableQDA "+__version__)
        self.sets=codeSetDict(memberTypes=(setCls,))  #index of Code elements, validate and make sure they last
        self.codes=codeSetDict(memberTypes=(codeCls,)) #index of Set elements, make sure they last in lxml's proxy
        self._codes_id = CODES_ID
        self._sets_id = SETS_ID
        self.miscElements=dict() #elements other than sets or codes, presumably none
        # http://schema.qdasoftware.org/versions/Codebook/v1.0/Codebook.xsd
        self.children = dict()
        #self.tree=etree.ElementTree(etree.XML("""<?xml version="1.0" encoding="UTF-8"?>
        self.tree=etree.ElementTree(etree.fromstring(CODEBOOK_UNPOPULATED))
        #print(self.tree.docinfo.doctype)
        #< !DOCTYPE root SYSTEM; "test" >
        #tree.docinfo.public_id = ’- // W3C // DTD; XHTML; 1.0; Transitional // EN’
        #self.tree.docinfo.system_url = ’file: // local.dtd’
        log.debug("tree created, root node: 'CodeBook'. see REFI-QDA 1.5")
        self.__output = None
        if output is not None:
            try: #test whether the requested output is writable
                self.__output=pathlib.Path(output)
                pass
                if len(self.__output.parts) == 1:
                    self.__output = self.__output.home() / self.__output
                if self.__output.exists():
                    self.__output.touch()
                else:
                    with open(self.__output,mode="wb") as fh:
                        fh.write(etree.tostring(element_or_tree=self.tree))
                log.info("output is {}".format(self.__output))
            except Exception as e:
                self.__output = None
                log.warning("output param not pointing to a writable file, setting to None. writeQdcFile() will use standard output, error: {}".format(e))
                log.info("for streaming output try writeQCDstream")
        #log.trace(self.tree.tostring())
        # if output is None:
        #     self.saxOutput = None
        # else:
        #     self.saxOutput=XMLGenerator(self.output, encoding='utf-8',
        #                  short_empty_elements=True)
        #     self.saxOutput.startDocument()
        #     self.saxOutput.startPrefixMapping(None, 'urn:QDA-XML:codebook:1:0')

    @property
    def input(self):
        return self.__input

    @input.setter
    def input(self,input,*args,**kwargs):
        if hasattr(input,"read"):
            self.__input=input
        else:
            try: #test whether the requested input is suitable
                self.__input=pathlib.Path(input)
                if len(self.__input.parts) == 1:
                    self.__input = pathlib.Path.cwd() / input
                    if not self.__input.exists():
                        self.__input = self.__input.home() / input
                if not self.__input.exists():
                    raise FileNotFoundError("tried {}, then {}".format(pathlib.Path.cwd() / input, self.__input.home() / input))
            except Exception as e:
                self.__input = None
                log.warning("input param: file not foound. setting to None. readQdcFile(input=___) need a valid input. {}".format(e))

    @property
    def output(self):
        return self.__output

    @output.setter
    def output(self,*args,**kwargs):
        log.warning("output set when codebook was instantiated, read-only attribute")

    def tostring(self,element_or_tree=None):
        if element_or_tree is None:
            element_or_tree = self.tree
        etree.tostring(element_or_tree=element_or_tree)

    def createElement(self,*args, elementCls: elementCls, name: str, parent = None,  **kwargs):
        error=True
        errorDesc=""
        if self.codes.allowType(elementCls):
            idx=self.codes
        elif self.sets.allowType(elementCls):
            idx=self.sets
        else:
            msg="element not recognised, indexed in miscElements"
            errorDesc+=msg+". "
            log.warning(msg)
            idx=self.miscElements
        if idx[name] is not None:
            msg="new element replaces existing one: {}" ,".format(name)"
            errorDesc+=msg+". "
            log.warning(msg)
        if parent is not None:
            if idx[parent] is None:
                msg="new orphan element {}. parent not found: {}".format(name, parent)
                errorDesc += msg+". "
                log.warning(msg)
        if "sets" in kwargs.keys():
            if elementCls is setCls:
                msg="sets are not allowed to nest, discarding argument. see REFI-QDA v1.5"
                errorDesc += msg+". "
                log.warning(msg)
                del kwargs["sets"]
        # Create code, sets are created by constructor if needed
        idx[name]=elementCls(ctnr=self, name=name,parent=idx[parent], **kwargs)
        if len(errorDesc) == 0:
            error = False
        return error,errorDesc,idx[name]


    def writeQdcFile(self):
        if self.output is None:
            log.info("codebook.output not set, printing XML to standard output".format(self))
            log.debug("document dump starts -----"+"8<----"*5)
            print(etree.tostring(self.tree, xml_declaration=True, encoding = ENCODING, pretty_print = True).
                  decode(ENCODING))
            log.debug("document dump ends -----"+"8<----"*5)
        else:
            #fh = open(self.output,"")
            log.info("exporting as REFI-QDC  codebook to file: {}".format(self.output))
            self.tree.write(str(self.output), xml_declaration=True, encoding = ENCODING, pretty_print = True)
            # self.saxOutput.startElementNS(
            #     (None, 'CodeBook'), 'CodeBook',
            #     AttributesNSImpl({(None, 'origin'): self.origin},
            #                      {(None, 'origin'): 'origin'}),
            # )
            # self.saxOutput.startElementNS(
            #     (None, 'Codes'), 'Codes',
            #     AttributesNSImpl({}, {}),
            # )
            # for codeKey in self.codes.keys():
            #     code = self.codes[codeKey]
            #     self.saxOutput.startElementNS(
            #         (None, 'Code'), 'Code',
            #         AttributesNSImpl({(None, 'guid'): code.guid,
            #                           (None, 'name'): code.name,
            #                           (None, 'color'): code.color,
            #                           (None, 'isCodable'): 'true'},
            #                          {(None, 'guid'): 'guid',
            #                           (None, 'name'): 'name',
            #                           (None, 'color'): 'color',
            #                           (None, 'isCodable'): 'isCodable'}),
            #     )
            #     self.saxOutput.startElementNS((None, 'Description'),
            #                                   'Description',
            #                                   AttributesNSImpl({},{}))
            #     self.saxOutput.characters(code.description)
            #     self.saxOutput.endElementNS((None, 'Description'), 'Description')
            #     self.saxOutput.endElementNS((None, 'Code'), 'Code')
            # self.saxOutput.endElementNS((None, 'Codes'), 'Codes')
            # self.saxOutput.startElementNS((None, 'Sets'), 'Sets',AttributesNSImpl({}, {}),)
            # for setKey in self.sets.keys():
            #     setObj = self.sets[setKey]
            #     self.saxOutput.startElementNS(
            #         (None, 'Set'), 'Set',
            #         AttributesNSImpl({(None, 'guid'): setObj.guid,
            #                           (None, 'name'): setObj.name},
            #                          {(None, 'guid'): 'guid',
            #                           (None, 'name'): 'name',}),
            #     )
            #     for memberCodeKey in setObj.memberCodes.keys():
            #         self.saxOutput.startElementNS((None, 'MemberCode'), 'MemberCode',
            #                 AttributesNSImpl({(None, 'guid'): setObj.memberCodes[memberCodeKey].guid},
            #                     {(None, 'guid'): 'guid'}))
            #         self.saxOutput.endElementNS((None, 'MemberCode'), 'MemberCode')
            #     self.saxOutput.endElementNS((None, 'Set'), 'Set')
            # self.saxOutput.endElementNS((None, 'Sets'), 'Sets')
            # self.saxOutput.endElementNS((None, 'CodeBook'), 'CodeBook')
            # self.saxOutput.endPrefixMapping(None)
            # self.saxOutput.endDocument()

    def writeQdcStream(self):
        if self.output is None:
            self.writeQdcFile()
        else:
            raise NotImplementedError("writing to stream not yet implemented, please try writeQdcFile()")
            #etree.xmlfile...

    def readQdcFile(self,input = None):
        """
        load date from a QDC file

        :param input: a file path, defaults to the input already set (codebookCls.input)
        :return:
        """

        if input is None:
            if self.input is None:
                raise ValueError("readQdcFile: specify input file, either setting the input attribute or as a parameter to readQdc()")
        else:
            self.input=input
            if self.input is not None:
                log.info("reading QDC data from {}".format(self.input))
                self.tree=etree.parse(str(self.__input))
        def tagMissing(id,tag):
            result = len(self.tree.getroot()) - 1 < id or \
                not self.tree.getroot()[id].tag.endswith(tag + "s")
            return  result
        #
        # validate input accordint to REFI-QDA 1.5
        #
        #look for "Codes" container
        if tagMissing(id=self._codes_id,tag=TAG_CODE): #Codes container not where it's supposed to be
            try:
                id_antes=self._codes_id
                self._codes_id=[i for i, e in enumerate(self.tree.getroot()[:]) if e.tag.endswith(TAG_CODE + "s")][0]
                log.debug("readQdcFile: {}s container not where it's supposed to be([0][{}]): found at tree[0][{}]".
                          format(TAG_CODE, id_antes, self._codes_id))
            except Exception as e:
                pass
            if tagMissing(id=self._codes_id,tag=TAG_CODE):
                raise ValueError("readQdcFile: tag {} not found (mandatory element under CodeBook tag)".format(TAG_CODE+"s"))

        #look for "Sets" container
        if tagMissing(id=self._sets_id,tag=TAG_SET): #Sets container not where it's supposed to be
            try:
                id_antes= self._sets_id
                self._sets_id=[i for i, e in enumerate(self.tree.getroot()[:]) if e.tag.endswith(TAG_SET + "s")][0]
                log.debug("readQdcFile: {}s container not where it's supposed to be([0][{}]): found at tree[0][{}]".
                          format(TAG_SET, id_antes, self._sets_id))
            except Exception as e:
                pass
            if tagMissing(id=self._sets_id,tag=TAG_SET):
                raise ValueError("readQdcFile: tag {} not found (mandatory element under CodeBook tag)".format(TAG_SET+"s"))

        #
        #
        #
        # if not hasattr(self.input,"read"):
        #     raise ValueError("{}.input is not a file-like object ('read' method expected)".format(self.__class__.__name__))
        # else:
        #     self.originDict["URI"]=str(self.input) #sort of ... what if its a stream ?
        #     parser = sax.make_parser()
        #     parser.setFeature(sax.handler.feature_namespaces, 0) # turn off namepsaces, why??
        #     handler=codebookHandler(ctnr=self)
        #     handler.tags["CodeBook"]=self
        #     handler.tags["Code"]=codeCls
        #     handler.tags["Set"]=setCls
        #     #handler.tags[""]=
        #     #handler.tags[""]=
        #     parser.setContentHandler(handler)
        #     parser.parse(self.input)
        #     pass

class projectCls():
    def __init__(self):
        raise NotImplementedError()

#class codeCls(elementCls,etree.ElementBase): #not a good idea according to docs :/
class codeCls(elementCls):
    TAG=TAG_CODE

    def __init__(self, ctnr: codebookCls, name: str, parent = None, color=None, guid=None, description="", sets=list()):
        self.name=name
        self.ctnr = ctnr
        attrib={"name":name,"guid":valid_guid(guid,name),"color":valid_color(color),"isCodable":"true"}
        #self.children = codeSetDict(memberTypes=(self.__class__,))
        self.sets=codeSetDict(memberTypes=(setCls,))
        # self.children = defaultdict(lambda : None)
        # self.sets=defaultdict(lambda : None)
        if parent is None:
            #Codes not really orphan: the are childs to de "Codes" container
            ctnr_idx=ctnr.tree.getroot()[ctnr._codes_id]
            self.etreeElement=etree.SubElement(ctnr_idx,self.__class__.TAG,attrib=attrib)
        else:
            self.etreeElement = etree.SubElement(parent.etreeElement, self.__class__.TAG, attrib=attrib)
        if len(description) > 0:
            etree.SubElement(self.etreeElement, TAG_DESC).text=description
        self.attrib = self.etreeElement.attrib
        for miSet in sets:
            if ctnr.sets[miSet] is None:
                msg="creating set {}".format(miSet)
                error, errorDesc, set = ctnr.createElement(elementCls=setCls, name=miSet,
                        description="project: {} :: document {}".format(miSet,miSet))
                if error:
                    msg = "error {} when ".format(errorDesc) + msg
                    log.warning(msg)
            if ctnr.sets[miSet] is None:
                msg = "code {} should be part of set {} ".format(name,miSet)
                log.warning(msg)
            else:
                ctnr.sets[miSet].appendMemberCode(self)
                msg = "added code {} to set {} ".format(name,miSet)
                log.debug(msg)
            #raise  ValueError("ERR: set '{}' not in codeBook , current sets: {}".format(miSet,ctnr.sets.keys()))


    def __repr__(self):
        return self.name

class setCls(elementCls):
    TAG=TAG_SET

    def __init__(self, ctnr: codebookCls, name: str, parent = None, guid=None, color = "#FFFFFF", description=""):
        self.name=name
        self.ctnr=ctnr
        attrib={"name":name,"guid":valid_guid(guid,name),"color":valid_color(color),"isCodable":"true"}
        self.memberCodes=codeSetDict(memberTypes=(codeCls,))
        #self.memberCodes = defaultdict(lambda : None)
        if parent is not None:
            log.warning("sets are not allowed to nest. see REFI-QDA 1.5")
        self.parent = None
        self.children = None# codeSetDict(memberTypes=(self.__class__,))# not defined in the standard
        ctnr_idx=ctnr.tree.getroot()[ctnr._sets_id]
        self.etreeElement=etree.SubElement(ctnr_idx,self.__class__.TAG,attrib=attrib)
        if len(description) > 0:
            etree.SubElement(self.etreeElement, TAG_DESC).text=description
            #raise  ValueError("ERR: set '{}' not in codeBook , current sets: {}".format(miSet,ctnr.sets.keys()))
        self.attrib=self.etreeElement.attrib

    def appendMemberCode(self,code):
        """
        add code to set, return silently if already there

        :param code:
        :return:
        """
        etree.SubElement(self.etreeElement, TAG_SET_MEMBERCODE, {"guid":code.attrib["guid"]})
        self.memberCodes[code] = code

    def __repr__(self):
        return self.name
