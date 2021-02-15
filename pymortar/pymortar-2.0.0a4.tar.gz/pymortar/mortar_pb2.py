# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mortar.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='mortar.proto',
  package='mortar',
  syntax='proto3',
  serialized_options=_b('Z\010mortarpb'),
  serialized_pb=_b('\n\x0cmortar.proto\x12\x06mortar\"L\n\x10GetAPIKeyRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\x14\n\x0crefreshtoken\x18\x03 \x01(\t\"5\n\x0e\x41PIKeyResponse\x12\r\n\x05token\x18\x01 \x01(\t\x12\x14\n\x0crefreshtoken\x18\x02 \x01(\t\"4\n\x0eQualifyRequest\x12\x10\n\x08required\x18\x01 \x03(\t\x12\x10\n\x08optional\x18\x02 \x03(\t\"/\n\x0fQualifyResponse\x12\r\n\x05\x65rror\x18\x01 \x01(\t\x12\r\n\x05sites\x18\x02 \x03(\t\"\xa4\x01\n\x0c\x46\x65tchRequest\x12\r\n\x05sites\x18\x01 \x03(\t\x12\x1f\n\x07streams\x18\x02 \x03(\x0b\x32\x0e.mortar.Stream\x12 \n\x04time\x18\x03 \x01(\x0b\x32\x12.mortar.TimeParams\x12\x1b\n\x05views\x18\x04 \x03(\x0b\x32\x0c.mortar.View\x12%\n\ndataFrames\x18\x05 \x03(\x0b\x32\x11.mortar.DataFrame\"\x80\x01\n\x06Stream\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x12\n\ndefinition\x18\x02 \x01(\t\x12\x10\n\x08\x64\x61taVars\x18\x06 \x03(\t\x12\r\n\x05uuids\x18\x03 \x03(\t\x12$\n\x0b\x61ggregation\x18\x04 \x01(\x0e\x32\x0f.mortar.AggFunc\x12\r\n\x05units\x18\x05 \x01(\t\"\xc0\x01\n\rFetchResponse\x12\r\n\x05\x65rror\x18\x01 \x01(\t\x12\x0c\n\x04site\x18\x02 \x01(\t\x12\x0c\n\x04view\x18\t \x01(\t\x12\x11\n\tdataFrame\x18\n \x01(\t\x12\x10\n\x08variable\x18\x03 \x01(\t\x12\x12\n\nidentifier\x18\x04 \x01(\t\x12\r\n\x05times\x18\x05 \x03(\x03\x12\x0e\n\x06values\x18\x06 \x03(\x01\x12\x11\n\tvariables\x18\x07 \x03(\t\x12\x19\n\x04rows\x18\x08 \x03(\x0b\x32\x0b.mortar.Row\"\"\n\x03Row\x12\x1b\n\x06values\x18\x01 \x03(\x0b\x32\x0b.mortar.URI\"\'\n\x03URI\x12\x11\n\tnamespace\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"I\n\nTimeParams\x12\r\n\x05start\x18\x01 \x01(\t\x12\x0b\n\x03\x65nd\x18\x02 \x01(\t\x12\x0e\n\x06window\x18\x03 \x01(\t\x12\x0f\n\x07\x61ligned\x18\x04 \x01(\x08\"7\n\x04View\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05sites\x18\x02 \x03(\t\x12\x12\n\ndefinition\x18\x03 \x01(\t\"\x94\x01\n\tDataFrame\x12\x0c\n\x04name\x18\x01 \x01(\t\x12$\n\x0b\x61ggregation\x18\x02 \x01(\x0e\x32\x0f.mortar.AggFunc\x12\x0e\n\x06window\x18\x03 \x01(\t\x12\x0c\n\x04unit\x18\x04 \x01(\t\x12&\n\ntimeseries\x18\x05 \x03(\x0b\x32\x12.mortar.Timeseries\x12\r\n\x05uuids\x18\x06 \x03(\t\",\n\nTimeseries\x12\x0c\n\x04view\x18\x01 \x01(\t\x12\x10\n\x08\x64\x61taVars\x18\x02 \x03(\t*\x8e\x01\n\x07\x41ggFunc\x12\x14\n\x10\x41GG_FUNC_INVALID\x10\x00\x12\x10\n\x0c\x41GG_FUNC_RAW\x10\x01\x12\x11\n\rAGG_FUNC_MEAN\x10\x02\x12\x10\n\x0c\x41GG_FUNC_MIN\x10\x03\x12\x10\n\x0c\x41GG_FUNC_MAX\x10\x04\x12\x12\n\x0e\x41GG_FUNC_COUNT\x10\x05\x12\x10\n\x0c\x41GG_FUNC_SUM\x10\x06\x32\xbb\x01\n\x06Mortar\x12=\n\tGetAPIKey\x12\x18.mortar.GetAPIKeyRequest\x1a\x16.mortar.APIKeyResponse\x12:\n\x07Qualify\x12\x16.mortar.QualifyRequest\x1a\x17.mortar.QualifyResponse\x12\x36\n\x05\x46\x65tch\x12\x14.mortar.FetchRequest\x1a\x15.mortar.FetchResponse0\x01\x42\nZ\x08mortarpbb\x06proto3')
)

_AGGFUNC = _descriptor.EnumDescriptor(
  name='AggFunc',
  full_name='mortar.AggFunc',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='AGG_FUNC_INVALID', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AGG_FUNC_RAW', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AGG_FUNC_MEAN', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AGG_FUNC_MIN', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AGG_FUNC_MAX', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AGG_FUNC_COUNT', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AGG_FUNC_SUM', index=6, number=6,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1160,
  serialized_end=1302,
)
_sym_db.RegisterEnumDescriptor(_AGGFUNC)

AggFunc = enum_type_wrapper.EnumTypeWrapper(_AGGFUNC)
AGG_FUNC_INVALID = 0
AGG_FUNC_RAW = 1
AGG_FUNC_MEAN = 2
AGG_FUNC_MIN = 3
AGG_FUNC_MAX = 4
AGG_FUNC_COUNT = 5
AGG_FUNC_SUM = 6



_GETAPIKEYREQUEST = _descriptor.Descriptor(
  name='GetAPIKeyRequest',
  full_name='mortar.GetAPIKeyRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='username', full_name='mortar.GetAPIKeyRequest.username', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='password', full_name='mortar.GetAPIKeyRequest.password', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='refreshtoken', full_name='mortar.GetAPIKeyRequest.refreshtoken', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=24,
  serialized_end=100,
)


_APIKEYRESPONSE = _descriptor.Descriptor(
  name='APIKeyResponse',
  full_name='mortar.APIKeyResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='token', full_name='mortar.APIKeyResponse.token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='refreshtoken', full_name='mortar.APIKeyResponse.refreshtoken', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=102,
  serialized_end=155,
)


_QUALIFYREQUEST = _descriptor.Descriptor(
  name='QualifyRequest',
  full_name='mortar.QualifyRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='required', full_name='mortar.QualifyRequest.required', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='optional', full_name='mortar.QualifyRequest.optional', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=157,
  serialized_end=209,
)


_QUALIFYRESPONSE = _descriptor.Descriptor(
  name='QualifyResponse',
  full_name='mortar.QualifyResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='error', full_name='mortar.QualifyResponse.error', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sites', full_name='mortar.QualifyResponse.sites', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=211,
  serialized_end=258,
)


_FETCHREQUEST = _descriptor.Descriptor(
  name='FetchRequest',
  full_name='mortar.FetchRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sites', full_name='mortar.FetchRequest.sites', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='streams', full_name='mortar.FetchRequest.streams', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='time', full_name='mortar.FetchRequest.time', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='views', full_name='mortar.FetchRequest.views', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dataFrames', full_name='mortar.FetchRequest.dataFrames', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=261,
  serialized_end=425,
)


_STREAM = _descriptor.Descriptor(
  name='Stream',
  full_name='mortar.Stream',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='mortar.Stream.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='definition', full_name='mortar.Stream.definition', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dataVars', full_name='mortar.Stream.dataVars', index=2,
      number=6, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='uuids', full_name='mortar.Stream.uuids', index=3,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='aggregation', full_name='mortar.Stream.aggregation', index=4,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='units', full_name='mortar.Stream.units', index=5,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=428,
  serialized_end=556,
)


_FETCHRESPONSE = _descriptor.Descriptor(
  name='FetchResponse',
  full_name='mortar.FetchResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='error', full_name='mortar.FetchResponse.error', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='site', full_name='mortar.FetchResponse.site', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='view', full_name='mortar.FetchResponse.view', index=2,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dataFrame', full_name='mortar.FetchResponse.dataFrame', index=3,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='variable', full_name='mortar.FetchResponse.variable', index=4,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='identifier', full_name='mortar.FetchResponse.identifier', index=5,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='times', full_name='mortar.FetchResponse.times', index=6,
      number=5, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='values', full_name='mortar.FetchResponse.values', index=7,
      number=6, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='variables', full_name='mortar.FetchResponse.variables', index=8,
      number=7, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='rows', full_name='mortar.FetchResponse.rows', index=9,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=559,
  serialized_end=751,
)


_ROW = _descriptor.Descriptor(
  name='Row',
  full_name='mortar.Row',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='values', full_name='mortar.Row.values', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=753,
  serialized_end=787,
)


_URI = _descriptor.Descriptor(
  name='URI',
  full_name='mortar.URI',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='namespace', full_name='mortar.URI.namespace', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='mortar.URI.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=789,
  serialized_end=828,
)


_TIMEPARAMS = _descriptor.Descriptor(
  name='TimeParams',
  full_name='mortar.TimeParams',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='start', full_name='mortar.TimeParams.start', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='end', full_name='mortar.TimeParams.end', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='window', full_name='mortar.TimeParams.window', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='aligned', full_name='mortar.TimeParams.aligned', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=830,
  serialized_end=903,
)


_VIEW = _descriptor.Descriptor(
  name='View',
  full_name='mortar.View',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='mortar.View.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sites', full_name='mortar.View.sites', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='definition', full_name='mortar.View.definition', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=905,
  serialized_end=960,
)


_DATAFRAME = _descriptor.Descriptor(
  name='DataFrame',
  full_name='mortar.DataFrame',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='mortar.DataFrame.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='aggregation', full_name='mortar.DataFrame.aggregation', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='window', full_name='mortar.DataFrame.window', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='unit', full_name='mortar.DataFrame.unit', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timeseries', full_name='mortar.DataFrame.timeseries', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='uuids', full_name='mortar.DataFrame.uuids', index=5,
      number=6, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=963,
  serialized_end=1111,
)


_TIMESERIES = _descriptor.Descriptor(
  name='Timeseries',
  full_name='mortar.Timeseries',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='view', full_name='mortar.Timeseries.view', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dataVars', full_name='mortar.Timeseries.dataVars', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1113,
  serialized_end=1157,
)

_FETCHREQUEST.fields_by_name['streams'].message_type = _STREAM
_FETCHREQUEST.fields_by_name['time'].message_type = _TIMEPARAMS
_FETCHREQUEST.fields_by_name['views'].message_type = _VIEW
_FETCHREQUEST.fields_by_name['dataFrames'].message_type = _DATAFRAME
_STREAM.fields_by_name['aggregation'].enum_type = _AGGFUNC
_FETCHRESPONSE.fields_by_name['rows'].message_type = _ROW
_ROW.fields_by_name['values'].message_type = _URI
_DATAFRAME.fields_by_name['aggregation'].enum_type = _AGGFUNC
_DATAFRAME.fields_by_name['timeseries'].message_type = _TIMESERIES
DESCRIPTOR.message_types_by_name['GetAPIKeyRequest'] = _GETAPIKEYREQUEST
DESCRIPTOR.message_types_by_name['APIKeyResponse'] = _APIKEYRESPONSE
DESCRIPTOR.message_types_by_name['QualifyRequest'] = _QUALIFYREQUEST
DESCRIPTOR.message_types_by_name['QualifyResponse'] = _QUALIFYRESPONSE
DESCRIPTOR.message_types_by_name['FetchRequest'] = _FETCHREQUEST
DESCRIPTOR.message_types_by_name['Stream'] = _STREAM
DESCRIPTOR.message_types_by_name['FetchResponse'] = _FETCHRESPONSE
DESCRIPTOR.message_types_by_name['Row'] = _ROW
DESCRIPTOR.message_types_by_name['URI'] = _URI
DESCRIPTOR.message_types_by_name['TimeParams'] = _TIMEPARAMS
DESCRIPTOR.message_types_by_name['View'] = _VIEW
DESCRIPTOR.message_types_by_name['DataFrame'] = _DATAFRAME
DESCRIPTOR.message_types_by_name['Timeseries'] = _TIMESERIES
DESCRIPTOR.enum_types_by_name['AggFunc'] = _AGGFUNC
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetAPIKeyRequest = _reflection.GeneratedProtocolMessageType('GetAPIKeyRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETAPIKEYREQUEST,
  __module__ = 'mortar_pb2'
  # @@protoc_insertion_point(class_scope:mortar.GetAPIKeyRequest)
  ))
_sym_db.RegisterMessage(GetAPIKeyRequest)

APIKeyResponse = _reflection.GeneratedProtocolMessageType('APIKeyResponse', (_message.Message,), dict(
  DESCRIPTOR = _APIKEYRESPONSE,
  __module__ = 'mortar_pb2'
  # @@protoc_insertion_point(class_scope:mortar.APIKeyResponse)
  ))
_sym_db.RegisterMessage(APIKeyResponse)

QualifyRequest = _reflection.GeneratedProtocolMessageType('QualifyRequest', (_message.Message,), dict(
  DESCRIPTOR = _QUALIFYREQUEST,
  __module__ = 'mortar_pb2'
  # @@protoc_insertion_point(class_scope:mortar.QualifyRequest)
  ))
_sym_db.RegisterMessage(QualifyRequest)

QualifyResponse = _reflection.GeneratedProtocolMessageType('QualifyResponse', (_message.Message,), dict(
  DESCRIPTOR = _QUALIFYRESPONSE,
  __module__ = 'mortar_pb2'
  # @@protoc_insertion_point(class_scope:mortar.QualifyResponse)
  ))
_sym_db.RegisterMessage(QualifyResponse)

FetchRequest = _reflection.GeneratedProtocolMessageType('FetchRequest', (_message.Message,), dict(
  DESCRIPTOR = _FETCHREQUEST,
  __module__ = 'mortar_pb2'
  # @@protoc_insertion_point(class_scope:mortar.FetchRequest)
  ))
_sym_db.RegisterMessage(FetchRequest)

Stream = _reflection.GeneratedProtocolMessageType('Stream', (_message.Message,), dict(
  DESCRIPTOR = _STREAM,
  __module__ = 'mortar_pb2'
  # @@protoc_insertion_point(class_scope:mortar.Stream)
  ))
_sym_db.RegisterMessage(Stream)

FetchResponse = _reflection.GeneratedProtocolMessageType('FetchResponse', (_message.Message,), dict(
  DESCRIPTOR = _FETCHRESPONSE,
  __module__ = 'mortar_pb2'
  # @@protoc_insertion_point(class_scope:mortar.FetchResponse)
  ))
_sym_db.RegisterMessage(FetchResponse)

Row = _reflection.GeneratedProtocolMessageType('Row', (_message.Message,), dict(
  DESCRIPTOR = _ROW,
  __module__ = 'mortar_pb2'
  # @@protoc_insertion_point(class_scope:mortar.Row)
  ))
_sym_db.RegisterMessage(Row)

URI = _reflection.GeneratedProtocolMessageType('URI', (_message.Message,), dict(
  DESCRIPTOR = _URI,
  __module__ = 'mortar_pb2'
  # @@protoc_insertion_point(class_scope:mortar.URI)
  ))
_sym_db.RegisterMessage(URI)

TimeParams = _reflection.GeneratedProtocolMessageType('TimeParams', (_message.Message,), dict(
  DESCRIPTOR = _TIMEPARAMS,
  __module__ = 'mortar_pb2'
  # @@protoc_insertion_point(class_scope:mortar.TimeParams)
  ))
_sym_db.RegisterMessage(TimeParams)

View = _reflection.GeneratedProtocolMessageType('View', (_message.Message,), dict(
  DESCRIPTOR = _VIEW,
  __module__ = 'mortar_pb2'
  # @@protoc_insertion_point(class_scope:mortar.View)
  ))
_sym_db.RegisterMessage(View)

DataFrame = _reflection.GeneratedProtocolMessageType('DataFrame', (_message.Message,), dict(
  DESCRIPTOR = _DATAFRAME,
  __module__ = 'mortar_pb2'
  # @@protoc_insertion_point(class_scope:mortar.DataFrame)
  ))
_sym_db.RegisterMessage(DataFrame)

Timeseries = _reflection.GeneratedProtocolMessageType('Timeseries', (_message.Message,), dict(
  DESCRIPTOR = _TIMESERIES,
  __module__ = 'mortar_pb2'
  # @@protoc_insertion_point(class_scope:mortar.Timeseries)
  ))
_sym_db.RegisterMessage(Timeseries)


DESCRIPTOR._options = None

_MORTAR = _descriptor.ServiceDescriptor(
  name='Mortar',
  full_name='mortar.Mortar',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1305,
  serialized_end=1492,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetAPIKey',
    full_name='mortar.Mortar.GetAPIKey',
    index=0,
    containing_service=None,
    input_type=_GETAPIKEYREQUEST,
    output_type=_APIKEYRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Qualify',
    full_name='mortar.Mortar.Qualify',
    index=1,
    containing_service=None,
    input_type=_QUALIFYREQUEST,
    output_type=_QUALIFYRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Fetch',
    full_name='mortar.Mortar.Fetch',
    index=2,
    containing_service=None,
    input_type=_FETCHREQUEST,
    output_type=_FETCHRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_MORTAR)

DESCRIPTOR.services_by_name['Mortar'] = _MORTAR

# @@protoc_insertion_point(module_scope)
