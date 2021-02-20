# -*- coding: utf-8 -*- --------------------------------------------------===#
#
#  Copyright 2018-2021 Trovares Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#===----------------------------------------------------------------------===#

import logging

import grpc
import six

from . import DataService_pb2 as data_proto
from . import ErrorMessages_pb2 as err_proto

log = logging.getLogger(__name__)

BOOLEAN = 'boolean'
INT = 'int'
FLOAT = 'float'
DATE = 'date'
TIME = 'time'
DATETIME = 'datetime'
IPADDRESS = 'ipaddress'
TEXT = 'text'

# Send in 2MB chunks (grpc recommends 16-64 KB, but this got the best performance locally)
# FYI: by default grpc only supports up to 4MB.
MAX_PACKET_SIZE = 2097152

class XgtError(Exception):
  """
  Base exception class from which all other xgt exceptions inherit. It is
  raised in error cases that don't have a specific xgt exception type.
  """
  def __init__(self, msg, trace=''):
    if six.PY2:
      if isinstance(msg, unicode):
        msg = msg.encode('utf-8')
      if isinstance(trace, unicode):
        trace = trace.encode('utf-8')
    self.msg = msg
    self.trace = trace

    if log.getEffectiveLevel() >= logging.DEBUG:
      if self.trace != '':
        log.debug(self.trace)
      else:
        log.debug(self.msg)
    Exception.__init__(self, self.msg)

class XgtNotImplemented(XgtError):
  """Raised for functionality with pending implementation."""
class XgtInternalError(XgtError):
  """
  Intended for internal server purposes only. This exception should not become
  visible to the user.
  """
class XgtIOError(XgtError):
  """An I/O problem occurred either on the client or server side."""
  def __init__(self, msg, trace='', job = None):
    self._job = job
    if job is not None:
      errors = job.get_data()
      for index, error in enumerate(errors):
       # Add 10 errors to the msg.
       if index == 10:
         msg += '\nThere are ' + str(len(errors) - index) + ' more errors present.'
         break
       msg += '\n' + str(error[0])
    XgtError.__init__(self, msg, trace)

  @property
  def job(self):
    """Job: Job associated with the load/insert operation if available. May be None."""
    return self._job
class XgtServerMemoryError(XgtError):
  """
  The server memory usage is close to or at capacity and work could be lost.
  """
class XgtConnectionError(XgtError):
  """
  The client cannot properly connect to the server. This can include a failure
  to connect due to an xgt module version error.
  """
class XgtSyntaxError(XgtError):
  """A query was provided with incorrect syntax."""
class XgtTypeError(XgtError):
  """
  An unexpected type was supplied.

  For queries, an invalid data type was used either as an entity or as a
  property. For frames, either an edge, vertex or table frames was expected
  but the wrong frame type or some other data type was provided. For
  properties, the property declaration establishes the expected data type. A
  type error is raise if the data type used is not appropriate.
  """
class XgtValueError(XgtError):
  """An invalid or unexpected value was provided."""
class XgtNameError(XgtError):
  """
  An unexpected name was provided. Typically can occur during object retrieval
  where the object name was not found.
  """
class XgtArithmeticError(XgtError):
  """An invalid arithmetic calculation was detected and cannot be handled."""
class XgtFrameDependencyError(XgtError):
  """
  The requested action will produce an invalid graph or break a valid graph.
  """
class XgtTransactionError(XgtError):
  """A Transaction was attempted but didn't complete."""
class XgtSecurityError(XgtError):
  """A security violation occured."""

# Validation support functions

def _validated_schema(obj):
  '''Takes a user-supplied object and returns a valid schema.

  Users can supply a variety of objects as valid schemas. To simplify internal
  processing, we canonicalize these into a list of string-type pairs,
  performing validation along the way.
  '''
  # Validate the shape first
  try:
    if len(obj) < 1:
      raise XgtTypeError('A schema must not be empty.')
    for pairlike in obj:
      assert len(pairlike) == 2
  except:
    raise XgtTypeError('A schema must be a non-empty list of (property, type) pairs.')
  # Looks good. Return a canonical schema.
  return [(_validated_property_name(name), _validated_property_type(xgt_type))
          for name,xgt_type in obj]

def _validated_frame_name(obj):
  '''Takes a user-supplied object and returns a unicode frame name string.'''
  name = _as_unicode(obj)
  if len(name) < 1:
    raise XgtNameError('Frame names cannot be empty.')
  if u'.' in name:
    raise XgtNameError('Frame names cannot contain periods: '+name)
  return name

def _validated_namespace_name(obj):
  '''Takes a user-supplied object and returns a unicode frame name string.'''
  name = _as_unicode(obj)
  if len(name) < 1:
    raise XgtNameError('Namespace names cannot be empty.')
  if u'.' in name:
    raise XgtNameError('Namespace names cannot contain periods: '+name)
  return name

def _validated_property_name(obj):
  '''Takes a user-supplied object and returns a unicode proprty name string.'''
  name = _as_unicode(obj)
  return name

def _get_valid_property_types_to_create():
  return [BOOLEAN, INT, FLOAT, DATE, TIME, DATETIME, IPADDRESS, TEXT]

def _get_valid_property_types_for_return_only():
  return ['container_id', 'job_id']

def _validated_property_type(obj):
  '''Takes a user-supplied object and returns an xGT schema type.'''
  prop_type = _as_unicode(obj)
  valid_prop_types = _get_valid_property_types_to_create()
  if prop_type.lower() not in valid_prop_types:
    if prop_type.lower in _get_valid_property_types_for_return_only():
      raise XgtTypeError('Invalid property type "'+prop_type+'". This type '
                         'cannot be used when creating a frame.')
    else:
      raise XgtTypeError('Invalid property type "'+prop_type+'"')
  return prop_type.upper()

def _validate_opt_level(optlevel):
  """
  Valid optimization level values are:
    - 0: No optimization.
    - 1: General optimization.
    - 2: WHERE-clause optimization.
    - 3: Degree-cycle optimization.
    - 4: Query order optimization.
  """
  if isinstance(optlevel, int):
    if optlevel not in [0, 1, 2, 3, 4]:
      raise XgtValueError("Invalid optlevel '" + str(optlevel) +"'")
  else:
    raise XgtTypeError("optlevel must be an integer")
  return True

def _assert_noerrors(response):
  if len(response.error) > 0:
    error = response.error[0]
    try:
      error_code_name = err_proto.ErrorCodeEnum.Name(error.code)
      error_class = _code_error_map[error_code_name]
      raise error_class(error.message, error.detail)
    except XgtError:
      raise
    except Exception as ex:
      raise XgtError("Error detected while raising exception" +
                     _to_unicode(ex), _to_unicode(ex))

def _assert_isstring(name, text):
  if not isinstance(text, six.string_types):
    msg = name + " is not a string: '" + _to_unicode(text) + "'"
    raise TypeError(msg)

# Unicode support functions.

# Why the two functions _to_* and _as_*? There are two general cases when you
# want to convert something to a certain type of string. The first case is if
# you are creating a string that will be handed to a user. Exceptions and log
# messages fall into this category. In this case, you really want a
# *constructor*, turning any object into some type of string, even if it
# doesn't natively contain character data. The second case is when you want to
# collapse unicode and byte data into one or the other. This includes most xGT
# operations, referencing frames or properties, for instance. In this case, if
# the method is passed some other type (maybe an int or class instance), you
# want an exception to be thrown.
#
# So, to summarize:
#   _to_unicode( u'xyzzy' ) => u'xyzzy'
#   _to_unicode( b'xyzzy' ) => u'xyzzy'
#   _to_unicode( 12345.67 ) => u'12345.67'
#
#   _as_unicode( u'xyzzy' ) => u'xyzzy'
#   _as_unicode( b'xyzzy' ) => u'xyzzy'
#   _as_unicode( 12345.67 ) => TypeError
#
# _to_bytes/_as_bytes and _to_str work similarly (_as_str is not provided, as
# it would effectively be the same as the str() built-in).

def _to_unicode(value):
  '''Constructs a unicode string out of any object.'''
  if isinstance(value, six.text_type):
    return value
  elif isinstance(value, six.binary_type):
    return value.decode('utf-8')
  else:
    return six.text_type(value)

def _as_unicode(value):
  '''Converts unicode or binary strings to unicode. Other types raise a TypeError.'''
  if isinstance(value, six.text_type):
    return value
  elif isinstance(value, six.binary_type):
    return value.decode('utf-8')
  raise TypeError('Cannot convert '+six.text_type(type(value))+' to unicode.')

def _to_bytes(value):
  '''Constructs a human-readable byte string out of any object.'''
  if isinstance(value, six.text_type):
    return value.encode('utf-8')
  elif isinstance(value, six.binary_type):
    return value
  else:
    return six.text_type(value).encode('utf-8')

def _as_bytes(value):
  '''Converts unicode or binary strings to bytes. Other types raise a TypeError.'''
  if isinstance(value, six.text_type):
    return value.encode('utf-8')
  elif isinstance(value, six.binary_type):
    return value
  raise TypeError('Cannot convert '+six.text_type(type(value))+' to bytes.')

def _to_str(value):
  '''Constructs a str out of any object.'''
  # We can't use the str built-in as a constructor because Python 2 believes
  # that unicode characters cannot be converted to str types. We want to.
  if isinstance(value, str):
    return value
  elif six.PY2 and isinstance(value, unicode):
    return value.encode('utf-8')
  elif six.PY3 and isinstance(value, bytes):
    return value.decode('utf-8')
  else:
    return str(value)

_code_error_map = {
  'GENERIC_ERROR': XgtError,
  'NOT_IMPLEMENTED': XgtNotImplemented,
  'INTERNAL_ERROR': XgtInternalError,
  'IO_ERROR': XgtIOError,
  'SERVER_MEMORY_ERROR': XgtServerMemoryError,
  'CONNECTION_ERROR': XgtConnectionError,
  'SYNTAX_ERROR': XgtSyntaxError,
  'TYPE_ERROR': XgtTypeError,
  'VALUE_ERROR': XgtValueError,
  'NAME_ERROR': XgtNameError,
  'ARITHMETIC_ERROR': XgtArithmeticError,
  'FRAME_DEPENDENCY_ERROR': XgtFrameDependencyError,
  'TRANSACTION_ERROR': XgtTransactionError,
  'SECURITY_ERROR': XgtSecurityError,
}
