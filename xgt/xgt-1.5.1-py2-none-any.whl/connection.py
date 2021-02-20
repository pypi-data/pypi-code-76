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

import collections
import numbers
import os
import time
from datetime import timedelta, datetime
from os.path import expanduser

import grpc
import six

from . import AdminService_pb2 as admin_proto
from . import AdminService_pb2_grpc as admin_grpc
from . import DataService_pb2_grpc as data_grpc
from . import GraphTypesService_pb2 as graph_proto
from . import GraphTypesService_pb2_grpc as graph_grpc
from . import JobService_pb2 as job_proto
from . import JobService_pb2_grpc as job_grpc
from . import MetricsService_pb2 as metrics_proto
from . import MetricsService_pb2_grpc as metrics_grpc
from . import SchemaMessages_pb2 as sch_proto
from .common import (_assert_noerrors, _validated_property_name,
                     _validated_schema, _validated_frame_name,
                     _validated_namespace_name, _to_str,
                     _validate_opt_level, _to_unicode,
                     XgtError, XgtNameError, XgtConnectionError, XgtValueError,
                     XgtTypeError, XgtNotImplemented)
from .graph import TableFrame, VertexFrame, EdgeFrame
from .job import Job
from .version import (
  __version__, __version_major__, __version_minor__, __version_patch__
)

# gRPC's interceptors are passed a client_call_details object which is,
# unfortunately, immutable. The interceptor API expects client_call_details to
# be passed on, but we must modify its metadata attribute en route. As such, we
# need to create an instance matching client_call_details. Unfortunately, the
# class provided by gRPC---grpc.ClientCallDetails---is supplied without a
# constructor (maybe because gRPC considers it experimental). As a result, the
# only way to modify metadata is to construct a new instance of a custom class
# which supplies the same attributes as grpc.ClientCallDetails.
# This is that class. It uses namedtuple to provide four fixed attributes.
class _ClientCallDetails(
    collections.namedtuple(
        '_ClientCallDetails',
        ('method', 'timeout', 'metadata', 'credentials')),
    grpc.ClientCallDetails):
  pass

class SessionTokenClientInterceptor(grpc.UnaryUnaryClientInterceptor,
                                    grpc.StreamUnaryClientInterceptor,
                                    grpc.UnaryStreamClientInterceptor):
  """
  Interceptor that inserts the session token into the metadata to be
  authenticated by the server.

  """
  def __init__(self):
    self._token = None

  def _intercept_call(self, continuation, client_call_details,
                      request_or_iterator):
    metadata = []
    if client_call_details.metadata is not None:
      metadata = list(client_call_details.metadata)
    metadata.append(('session_token', self._token))
    client_call_details = _ClientCallDetails(
        client_call_details.method, client_call_details.timeout, metadata,
        client_call_details.credentials)
    response = continuation(client_call_details, request_or_iterator)
    return response

  def intercept_unary_unary(self, continuation, client_call_details, request):
    return self._intercept_call(continuation, client_call_details, request)

  def intercept_stream_unary(self, continuation, client_call_details, request_iterator):
    return self._intercept_call(continuation, client_call_details, request_iterator)

  def intercept_unary_stream(self, continuation, client_call_details, request):
    return self._intercept_call(continuation, client_call_details, request)

  def _set_token(self, token):
    self._token = token

class Connection(object):
  """
  Connection to the server with functionality to create, change, and remove
  graph structures and run jobs.

  Parameters
  ----------
  host : str
    IP address of the computer where the server is running.
  port : int
    Port where the server is listening on for RPC calls.
  userid : str
    The user name to authenticate as.
  credentials : str
    Credentials used to authenticate.
  flags: dict
    Dictionary containing flags. Possible flags are:

    aws_access_key_id : str
      Amazon Access Key ID, used for authentication when loading data
      files from S3 buckets. The default is an empty string.
    aws_secret_access_key : str
      Amazon Access Key ID, used for authentication when loading data
      files from S3 buckets. The default is an empty string.
    ssl : boolean
      If true use ssl authentication for secure server channels.
      The default is False.
    ssl_root_dir : str
      Path to the root folder for ssl certificates and private keys.
      Defaults to the user's home directory.
    ssl_server_cn : str
      Common name on the certificate of the server to connect to.
      The default is the hostname.
  """

  _GIB = 1024 * 1024 * 1024

  def __init__(self, host='127.0.0.1', port=4367, flags=None, userid='',
               credentials=''):
    """
    Constructor for Connection. Called when Connection is created.
    """
    if flags is None:
      flags = {}
    self.port = port
    self.aws_access_key_id = flags.get('aws_access_key_id', '')
    self.aws_secret_access_key = flags.get('aws_secret_access_key', '')
    self.ssl = flags.get('ssl', False)
    self.ssl_root_dir = flags.get('ssl_root_dir', expanduser("~") + '/.ssl/')
    self.ssl_server_cn = flags.get('ssl_server_cn', host)
    self.host = host
    self.cwd = os.getcwd()
    self.client = six.moves.http_client

    self._metadata_interceptor = SessionTokenClientInterceptor()
    self._channel = self._create_channel()
    self._admin_svc = admin_grpc.AdminServiceStub(self._channel)
    self._data_svc = data_grpc.DataServiceStub(self._channel)
    self._graph_svc = graph_grpc.GraphTypesServiceStub(self._channel)
    self._job_svc = job_grpc.JobServiceStub(self._channel)
    self._metrics_svc = metrics_grpc.MetricsServiceStub(self._channel)

    self._version_check()
    self._request_session_token(userid, credentials)

  # Close outstanding session on destruction of this instance.
  def __del__(self):
    try:
      request = admin_proto.CloseSessionRequest()
      self._call(request, self._admin_svc.CloseSession)
    except XgtConnectionError:
      # The connection will drop after closing this current session.
      pass

  def _create_channel(self):
    channel = None
    connection_string = self.host + ':' + _to_unicode(self.port)
    if (self.ssl):
      chain_cert = open(self.ssl_root_dir + '/certs/ca-chain.cert.pem', 'rb').read()
      client_key = open(self.ssl_root_dir + '/private/client.key.pem', 'rb').read()
      client_cert = open(self.ssl_root_dir + '/certs/client.cert.pem', 'rb').read()
      channel_credentials = grpc.ssl_channel_credentials(
          chain_cert, client_key, client_cert)
      try:
        channel = grpc.secure_channel(
            connection_string, channel_credentials,
            options=(('grpc.ssl_target_name_override', self.ssl_server_cn,),))
      except grpc.RpcError as ex:
        raise XgtConnectionError(ex.details, '')
    else:
      try:
        channel = grpc.insecure_channel(connection_string)
      except grpc.RpcError as ex:
        raise XgtConnectionError(ex.details, '')
    return grpc.intercept_channel(channel, self._metadata_interceptor)

  # Authenticate and request a session token that persists for the lifetime of
  # the session.
  def _request_session_token(self, userid, credentials):
    try:
      request = admin_proto.AuthenticateRequest()
      request.userid = userid
      request.credentials = credentials
      response = self._call(request, self._admin_svc.Authenticate)
      self._metadata_interceptor._set_token(response.session_token)
    except Exception:
      raise XgtConnectionError('Failure on session token request.')

  def _call(self, request, rpc_function):
    try:
      response = rpc_function(request)
    except grpc.RpcError as ex:
      raise XgtConnectionError(ex.details, '')
    try:
      _ = iter(response)
      # For streaming responses that return an iterator, it is the caller's
      # responsibility to check each packet for errors. E.g.:
      #   for result in response:
      #     _assert_noerrors(result)
      # If the response is non-streaming (i.e. not an iterable object), the
      # response is checked for errors below.
      return response
    except TypeError:
      pass
    _assert_noerrors(response)
    return response

  def _version_check(self):
    server_version = None
    request = admin_proto.VersionRequest()
    response = self._call(request, self._admin_svc.Version)
    server_version = response.version
    bad = server_version is None
    if not bad:
      fields = server_version.split('.')
      if len(fields) != 3:
        bad = True
    if bad or fields[0] != __version_major__ or fields[1] != __version_minor__:
      msg = "Version matching for xgt and " \
            "the server failed. Install the appropriate xgt " \
            "package. xGT version: " + server_version
      raise XgtError(msg)

  def _change_exit_error_count(self, action):
    action_u = action.upper()
    request = admin_proto.ChangeErrorCountRequest()
    request.action = admin_proto.ErrorCountActionEnum.Value(action_u)
    response = self._call(request, self._admin_svc.ChangeErrorCount)
    return response.error_count

  def _process_kwargs(self, request, args_to_expand):
    for k,v in args_to_expand.items():
      if v is not None:
        if isinstance(v, bool):
          request.kwargs[k].bool_value = v
        elif isinstance(v, six.integer_types):
          request.kwargs[k].int_value = v
        elif isinstance(v, float):
          request.kwargs[k].float_value = v
        elif isinstance(v, six.string_types):
          request.kwargs[k].string_value = v

  def _launch_job(self, query, **kwargs):
    if not isinstance(query, six.string_types):
      raise TypeError(
          "Unexpected argument type '" + _to_unicode(type(query)) + "'")
    if 'optlevel' in kwargs:
      _validate_opt_level(kwargs['optlevel'])

    request = job_proto.ScheduleJobsCypherRequest()
    request.cypher_query.extend([query])
    self._process_kwargs(request, kwargs)
    response = self._call(request, self._job_svc.ScheduleJobsCypher)
    one_job = response.job_status[0]
    if response.HasField('query_plan'):
      return Job(self, one_job, response.query_plan)
    else:
      return Job(self, one_job)

  #------------------------- Housekeeping Methods
  @property
  def server_version(self):
    """
    Obtains the current product version from the server.

    Returns
    -------
    str
      Version number.

    """
    request = admin_proto.VersionRequest()
    response = self._call(request, self._admin_svc.Version)
    return response.version

  @property
  def max_user_memory_size(self):
    """
    Returns the maximum amount of memory available for user data on the xGT server.

    Returns
    -------
    float
      Maximum available user memory, in gibibytes.
    """
    request = admin_proto.MaxUserMemorySizeRequest()
    response = self._call(request, self._admin_svc.MaxUserMemorySize)
    return response.pool_size / Connection._GIB

  @property
  def free_user_memory_size(self):
    """
    Returns the amount of free memory available for user data on the xGT server.

    Returns
    -------
    float
      Currently available user memory, in gibibytes.
    """
    request = admin_proto.FreeUserMemorySizeRequest()
    response = self._call(request, self._admin_svc.FreeUserMemorySize)
    return response.free_memory_size / Connection._GIB

  #------------------------- Catalog Getter Methods
  def get_table_frames(self,names=None, namespace=None):
    """
    Get a list of TableFrame objects that correspond to each table frame in the xGT server.
    Only frames that the calling user has permission to read are returned.

    A TableFrame object allows for interaction with a table present in the xGT server.
    For example, a table may be created by a MATCH query and may contain query results.
    It may also be explicitly created with `Connection.create_table_frame()`.

    Parameters
    ----------
    names : list of strings or None
      If a list, the list of names of tables frames to retrieve.
      Each name must be a fully qualifed name that includes the namespace in which
      the frame exists.
      If None and the parameter namespace is None, all table frames are
      returned.
    namespace: string or None
      Returns all table frames in this namespace.
      At most one of names and namespace can be a value other than None.

    Returns
    -------
    list
      TableFrame objects representing tables present in the server.

    Raises
    -------
    XgtNameError
      If a table frame name requested does not exist or is not visible to the user.
      If a table frame or namespace name does not follow naming rules.
    XgtTransactionError
      If a conflict with another transaction occurs.

    Examples
    --------
    >>> conn = xgt.Connection()
    >>> ... create graph in the namespace career
    >>> qr1 = 'MATCH (a:career__Employee) RETURN a.PersonID INTO career__Results1'
    >>> conn.run_job(qr1)
    >>> table_frames = conn.get_table_frames()
    >>> print(str([f.name for f in table_frames]))
    ['career__Results1']
    >>> results1_data = conn.get_table_frame('career__Results1').get_data_pandas()

    """

    if names is not None and namespace is not None:
      raise ValueError('Only one of "names" and "namespaces" should be passed.')
    if names is None:
      names = []
    elif isinstance(names, six.string_types):
      raise TypeError('Invalid argument: "names" must be a list of strings')
    else:
      names = [_validated_frame_name(n) for n in names]

    request = graph_proto.GetFramesMetadataRequest()
    if names is not None:
      request.name.extend(names)
    if namespace is not None:
      request.namespace_name = _validated_namespace_name(namespace)
    response = self._call(request, self._graph_svc.GetTableFrames)

    frames = []
    for data in response.container:
      schema = []
      for prop in data.schema.property:
        prop_type = sch_proto.UvalTypeEnum.Name(prop.data_type).lower()
        prop_type = _to_unicode(prop_type)
        schema.append([prop.name, prop_type])
      frames.append(TableFrame(self, data.name, schema))
    return frames

  def get_table_frame(self, name):
    """
    Get a TableFrame object that allows interaction with a table present in the xGT server.

    A TableFrame object allows for interaction with a table present in the xGT server.
    For example, a table may be created by a MATCH query and may contain query results.
    It may also be explicitly created with `Connection.create_table_frame()`.

    Parameters
    ----------
    name : str
      Table frame name. The name must be a fully qualifed name that includes the
      namespace in which the frame exists.

    Returns
    -------
    TableFrame
      Frame to the table.

    Raises
    -------
    XgtNameError
      If the frame requested does not exist or is not visible to the user.
    XgtTransactionError
      If a conflict with another transaction occurs.

    Examples
    --------
    >>> conn = xgt.Connection()
    >>> ... create graph in the namespace career and run queries ...
    >>> t = conn.get_table_frame('career__EmployeeData')
    >>> print(str(t))
    {
      'name': 'career__EmployeeData',
      'schema': [
        ['person_id', 'int'],
        ['name', 'text'],
        ['postal_code', 'int']]
    }
    >>> qr1 = 'MATCH (a:career__EmployeeData) RETURN a.person_id INTO career__Results1'
    >>> conn.run_job(qr1)
    >>> results = conn.get_table_frame('career__Results1')
    >>> num_results = results.num_rows
    >>> results_data = results.get_data_pandas()

    """
    frames = self.get_table_frames([name])
    if len(frames) == 0:
      error_msg = ("Frame not found: table frame {0}. It either does not "
                   "exist or the user lacks permission to read it".format(name))
      raise XgtNameError(error_msg)
    return frames[0]

  def get_vertex_frames(self, names = None, namespace = None):
    """
    Get a list of VertexFrame objects corresponding to each vertex frame in the xGT server.
    Only frames that the calling user has permission to read are returned.

    A VertexFrame represents a collection of vertices held on the xGT
    server and can be used to retrieve information about them.
    `VertexFrame.get_data_pandas()` and `VertexFrame.get_data()` are
    used to retrieve member vertices.
    Each vertex in a VertexFrame shares the same properties,
    described in `VertexFrame.schema`. Each vertex in a VertexFrame
    is uniquely identified by the property listed in `VertexFrame.key`.

    Parameters
    ----------
    names : list of strings or None
      If a list, the list of names of vertex frames to retrieve.
      Each name must be a fully qualifed name that includes the namespace in which
      the frame exists.
      If None and the parameter namespace is None, all vertex frames are
      returned.
    namespace: string or None
      Returns all vertex frames in this namespace.
      At most one of names and namespace can be a value other than None.

    Returns
    -------
    list
      VertexFrame objects corresponding to the vertex frames present in the server.

    Raises
    -------
    XgtNameError
      If a vertex frame name requested does not exist or is not visible to the user.
      If a vertex frame or namespace name does not follow naming rules.
    XgtTransactionError
      If a conflict with another transaction occurs.

    Examples
    --------
    >>> conn = xgt.Connection()
    >>> print [f.name for f in conn.get_vertex_frames()]
    ['career__Companies', 'career__People']
    >>> print [f.num_vertices for f in conn.get_vertex_frames()]
    [3, 101]

    """
    if names is not None and namespace is not None:
      raise ValueError('Only one of "names" and "namespaces" should be passed.')
    if names is None:
      names = []
    elif isinstance(names, six.string_types):
      raise TypeError('Invalid argument: "names" must be a list of strings')
    else:
      names = [_validated_frame_name(n) for n in names]

    request = graph_proto.GetFramesMetadataRequest()
    if names is not None:
      request.name.extend(names)
    if namespace is not None:
      request.namespace_name = _validated_namespace_name(namespace)
    response = self._call(request, self._graph_svc.GetVertexFrames)

    frames = []
    for data in response.container:
      schema = []
      vertex_key_val = sch_proto.RoleEnum.Value('VERTEX_KEY')
      key = None
      for prop in data.schema.property:
        prop_type = sch_proto.UvalTypeEnum.Name(prop.data_type).lower()
        prop_type = _to_unicode(prop_type)
        schema.append([prop.name, prop_type])
        if prop.role == vertex_key_val:
          key = prop.name
      frames.append(VertexFrame(self, data.name, schema, key))
    return frames

  def get_vertex_frame(self, name):
    """
    Get a VertexFrame object that allows interaction with a collection of vertices.

    A VertexFrame represents a collection of vertices held on the xGT
    server and can be used to retrieve information about them.
    `VertexFrame.get_data_pandas()` and `VertexFrame.get_data()` are
    used to retrieve member vertices.
    Each vertex in a VertexFrame shares the same properties,
    described in `VertexFrame.schema`. Each vertex in a VertexFrame
    is uniquely identified by the property listed in `VertexFrame.key`.

    Parameters
    ----------
    name : str
      Vertex frame name. The name must be a fully qualifed name that includes the
      namespace in which the frame exists.

    Returns
    -------
    VertexFrame
      Frame to the collection of vertices.

    Raises
    -------
    XgtNameError
      If the frame requested does not exist or is not visible to the user.
    XgtTransactionError
      If a conflict with another transaction occurs.

    Examples
    --------
    >>> conn = xgt.Connection()
    >>> v = conn.get_vertex_frame('career__People')
    >>> print(str(v))
    {
      'name': 'career__People',
      'key': 'id',
      'schema': [
        ['id', 'int'],
        ['name', 'text']],
    }
    >>> print(str(v.num_vertices))
    101
    >>> vertices = v.get_data_pandas()

    """
    frames = self.get_vertex_frames([name])
    if len(frames) == 0:
      error_msg = ("Frame not found: vertex frame {0}. It either does not "
                   "exist or the user lacks permission to read it".format(name))
      raise XgtNameError(error_msg)
    return frames[0]

  def get_edge_frames(self, names=None, namespace=None):
    """
    Get a list of EdgeFrame objects corresponding to each edge frame in the xGT server.
    Only frames that the calling user has permission to read are returned.

    An EdgeFrame represents a collection of edges held on the xGT
    server and can be used to retrieve information about them.
    `EdgeFrame.get_data_pandas()` and `EdgeFrame.get_data()` are
    used to retrieve member edges.
    Each edge in an EdgeFrame shares the same properties, described
    in `EdgeFrame.schema`.

    Parameters
    ----------
    names : list of strings or None
      If a list, the list of names of edge frames to retrieve.
      Each name must be a fully qualifed name that includes the namespace in which
      the frame exists.
      If None and the parameter namespace is None, all edge frames are returned.
    namespace: string or None
      Returns all edge frames in this namespace.
      At most one of names and namespace can be a value other than None.

    Returns
    -------
    list
      EdgeFrame objects corresponding to edge frames present in the server.

    Raises
    -------
    XgtNameError
      If an edge frame name requested does not exist or is not visible to the user.
      If an edge frame or namespace name does not follow naming rules.
    XgtTransactionError
      If a conflict with another transaction occurs.

    Examples
    --------
    >>> conn = xgt.Connection()
    >>> print [f.name for f in conn.get_edge_frames()]
    ['career__RelatedTo', 'career__WorksFor']

    """
    if names is not None and namespace is not None:
      raise ValueError('Only one of "names" and "namespaces" should be passed.')
    if names is None:
      names = []
    elif isinstance(names, six.string_types):
      raise TypeError('Invalid argument: "names" must be a list of strings')
    else:
      names = [_validated_frame_name(n) for n in names]

    request = graph_proto.GetFramesMetadataRequest()
    if names is not None:
      request.name.extend(names)
    if namespace is not None:
      request.namespace_name = _validated_namespace_name(namespace)
    response = self._call(request, self._graph_svc.GetEdgeFrames)
    frames = []
    for data in response.container:
      schema = []
      for prop in data.schema.property:
        prop_type = sch_proto.UvalTypeEnum.Name(prop.data_type).lower()
        prop_type = _to_unicode(prop_type)
        schema.append([prop.name, prop_type])
      frames.append(EdgeFrame(self, data.name, schema,
                              data.source_vertex, data.target_vertex,
                              data.source_key, data.target_key))
    return frames

  def get_edge_frame(self, name):
    """
    Get an EdgeFrame object that allows interaction with a collection of edges.

    An EdgeFrame represents a collection of edges held on the xGT
    server and can be used to retrieve information about them.
    `EdgeFrame.get_data_pandas()` and `EdgeFrame.get_data()` are
    used to retrieve member edges.
    Each edge in an EdgeFrame shares the same properties, described
    in `EdgeFrame.schema`.

    Parameters
    ----------
    name : str
      EdgeFrame name. The name must be a fully qualifed name that includes the
      namespace in which the frame exists.

    Returns
    -------
    EdgeFrame
      Frame to the collection of edges.

    Raises
    -------
    XgtNameError
      If the frame requested does not exist or is not visible to the user.
    XgtTransactionError
      If a conflict with another transaction occurs.

    Examples
    --------
    >>> conn = xgt.Connection()
    >>> ... create graph and run queries ...
    >>> e = conn.get_edge_frame('career__WorksFor')
    >>> print(str(e))
    {
      'name': 'career__WorksFor',
      'source': 'career__People',
      'target': 'career__Companies',
      'schema': [
        ['srcid', 'int'],
        ['trgid', 'int']],
      'source_key' : 'srcid',
      'target_key' : 'trgid'
    }
    >>> edges = e.get_data_pandas()

    """
    frames = self.get_edge_frames([name])
    if len(frames) == 0:
      error_msg = ("Frame not found: edge frame {0}. It either does not "
                   "exist or the user lacks permission to read it".format(name))
      raise XgtNameError(error_msg)
    return frames[0]

  def get_namespaces(self):
    """
    Get a list of namespaces present in the xGT server.

    Returns
    -------
    list
      Names of namespaces present in the server.

    Examples
    --------
    >>> conn = xgt.Connection()
    >>> namespaces = conn.get_namespaces()
    >>> for ns in namespaces:
    >>> ... conn.drop_namespace(ns)
    """

    request = graph_proto.GetNamespacesRequest()
    response = self._call(request, self._graph_svc.GetNamespaces)
    return list(response.namespace_name)

  #------------------------- DDL Methods
  def _container_labels_helper(self, request, frame_labels,
                               security_labels, row_label_universe):
    if frame_labels is not None and security_labels is not None:
      raise ValueError('Cannot pass frame labels in both the "frame_labels"' +
                       ' and "security_labels" parameters.  Please use only ' +
                       ' the "frame_labels" parameter.')
    if frame_labels is None and security_labels is not None:
      frame_labels = security_labels
    if frame_labels is not None:
      for access in frame_labels:
        access_lower = access.lower()
        if access_lower not in ["create", "read", "update", "delete"]:
          raise XgtValueError("Invalid security access type: " + access)

        for l in frame_labels[access]:
          request.frame_label_map.access_labels[access_lower].label.append(l)

    if row_label_universe is not None:
      for label in row_label_universe:
        if isinstance(label, six.string_types):
          request.row_label_universe.label.append(label)
        else:
          raise TypeError('Invalid argument: row labels must be strings')

    return request

  def create_namespace(self, name, frame_labels = None, security_labels = None,
                       row_label_universe = None, attempts = 1):
    """
    Create a new empty namespace on the server.

    Parameters
    ----------
    name : str
      The name of the namespace to create.
    frame_labels : dictionary
      A dictionary mapping a string to a list of strings. The key represents
      the permission type. The value represents the labels required for this
      permission. Permission types are "create", "read", "update", and "delete".
      By default no labels are required.
    security_labels : dictionary
      same as frame_labels (DEPRECATED)
    row_label_universe :  array
      **NOT yet supported**.
      An array of all possible labels to be used for rows inside this namespace.
      A maximum of 128 labels are supported for rows in each frame.
      By default no row labels are required.
    attempts : int
      Number of times to attempt the creation of the namespace.
      It will be retried if it fails due to transactional conflicts.
      (since version 1.4.1)

    Raises
    -------
    XgtNameError
      If the name provided does not follow rules for namespace names.
      A namespace name cannot contain "__", which is used as a separator
      between namespace and name in fully qualified frame names.
      If a namespace with this name already exists.
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.

    Examples
    --------
    >>> import xgt
    >>> conn = xgt.Connection()
    >>> labels = { 'create' : ['label1', 'label2'], 'read' : ['label1'],
                   'update' : ['label1'], 'delete' : ['label1', 'label2', 'label3'] }
    >>> row_label_universe = [ 'label1', 'label4' ]
    >>> conn.create_namespace('career', labels, row_label_universe)

    """
    request = graph_proto.CreateNamespaceRequest()
    request.frame_name = _validated_namespace_name(name)
    request = self._container_labels_helper(request, frame_labels,
                                            security_labels, row_label_universe)
    self._process_kwargs(request,  {'attempts':attempts})
    self._call(request, self._graph_svc.CreateNamespace)

  def create_table_frame(self, name, schema, frame_labels = None,
                         security_labels = None,
                         row_label_universe = None, attempts = 1):
    """
    Create a new TableFrame in the server.

    A TableFrame object represents a table held on the xGT server and can be
    used to retrieve information about it. The TableFrame schema describes
    the names and data types of table properties.

    Parameters
    ----------
    name : str
      Name of table.
      Fully qualified frame name. It must include the namespace in which the frame
      will be created.
    schema : list of pairs
      List of pairs associating property names with xGT data types.
    frame_labels : dictionary
      A dictionary mapping a string to a list of strings. The key represents
      the permission type. The value represents the labels required for this
      permission. Permission types are create, read, update, and delete.
      By default no labels are required.
    security_labels : dictionary
      same as frame_labels (DEPRECATED)
    row_label_universe :  array
      An array of all possible labels to be used for rows inside this table frame.
      A maximum of 128 labels are supported for rows in each frame.
      By default no row labels are required.
      (since version 1.5.0)
    attempts : int
      Number of times to attempt the creation of the TableFrame.
      It will be retried if it fails due to transactional conflicts.
      (since version 1.4.1)

    Returns
    -------
    TableFrame
      Frame to the table.

    Raises
    -------
    XgtNameError
      If the name provided is not a correct fully qualified name or
      a frame with this name already exists in the namespace.
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.

    Examples
    --------
    >>> import xgt
    >>> conn = xgt.Connection()
    >>> conn.create_table_frame(
    ...   name = 'career__Table1',
    ...   schema = [['id', xgt.INT],
    ...             ['name', xgt.TEXT]],
    ...   frame_labels = { 'create' : ['label1'],
    ...                    'delete' : ['label1', 'label2'] })

    """
    name = _validated_frame_name(name)
    schema = _validated_schema(schema)

    request = graph_proto.CreateFrameRequest()
    request.type = sch_proto.FrameTypeEnum.Value('TABLE')
    request.frame_name = name

    for col_name,col_type in schema:
      prop = sch_proto.Property()
      prop.name = col_name
      prop.data_type = sch_proto.UvalTypeEnum.Value(col_type)
      prop.role = sch_proto.RoleEnum.Value('PROPERTY')
      request.schema.property.extend([prop])

    request = self._container_labels_helper(request, frame_labels,
                                            security_labels, row_label_universe)

    self._process_kwargs(request, {'attempts':attempts})
    response =  self._call(request, self._graph_svc.CreateFrame)

    data = response.container[0]
    schema_returned = []
    for prop in data.schema.property:
      prop_type = sch_proto.UvalTypeEnum.Name(prop.data_type).lower()
      prop_type = _to_unicode(prop_type)
      schema_returned.append([prop.name, prop_type])

    frame = TableFrame(self, data.name, schema_returned)
    return frame

  def create_vertex_frame(self, name, schema, key, frame_labels = None,
                          security_labels = None,
                          row_label_universe = None, attempts = 1):
    """
    Create a new VertexFrame in the server.

    A VertexFrame represents a grouping or collection of vertices
    held on the xGT server, all sharing the same property names
    and types. This function creates a new frame of vertices
    on the xGT server and returns a VertexFrame representing it.

    Parameters
    ----------
    name : str
      Fully qualified frame name. It must include the namespace in which the frame
      will be created.
    schema : list of pairs
      List of pairs associating property names with xGT data types.
      Each vertex in the VertexFrame will have these properties.
    key : str
      The property name used to uniquely identify vertices in the graph.
      This is the name of one of the properties from the schema and
      must be unique for each vertex in the frame.
    frame_labels : dictionary
      A dictionary mapping a string to a list of strings. The key represents
      the permission type. The value represents the labels required for this
      permission. Permission types are create, read, update, and delete.
      By default no labels are required.
    security_labels : dictionary
      same as frame_labels (DEPRECATED)
    row_label_universe :  array
      An array of all possible labels to be used for rows inside this vertex frame.
      A maximum of 128 labels are supported for rows in each frame.
      By default no row labels are required.
      (since version 1.5.0)
    attempts : int
      Number of times to attempt the creation of the VertexFrame.
      It will be retried if it fails due to transactional conflicts.
      (since version 1.4.1)

    Returns
    -------
    VertexFrame
      Frame to the collection of vertices.

    Raises
    -------
    XgtNameError
      If the name provided is not a correct fully qualified name.
      If the key is not in the schema.
      If a frame with this name already exists in the namespace.
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.

    Examples
    --------
    >>> import xgt
    >>> conn = xgt.Connection()
    >>> people = conn.create_vertex_frame(
    ...            name = 'career__People',
    ...            schema = [['id', xgt.INT],
    ...                      ['name', xgt.TEXT]],
    ...            key = 'id',
    ...            frame_labels = { 'create' : ['label1'],
    ...                             'delete' : ['label1', 'label2'] })

    """
    name = _validated_frame_name(name)
    schema = _validated_schema(schema)
    key = _validated_property_name(key)

    key_found = False
    if key not in [prop for prop,_ in schema]:
      msg = u'The vertex key "{0}" does not match any schema property ' \
            u'name in this frame.'
      raise XgtNameError(msg.format(key))

    request = graph_proto.CreateFrameRequest()
    request.type = sch_proto.FrameTypeEnum.Value('VERTEX')
    request.frame_name = name

    for col_name,col_type in schema:
      prop = sch_proto.Property()
      prop.name = col_name
      prop.data_type = sch_proto.UvalTypeEnum.Value(col_type)

      if col_name == key:
        prop.role = sch_proto.RoleEnum.Value('VERTEX_KEY')
      else:
        prop.role = sch_proto.RoleEnum.Value('PROPERTY')
      request.schema.property.extend([prop])

    request = self._container_labels_helper(request, frame_labels,
                                            security_labels, row_label_universe)

    self._process_kwargs(request, {'attempts':attempts})
    response =  self._call(request, self._graph_svc.CreateFrame)

    data = response.container[0]
    schema_returned = []
    vertex_key_val = sch_proto.RoleEnum.Value('VERTEX_KEY')
    key_returned = None

    for prop in data.schema.property:
      prop_type = sch_proto.UvalTypeEnum.Name(prop.data_type).lower()
      prop_type = _to_unicode(prop_type)
      schema_returned.append([prop.name, prop_type])
      if prop.role == vertex_key_val:
        key_returned = prop.name

    frame = VertexFrame(self, data.name, schema_returned, key_returned)
    return frame


  def create_edge_frame(self, name, schema, source, target, source_key,
                        target_key, frame_labels = None, security_labels = None,
                        row_label_universe = None, attempts = 1):
    """
    Create a new EdgeFrame in the server.

    An EdgeFrame represents a collection of edges held on the xGT server
    that share the same property names and types. The source vertex
    of each edge in an EdgeFrame must belong to the same VertexFrame.
    This source VertexFrame is identified by the source parameter of
    this function. The target vertex of each edge in an EdgeFrame must
    belong to the same VertexFrame. This target VertexFrame is identified
    by the target parameter.

    For each edge in the EdgeFrame, its source vertex is identified by
    the edge property name given in the parameter source_key, which must
    be one of the properties listed in the schema. The edge target vertex
    is identified by the property name given in the parameter target_key,
    which must be one of the properties listed in the schema.

    Parameters
    ----------
    name : str
      Fully qualified frame name. It must include the namespace in which the frame
      will be created.
    schema : list of pairs
      List of pairs associating property names with xGT data types.
      Each edge in the EdgeFrame will have these properties.
    source : str or VertexFrame
      The name of a VertexFrame or a VertexFrame object.
      The source vertex of each edge in this EdgeFrame will belong
      to this VertexFrame.
    target : str or VertexFrame
      The name of a VertexFrame or a VertexFrame object.
      The target vertex of each edge in this EdgeFrame will belong
      to this VertexFrame.
    source_key : str
      The edge property name that identifies the source vertex of an edge.
      This is one of the properties from the schema.
    target_key : str
      The edge property name that identifies the target vertex of an edge.
      This is one of the properties from the schema.
    frame_labels : dictionary
      A dictionary mapping a string to a list of strings. The key represents
      the permission type. The value represents the labels required for this
      permission. Permission types are create, read, update, and delete.
      By default no labels are required.
    security_labels : dictionary
      same as frame_labels (DEPRECATED)
    row_label_universe :  array
      An array of all possible labels to be used for rows inside this edge frame.
      A maximum of 128 labels are supported for rows in each frame.
      By default no row labels are required.
      (since version 1.5.0)
    attempts : int
      Number of times to attempt the creation of the EdgeFrame.
      It will be retried if it fails due to transactional conflicts.
      (since version 1.4.1)

    Returns
    -------
    EdgeFrame
      Frame to the collection of edges.

    Raises
    -------
    XgtNameError
      If the name provided is not a correct fully qualified name.
      If the source_key or target_key are not in the schema. If the source or
      target VertexFrames are not found.
      If a frame with this name already exists in the namespace.
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.

    Examples
    --------
    >>> import xgt
    >>> conn = xgt.Connection()
    >>> conn.create_vertex_frame(
          name = 'career__People',
    ...   schema = [['id', xgt.INT],
    ...             ['name', xgt.TEXT]],
    ...   key = 'id')
    >>> conn.create_vertex_frame(
          name = 'career__Companies',
    ...   schema = [['id', xgt.INT],
    ...             ['size', xgt.TEXT],
    ...             ['name', xgt.TEXT]],
    ...   key = 'id',
    ...   frame_labels = { 'create' : ['label1'],
    ...                    'delete' : ['label1', 'label2'] })
    >>> conn.create_edge_frame(
          name = 'career__WorksFor',
    ...   schema = [['srcid', xgt.INT],
    ...             ['role', xgt.TEXT],
    ...             ['trgid', xgt.INT]],
    ...   source = 'career__People',
    ...   target = 'career__Companies',
    ...   source_key = 'srcid',
    ...   target_key = 'trgid',
    ...   frame_labels = { 'create' : ['label1'],
    ...                    'update' : ['label3'],
    ...                    'delete' : ['label1', 'label2'] })

    """
    name = _validated_frame_name(name)
    schema = _validated_schema(schema)
    source_key = _validated_property_name(source_key)
    target_key = _validated_property_name(target_key)

    if source_key not in [prop for prop, _ in schema]:
      msg = u'The source key "{0}" does not match any schema property ' \
            u'name in this frame.'
      raise XgtNameError(msg.format(source_key))
    if target_key not in [prop for prop, _ in schema]:
      msg = u'The target key "{0}" does not match any schema property ' \
            u'name in this frame.'
      raise XgtNameError(msg.format(target_key))

    if isinstance(source, VertexFrame):
      source_name = source.name
    else:
      source_name = _validated_frame_name(source)
    if isinstance(target, VertexFrame):
      target_name = target.name
    else:
      target_name = _validated_frame_name(target)

    request = graph_proto.CreateFrameRequest()
    request.type = sch_proto.FrameTypeEnum.Value('EDGE')
    request.frame_name = name
    request.source_key = source_key
    request.target_key = target_key
    request.source_vertex = source_name
    request.target_vertex = target_name

    for col_name, col_type in schema:
      prop = sch_proto.Property()
      prop.name = col_name
      prop.data_type = sch_proto.UvalTypeEnum.Value(col_type)

      if col_name == source_key:
        prop.role = sch_proto.RoleEnum.Value('EDGE_SOURCE_KEY')
      elif col_name == target_key:
        prop.role = sch_proto.RoleEnum.Value('EDGE_TARGET_KEY')
      else:
        prop.role = sch_proto.RoleEnum.Value('PROPERTY')
      request.schema.property.extend([prop])

    request = self._container_labels_helper(request, frame_labels,
                                            security_labels, row_label_universe)

    self._process_kwargs(request, {'attempts':attempts})
    response =  self._call(request, self._graph_svc.CreateFrame)

    data = response.container[0]
    schema_returned = []
    for prop in data.schema.property:
      prop_type = sch_proto.UvalTypeEnum.Name(prop.data_type).lower()
      prop_type = _to_unicode(prop_type)
      schema_returned.append([prop.name, prop_type])

    frame = EdgeFrame(self, data.name, schema_returned, data.source_vertex,
                      data.target_vertex, data.source_key, data.target_key)
    return frame

  def drop_namespace(self, namespace, force_drop = False, attempts = 10):
    """
    Drop a namespace from the server.

    Parameters
    ----------
    name : str
      The name of the namespace to drop.
    force_drop : bool
      If True, the namespace will be dropped even if it is not empty along with
      any frames it contains. If False, a non-empty namespace will not be dropped.
    attempts : int
      Number of times to attempt the deletion of the namespace.
      It will be retried if it fails due to transactional conflicts.
      (since version 1.4.1)

    Returns
    -------
    bool
      True if the namespace was found and dropped. False if the namespace was
      not found.

    Raises
    -------
    XgtFrameDependencyError
      If the namespace is not empty and force_drop is False.
    XgtNameError
      If the name provided does not follow rules for namespace names.
      A namespace name cannot contain "__", which is used as a separator
      between namespace and name in fully qualified frame names.
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.

    Examples
    --------
    >>> import xgt
    >>> conn = xgt.Connection()
    >>> labels = { 'create' : ['label1', 'label2'], 'read' : ['label1'],
    ...            'update' : ['label1'], 'delete' : ['label1', 'label2', 'label3'] }
    >>> conn.create_namespace('career', labels)
    >>> conn.drop_namespace('career')
    >>> conn.drop_namespace('career', force_drop = True)

    """
    request = graph_proto.DeleteNamespaceRequest()
    request.frame_name = namespace
    request.force_drop = force_drop
    self._process_kwargs(request, {'attempts':attempts})
    response = self._call(request, self._graph_svc.DeleteNamespace)
    return response.found_and_deleted

  def drop_frame(self, frame, attempts = 10):
    """
    Drop a VertexFrame, EdgeFrame, or TableFrame.

    Parameters
    ----------
    frame : str, VertexFrame, EdgeFrame, or TableFrame
      A frame or the name of a frame to drop on the xGT server.
      The name must be a fully qualifed name that includes the
      namespace in which the frame exists.
    attempts : int
      Number of times to attempt the deletion of the frame.
      It will be retried if it fails due to transactional conflicts.
      (since version 1.4.1)

    Returns
    -------
    bool
      True if frame was found and dropped and False if frame was not found.

    Raises
    -------
    XgtFrameDependencyError
      If another frame depends on this frame. The depending frame should be
      dropped first.
    XgtNameError
      If the name provided is not a correct fully qualified name.
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.

    """
    if isinstance(frame, TableFrame):
      name = frame.name
    else:
      name = _validated_frame_name(frame)
    request = graph_proto.DeleteFrameRequest()
    request.frame_name = name
    self._process_kwargs(request, {'attempts':attempts})
    response = self._call(request, self._graph_svc.DeleteFrame)
    return response.found_and_deleted

  def get_frame_labels(self, frame):
    """
    Retrieve the current security labels (CRUD) on a specific frame.

    Parameters
    ----------
    frame : str, VertexFrame, EdgeFrame, or TableFrame
      A frame or the name of a frame from which to retrieve the security labels

    Returns
    -------
    dict
      A dictionary in the form:

      .. code-block:: python

        {
          "create" : ['label1', ... ],
          "read" : ['label1', ... ],
          "update" : ['label1', ... ],
          "delete" : ['label1', ... ],
        }

    Raises
    -------
    XgtNameError
      If the name provided is not a correct fully qualified name.
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.
    """
    if isinstance(frame, TableFrame):
      name = frame.name
    else:
      name = _validated_frame_name(frame)
    request = graph_proto.GetFrameLabelsRequest()
    request.frame_name = name
    response = self._call(request, self._graph_svc.GetFrameLabels)
    try:
      access_labels = response.frame_label_map.access_labels
    except:
      return response
    label_map = dict()
    for key in access_labels.keys():
      label_map[key] = [_ for _ in access_labels[key].label]
    return label_map

  #------------------------- Job Methods

  def set_optimization_level(self, optlevel=None):
    """
    Set the optimization level for TQL queries.  (Removed in 1.4.1)

    See the documentation for :py:meth:`~Connection.run_job`
    and :py:meth:`~Connection.schedule_job` for how to pass
    optimization levels to each job.
    """
    raise XgtNotImplemented('set_optimization_level was Removed in 1.4.1')

  def get_jobs(self, jobids=None):
    """
    Get a list of Job objects, each representing the state of
    the job on the server at the point in time of the
    invocation of this function.

    Parameters
    ----------
    jobids : list of ints
      A list of job ids for which to return Job objects.
      By default all jobs are returned.

    Returns
    -------
    list
      A list of Job objects, each representing the state
      of a job in the server.

    Examples
    --------
    >>> conn = xgt.Connection()
    >>> ... create vertices and edges and run queries ...
    >>> all_jobs = conn.get_jobs()
    >>> for j in all_jobs:
    >>> ... print j
    id:6, status:completed
    id:7, status:completed
    id:8, status:running

    """
    jobs = []
    request = job_proto.GetJobsRequest()
    if (jobids is not None):
      for jobid in jobids:
        request.job_id.extend([jobid])
    responses = self._call(request, self._job_svc.GetJobs)
    for response in responses:
      _assert_noerrors(response)
      if (response.HasField("job_status")):
        jobs.append(response.job_status)
    return [Job(self, i) for i in jobs]

  def cancel_job(self, job):
    """
    Cancel the execution of a job in the server.

    A job can be canceled only if it is *running* and will have a status of
    *canceled* after its cancellation. A job that already had a status of
    *completed* or *failed* before invoking this function will keep that
    status after invoking this function.

    Parameters
    ----------
    job : Job, int
      A Job object or an integer job id to cancel.

    Returns
    -------
    bool
      True if the job was cancelled. False if the job already had a
      status of completed or failed before invoking this function.

    Raises
    -------
    XgtSecurityError
      If the user does not have required permissions for this action.

    Examples
    --------
    >>> conn = xgt.Connection()
    >>> ... create vertices and edges and run queries ...
    >>> print(conn.cancel_job(18))
    True
    >>> all_jobs = conn.get_jobs()
    >>> for j in all_jobs:
    >>> ... conn.cancel_job(j)

    """
    if isinstance(job, Job):
      jobid = job.id
    elif isinstance(job, six.integer_types):
      jobid = job
    else:
      raise TypeError("Job must be a Job object or an int.")

    # Get job status.
    request = job_proto.GetJobsRequest()
    request.job_id.extend([jobid])
    responses = self._call(request, self._job_svc.GetJobs)
    # Cancel job if it's not in a terminal state.
    for response in responses: # Expect only one response.
      if (response.HasField("job_status")):
        job_status = response.job_status
        if job_status.status in [sch_proto.JobStatusEnum.Value('SCHEDULED'),
                                 sch_proto.JobStatusEnum.Value('RUNNING')]:
          request = job_proto.CancelJobsRequest()
          request.job_id.extend([jobid])
          self._call(request, self._job_svc.CancelJobs)
          return True
    return False

  def run_job(self, query, optlevel=4, description=None, timeout=0,
              record_history=True):
    """
    Run a TQL query as a job. This function blocks
    until the job stops running.

    Parameters
    ----------
    query : str
      One TQL query string.
    optlevel : int
      Sets the level of query optimization. The valid values are:

        - 0: No optimization.
        - 1: General optimization.
        - 2: WHERE-clause optimization.
        - 3: Degree-cycle optimization.
        - 4: Query order optimization.
    description : str
      Optional description of the job.
      If description is None, this will default to the query text.
      (since version 1.4.0)
    timeout : int
      Maximum number of seconds that the query should take before being
      automatically canceled.
      A value less than or equal to zero means no limit on the query time.
    record_history : bool
      If true, records the history of the job.
      (since version 1.4.0)

    Returns
    -------
    Job
      A Job object for the query.

    Raises
    -------
    XgtSyntaxError
      If there is a syntax error in the TQL query.
    XgtNameError
      If there is a name error in the TQL query, such as specifying a frame that
      does not exist.
    XgtTypeError
      If there is a type error in the TQL query, such as comparing a schema
      property to the wrong data type.
    XgtValueError
      If there is a value error in the TQL query.
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.

    Examples
    --------
    >>> conn = xgt.Connection()
    >>> ... create vertices and edges ...
    >>> job = conn.run_job('MATCH (a:career__Employees) RETURN a.person_id INTO career__Results1', timeout=200)
    >>> print(job)
    id:20, status:completed

    >>> conn.run_job('MATCH (a) RETURN a.id INTO career__Results1')
    ...
    xgt.common.XgtValueError: Invalid column name: 'id'

    """
    job_obj = self._launch_job(query, wait=True, optlevel=optlevel,
                               description=description,
                               timeout=timeout, record_history=record_history)
    if job_obj.status == 'failed' or job_obj.status == 'rollback':
      msg = (u'Failed job. id={0} msg="{1}"').format(job_obj.id, job_obj.error)
      raise job_obj.error_type(msg, job_obj.trace)
    return job_obj

  def schedule_job(self, query, optlevel=4, description=None,
                   record_history=True):
    """
    Schedule a TQL query as a job. This function
    returns immediately after scheduling the job.

    Parameters
    ----------
    query : str
      One TQL query string.
    optlevel : int
      Sets the level of query optimization. The valid values are:

        - 0: No optimization.
        - 1: General optimization.
        - 2: WHERE-clause optimization.
        - 3: Degree-cycle optimization.
        - 4: Query order optimization.
    description : str
      Optional description of the job.
      If description is None, this will default to the query text.
      (since version 1.4.0)
    record_history : bool
      If true, records the history of the job.
      (since version 1.4.0)

    Returns
    -------
    Job
      A Job object representing the job that has been scheduled.

    Raises
    -------
    XgtSyntaxError
      If there is a syntax error in the TQL query.
    XgtNameError
      If there is a name error in the TQL query, such as specifying a frame that
      does not exist.
    XgtTypeError
      If there is a type error in the TQL query, such as comparing a schema
      property to the wrong data type.
    XgtValueError
      If there is a value error in the TQL query.
    XgtSecurityError
      If the user does not have required permissions for this action.

    Examples
    --------
    >>> conn = xgt.Connection()
    >>> ... create vertices and edges ...
    >>> query = 'MATCH (a:career__Employees) RETURN a.person_id INTO career__Results1'
    >>> job = conn.schedule_job(query)
    >>> print(job)
    id:25, status:scheduled

    """
    return self._launch_job(query, wait=False, optlevel=optlevel,
                            description=description,
                            timeout=0, record_history=record_history)

  def wait_for_job(self, job, timeout=0):
    """
    Wait for a job. This function blocks until the job stops running.

    Parameters
    ----------
    job : Job, int
      A Job object or an integer job id.
    timeout : int
      Number of seconds each job is allowed to execute before being
      automatically cancelled.
      A value less than or equal to zero means no limit on the wait time.

    Returns
    -------
    Job
      A Job object representing the state of the job on the server.

    Raises
    -------
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.
    XgtError
      If one or more query jobs failed.

    Examples
    --------
    >>> conn = xgt.Connection()
    >>> ... create vertices and edges ...
    >>> qr1 = 'MATCH (a:career__Employees) RETURN a.person_id INTO career__Results0'
    >>> jb1 = conn.schedule_job(qr1)
    >>> qr2 = 'MATCH (b:career__Companies) RETURN b.company_id INTO career__Results1'
    >>> jb2 = conn.schedule_job(qr2)
    >>> jb1 = conn.wait_for_job(jb1)
    >>> print(jb1)
    id:31, status:completed
    >>> jb2 = conn.wait_for_job(jb2)
    >>> print(jb2)
    id:32, status:completed

    """
    if isinstance(job, Job):
      jobid = job.id
    elif isinstance(job, six.integer_types):
      jobid = job
    else:
      raise TypeError('Job must be a Job object or an int.')
    if not (timeout is None or isinstance(timeout, numbers.Number)):
      raise TypeError('Timeout must be a number or None.')

    request = job_proto.WaitJobsRequest()
    request.job_id.extend([jobid])
    if (timeout is None):
      request.timeout = 0
    else:
      request.timeout = timeout
    response = self._call(request, self._job_svc.WaitJobs)
    one_job = response.job_status[0]
    job_obj = Job(self, one_job)
    if job_obj.status == 'failed' or job_obj.status == 'rollback':
      msg = (u'Failed job. id={0} msg="{1}"').format(jobid, job_obj.error)
      raise job_obj.error_type(msg, job_obj.trace)
    return job_obj

  def get_metrics_status(self):
    """
    Check whether the metrics cache is on and finished with updates. A status of
    metrics_complete is only valid for as long as no vertex or edge frames are
    modified or created.

    Returns
    -------
    str
      The status of metrics collection: metrics_completed, metrics_running, or
      metrics_off.

    Examples
    --------
    >>> conn = xgt.Connection()
    >>> conn.get_metrics_status()
    """

    request = metrics_proto.MetricsStatusRequest()
    response = self._call(request, self._metrics_svc.GetMetricsStatus)
    status = metrics_proto.MetricsStatusEnum.Name(response.status).lower()
    return status

  def wait_for_metrics(self, timeout=0):
    """
    Wait until the metrics cache is finished with updates. This function blocks
    until there are no more metrics to update or until metrics collection is
    turned off through the config or until the optional timeout is reached.

    Parameters
    ----------
    timeout : float
      Max number of seconds the function will block.
      A value less than or equal to zero means no limit on the block time.

    Returns
    -------
    bool
      Returns True if metrics collection was finished when the function returned.
      Returns False if metrics collection is not finished (if either metrics
      collection didn't complete before the timeout or if metrics cache is off.)

    Examples
    --------
    >>> conn = xgt.Connection()
    >>> finished = conn.wait_for_metrics()
    """

    begin = datetime.utcnow()
    check_interval_sec = 0.1
    status = self.get_metrics_status()
    while ((status == 'metrics_running') and
           (timeout is None or timeout <= 0 or
            datetime.utcnow() < begin + timedelta(seconds=timeout))):
      time.sleep(check_interval_sec)
      status = self.get_metrics_status()

    return (status == 'metrics_completed')

  def get_config(self, keys=None):
    """
    Get one or more configuration values from the server.

    Parameters
    ----------
    keys : list of strings or None
        If a list, the list of config keys to retrieve.
        If None, all config values are returned.

    Returns
    -------
    dict
      Dictionary of key-value pairs representing configuration information
      from the server.

    Raises
    -------
    XgtNameError
      If any keys requested are not valid.
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.

    Examples
    --------
    >>> conn = xgt.Connection()
    >>> conf1 = conn.get_config()
    >>> conf2 = conn.get_config(["key1", "key2", ... ])
    """

    if keys is None:
      keys = []
    elif isinstance(keys, six.string_types):
      raise TypeError('Invalid get_config argument: "keys" must be a list of strings')
    else:
      keys = [str(k) for k in keys]

    request = admin_proto.GetConfigRequest()
    request.key.extend(keys)
    response = self._call(request, self._admin_svc.GetConfig)
    keyvalues = dict()
    for key in response.entries:
      value = response.entries[key]
      if value.HasField("bool_value"):
        keyvalues[key] = value.bool_value
      elif value.HasField("int_value"):
        keyvalues[key] = value.int_value
      elif value.HasField("float_value"):
        keyvalues[key] = value.float_value
      elif value.HasField("string_value"):
        keyvalues[key] = value.string_value
      elif value.HasField("string_array_value"):
        keyvalues[key] = [i for i in value.string_array_value.string_value]
      else:
        raise XgtTypeError('Config value for key {} has an unknown type'.format(_to_str(key)))
    return keyvalues

  def set_config(self, config_dict):
    """
    Set key-value pairs in the server configuration.

    Parameters
    ----------
    config_dict: dict
      Dictionary containing config key-values.

    Raises
    -------
    XgtNameError
      If any keys provided are not valid.
    XgtTypeError
      If any config values provided are of the wrong type.
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.

    Examples
    --------
    >>> conn = xgt.Connection()
    >>> conn.set_config({"mykey" : 14, "another_key" : "This string"})
    """

    request = admin_proto.SetConfigRequest()
    for k,v in config_dict.items():
      if isinstance(v, bool):
        request.entries[k].bool_value = v
      elif isinstance(v, six.integer_types):
        request.entries[k].int_value = v
      elif isinstance(v, float):
        request.entries[k].float_value = v
      elif isinstance(v, six.string_types):
        request.entries[k].string_value = v
      else:
        raise XgtTypeError('Setting config value for key [{0}] has a value [{1}] whose type is not supported'.format(_to_str(k), _to_str(v)))
    response = self._call(request, self._admin_svc.SetConfig)
    return None
