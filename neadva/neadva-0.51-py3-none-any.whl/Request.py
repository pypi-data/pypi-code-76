#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""NAV reporting Request module

This module is a NAV report protocol implementation for Python.

Do not use this module directly, instead import from NAV module itself like:

    from neadva import Invoice, Transaction, SubmitInvoices, MapTaxNumber, Config
    Config.user = {"login": "login",
            "password": "password",
            "taxNumber": "12345678",
            "signKey": "12-345678-910111213141516",
            "exchangeKey": "12345678910"}
    Config.software = {"softwareId": "HU12345678RANDOM",
                "softwareName": "None",
                "softwareOperation": "LOCAL_SOFTWARE",
                "softwareMainVersion": "0",
                "softwareDevName": "NAV Kft.",
                "softwareDevContact": "nun@nil.com"}
    test = MapTaxNumber('12345678')
    test = test()

Optionally you can choose to not compress data:
    Config.compression = False

Or go live with:
    Config.live = True

Config class is global for all instances in the current interpreter run.
However you can supply an instance explicitly via config = Config(**configvalues) where configvalues
has user dict and software dict and includes other non-default modifications
"""
import sys
import secrets
import base62
import base64
import requests
import gzip
import traceback
import _locale
import os
import lxml
from . import Util
from .Config import Config
from time import sleep
from urllib.request import pathname2url
from urllib.parse import urljoin
from datetime import datetime, timezone
from typing import Optional, Callable, Literal, Union, List, Iterable
from enum import Enum
from pprint import pprint
from collections import deque
from lxml import objectify, etree


class STATUSOP(Enum):
    PREPARE = "PREPARE"
    DONE = "DONE"
    FAILED = "FAILED"


class INVOICEOP(Enum):
    DELETE = "ANNUL"
    CREATE = "CREATE"
    UPDATE = "MODIFY"
    CANCEL = "STORNO"


class RESPONSEOP(Enum):
    RECEIVED = "RECEIVED"
    PROCESSING = "PROCESSING"
    SAVED = "SAVED"
    FINISHED = "FINISHED"
    NOTIFIED = "NOTIFIED"


class ObjectError(Exception):
    pass


class ResponseError(Exception):
    pass


class RequestError(Exception):
    pass


class DocumentError(Exception):
    pass


class CheckError(Exception):
    pass


class _BaseRequest(object):
    """
    Base request class implementing all the necessary xml checks and requests to server
    Returns:
        (str): returns either request if no call done yet or response.
    """
    __operation_mapping = {'ManageAnnulment': 'manageAnnulment', 'ManageInvoice': 'manageInvoice', 'QueryInvoiceChainDigest': 'queryInvoiceChainDigest',
                           'QueryInvoiceCheck': 'queryInvoiceCheck', 'QueryInvoiceData': 'queryInvoiceData', 'QueryTaxpayer': 'queryTaxpayer', 'QueryTransactionList': 'queryTransactionList', 'QueryTransactionStatus': 'queryTransactionStatus', 'TokenExchange': 'tokenExchange'}

    def __init__(self, operation: str, config: Optional[Config] = None) -> None:
        self.request_status = STATUSOP.PREPARE
        self.request_id = None
        self.operation = None
        self.request_command = None
        self.config = None
        self.request_timestamp = None
        self.request_version = None
        self.response_status = None
        self.response_nsmap = dict()
        self.request_xml = None
        self.request_signature_string = ""
        if operation in self.__operation_mapping:
            self.request_command = operation + 'Request'
            self.operation = self.__operation_mapping[operation]
        else:
            raise CheckError(
                "Error:Invalid:Command", f"{operation} is not within [{', '.join(self.__operation_mapping)}]")
        if not config:
            if Config:
                config = Config()
            else:
                raise CheckError("Error:No:Configuration", 'No config defined')
        self.config = config
        self.request_id = base62.encodebytes(secrets.token_bytes(25))[:30]
        self.request_timestamp = datetime.now(timezone.utc).isoformat(
            timespec="milliseconds").replace("+00:00", "Z")
        self.request_version = self.config.apiversion
        COMMON = self.config.ns('common')
        APINS = self.config.ns('api')
        NSMAP = {None: APINS[1:-1],
                 'common': COMMON[1:-1]}
        self.request_xml = etree.Element(
            f"{APINS}{self.request_command}", nsmap=NSMAP)
        # Header
        header = etree.SubElement(self.request_xml, f"{COMMON}header")
        etree.SubElement(header, f"{COMMON}requestId").text = self.request_id
        etree.SubElement(
            header, f"{COMMON}timestamp").text = self.request_timestamp
        etree.SubElement(
            header, f"{COMMON}requestVersion").text = self.request_version
        etree.SubElement(header, f"{COMMON}headerVersion").text = '1.0'
        # User
        user = etree.SubElement(self.request_xml, f"{COMMON}user")
        etree.SubElement(
            user, f"{COMMON}login").text = self.config.user['login']
        etree.SubElement(user, f"{COMMON}passwordHash",
                         cryptoType='SHA-512').text = self.config.passwordHash
        etree.SubElement(
            user, f"{COMMON}taxNumber").text = self.config.user['taxNumber']
        self.request_signature_xml = etree.SubElement(user, f"{COMMON}requestSignature",
                                                      cryptoType='SHA3-512')
        # Software
        software = etree.SubElement(self.request_xml, f"{APINS}software")
        for k, v in self.config.software.items():
            etree.SubElement(software, f"{APINS}{k}").text = v
        self.request_signature_xml.text = self.signature
        super().__init__()

    def __call__(self) -> bool:
        """
        Call overload. To send the request just get and instance and call it like:
            f = _BaseRequest('doSomething',config=Config())
            f()
        response_xml property will be filled with lxml.etree.Element
        Will raise an error in case the request is invalid - shouldn't happen.
        Raises DocumentError in case of invalid XML before request
        Raises RequestError in and during Transport
        Raises ResponseError in case of invalid response which doesn't validate
        """
        if not self.request_valid:
            raise DocumentError(
                "Error:Invalid:XMLData", "XML did not validate, check the xml of request") from exc
        else:
            self.__post()
            self.request_status = STATUSOP.DONE  # After this portion request is done
            if len(self.response_xml):
                try:
                    self.validate('api', self.response_xml)
                except Exception as exc:
                    self.response_status = STATUSOP.FAILED
                    raise ResponseError(
                        "Error:Invalid:Response", "Response did not validate, check xml of response") from exc
                try:
                    self.response_nsmap = self.response_xml.nsmap
                    status = self.response_xml.findtext(
                        f".//{self.config.ns('common')}funcCode")
                    if status.upper() == 'OK':
                        self.response_status = STATUSOP.DONE
                    else:
                        self.response_status = STATUSOP.FAILED
                except Exception as exc:
                    raise ResponseError("Error:Invalid:Response",
                                        "Response has problems") from exc
                else:
                    return True
            else:
                raise ResponseError("Error:No:Response",
                                    "Response from endpoint is empty")

    def __post(self) -> None:
        """
        Posts the request to endpoint
        """
        try:
            request = requests.post(urljoin(self.config.URL, self.operation), data=self.request, headers={
                'Content-Type': 'application/xml;charset="UTF-8"', 'Accept': 'application/xml'}, timeout=60)
            self.response_xml = etree.XML(request.content)
        except requests.exceptions.Timeout:
            self.request_status = STATUSOP.FAILED
            self.response_status = STATUSOP.FAILED
            raise RequestError("Error:Timeout:Request",
                               "Response from endpoint timed out")
        except requests.exceptions.HTTPError:
            self.request_status = STATUSOP.FAILED
            self.response_status = STATUSOP.FAILED
            raise RequestError("Error:Invalid:Request",
                               "HTTP Error")
        except requests.exceptions.TooManyRedirects:
            self.request_status = STATUSOP.FAILED
            self.response_status = STATUSOP.FAILED
            raise RequestError("Error:Invalid:Request",
                               "Endpoint reports redirects which should not happen")
        except Exception as exc:
            self.request_status = STATUSOP.FAILED
            self.response_status = STATUSOP.FAILED
            raise RequestError(
                "Error:Unknown:Request", "Unknown error raised, check previous exceptions") from exc

    def validate(self, scheme: Literal['api', 'data', 'annulment'] = 'api', xml: Optional[etree.Element] = []) -> None:
        """
        Raises lxml errors on bad validation of xml
        """
        if not len(xml):
            xml = self.request_xml
        if not len(xml):
            raise RequestError("Error:No:XMLData",
                               "No XML to validate found, error")
        xmlschemadoc = etree.parse(getattr(self.config, scheme + 'XsdFile'))
        for i in xmlschemadoc.findall(".//{http://www.w3.org/2001/XMLSchema}import"):
            i.attrib['schemaLocation'] = self.config.revxsdns(
                i.attrib['namespace'])
        xmlschema = etree.XMLSchema(xmlschemadoc)
        try:
            xmlschema.assertValid(xml)
        except lxml.etree.DocumentInvalid:
            errors = []
            for error in xmlschema.error_log:
                errors.append(f'{error.message}: {error.line}')
            raise CheckError("Error:Invalid:Xml", '\n'.join(errors))

    @property
    def request_valid(self) -> bool:
        """
        Soft function to check if valid or not, run validate to get errors raised
        """
        try:
            self.validate()
        except Exception as exc:
            raise CheckError("Error:Invalid:XML",
                             "XML data didn't verify with xsd") from exc
        else:
            return True

    @property
    def valid(self) -> bool:
        """
        Returns if there's a response_xml, otherwise raises ResponseError
        """
        try:
            getattr(self, 'response_xml')
        except AttributeError:
            raise ResponseError(
                "Error:Invalid:Response", "Response not received")
        else:
            return True

    @classmethod
    def _parseval(cls, tag):
        """
        Returns tuple from tag of name without namespace and text
        """
        return tag.tag.split('}')[1], tag.text

    @ property
    def signature(self) -> str:
        """
        Final signature stamp to put into signKey element, contains request_signature_string
        """
        ts = ''.join(filter(lambda x: x.isnumeric(),
                            self.request_timestamp))[:-3]
        return Util.sha3_512(f"{self.request_id}{ts}{self.config.user['signKey']}{self.request_signature_string}")

    @ property
    def request(self):
        """
        String representation of the request
        """
        return etree.tostring(self.request_xml, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode()

    @ property
    def response(self):
        """
        String representation of the response
        """
        if self.valid:
            return etree.tostring(self.response_xml, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode()
        else:
            return ""

    def __str__(self):
        if self.valid:
            return self.response
        else:
            return self.request

    @ request_valid.setter
    @ request_valid.deleter
    @ valid.setter
    @ valid.deleter
    @ signature.setter
    @ signature.deleter
    @ response.setter
    @ response.deleter
    @ request.setter
    @ request.deleter
    def passer(self, *args, **kwargs):
        raise NotImplementedError("Function not implemented")


class _ImmutableAttributesMixIn(object):
    """
    Allows to access object attributes in a predictable way as a dict.
    """
    _config = None

    def __init__(self, *args, **kwargs):
        if 'config' in kwargs:
            self._config = kwargs['config']
        for x in args:
            if isinstance(x, Config):
                self._config = x
        if not self._config:
            self._config = Config()
        if getattr(self, 'accessible_attributes', None):
            for i, v in self.accessible_attributes.items():
                setattr(self, i, v)
        try:
            # This is to init any non-mixin classes
            super().__init__(*args, **kwargs)
        except TypeError:
            # object always comes last, so we just init it
            super().__init__()

    def __len__(self):
        if getattr(self, 'accessible_attributes', None):
            return self.accessible_attributes.__len__()
        return 0

    def __getitem__(self, key):
        if not getattr(self, 'accessible_attributes', None):
            raise KeyError
        if not key in self.accessible_attributes:
            raise KeyError
        return getattr(self, key)

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

    def __missing__(self, key):
        return KeyError

    def items(self):
        if not getattr(self, 'accessible_attributes', None):
            return {}
        for i in self.accessible_attributes:
            yield i, getattr(self, i)

    def keys(self):
        if not getattr(self, 'accessible_attributes', None):
            return []
        return self.accessible_attributes.keys()

    def values(self):
        if not getattr(self, 'accessible_attributes', None):
            return []
        ret = []
        for i in self.accessible_attributes:
            ret.append(getattr(self, i))
        return ret


class Token(_ImmutableAttributesMixIn, _BaseRequest):
    """
    Token class, mostly for internal use.
    Arguments:
        config (Config): optionally provide custom config.
    Attributes:
        .valid provides information whether it is still valid to use or not.
        .validfrom datetime of validity from
        .validtill datetime of validity till
        .used is whether it is used or not.
    Returns:
        str: returns token decoded in text form, unless it is not valid anymore, then empty string.
    """

    def __init__(self, config: Optional[Config] = None):
        self.accessible_attributes = {'token': None, 'validtill': datetime.now(
            timezone.utc), 'used': 0, 'validfrom': datetime.now(timezone.utc)}
        super().__init__('TokenExchange', self._config)

    def __call__(self):
        api = self.config.ns('api')
        super().__call__()
        self.token = Util.aes128_decrypt(self.response_xml.findtext(
            f'.//{api}encodedExchangeToken'), self.config.user['exchangeKey'])
        self.validfrom = datetime.fromisoformat(
            self.response_xml.findtext(f'.//{api}tokenValidityFrom').replace('Z', '+00:00'))
        self.validtill = datetime.fromisoformat(
            self.response_xml.findtext(f'.//{api}tokenValidityTo').replace('Z', '+00:00'))
        return self

    def __eq__(self, other):
        if isinstance(other, None):
            return not self.valid
        if isinstance(other, Token):
            return self.token == other.token
        return NotImplemented

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        x = self.__eq__(other)
        if x is NotImplemented:
            return NotImplemented
        return not x

    def __str__(self):
        if self.token:
            if self.valid:
                return self.token
        return "INVALID"

    @property
    def valid(self) -> bool:
        """
        Returns validity of token, returns False or True
        """
        if self.used:
            return False
        try:
            sleep((self.validfrom - datetime.now(timezone.utc)).total_seconds())
        except ValueError:
            pass  # bug if nav server drifting.
        return self.validfrom < datetime.now(timezone.utc) < self.validtill


class MapTaxNumber(_ImmutableAttributesMixIn, _BaseRequest):
    """Gets tax number data

    Arguments:
        tax_number (str): first 8 letters of tax_number, automatically truncated
        config (Config): optionally provide Config instance

    Returns:
        (str): returns name and addresslist
        (dict): following keys: modificationtime, name, type, id, vatcode, addresslist
            addresslist consists of dictionaries with name of address (i.e. HQ) as key and dictionary of returned data from NAV
    """

    def __init__(self, tax_number: str, config: Optional[Config] = None):
        self.accessible_attributes = {'modificationtime': None, 'name': None, 'type': None,
                                      'id': None, 'vatcode': None, 'addresslist': list()}
        super().__init__(operation='QueryTaxpayer', config=self._config)
        self._validtaxpayer = None
        etree.SubElement(
            self.request_xml, f"{self._config.ns('api')}taxNumber").text = tax_number[:8]

    def __call__(self):
        api = self.config.ns('api')
        base = self.config.ns('base')
        super().__call__()
        self.modificationtime = datetime.fromisoformat(self.response_xml.findtext(
            f".//{api}infoDate").replace('Z', '+00:00'))
        self.name = self.response_xml.findtext(f'.//{api}taxpayerName').title()
        self.type = self.response_xml.findtext(
            f'.//{api}incorporation').title()
        self.id = self.response_xml.findtext(f'.//{base}taxpayerId')
        self.vatcode = self.response_xml.findtext(f'.//{base}vatCode')
        self._validtaxpayer = bool(self.response_xml.findtext(
            f'.//{api}taxpayerValidity'))
        for i in self.response_xml.iterfind(f'.//{api}taxpayerAddressItem'):
            name = i.findtext(f'.//{api}taxpayerAddressType')
            addressdata = {}
            for x in i.findall(f'.//{api}taxpayerAddress/*'):
                an, av = self._parseval(x)
                an = an.lower()
                if not 'code' in an:
                    av = av.title()
                addressdata[an] = av
            self.addresslist.append({name: addressdata})
        return self

    def __str__(self):
        if getattr(self, 'name', None):
            if self.valid:
                retval = f'{self.name}\n'
                for i in self.addresslist:
                    k, v = next(iter(i.items()))
                    retval += f"{k}: {' '.join(v.values())}\n"
                return retval.strip()
        return ""

    @ property
    def valid(self) -> bool:
        """
        Returns validity of tax number if there's a respone otherwise None
        """
        if self._validtaxpayer:
            return self._validtaxpayer


class _GetTransactionState(_ImmutableAttributesMixIn, _BaseRequest):

    def __init__(self, id, config: Optional[Config] = None):
        self.accessible_attributes = {'id': None,
                                      'originalrequest': None, 'state': None}
        super().__init__(operation='QueryTransactionStatus', config=self._config)
        self.id = id

    def __call__(self, returnrequest: bool = False):
        api = self.config.ns('api')
        etree.SubElement(
            self.request_xml, f"{api}transactionId").text = self.id
        if returnrequest:
            etree.SubElement(
                self.request_xml, f"{api}returnOriginalRequest").text = 'true'
        else:
            etree.SubElement(
                self.request_xml, f"{api}returnOriginalRequest").text = 'false'
        super().__call__()
        return self

    def __str__(self):
        return self.response


class Transaction(_ImmutableAttributesMixIn):
    """
    Todo: If required, will be a class implementing Transaction querying in a form of lazy document akin to ORM
    Right now - not necessary in depth, we just need the status.
    """
    statuses = [RESPONSEOP.RECEIVED, RESPONSEOP.PROCESSING,
                RESPONSEOP.SAVED, RESPONSEOP.FINISHED, RESPONSEOP.NOTIFIED]

    def __init__(self, id: str, date: datetime = datetime.now(timezone.utc), config: Optional[Config] = None):
        self.accessible_attributes = {'id': None}
        super().__init__(config=self._config)
        self.id = id

    def __str__(self):
        return self.id

    def __bytes__(self):
        return self.id.encode()

    def __repr__(self):
        return f"<Transaction.{self.id}>"

    def __call__(self):
        state = _GetTransactionState(self.id, config=self._config)()
        self.request_xml = state.request_xml
        self.response_xml = state.response_xml
        self.request = state.request
        self.valid = state.valid
        self.request_valid = state.request_valid
        return self

    @property
    def status(self) -> list:
        if self.response_xml is not None:
            returnlist = []
            for i in self.response_xml.iterfind(f".//{self._config.ns('api')}processingResult"):
                retval = []
                for x in i.iter():
                    if 'businessValidationMessages' in x.tag or 'technicalValidationMessages' in x.tag:
                        for d in x.iter():
                            if d.text:
                                retval.append({d.tag.split('}')[1]: d.text})
                        continue
                    if x.text:
                        retval.append({x.tag.split('}')[1]: x.text})
                returnlist.append(retval)
            return returnlist
        else:
            raise CheckError('Error:Invalid:Call',
                             'Cannot retreive status without calling the class')


class Invoice(_ImmutableAttributesMixIn):
    """
    Invoice representation
    Arguments:
        xml (str): XML data of invoice
        operation (neadva.INVOICEOP): one of the operations from enum neadva.INVOICEOP
    Attributes:
        .operation (neadva.INVOICEOP): one of the operations from enum neadva.INVOICEOP
        .xml (str): XML data of invoice
        .byteval (bytes): byte value of the compressed or non-compressed invoice (based on config instance value)
    Returns:
        (str): conversion returns raw xml
        (bytes): returns base64 encoded bytes of either compressed or not data
    """

    def __init__(self, xml: str, operation: Literal[INVOICEOP.CREATE, INVOICEOP.UPDATE, INVOICEOP.CANCEL] = INVOICEOP.CREATE, config: Optional[Config] = None):
        self.accessible_attributes = {'operation': None,
                                      'xml': None, 'byteval': b''}
        super().__init__(config=self._config)
        self.xml = xml
        self.operation = operation
        self.compression = self._config.compression
        self.validateXML = self._config.validateDataScheme
        self.dataXsdFile = self._config.dataXsdFile
        self.valid
        if self.compression:
            self.byteval = base64.b64encode(
                gzip.compress(self.xml.encode(), 1))
        else:
            self.byteval = base64.b64encode(self.xml.encode())

        self.signature = Util.sha3_512(
            self.operation.value.encode()+self.byteval)

    @classmethod
    def fromfile(cls, filename: str, operation: Literal[INVOICEOP.CREATE, INVOICEOP.UPDATE, INVOICEOP.CANCEL] = INVOICEOP.CREATE, config: Optional[Config] = None):
        data = ""
        with open(filename, 'r') as f:
            data = f.read()
        return cls(data, operation=operation, config=config)

    def __bytes__(self):
        if self.valid:
            return self.byteval
        else:
            raise ObjectError("Error:Invalid:XMLData", "XMLData is invalid")

    def __str__(self):
        return self.xml

    def __repr__(self):
        return f"<Invoice.#{self.signature}>"

    @ property
    def valid(self) -> bool:
        """
        Returns if there's a valid xml, otherwise raises lxml errors
        """
        if len(self.xml) > 15728640:
            return False
        try:
            if self.validateXML:
                xmlschemadoc = etree.parse(self.dataXsdFile)
                for i in xmlschemadoc.findall(".//{http://www.w3.org/2001/XMLSchema}import"):
                    i.attrib['schemaLocation'] = self._config.revxsdns(
                        i.attrib['namespace'])
                xmlschema = etree.XMLSchema(xmlschemadoc)
                try:
                    xmlschema.assertValid(etree.XML(self.xml.encode()))
                except lxml.etree.DocumentInvalid:
                    print(
                        'Validation errors found using schema {0}'.format(self.dataXsdFile))
                    errors = []
                    for error in xmlschema.error_log:
                        errors.append((error.message, error.line))
                    pprint(errors)
                    return False
        except:
            return False
        else:
            return True

    @ valid.setter
    @ valid.deleter
    def passer(self, *args, **kwargs):
        raise NotImplementedError("Function not implemented")


class SubmitInvoices(_ImmutableAttributesMixIn, _BaseRequest):
    """
    Invoice processing class. Can be used as list to manipulate invoices list before requesting.
    When instance is called successfully transaction is saved into .transaction attribute

    Arguments:
        invoice (list(neadva.Invoice)): optionally provide list of invoices.
        config (neadva.Config): optionally provide custom Config instance
    Attributes:
        .transaction (neadva.Transaction): transaction instance
        .invoices (deque(neadva.Invoice, 100)): limited list of invoices.
        .compression: whether to compress or not, gets data from Config - please make sure not to manipulate this as you cannot send compressed and non-compressed invoices
    Returns:
        (str): representation is empty
    """

    def __init__(self, invoices: Optional[List[Invoice]] = [], config: Optional[Config] = None):
        self.accessible_attributes = {'invoices': deque(
            invoices, 100), 'compression': Config.compression, 'token': None, 'transaction': None}
        super().__init__('ManageInvoice', self._config)
        self.compression = self._config.compression
        for i in ['__len__', '__add__', '__iadd__', '__contains__']:
            attr = getattr(self.invoices, i, None)
            if attr:
                # Link deque of invoices to make our object a list like property handler
                setattr(self, i, attr)

    def __contains__(self, val: Invoice):
        return self.invoices.__contains__(val)

    def append(self, val: Invoice):
        if not val in self:
            return self.invoices.append(val)
        else:
            pass

    def __add__(self, val: List[Invoice]):
        for i in val:
            self.append(i)

    def __iadd__(self, val: Iterable[List[Invoice]]):
        for i in val:
            self.append(i)

    def extend(self, val: List[Invoice]):
        for i in val:
            self.append(i)

    def insert(self, i: int, val: Invoice):
        return self.invoices.insert(i+1, val)

    def index(self, val: Invoice, start: Optional[int] = None, stop: Optional[int] = None):
        if start:
            start -= 1
        if stop:
            stop -= 1
        return self.invoices.index(val, start, stop)

    def pop(self, val: Optional[int] = None):
        if val:
            return self.invoices.pop(val - 1)
        else:
            return self.invoices.pop()

    def remove(self, val: Invoice):
        return self.invoices.remove(val)

    def count(self, val: Invoice):
        return self.invoices.count(val)

    def __str__(self):
        return ""

    def __call__(self):
        if not self.token:
            self.token = Token(config=self._config)()
        etree.SubElement(
            self.request_xml, f"{self._config.ns('api')}exchangeToken").text = str(self.token)
        invoice_operations = etree.SubElement(
            self.request_xml, f"{self._config.ns('api')}invoiceOperations")
        etree.SubElement(invoice_operations,
                         f"{self._config.ns('api')}compressedContent").text = str(self.compression).lower()
        for invoice in self.invoices:
            if not invoice.valid:
                self.remove(invoice)
        for index, invoice in enumerate(self.invoices, 1):
            invoiceOperation = etree.SubElement(invoice_operations,
                                                f"{self._config.ns('api')}invoiceOperation")
            etree.SubElement(invoiceOperation,
                             f"{self._config.ns('api')}index").text = str(index)
            etree.SubElement(invoiceOperation,
                             f"{self._config.ns('api')}invoiceOperation").text = invoice.operation.value
            invoicebody = bytes(invoice).decode()
            etree.SubElement(invoiceOperation,
                             f"{self._config.ns('api')}invoiceData").text = invoicebody
            self.request_signature_string += invoice.signature
        self.request_signature_xml.text = self.signature
        super().__call__()
        tid = self.response_xml.findtext(
            f".//{self.config.ns('api')}transactionId")
        ttime = self.response_xml.findtext(
            f".//{self.config.ns('common')}timestamp")
        self.transaction = Transaction(
            tid, date=datetime.fromisoformat(ttime.replace('Z', '+00:00')), config=self._config)
        self.token.used += 1
        return self

    @ property
    def valid(self) -> bool:
        """
        Returns whether request succeeded or not, or False if no request made
        """
        if self.request_status == STATUSOP.PREPARE:
            return False
        return self.request_status == STATUSOP.DONE and self.response_status == STATUSOP.DONE

    @ property
    def request_valid(self) -> bool:
        if not self.token:
            return False
        if not all([x.valid for x in self.invoices]):
            raise CheckError('Error:Invalid:Invoice',
                             'Some invoices are not valid')
        return super().request_valid


class ProcessAnnulments(SubmitInvoices):
    """
    Not implemented yet. Should take SubmitInvoices and wrap them with a checker for 'annulment', send an 'annulment' request instead.
    As data should accept Annulment type.
    """

    def __init__(self):
        raise NotImplementedError()
