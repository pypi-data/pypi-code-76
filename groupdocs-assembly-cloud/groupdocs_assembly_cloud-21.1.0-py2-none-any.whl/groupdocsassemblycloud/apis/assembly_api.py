# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose" file="assembly_api.py">
#   Copyright (c) 2021 GroupDocs.Assembly for Cloud
# </copyright>
# <summary>
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# </summary>
# -----------------------------------------------------------------------------------


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six
from groupdocsassemblycloud.rest import ApiException
from groupdocsassemblycloud.api_client import ApiClient


class AssemblyApi(object):
    """
    GroupDocs.Assembly for Cloud API

    :param api_client: an api client to perfom http requests
    """
    def __init__(self, app_sid, app_key):
        self.api_client = ApiClient()
        self.api_client.configuration.api_key['api_key'] = app_key
        self.api_client.configuration.api_key['app_sid'] = app_sid

    def assemble_document(self, request, **kwargs):  # noqa: E501
        """Builds a document using document template and XML or JSON data passed in request.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param assemble_options AssembleOptions : Assemble Options. It should be JSON or XML with TemplateFileInfo, SaveFormat, ReportData and etc.              (required)
        :return: file
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.assemble_document_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.assemble_document_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.api_client.request_token()
                if kwargs.get('is_async'):
                    return self.assemble_document_with_http_info(request, **kwargs)  # noqa: E501
                else:
                    (data) = self.assemble_document_with_http_info(request, **kwargs)  # noqa: E501
                    return data
        
    def assemble_document_with_http_info(self, request, **kwargs):  # noqa: E501
        """Builds a document using document template and XML or JSON data passed in request.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param request AssembleDocumentRequest object with parameters
        :return: file
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method assemble_document" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'assemble_options' is set
        if request.assemble_options is None:
            raise ValueError("Missing the required parameter `assemble_options` when calling `assemble_document`")  # noqa: E501

        collection_formats = {}
        path = '/v1.0/assembly/assemble'
        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.assemble_options is not None:
            body_params = request.assemble_options

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        
        # Authentication setting
        auth_settings = ['JWT']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='file',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def copy_file(self, request, **kwargs):  # noqa: E501
        """Copy file  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param dest_path str : Destination file path (required)
        :param src_path str : Source file's path e.g. '/Folder 1/file.ext' or '/Bucket/Folder 1/file.ext' (required)
        :param src_storage_name str : Source storage name
        :param dest_storage_name str : Destination storage name
        :param version_id str : File version ID to copy
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.copy_file_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.copy_file_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.api_client.request_token()
                if kwargs.get('is_async'):
                    return self.copy_file_with_http_info(request, **kwargs)  # noqa: E501
                else:
                    (data) = self.copy_file_with_http_info(request, **kwargs)  # noqa: E501
                    return data
        
    def copy_file_with_http_info(self, request, **kwargs):  # noqa: E501
        """Copy file  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param request CopyFileRequest object with parameters
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method copy_file" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'dest_path' is set
        if request.dest_path is None:
            raise ValueError("Missing the required parameter `dest_path` when calling `copy_file`")  # noqa: E501
        # verify the required parameter 'src_path' is set
        if request.src_path is None:
            raise ValueError("Missing the required parameter `src_path` when calling `copy_file`")  # noqa: E501

        collection_formats = {}
        path = '/v1.0/assembly/storage/file/copy/{srcPath}'
        path_params = {}
        if request.src_path is not None:
            path_params[self.__downcase_first_letter('SrcPath')] = request.src_path  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('DestPath') in path:
            path = path.replace('{' + self.__downcase_first_letter('DestPath' + '}'), request.dest_path if request.dest_path is not None else '')
        else:
            if request.dest_path is not None:
                query_params.append((self.__downcase_first_letter('DestPath'), request.dest_path))  # noqa: E501
        if self.__downcase_first_letter('SrcStorageName') in path:
            path = path.replace('{' + self.__downcase_first_letter('SrcStorageName' + '}'), request.src_storage_name if request.src_storage_name is not None else '')
        else:
            if request.src_storage_name is not None:
                query_params.append((self.__downcase_first_letter('SrcStorageName'), request.src_storage_name))  # noqa: E501
        if self.__downcase_first_letter('DestStorageName') in path:
            path = path.replace('{' + self.__downcase_first_letter('DestStorageName' + '}'), request.dest_storage_name if request.dest_storage_name is not None else '')
        else:
            if request.dest_storage_name is not None:
                query_params.append((self.__downcase_first_letter('DestStorageName'), request.dest_storage_name))  # noqa: E501
        if self.__downcase_first_letter('VersionId') in path:
            path = path.replace('{' + self.__downcase_first_letter('VersionId' + '}'), request.version_id if request.version_id is not None else '')
        else:
            if request.version_id is not None:
                query_params.append((self.__downcase_first_letter('VersionId'), request.version_id))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        
        # Authentication setting
        auth_settings = ['JWT']  # noqa: E501

        return self.api_client.call_api(
            path, 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def copy_folder(self, request, **kwargs):  # noqa: E501
        """Copy folder  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param dest_path str : Destination folder path e.g. '/dst' (required)
        :param src_path str : Source folder path e.g. /Folder1 (required)
        :param src_storage_name str : Source storage name
        :param dest_storage_name str : Destination storage name
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.copy_folder_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.copy_folder_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.api_client.request_token()
                if kwargs.get('is_async'):
                    return self.copy_folder_with_http_info(request, **kwargs)  # noqa: E501
                else:
                    (data) = self.copy_folder_with_http_info(request, **kwargs)  # noqa: E501
                    return data
        
    def copy_folder_with_http_info(self, request, **kwargs):  # noqa: E501
        """Copy folder  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param request CopyFolderRequest object with parameters
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method copy_folder" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'dest_path' is set
        if request.dest_path is None:
            raise ValueError("Missing the required parameter `dest_path` when calling `copy_folder`")  # noqa: E501
        # verify the required parameter 'src_path' is set
        if request.src_path is None:
            raise ValueError("Missing the required parameter `src_path` when calling `copy_folder`")  # noqa: E501

        collection_formats = {}
        path = '/v1.0/assembly/storage/folder/copy/{srcPath}'
        path_params = {}
        if request.src_path is not None:
            path_params[self.__downcase_first_letter('SrcPath')] = request.src_path  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('DestPath') in path:
            path = path.replace('{' + self.__downcase_first_letter('DestPath' + '}'), request.dest_path if request.dest_path is not None else '')
        else:
            if request.dest_path is not None:
                query_params.append((self.__downcase_first_letter('DestPath'), request.dest_path))  # noqa: E501
        if self.__downcase_first_letter('SrcStorageName') in path:
            path = path.replace('{' + self.__downcase_first_letter('SrcStorageName' + '}'), request.src_storage_name if request.src_storage_name is not None else '')
        else:
            if request.src_storage_name is not None:
                query_params.append((self.__downcase_first_letter('SrcStorageName'), request.src_storage_name))  # noqa: E501
        if self.__downcase_first_letter('DestStorageName') in path:
            path = path.replace('{' + self.__downcase_first_letter('DestStorageName' + '}'), request.dest_storage_name if request.dest_storage_name is not None else '')
        else:
            if request.dest_storage_name is not None:
                query_params.append((self.__downcase_first_letter('DestStorageName'), request.dest_storage_name))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        
        # Authentication setting
        auth_settings = ['JWT']  # noqa: E501

        return self.api_client.call_api(
            path, 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_folder(self, request, **kwargs):  # noqa: E501
        """Create the folder  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param path str : Target folder's path e.g. Folder1/Folder2/. The folders will be created recursively (required)
        :param storage_name str : Storage name
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.create_folder_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.create_folder_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.api_client.request_token()
                if kwargs.get('is_async'):
                    return self.create_folder_with_http_info(request, **kwargs)  # noqa: E501
                else:
                    (data) = self.create_folder_with_http_info(request, **kwargs)  # noqa: E501
                    return data
        
    def create_folder_with_http_info(self, request, **kwargs):  # noqa: E501
        """Create the folder  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param request CreateFolderRequest object with parameters
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_folder" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'path' is set
        if request.path is None:
            raise ValueError("Missing the required parameter `path` when calling `create_folder`")  # noqa: E501

        collection_formats = {}
        path = '/v1.0/assembly/storage/folder/{path}'
        path_params = {}
        if request.path is not None:
            path_params[self.__downcase_first_letter('Path')] = request.path  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('StorageName') in path:
            path = path.replace('{' + self.__downcase_first_letter('StorageName' + '}'), request.storage_name if request.storage_name is not None else '')
        else:
            if request.storage_name is not None:
                query_params.append((self.__downcase_first_letter('StorageName'), request.storage_name))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        
        # Authentication setting
        auth_settings = ['JWT']  # noqa: E501

        return self.api_client.call_api(
            path, 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_file(self, request, **kwargs):  # noqa: E501
        """Delete file  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param path str : Path of the file including file name and extension e.g. /Folder1/file.ext (required)
        :param storage_name str : Storage name
        :param version_id str : File version ID to delete
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.delete_file_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.delete_file_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.api_client.request_token()
                if kwargs.get('is_async'):
                    return self.delete_file_with_http_info(request, **kwargs)  # noqa: E501
                else:
                    (data) = self.delete_file_with_http_info(request, **kwargs)  # noqa: E501
                    return data
        
    def delete_file_with_http_info(self, request, **kwargs):  # noqa: E501
        """Delete file  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param request DeleteFileRequest object with parameters
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_file" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'path' is set
        if request.path is None:
            raise ValueError("Missing the required parameter `path` when calling `delete_file`")  # noqa: E501

        collection_formats = {}
        path = '/v1.0/assembly/storage/file/{path}'
        path_params = {}
        if request.path is not None:
            path_params[self.__downcase_first_letter('Path')] = request.path  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('StorageName') in path:
            path = path.replace('{' + self.__downcase_first_letter('StorageName' + '}'), request.storage_name if request.storage_name is not None else '')
        else:
            if request.storage_name is not None:
                query_params.append((self.__downcase_first_letter('StorageName'), request.storage_name))  # noqa: E501
        if self.__downcase_first_letter('VersionId') in path:
            path = path.replace('{' + self.__downcase_first_letter('VersionId' + '}'), request.version_id if request.version_id is not None else '')
        else:
            if request.version_id is not None:
                query_params.append((self.__downcase_first_letter('VersionId'), request.version_id))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        
        # Authentication setting
        auth_settings = ['JWT']  # noqa: E501

        return self.api_client.call_api(
            path, 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_folder(self, request, **kwargs):  # noqa: E501
        """Delete folder  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param path str : Folder path e.g. /Folder1s (required)
        :param storage_name str : Storage name
        :param recursive bool : Enable to delete folders, subfolders and files
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.delete_folder_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.delete_folder_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.api_client.request_token()
                if kwargs.get('is_async'):
                    return self.delete_folder_with_http_info(request, **kwargs)  # noqa: E501
                else:
                    (data) = self.delete_folder_with_http_info(request, **kwargs)  # noqa: E501
                    return data
        
    def delete_folder_with_http_info(self, request, **kwargs):  # noqa: E501
        """Delete folder  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param request DeleteFolderRequest object with parameters
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_folder" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'path' is set
        if request.path is None:
            raise ValueError("Missing the required parameter `path` when calling `delete_folder`")  # noqa: E501

        collection_formats = {}
        path = '/v1.0/assembly/storage/folder/{path}'
        path_params = {}
        if request.path is not None:
            path_params[self.__downcase_first_letter('Path')] = request.path  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('StorageName') in path:
            path = path.replace('{' + self.__downcase_first_letter('StorageName' + '}'), request.storage_name if request.storage_name is not None else '')
        else:
            if request.storage_name is not None:
                query_params.append((self.__downcase_first_letter('StorageName'), request.storage_name))  # noqa: E501
        if self.__downcase_first_letter('Recursive') in path:
            path = path.replace('{' + self.__downcase_first_letter('Recursive' + '}'), request.recursive if request.recursive is not None else '')
        else:
            if request.recursive is not None:
                query_params.append((self.__downcase_first_letter('Recursive'), request.recursive))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        
        # Authentication setting
        auth_settings = ['JWT']  # noqa: E501

        return self.api_client.call_api(
            path, 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def download_file(self, request, **kwargs):  # noqa: E501
        """Download file  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param path str : Path of the file including the file name and extension e.g. /folder1/file.ext (required)
        :param storage_name str : Storage name
        :param version_id str : File version ID to download
        :return: file
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.download_file_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.download_file_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.api_client.request_token()
                if kwargs.get('is_async'):
                    return self.download_file_with_http_info(request, **kwargs)  # noqa: E501
                else:
                    (data) = self.download_file_with_http_info(request, **kwargs)  # noqa: E501
                    return data
        
    def download_file_with_http_info(self, request, **kwargs):  # noqa: E501
        """Download file  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param request DownloadFileRequest object with parameters
        :return: file
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method download_file" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'path' is set
        if request.path is None:
            raise ValueError("Missing the required parameter `path` when calling `download_file`")  # noqa: E501

        collection_formats = {}
        path = '/v1.0/assembly/storage/file/{path}'
        path_params = {}
        if request.path is not None:
            path_params[self.__downcase_first_letter('Path')] = request.path  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('StorageName') in path:
            path = path.replace('{' + self.__downcase_first_letter('StorageName' + '}'), request.storage_name if request.storage_name is not None else '')
        else:
            if request.storage_name is not None:
                query_params.append((self.__downcase_first_letter('StorageName'), request.storage_name))  # noqa: E501
        if self.__downcase_first_letter('VersionId') in path:
            path = path.replace('{' + self.__downcase_first_letter('VersionId' + '}'), request.version_id if request.version_id is not None else '')
        else:
            if request.version_id is not None:
                query_params.append((self.__downcase_first_letter('VersionId'), request.version_id))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        
        # Authentication setting
        auth_settings = ['JWT']  # noqa: E501

        return self.api_client.call_api(
            path, 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='file',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_files_list(self, request, **kwargs):  # noqa: E501
        """Get all files and folders within a folder  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param path str : Folder path e.g. /Folder1 (required)
        :param storage_name str : Storage name
        :return: FilesList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.get_files_list_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.get_files_list_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.api_client.request_token()
                if kwargs.get('is_async'):
                    return self.get_files_list_with_http_info(request, **kwargs)  # noqa: E501
                else:
                    (data) = self.get_files_list_with_http_info(request, **kwargs)  # noqa: E501
                    return data
        
    def get_files_list_with_http_info(self, request, **kwargs):  # noqa: E501
        """Get all files and folders within a folder  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param request GetFilesListRequest object with parameters
        :return: FilesList
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_files_list" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'path' is set
        if request.path is None:
            raise ValueError("Missing the required parameter `path` when calling `get_files_list`")  # noqa: E501

        collection_formats = {}
        path = '/v1.0/assembly/storage/folder/{path}'
        path_params = {}
        if request.path is not None:
            path_params[self.__downcase_first_letter('Path')] = request.path  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('StorageName') in path:
            path = path.replace('{' + self.__downcase_first_letter('StorageName' + '}'), request.storage_name if request.storage_name is not None else '')
        else:
            if request.storage_name is not None:
                query_params.append((self.__downcase_first_letter('StorageName'), request.storage_name))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        
        # Authentication setting
        auth_settings = ['JWT']  # noqa: E501

        return self.api_client.call_api(
            path, 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FilesList',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_supported_file_formats(self, request, **kwargs):  # noqa: E501
        """Retrieves list of supported file formats.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :return: FileFormatsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.get_supported_file_formats_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.get_supported_file_formats_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.api_client.request_token()
                if kwargs.get('is_async'):
                    return self.get_supported_file_formats_with_http_info(request, **kwargs)  # noqa: E501
                else:
                    (data) = self.get_supported_file_formats_with_http_info(request, **kwargs)  # noqa: E501
                    return data
        
    def get_supported_file_formats_with_http_info(self, request, **kwargs):  # noqa: E501
        """Retrieves list of supported file formats.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param request GetSupportedFileFormatsRequest object with parameters
        :return: FileFormatsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_supported_file_formats" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}
        path = '/v1.0/assembly/formats'
        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        
        # Authentication setting
        auth_settings = ['JWT']  # noqa: E501

        return self.api_client.call_api(
            path, 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FileFormatsResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def move_file(self, request, **kwargs):  # noqa: E501
        """Move file  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param dest_path str : Destination file path e.g. '/dest.ext' (required)
        :param src_path str : Source file's path e.g. '/Folder 1/file.ext' or '/Bucket/Folder 1/file.ext' (required)
        :param src_storage_name str : Source storage name
        :param dest_storage_name str : Destination storage name
        :param version_id str : File version ID to move
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.move_file_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.move_file_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.api_client.request_token()
                if kwargs.get('is_async'):
                    return self.move_file_with_http_info(request, **kwargs)  # noqa: E501
                else:
                    (data) = self.move_file_with_http_info(request, **kwargs)  # noqa: E501
                    return data
        
    def move_file_with_http_info(self, request, **kwargs):  # noqa: E501
        """Move file  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param request MoveFileRequest object with parameters
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method move_file" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'dest_path' is set
        if request.dest_path is None:
            raise ValueError("Missing the required parameter `dest_path` when calling `move_file`")  # noqa: E501
        # verify the required parameter 'src_path' is set
        if request.src_path is None:
            raise ValueError("Missing the required parameter `src_path` when calling `move_file`")  # noqa: E501

        collection_formats = {}
        path = '/v1.0/assembly/storage/file/move/{srcPath}'
        path_params = {}
        if request.src_path is not None:
            path_params[self.__downcase_first_letter('SrcPath')] = request.src_path  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('DestPath') in path:
            path = path.replace('{' + self.__downcase_first_letter('DestPath' + '}'), request.dest_path if request.dest_path is not None else '')
        else:
            if request.dest_path is not None:
                query_params.append((self.__downcase_first_letter('DestPath'), request.dest_path))  # noqa: E501
        if self.__downcase_first_letter('SrcStorageName') in path:
            path = path.replace('{' + self.__downcase_first_letter('SrcStorageName' + '}'), request.src_storage_name if request.src_storage_name is not None else '')
        else:
            if request.src_storage_name is not None:
                query_params.append((self.__downcase_first_letter('SrcStorageName'), request.src_storage_name))  # noqa: E501
        if self.__downcase_first_letter('DestStorageName') in path:
            path = path.replace('{' + self.__downcase_first_letter('DestStorageName' + '}'), request.dest_storage_name if request.dest_storage_name is not None else '')
        else:
            if request.dest_storage_name is not None:
                query_params.append((self.__downcase_first_letter('DestStorageName'), request.dest_storage_name))  # noqa: E501
        if self.__downcase_first_letter('VersionId') in path:
            path = path.replace('{' + self.__downcase_first_letter('VersionId' + '}'), request.version_id if request.version_id is not None else '')
        else:
            if request.version_id is not None:
                query_params.append((self.__downcase_first_letter('VersionId'), request.version_id))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        
        # Authentication setting
        auth_settings = ['JWT']  # noqa: E501

        return self.api_client.call_api(
            path, 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def move_folder(self, request, **kwargs):  # noqa: E501
        """Move folder  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param dest_path str : Destination folder path to move to e.g '/dst' (required)
        :param src_path str : Source folder path e.g. /Folder1 (required)
        :param src_storage_name str : Source storage name
        :param dest_storage_name str : Destination storage name
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.move_folder_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.move_folder_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.api_client.request_token()
                if kwargs.get('is_async'):
                    return self.move_folder_with_http_info(request, **kwargs)  # noqa: E501
                else:
                    (data) = self.move_folder_with_http_info(request, **kwargs)  # noqa: E501
                    return data
        
    def move_folder_with_http_info(self, request, **kwargs):  # noqa: E501
        """Move folder  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param request MoveFolderRequest object with parameters
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method move_folder" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'dest_path' is set
        if request.dest_path is None:
            raise ValueError("Missing the required parameter `dest_path` when calling `move_folder`")  # noqa: E501
        # verify the required parameter 'src_path' is set
        if request.src_path is None:
            raise ValueError("Missing the required parameter `src_path` when calling `move_folder`")  # noqa: E501

        collection_formats = {}
        path = '/v1.0/assembly/storage/folder/move/{srcPath}'
        path_params = {}
        if request.src_path is not None:
            path_params[self.__downcase_first_letter('SrcPath')] = request.src_path  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('DestPath') in path:
            path = path.replace('{' + self.__downcase_first_letter('DestPath' + '}'), request.dest_path if request.dest_path is not None else '')
        else:
            if request.dest_path is not None:
                query_params.append((self.__downcase_first_letter('DestPath'), request.dest_path))  # noqa: E501
        if self.__downcase_first_letter('SrcStorageName') in path:
            path = path.replace('{' + self.__downcase_first_letter('SrcStorageName' + '}'), request.src_storage_name if request.src_storage_name is not None else '')
        else:
            if request.src_storage_name is not None:
                query_params.append((self.__downcase_first_letter('SrcStorageName'), request.src_storage_name))  # noqa: E501
        if self.__downcase_first_letter('DestStorageName') in path:
            path = path.replace('{' + self.__downcase_first_letter('DestStorageName' + '}'), request.dest_storage_name if request.dest_storage_name is not None else '')
        else:
            if request.dest_storage_name is not None:
                query_params.append((self.__downcase_first_letter('DestStorageName'), request.dest_storage_name))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        
        # Authentication setting
        auth_settings = ['JWT']  # noqa: E501

        return self.api_client.call_api(
            path, 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def upload_file(self, request, **kwargs):  # noqa: E501
        """Upload file  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param file_content file : File to upload (required)
        :param path str : Path where to upload including filename and extension e.g. /file.ext or /Folder 1/file.ext              If the content is multipart and path does not contains the file name it tries to get them from filename parameter              from Content-Disposition header. (required)
        :param storage_name str : Storage name
        :return: FilesUploadResult
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.upload_file_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.upload_file_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.api_client.request_token()
                if kwargs.get('is_async'):
                    return self.upload_file_with_http_info(request, **kwargs)  # noqa: E501
                else:
                    (data) = self.upload_file_with_http_info(request, **kwargs)  # noqa: E501
                    return data
        
    def upload_file_with_http_info(self, request, **kwargs):  # noqa: E501
        """Upload file  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param request UploadFileRequest object with parameters
        :return: FilesUploadResult
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method upload_file" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'file_content' is set
        if request.file_content is None:
            raise ValueError("Missing the required parameter `file_content` when calling `upload_file`")  # noqa: E501
        # verify the required parameter 'path' is set
        if request.path is None:
            raise ValueError("Missing the required parameter `path` when calling `upload_file`")  # noqa: E501

        collection_formats = {}
        path = '/v1.0/assembly/storage/file/{path}'
        path_params = {}
        if request.path is not None:
            path_params[self.__downcase_first_letter('Path')] = request.path  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('StorageName') in path:
            path = path.replace('{' + self.__downcase_first_letter('StorageName' + '}'), request.storage_name if request.storage_name is not None else '')
        else:
            if request.storage_name is not None:
                query_params.append((self.__downcase_first_letter('StorageName'), request.storage_name))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []
        if request.file_content is not None:
            local_var_files.append((self.__downcase_first_letter('FileContent'), request.file_content))  # noqa: E501

        body_params = None

        header_params['Content-Type'] = 'multipart/form-data'
        
        # Authentication setting
        auth_settings = ['JWT']  # noqa: E501

        return self.api_client.call_api(
            path, 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FilesUploadResult',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    # Helper method to convert first letter to downcase
    def __downcase_first_letter(self, s):
        if len(s) == 0:
            return s
        else:
            return s[0].lower() + s[1:]

    def __request_token(self):
        config = self.api_client.configuration
        request_url = "/connect/token"
        form_params = [('grant_type', 'client_credentials'), ('client_id', config.api_key['app_sid']),
                       ('client_secret', config.api_key['api_key'])]

        header_params = {'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}

        data = self.api_client.call_api(request_url, 'POST',
                                        {},
                                        [],
                                        header_params,
                                        post_params=form_params,
                                        response_type='object',
                                        files={}, _return_http_data_only=True)
        access_token = data['access_token'] if six.PY3 else data['access_token'].encode('utf8')
        self.api_client.configuration.access_token = access_token