# -*- coding: utf-8 -*-
import datetime
import json
import xmltodict
import dicttoxml
from munch import munchify

from .exceptions import APIError


def _get_value(val):
    if isinstance(val, datetime.datetime):
        return val.isoformat()
    return val


class Resource(object):

    def __init__(self, api_client):
        self._http_client = api_client

    def _make_request(self, resource, **kwargs):
        response = self._http_client.make_request(resource, **kwargs)

        if response.status_code not in [200, 201]:
            raise APIError('{}. {}'.format(response.reason, response.text),
                           response.status_code)
        return response

    def _response_to_object(self, response):
        object_response = munchify(xmltodict.parse(response.content))
        return object_response


class ListResource(Resource):

    def get(self, resource_id):
        return munchify(json.loads(self._make_request(self.resource_name, resource_id=str(resource_id)).content))

    def search(self, filters=None):
        resource_list = []
        for resource_ids in self._search(filters):
            resource_list += resource_ids
        return resource_list

    def _search(self, filters=None):
        """ Return a list of ids of the given criteria"""
        # TODO: Paginate

        extra = dict()
        if filters:
            extra = {k: _get_value(v) for k, v in filters.items()}
        params = {
            'resource': self.resource_name,
            'extra': extra
        }
        page = 1
        while True:
            response = self._make_request(**params)
            object_response = self._response_to_object(response)
            size = int(object_response.result.size)

            if not size:
                return []
            elif size == 1:
                yield [object_response.result.entries.entry['@id']]
                break
            elif size <= 19:
                yield [int(x['@id']) for x in object_response.result.entries.entry]
                break
            else:
                yield [int(x['@id']) for x in object_response.result.entries.entry]
                page = page + 1
                params.get('extra').update({
                    'paging.page': page
                })

    def read(self, resource_id):
        params = {
            'resource': self.resource_name,
            'resource_id': resource_id
        }
        response = self._make_request(**params)
        return self._response_to_object(response)[self.resource_name]

    def _prepare_xml(self, resource_dict):
        request_dict = dict()
        request_dict[self.resource_name] = resource_dict
        request_xml = dicttoxml.dicttoxml(request_dict, root=False, attr_type=False)
        return request_xml

    def add(self, resource_dict):
        request_xml = self._prepare_xml(resource_dict)
        return self._add(request_xml)

    def _add(self, resource_xml):
        response = self._make_request(self.resource_name, data=resource_xml, verb='post')
        return self._response_to_object(response).result

    def update(self, resource_dict):
        res_id = str(resource_dict.pop('id'))
        request_xml = self._prepare_xml(resource_dict)
        return self._update(res_id, request_xml)

    def _update(self, res_id, resource_xml):
        response = self._make_request(self.resource_name + '/' + res_id, data=resource_xml, verb='post')
        return self._response_to_object(response).result

    def command(self, resource_update_dict, **kwargs):
        res_id = str(resource_update_dict['id'])
        return munchify(
            json.loads(
                self._make_request(
                    self.resource_name, resource_id=res_id,
                    data=resource_update_dict, verb='post', **kwargs
                ).text
            )
        )

    def delete(self, resource_delete_dict):
        res_id = str(resource_delete_dict['id'])
        return munchify(json.loads(self._make_request(self.resource_name, resource_id=res_id, verb='delete').text))


# class ListSubResource(ListResource):
#
#     def __init__(self, resource, subresource):
#         super(ListSubResource, self).__init__(resource._http_client, resource.store_id)
#         self.resource_name = resource.resource_name
#         self.subresource = subresource
#
#     def get(self, resource_id, id):
#         return munchify(json.loads(self._make_request(
#             self.resource_name,
#             resource_id=str(resource_id),
#             subresource=self.subresource,
#             subresource_id=str(id)).content)
#         )
#
#     def list(self, resource_id, filters={}, fields={}):
#         """
#         Get the list of customers for a store.
#         """
#         extra = {k:_get_value(v) for k,v in filters.items()}
#         if fields:
#             extra['fields'] = fields
#         return munchify(json.loads(self._make_request(
#             self.resource_name,
#             resource_id=str(resource_id),
#             subresource=self.subresource,
#             extra=extra).content)
#         )
#
#     def add(self, resource_id, subresource_dict):
#         return munchify(json.loads(self._make_request(
#             self.resource_name,
#             resource_id=str(resource_id),
#             subresource=self.subresource,
#             data=subresource_dict,
#             verb='post').text))
#
#     def update(self, resource_id, subresource_update_dict):
#         return munchify(json.loads(self._make_request(
#             self.resource_name,
#             resource_id=str(resource_id),
#             subresource=self.subresource,
#             subresource_id=subresource_update_dict['id'],
#             data=subresource_update_dict,
#             verb='put').text))
