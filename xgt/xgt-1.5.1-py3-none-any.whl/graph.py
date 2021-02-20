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

import json
import math
import sys
import traceback

import grpc
import six

try:
  from collections.abc import Iterable
except ImportError:
  from collections import Iterable

from . import DataService_pb2 as data_proto
from . import DataService_pb2_grpc as data_grpc
from . import GraphTypesService_pb2 as graph_proto
from . import SchemaMessages_pb2 as sch_proto
from .common import (_as_unicode, _assert_noerrors,
                     _get_valid_property_types_for_return_only,
                     _get_valid_property_types_to_create,
                     _to_bytes, _to_str, _to_unicode, XgtNotImplemented,
                     XgtIOError, XgtValueError, XgtInternalError, XgtTypeError,
                     MAX_PACKET_SIZE)
from .job import Job

class HeaderMode:
  NONE = 'none'
  IGNORE = 'ignore'
  NORMAL = 'normal'
  STRICT = 'strict'

  _all = [NONE,IGNORE,NORMAL,STRICT]

def _validate_row_level_labels_for_ingest(row_labels,
                                          row_label_columns = None):
  if row_labels is not None and row_label_columns is not None:
    error = ("Only one of row_labels and "
             "row_label_columns must be passed."
            )
    raise ValueError(error)
  if row_labels is not None and \
     not isinstance(row_labels, (list, tuple)):
    raise TypeError('row_labels must be a list or tuple of string labels.')
  if row_label_columns is not None and \
     not isinstance(row_label_columns, (list, tuple)):
    raise TypeError('row_label_columns must be a list or tuple.')

def _get_processed_row_level_label_columns(row_label_columns,
                                           headerMode = HeaderMode.NONE):
  if row_label_columns is None:
    return None
  elif headerMode == HeaderMode.NONE or headerMode == HeaderMode.IGNORE:
    return [int(col) for col in row_label_columns]
  elif headerMode == HeaderMode.NORMAL or headerMode == HeaderMode.STRICT:
    return [_as_unicode(col) for col in row_label_columns]

def _row_level_labels_helper(request, row_labels, row_label_columns,
                             source_vertex_row_labels, target_vertex_row_labels,
                             headerMode):
  if row_labels is not None:
    if len(row_labels) == 0:
      row_labels.append("")
    for label in row_labels:
      request.row_labels.labels.extend([label])
  if source_vertex_row_labels is not None:
    for label in source_vertex_row_labels:
      request.row_labels.implicit_source_vertex_labels.extend([label])
  if target_vertex_row_labels is not None:
    for label in target_vertex_row_labels:
      request.row_labels.implicit_target_vertex_labels.extend([label])
  if row_label_columns is not None:
    if headerMode == HeaderMode.NONE or headerMode == HeaderMode.IGNORE:
      for col in row_label_columns:
        request.row_labels.label_column_indices.extend([col])
    elif headerMode == HeaderMode.NORMAL or headerMode == HeaderMode.STRICT:
      for col in row_label_columns:
        request.row_labels.label_column_names.extend([col])
  return request

# -----------------------------------------------------------------------------

class TableFrame(object):
  """
  TableFrame object represent a table held on the xGT server. It can be
  used to retrieve information about it and should not be instantiated directly
  by the user. Methods that return this object: `Connection.get_table_frame()`,
  `Connection.get_table_frames()` and `Connection.create_table_frame()`. A table
  may also be created by a MATCH query and may contain query results.

  Parameters
  ----------
  conn : Connection
    An open connection to an xGT server.
  name : str
    Fully qualified name of the frame, including the namespace.
  schema : list of pairs
    List of pairs associating property names with xGT data types.

  Examples
  --------
  >>> import xgt
  >>> conn = xgt.Connection()
  >>> ... run query and store results in Results
  >>> t = conn.get_table_frame('career__Results')
  >>> print(t.name)

  """
  def __init__(self, conn, name, schema):
    """
    Constructor for TableFrame. Called when TableFrame is created.
    """
    self._conn = conn
    self._name = name
    # Check the schema against the valid property types.
    valid_prop_types = _get_valid_property_types_to_create() + \
                       _get_valid_property_types_for_return_only()

    for _, prop_type in schema:
      if prop_type not in valid_prop_types:
        raise XgtTypeError('Invalid property type "' + prop_type + '"')

    self._schema = [[c[0], c[1]] for c in schema]

  @property
  def name(self):
    """str: Name of the frame."""
    return self._name

  @property
  def schema(self):
    """list of lists: Gets the property names and types of the frame."""
    return self._schema

  @property
  def connection(self):
    """Connection object: The connection used when constructing the frame."""
    return self._conn

  def load(self, paths, headerMode = HeaderMode.NONE, record_history = True,
           row_labels = None, row_label_columns = None, delimiter = ','):
    """
    Loads data from one or more CSV files specified in the list of paths.
    Each path may have its own protocol as described below.

    Parameters
    ----------
    paths : list
      Paths to the CSV files.

      ==================== =====================================
                      Syntax for one CSV file path
      ----------------------------------------------------------
          Resource type                 Path syntax
      ==================== =====================================
          local to Python: '<path to csv file>'
                           'xgt://<path to csv file>'
          xGT server:      'xgtd://<path to csv file>'
          AWS s3:          's3://<path to csv file>'
          https site:      'https://<path to csv file>'
          http site:       'http://<path to csv file>'
          ftps server:     'ftps://<path to csv file>'
          ftp server:      'ftp://<path to csv file>'
      ==================== =====================================

    headerMode : str
      Indicates how the file header should be processed:
        - HeaderMode.NONE:
          No header exists.
        - HeaderMode.IGNORE:
          Ignore the first line containing the header.
        - HeaderMode.NORMAL:
          Process the header in non-strict mode. If a schema column is missing,
          a null value is ingested for that schema column. Any file column whose
          name does not correspond to a schema column or a security label column
          is ignored.
        - HeaderMode.STRICT:
          Process the header in strict mode. The name of each header column
          should correspond to a schema column, a security label column, or be
          named IGNORE. Each schema column must appear in the file.

      Optional. Default=HeaderMode.NONE.

    record_history : bool
      If true, records the history of the job.
      (since version 1.4.0)

    row_labels : list
      A list of security labels to attach to each row inserted with the load.
      Each label must have been passed in to the row_label_universe
      parameter when creating the frame. Note: Only one of row_labels
      and row_label_columns must be passed.
      (since version 1.5.0)

    row_label_columns: list
      A list of columns indicating which columns in the CSV file contain
      security labels to attach to the inserted row. If the header mode is
      NONE or IGNORE, this must be a list of integer column indices. If the
      header mode is NORMAL or STRICT, this must be a list of string column
      names. Note: Only one of row_labels and
      row_label_columns must be passed.
      (since version 1.5.0)

    delimiter : str
      Delimiter for data.
      (since version 1.6.0) (Fixme(version) : correct version)

    Returns
    -------
    Job
      A Job object representing the job that has executed the load.

    Raises
    -------
    XgtIOError
      If a file specified cannot be opened.
      Errors generated during the load operation will throw an XgtIOError and
      can be retrieved from the job object stored in the exception using its
      get_data() methods.
    XgtNameError
      If the frame does not exist on the server.
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.

    """
    return self._load(paths, headerMode, record_history, row_labels,
                      row_label_columns, delimiter = delimiter)

  def _load(self, paths, headerMode = HeaderMode.NONE, record_history = True,
            row_labels = None, row_label_columns = None,
            source_vertex_row_labels = None, target_vertex_row_labels = None,
            delimiter = ',', **kwargs):
    if not isinstance(delimiter, (six.string_types)) or len(delimiter) != 1:
      error = ("Delimiter must be a single character string.")
      raise ValueError(error)

    if headerMode is None:
      raise TypeError('the "headerMode" parameter is None')
    if headerMode not in HeaderMode._all:
      raise TypeError('Invalid header mode: "{0}"'.format(_to_str(headerMode)))

    _validate_row_level_labels_for_ingest(row_labels,
                                          row_label_columns)
    _validate_row_level_labels_for_ingest(source_vertex_row_labels)
    _validate_row_level_labels_for_ingest(target_vertex_row_labels)
    row_label_columns = _get_processed_row_level_label_columns(
        row_label_columns, headerMode)

    if paths is None:
      raise TypeError('the "paths" parameter is None')
    if not isinstance(paths, (list, tuple, six.string_types)):
      raise TypeError('one or more file paths are expected; the data type of the "paths" parameter is "{0}"'.format(type(paths)))
    client_paths, server_paths, url_paths = _group_paths(paths, True)
    if len(client_paths) == 0 and len(server_paths) == 0 and len(url_paths) == 0:
      raise XgtIOError('no valid paths found: ' + _to_unicode(paths))
    if len(client_paths) > 0:
      return self._insert_from_csv(client_paths, headerMode, row_labels,
                                   row_label_columns, source_vertex_row_labels,
                                   target_vertex_row_labels, delimiter)
    if len(server_paths) > 0:
      return self._ingest(server_paths, headerMode, row_labels,
                          row_label_columns, source_vertex_row_labels,
                          target_vertex_row_labels,
                          delimiter, record_history = record_history, **kwargs)
    if len(url_paths) > 0:
      return self._ingest(url_paths, headerMode, row_labels, row_label_columns,
                          source_vertex_row_labels, target_vertex_row_labels,
                          delimiter, record_history = record_history, **kwargs)

  def save(self, path, offset = 0, length = None, headers = False,
           record_history = True, include_row_labels = False,
           row_label_column_header = None, preserve_order = False):
    """
    Writes the rows from the frame to a CSV file in the path and the
    computer indicated by the path.

    Parameters
    ----------
    path : str
      Path to the CSV file.

      ==================== =====================================
                      Syntax for one CSV file path
      ----------------------------------------------------------
          Resource type                 Path syntax
      ==================== =====================================
          local to Python: '<path to csv file>'
                           'xgt://<path to csv file>'
          xGT server:      'xgtd://<path to csv file>'
      ==================== =====================================

    offset : int
      Position (index) of the first row to be retrieved.
      Optional. Default=0.
    length : int
      Maximum number of rows to be retrieved.
      Optional. Default=None.
    headers : boolean
      Indicates if headers should be added.
      Optional. Default=False.
    record_history : bool
      If true, records the history of the job.
      (since version 1.4.0)
    include_row_labels : bool
      Indicates whether the security labels for each row
      should be egested along with the row.
      (since version 1.5.0)
    row_label_column_header : str
      The header column name to use for all row labels
      if include_row_labels is true and headers is true.
      (since version 1.5.0)
    preserve_order : boolean
      Indicates if the output should keep the order the
      frame is stored in.
      Optional. Default=False.
      (since version 1.6.0) (Fixme(version) : correct version)

    Returns
    -------
    Job
      A Job object representing the job that has executed the save.

    Raises
    -------
    XgtIOError
      If a file specified cannot be opened.
    XgtNameError
      If the frame does not exist on the server.
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.

    """
    return self._save(path, offset, length, headers, record_history,
                      include_row_labels,
                      row_label_column_header, preserve_order)

  def _save(self, path, offset = 0, length = None, headers = False,
            record_history = True, include_row_labels = False,
            row_label_column_header=None, preserve_order = False,
            **kwargs):
    if path is None:
      raise TypeError('the "paths" parameter is None')
    if not isinstance(path, six.string_types):
      msg = 'a file path is expected; the data type of the "path" ' \
            'parameter is "{0}"'.format(type(path))
      raise TypeError(msg)

    client_paths, server_paths, url_paths = _group_paths(path, False)
    if (len(client_paths) == 0 and len(server_paths) == 0 and
        len(url_paths) == 0):
      raise XgtIOError('no valid paths found: ' + _to_unicode(path))
    if len(client_paths) > 0:
      return self._save_to_csv(client_paths[0], offset, length, headers,
                         include_row_labels = include_row_labels,
                         row_label_column_header = row_label_column_header)
    if len(server_paths) > 0:
      return self._egest(server_paths[0], headers,
                         record_history=record_history,
                         include_row_labels = include_row_labels,
                         row_label_column_header = row_label_column_header,
                         preserve_order = preserve_order, **kwargs)

  def _insert_packet_generator(self, data, is_pandas,
                               row_labels = None,
                               row_label_columns = None,
                               source_vertex_row_labels = None,
                               target_vertex_row_labels = None):
    columns = []
    column_types = {}
    for item in self.schema:
      columns.append(item[0])
      column_types[item[0]] = item[1]
    schemasize = len(columns)
    nrow = len(data)
    col_names = '"' + ('","'.join(columns)) + '"'

    try:
      tbl = ''
      for i in range(nrow):
        row = ''
        data_row = ''
        if is_pandas:
          length = len(data.columns)
        else:
          length = len(data[i])
        for j in range(length):
          if is_pandas:
            col = data[columns[j]][i]
          else:
            col = data[i][j]
          if j < schemasize:
            col_type = column_types[columns[j]]
            if col is None:
              strcol = ''
            else:
              strcol = _to_unicode(col)
              if isinstance(col, bool):
                  strcol = strcol.lower()
              if isinstance(col, six.string_types):
                  strcol = '"' + strcol + '"'
            row = row + strcol + ','
          else:
            if col is None:
              row = row + ','
            else:
              row = row + _to_unicode(col) + ','
        tbl = tbl + row[:-1] + '\n'
        if len(tbl) >= MAX_PACKET_SIZE:
          request = data_proto.UploadDataRequest()
          request.frame_name = self._name.encode('utf-8')
          request.content_type = data_proto.CSV
          request.header_mode = data_proto.NONE
          request.content = tbl.encode('utf-8')
          request.implicit_vertices = True
          request.delimiter = ','
          request = _row_level_labels_helper(request, row_labels,
                                             row_label_columns,
                                             source_vertex_row_labels,
                                             target_vertex_row_labels,
                                             HeaderMode.NONE)
          yield request
          tbl = ''
      if len(tbl) > 0:
        request = data_proto.UploadDataRequest()
        request.frame_name = self._name.encode('utf-8')
        request.content_type = data_proto.CSV
        request.header_mode = data_proto.NONE
        request.content = tbl.encode('utf-8')
        request.implicit_vertices = True
        request.delimiter = ','
        request = _row_level_labels_helper(request, row_labels,
                                           row_label_columns,
                                           source_vertex_row_labels,
                                           target_vertex_row_labels,
                                           HeaderMode.NONE)
        yield request
        tbl = ''
    except:
      #Print the error and don't throw since grpc will give an unknown error.
      traceback.print_exc(file=sys.stderr)
      sys.stderr.write("\n")
      pass

  def insert(self, data, row_labels = None,
             row_label_columns = None):
    """
    Inserts data rows. The properties of the new data must match the schema
    in both order and type.

    Parameters
    ----------
    data : list or Pandas dataframe
      Data represented by a list of lists of data items or by a
      Pandas Dataframe.

    row_labels : list
      A list of security labels to attach to each row inserted.
      Each label must have been passed in to the row_label_universe
      parameter when creating the frame. Note: Only one of row_labels
      and row_label_columns must be passed.
      (since version 1.5.0)

    row_label_columns: list
      A list of integer column indices indicating which columns in the input
      data contain security labels to attach to the inserted row. Note: Only
      one of row_labels and row_label_columns must be passed.
      (since version 1.5.0)

    Returns
    -------
    Job
      A Job object representing the job that has executed the insert.

    Raises
    -------
    XgtIOError
      Errors generated during the load operation will throw an XgtIOError and
      can be retrieved from the job object stored in the exception using its
      get_data() methods.
    XgtNameError
      If the frame does not exist on the server.
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.

    """
    if data is None:
      return
    if len(data) == 0:
      return

    #---- if user passed in a pandas frame
    is_pandas = False
    try:
      import pandas
      if isinstance(data, pandas.DataFrame):
        is_pandas = True
    except:
      pass

    # Exceptions for iterators get eaten by grpc so we check outside
    # the generator function:
    if not is_pandas:
      if (isinstance(data, six.text_type) or
          not isinstance(data, Iterable)):
        raise TypeError('a list of lists or a Pandas DataFrame is expected')
      for i in range(len(data)):
          if not isinstance(data[i], Iterable):
              msg = 'Row #{0} is not a list. A list of lists ' \
                    'or a Pandas DataFrame is expected'.format(i)
              raise TypeError(msg)

    _validate_row_level_labels_for_ingest(row_labels,
                                          row_label_columns)
    row_label_columns = _get_processed_row_level_label_columns(
        row_label_columns, HeaderMode.NONE)

    data_iter = self._insert_packet_generator(data, is_pandas,
                                              row_labels,
                                              row_label_columns)
    response = self._conn._call(data_iter, self._conn._data_svc.UploadData)
    job = Job(self._conn, response.job_status)
    if job.get_data() is not None:
      raise XgtIOError('Errors present in data insert for Frame ' + self._name + ':',  job = job)
    return job

  def _process_get_data_null_values(self, jsn, num_labels = 0):
    # Empty string currently means null. Return as None.
    for row_idx, row in enumerate(jsn[1:]):
      for idx in range(0, len(row) - num_labels):
        if row[idx] == '':
          jsn[row_idx + 1][idx] = None
    return jsn

  def get_data(self, offset = 0, length = None, include_row_labels = False):
    """
    Returns frame data starting at a given offset and spanning a given
    length.

    Parameters
    ----------
    offset : int
      Position (index) of the first row to be retrieved.
      Optional. Default=0.
    length : int
      Maximum number of rows to be retrieved starting from the row
      indicated by offset. A value of 'None' means 'all rows' on and
      after the offset.
      Optional. Default=None.
    include_row_labels : bool
      Indicates whether the security labels for each row
      should be egested along with the row.
      (since version 1.5.0)

    Returns
    -------
    list of lists

    Raises
    -------
    XgtNameError
      If the frame does not exist on the server.
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.

    """
    # Uses JSON conversion.  Results can get huge, which might result in the
    # client runnning out of memory.
    responses = self._get_data(offset=offset, length=length,
                               include_row_labels = include_row_labels,
                               row_label_column_header = None)
    res = ''
    num_labels = 0
    num_labels_set = False
    for response in responses:
        _assert_noerrors(response)
        res += response.content.decode('utf-8')
        # The last message won't have data or the number of labels so set only
        # once.
        if not num_labels_set:
          num_labels = response.num_row_labels
          num_labels_set = True
    try:
      jsn = json.loads('['+res+']')
      jsn = self._process_get_data_null_values(jsn, num_labels)

    except ValueError as ex:
      raise XgtInternalError('Corrupted data packet received: '+_to_unicode(ex))
    return jsn[1:]

  def get_data_pandas(self, offset = 0, length = None, include_row_labels = False,
                      row_label_column_header = None):
    """
    Returns a Pandas DataFrame containing frame data starting at a given
    offset and spanning a given length.

    Parameters
    ----------
    offset : int
      Position (index) of the first row to be retrieved.
      Optional. Default=0.
    length : int
      Maximum number of rows to be retrieved starting from the row
      indicated by offset. A value of 'None' means 'all rows' on and
      after the offset.
      Optional. Default=None.
    include_row_labels : bool
      Indicates whether the security labels for each row
      should be egested along with the row.
      (since version 1.5.0)
    row_label_column_header : str
      The header column name to use for all row labels
      if include_row_labels is true and headers is true.
      (since version 1.5.0)

    Returns
    -------
    Pandas DataFrame

    Raises
    -------
    XgtNameError
      If the frame does not exist on the server.
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.

    """
    import pandas
    # Uses JSON conversion.  Results can get huge, which might result in the
    # client runnning out of memory.
    responses = self._get_data(offset = offset, length = length,
                               include_row_labels = include_row_labels,
                               row_label_column_header = row_label_column_header)
    res = ''
    num_labels = 0
    num_labels_set = False
    for response in responses:
        _assert_noerrors(response)
        res += response.content.decode('utf-8')
        # The last message won't have data or the number of labels so set only
        # once.
        if not num_labels_set:
          num_labels = response.num_row_labels
          num_labels_set = True
    try:
      jsn = json.loads('['+res+']')
      jsn = self._process_get_data_null_values(jsn, num_labels)
    except ValueError as ex:
      raise XgtInternalError('Corrupted data packet received: '+_to_unicode(ex))
    return pandas.DataFrame(columns=jsn[0:1][0], data=jsn[1:])

  @property
  def num_rows(self):
    """int: Gets the number of rows in the frame."""
    request = graph_proto.GetFrameSizeRequest()
    request.frame_name = self._name
    response = self._conn._call(request, self._conn._graph_svc.GetFrameSize)
    return response.size

  def _get_data(self, offset = 0, length = None, headers = True,
                content_type = data_proto.JSON, include_row_labels = False,
                row_label_column_header = None):
    if isinstance(offset, six.string_types):
      offset = int(offset)
    if isinstance(length, six.string_types):
      length = int(length)
    if isinstance(offset, int):
      if offset < 0:
        raise ValueError('offset is negative')
    if isinstance(length, int):
      if length < 0:
        raise ValueError('length is negative')

    request = data_proto.DownloadDataRequest()
    request.repository_name = self._name
    if offset is not None:
      request.offset.value = offset
    if length is not None:
      request.length.value = length
    request.with_headers = headers
    request.content_type = content_type
    # Egesting data uses common options on the server side.
    # This option is currently not supported for get data,
    # Data will always be ordered. In the future, this
    # may change.
    request.preserve_order = True

    request.row_labels.egest_labels = include_row_labels
    if row_label_column_header is not None:
      request.row_labels.label_header_name = _as_unicode(
          row_label_column_header)
    else:
      request.row_labels.label_header_name = "ROWLABEL"

    responses = self._conn._call(request, self._conn._data_svc.DownloadData)
    return responses

  def _create_csv_packet (self, frame_name, data, headerMode, row_labels,
                          row_label_columns, source_vertex_row_labels,
                          target_vertex_row_labels, delimiter):
    request = data_proto.UploadDataRequest()
    request.frame_name = frame_name.encode('utf-8')
    request.content = _to_bytes(data)
    request.content_type = data_proto.CSV

    request = _row_level_labels_helper(request, row_labels,
                                                row_label_columns,
                                                source_vertex_row_labels,
                                                target_vertex_row_labels,
                                                headerMode)

    request.delimiter = delimiter;

    if headerMode == HeaderMode.IGNORE:
      request.header_mode = data_proto.IGNORE_HEADERS
    elif headerMode == HeaderMode.NORMAL:
      request.header_mode = data_proto.NORMAL
    elif headerMode == HeaderMode.STRICT:
      request.header_mode = data_proto.STRICT
    else:
      request.header_mode = data_proto.NONE
    request.implicit_vertices = True

    return request

  def _insert_csv_packet_generator(self, paths, headerMode, row_labels,
                                   row_label_columns, source_vertex_row_labels,
                                   target_vertex_row_labels, delimiter):
    for fpath in paths:
        try:
          header = ''
          data = ''
          dsize = 0
          with open(fpath, 'rb') as f:
            line = f.readline()
            while line:
              line = _to_unicode(line)
              lsize = len(line)
              if (dsize + lsize) < MAX_PACKET_SIZE:
                data += line
                dsize += lsize
              else:
                yield self._create_csv_packet(self._name, data, headerMode,
                                              row_labels, row_label_columns,
                                              source_vertex_row_labels,
                                              target_vertex_row_labels,
                                              delimiter)
                data = line
                dsize = len(data)
              line = f.readline()
            yield self._create_csv_packet(self._name, data, headerMode,
                                          row_labels, row_label_columns,
                                          source_vertex_row_labels,
                                          target_vertex_row_labels, delimiter)
        except:
          #Print the error and don't throw since grpc will give an unknown error.
          sys.stderr.write("Error in " + fpath + ": ")
          traceback.print_exc(file=sys.stderr)
          sys.stderr.write("\n")
          pass

  def _insert_from_csv(self, paths, headerMode=HeaderMode.NONE,
                       row_labels = None, row_label_columns = None,
                       source_vertex_row_labels = None,
                       target_vertex_row_labels = None, delimiter = ','):
    data_iter = self._insert_csv_packet_generator(paths, headerMode, row_labels,
                                                  row_label_columns,
                                                  source_vertex_row_labels,
                                                  target_vertex_row_labels,
                                                  delimiter)
    response = self._conn._call(data_iter, self._conn._data_svc.UploadData)
    job = Job(self._conn, response.job_status)
    if job.get_data() is not None:
      raise XgtIOError('Errors present in data insert for Frame ' + self._name + ':', job = job)
    return job

  def _ingest(self, paths, headerMode = HeaderMode.NONE,
              row_labels = None, row_label_columns = None,
              source_vertex_row_labels = None,
              target_vertex_row_labels = None, delimiter = ',', **kwargs):
    request = data_proto.IngestUriRequest()
    request.frame_name = self._name
    request = _row_level_labels_helper(request, row_labels,
                                                row_label_columns,
                                                source_vertex_row_labels,
                                                target_vertex_row_labels,
                                                headerMode)

    if isinstance(paths, (list, tuple)):
      request.content_uri.extend(paths)
    else:
      request.content_uri.extend([paths])

    if headerMode == HeaderMode.IGNORE:
      request.header_mode = data_proto.IGNORE_HEADERS
    elif headerMode == HeaderMode.NORMAL:
      request.header_mode = data_proto.NORMAL
    elif headerMode == HeaderMode.STRICT:
      request.header_mode = data_proto.STRICT
    else:
      request.header_mode = data_proto.NONE

    if (len(self._conn.aws_access_key_id) > 0 and \
        len(self._conn.aws_secret_access_key) > 0):
      request.authorization = self._conn.aws_access_key_id + ':' + \
                              self._conn.aws_secret_access_key

    request.implicit_vertices = True
    request.delimiter = delimiter;

    for k,v in kwargs.items():
      if isinstance(v, bool):
        request.kwargs[k].bool_value = v
      elif isinstance(v, six.integer_types):
        request.kwargs[k].int_value = v
      elif isinstance(v, float):
        request.kwargs[k].float_value = v
      elif isinstance(v, six.string_types):
        request.kwargs[k].string_value = v

    response = self._conn._call(request, self._conn._data_svc.IngestUri)
    job = Job(self._conn, response.job_status)
    if job.get_data() is not None:
      raise XgtIOError('Errors present in data ingest for Frame ' + self._name + ':', job = job)
    return job

  def _save_to_csv(self, path, offset = 0, length = None, headers = False,
                   include_row_labels = False, row_label_column_header = None):
    # This will stream the bytes directly which is > 10X faster than using json.
    responses = self._get_data(offset=offset, length=length, headers=headers,
                               content_type=data_proto.CSV,
                               include_row_labels = include_row_labels,
                               row_label_column_header = row_label_column_header)
    job_status = None
    with open(path, 'wb') as fobject:
      # Each packet can be directly written to the file since we have the
      # raw data. This avoids extra conversion issues and extra memory from
      # json.
      for response in responses:
          _assert_noerrors(response)
          fobject.write(response.content)
          if (response.HasField("job_status")):
            if (job_status is None):
              job_status = response.job_status
            else:
              raise XgtInternalError('Job status already set in packet stream')
    fobject.close()
    return job_status

  def _egest(self, path, headers = False, include_row_labels = False,
             row_label_column_header = None, preserve_order = False, **kwargs):
    request = data_proto.EgestUriRequest()
    request.frame_name = self._name
    request.file_name = path
    request.with_headers = headers
    request.preserve_order = preserve_order

    request.row_labels.egest_labels = include_row_labels
    if row_label_column_header is not None:
      request.row_labels.label_header_name = _as_unicode(
          row_label_column_header)
    else:
      request.row_labels.label_header_name = "ROWLABEL"

    for k,v in kwargs.items():
      if isinstance(v, bool):
        request.kwargs[k].bool_value = v
      elif isinstance(v, six.integer_types):
        request.kwargs[k].int_value = v
      elif isinstance(v, float):
        request.kwargs[k].float_value = v
      elif isinstance(v, six.string_types):
        request.kwargs[k].string_value = v

    response = self._conn._call(request, self._conn._data_svc.EgestUri)
    return Job(self._conn, response.job_status)

  def __str__(self):
    print_frame = "{'name': '" + self.name + "'" + \
                  ", 'schema': " + _to_unicode(self.schema) + "}"
    return _to_str(print_frame)

  @property
  def row_label_universe(self):
    """list of strings: Gets the universe of row security labels that can be
       attached to rows of this frame. Only labels that are also in the
       authenticated user's label set are returned."""
    request = graph_proto.GetRowLabelUniverseRequest()
    request.frame_name = self.name
    response = self._conn._call(request, self._conn._graph_svc.GetRowLabelUniverse)
    return response.row_labels.label

# -----------------------------------------------------------------------------

class VertexFrame(TableFrame):
  """
  VertexFrame object represents a collection of vertices held on the xGT
  server; it can be used to retrieve information about them and should not be
  instantiated directly by the user. Methods that return this object:
  `Connection.get_vertex_frame()`, `Connection.get_vertex_frames()` and
  `Connection.create_vertex_frame()`.

  Each vertex in a VertexFrame shares the same properties,
  described in `VertexFrame.schema`. Each vertex in a VertexFrame
  is uniquely identified by the property listed in `VertexFrame.key`.

  Parameters
  ----------
  conn : Connection
    An open connection to an xGT server.
  name : str
    Fully qualified name of the vertex frame, including the namespace.
  schema : list of pairs
    List of pairs associating property names with xGT data types.
    Each vertex in the VertexFrame will have these properties.
  key : str
    The property name used to uniquely identify vertices in the graph.
    This is the name of one of the properties from the schema and
    must be unique for each vertex in the frame.

  Examples
  --------
  >>> import xgt
  >>> conn = xgt.Connection()
  >>> v1 = conn.create_vertex_frame(
  ...        name = 'career__People',
  ...        schema = [['id', xgt.INT],
  ...                  ['name', xgt.TEXT]],
  ...        key = 'id')
  >>> v2 = conn.get_vertex_frame('career__Companies') # An existing vertex frame
  >>> print(v1.name, v2.name)

  """
  def __init__(self, conn, name, schema, key):
    """
    Constructor for VertexFrame. Called when VertexFrame is created.
    """
    super(VertexFrame, self).__init__(conn, name, schema)
    self._key = key

  @property
  def key(self):
    """str: Gets the property name that uniquely identifies vertices of this type."""
    return self._key

  @property
  def num_vertices(self):
    """int: Gets the number of vertices in the VertexFrame."""
    return self.num_rows

  def __str__(self):
    print_frame = ("{'name': '" + self.name + "'" +
                   ", 'schema': " + _to_unicode(self.schema) +
                   ", 'key': '" + self.key + "'}")
    return _to_str(print_frame)

# -----------------------------------------------------------------------------

class EdgeFrame(TableFrame):
  """
  EdgeFrame object represents a collection of edges held on the xGT server;
  it can be used to retrieve information about them and should not be
  instantiated directly by the user. Methods that return this object:
  `Connection.get_edge_frame()`, `Connection.get_edge_frames()` and
  `Connection.create_edge_frame()`. Each edge in an EdgeFrame shares the same
  properties, described in `EdgeFrame.schema`.

  The source vertex of each edge in an EdgeFrame must belong to the same
  VertexFrame. This name of this VertexFrame is given by `EdgeFrame.source_name`.
  The targe vertex of each edge in an EdgeFrame must belong to the same
  VertexFrame. This name of this VertexFrame is given by `EdgeFrame.target_name`.

  For each edge in the EdgeFrame, its source vertex is identified by
  the edge property name given by `EdgeFrame.source_key`, which is
  be one of the properties listed in the schema. The edge target vertex
  is identified by the property name given by `EdgeFrame.target_key`.

  Parameters
  ----------
  conn : Connection
    An open connection to an xGT server.
  name : str
    Fully qualified name of the edge frame, including the namespace.
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

  Examples
  --------
  >>> import xgt
  >>> conn = xgt.Connection()
  >>> e1 = conn.create_edge_frame(
  ...        name = 'career__WorksFor',
  ...        schema = [['srcid', xgt.INT],
  ...                  ['role', xgt.TEXT],
  ...                  ['trgid', xgt.INT]],
  ...        source = 'career__People',
  ...        target = 'career__Companies',
  ...        source_key = 'srcid',
  ...        target_key = 'trgid')
  >>> e2 = conn.get_edge_frame('career__RelatedTo') # An existing edge frame
  >>> print(e1.name, e2.name)

  """
  def __init__(self, conn, name, schema, source, target, source_key, target_key):
    """
    Constructor for EdgeFrame. Called when EdgeFrame is created.
    """
    super(EdgeFrame, self).__init__(conn, name, schema)
    self._source_name = source
    self._target_name = target
    self._source_key = source_key
    self._target_key = target_key

  @property
  def source_name(self):
    """str: Gets the name of the source vertex frame."""
    return self._source_name

  @property
  def target_name(self):
    """str: Gets the name of the target vertex frame."""
    return self._target_name

  @property
  def source_key(self):
    """str: The edge property name that identifies the source vertex of an edge."""
    return self._source_key

  @property
  def target_key(self):
    """str: The edge property name that identifies the target vertex of an edge."""
    return self._target_key

  @property
  def num_edges(self):
    """int: Gets the number of edges in the EdgeFrame."""
    return self.num_rows

  def __str__(self):
    print_frame = ("{'name': '" + self.name + "'" +
                   ", 'source': '" + self.source_name + "'" +
                   ", 'target': '" + self.target_name + "'" +
                   ", 'schema': " + _to_unicode(self.schema) +
                   ", 'source_key': '" + self.source_key + "'" +
                   ", 'target_key': '" + self.target_key + "'}")
    return _to_str(print_frame)

  def load(self, paths, headerMode = HeaderMode.NONE, record_history = True,
           row_labels = None, row_label_columns = None,
           source_vertex_row_labels = None, target_vertex_row_labels = None,
           delimiter = ','):
    """
    Loads data from one or more CSV files specified in the list of paths.
    Each path may have its own protocol as described below.

    Parameters
    ----------
    paths : list
      Paths to the CSV files.

      ==================== =====================================
                      Syntax for one CSV file path
      ----------------------------------------------------------
          Resource type                 Path syntax
      ==================== =====================================
          local to Python: '<path to csv file>'
                           'xgt://<path to csv file>'
          xGT server:      'xgtd://<path to csv file>'
          AWS s3:          's3://<path to csv file>'
          https site:      'https://<path to csv file>'
          http site:       'http://<path to csv file>'
          ftps server:     'ftps://<path to csv file>'
          ftp server:      'ftp://<path to csv file>'
      ==================== =====================================

    headerMode : str
      Indicates if the files contain headers:
        - HeaderMode.NONE
        - HeaderMode.IGNORE
        - HeaderMode.NORMAL
        - HeaderMode.STRICT

      Optional. Default=HeaderMode.NONE.

    record_history : bool
      If true, records the history of the job.
      (since version 1.4.0)

    row_labels : list
      A list of security labels to attach to each row inserted with the load.
      Each label must have been passed in to the row_label_universe
      parameter when creating the frame. Note: Only one of row_labels
      and row_label_columns must be passed.

    row_label_columns: list
      A list of columns indicating which columns in the CSV file contain
      security labels to attach to the inserted row. If the header mode is
      NONE or IGNORE, this must be a list of integer column indices. If the
      header mode is NORMAL or STRICT, this must be a list of string column
      names. Note: Only one of row_labels and
      row_label_columns must be passed.

    source_vertex_row_labels : list
      A list of security labels to attach to each source vertex that is
      implicitly inserted. Each label must have been passed in to the
      row_label_universe parameter when creating the frame.

    target_vertex_row_labels : list
      A list of security labels to attach to each target vertex that is
      implicitly inserted. Each label must have been passed in to the
      row_label_universe parameter when creating the frame.

    delimiter : str
      Delimiter for data.
      (since version 1.6.0) (Fixme(version) : correct version)

    Returns
    -------
    Job
      A Job object representing the job that has executed the load.

    Raises
    -------
    XgtIOError
      If a file specified cannot be opened.
      Errors generated during the load operation will throw an XgtIOError and
      can be retrieved from the job object stored in the exception using its
      get_data() methods.
    XgtNameError
      If the frame does not exist on the server.
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.

    """
    return self._load(paths, headerMode, record_history, row_labels,
                      row_label_columns, source_vertex_row_labels,
                      target_vertex_row_labels, delimiter)

  def insert(self, data, row_labels = None,
             row_label_columns = None,
             source_vertex_row_labels = None,
             target_vertex_row_labels = None):
    """
    Inserts data rows. The properties of the new data must match the schema
    in both order and type.

    Parameters
    ----------
    data : list or Pandas dataframe
      Data represented by a list of lists of data items or by a
      Pandas Dataframe.

    row_labels : list
      A list of security labels to attach to each row inserted.
      Each label must have been passed in to the row_label_universe
      parameter when creating the frame. Note: Only one of row_labels
      and row_label_columns must be passed.
      (since version 1.5.0)

    row_label_columns: list
      A list of integer column indices indicating which columns in the input
      data contain security labels to attach to the inserted row. Note: Only
      one of row_labels and row_label_columns must be passed.
      (since version 1.5.0)

    source_vertex_row_labels : list
      A list of security labels to attach to each source vertex that is
      implicitly inserted. Each label must have been passed in to the
      row_label_universe parameter when creating the frame.
      (since version 1.5.0)

    target_vertex_row_labels : list
      A list of security labels to attach to each target vertex that is
      implicitly inserted. Each label must have been passed in to the
      row_label_universe parameter when creating the frame.
      (since version 1.5.0)

    Returns
    -------
    Job
      A Job object representing the job that has executed the insert.

    Raises
    -------
    XgtIOError
      Errors generated during the load operation will throw an XgtIOError and
      can be retrieved from the job object stored in the exception using its
      get_data() methods.
    XgtNameError
      If the frame does not exist on the server.
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.

    """
    if data is None:
      return
    if len(data) == 0:
      return

    #---- if user passed in a pandas frame
    is_pandas = False
    try:
      import pandas
      if isinstance(data, pandas.DataFrame):
        is_pandas = True
    except:
      pass

    # Exceptions for iterators get eaten by grpc so we check outside
    # the generator function:
    if not is_pandas:
      if (isinstance(data, six.text_type) or
          not isinstance(data, Iterable)):
        raise TypeError('a list of lists or a Pandas DataFrame is expected')
      for i in range(len(data)):
          if not isinstance(data[i], Iterable):
              msg = 'Row #{0} is not a list. A list of lists ' \
                    'or a Pandas DataFrame is expected'.format(i)
              raise TypeError(msg)

    _validate_row_level_labels_for_ingest(row_labels,
                                          row_label_columns)
    _validate_row_level_labels_for_ingest(source_vertex_row_labels)
    _validate_row_level_labels_for_ingest(target_vertex_row_labels)
    row_label_columns = _get_processed_row_level_label_columns(
        row_label_columns, HeaderMode.NONE)

    data_iter = self._insert_packet_generator(data, is_pandas,
                                              row_labels,
                                              row_label_columns,
                                              source_vertex_row_labels,
                                              target_vertex_row_labels)
    response = self._conn._call(data_iter, self._conn._data_svc.UploadData)
    job = Job(self._conn, response.job_status)
    if job.get_data() is not None:
      raise XgtIOError('Errors present in data insert for Frame ' + self._name + ':', job = job)
    return job

# -----------------------------------------------------------------------------

def _group_paths(paths, for_ingest):
  client_prefix = 'xgt://'
  server_prefix = 'xgtd://'
  url_prefixes = ['s3://', 'https://', 'http://', 'ftps://', 'ftp://']
  client_paths = []
  server_paths = []
  url_paths = []
  if isinstance(paths, six.string_types):
    paths = [paths]
  elif not isinstance(paths, (list, tuple)):
    return client_paths, server_paths, url_paths
  for one_path in paths:
    if one_path == "":
      raise ValueError('one or more "paths" are empty')
    if one_path.startswith(client_prefix):
      _validate_client_path(one_path)
      client_paths.append(one_path[len(client_prefix):])
    elif one_path.startswith(server_prefix):
      server_paths.append(one_path[len(server_prefix):])
    elif any(map(lambda p: one_path.startswith(p), url_prefixes)):
      for url_prefix in url_prefixes:
        if for_ingest == False:
          msg = 'Url paths are invalid for data writing ' \
                '"{0}".'.format(one_path)
          raise XgtNotImplemented(msg)
        if one_path.startswith(url_prefix):
          url_paths.append(one_path)
          break
    else:
      if '://' in one_path:
        msg = 'Unsupported url protocol in path "{0}".'.format(one_path)
        raise XgtNotImplemented(msg)
      _validate_client_path(one_path)
      client_paths.append(one_path)
  return client_paths, server_paths, url_paths

def _validate_client_path(one_path):
  if one_path.endswith('.gz') or one_path.endswith('.bz2'):
    msg = 'Loading compressed files from a local filesystem is ' \
          'not supported: {0}'.format(one_path)
    raise XgtNotImplemented(msg)
