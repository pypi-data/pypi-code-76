from alas_tools.clients.cn_admin.corenet_api_client import CoreNetApiClient
from alas_tools.common.clients import api_client as clients


class ServiceApiClient(CoreNetApiClient):
    service_endpoint_base_url = '/api/services/app/'

    def _validate(self):
        if self.entity_endpoint_base_url == '':
            raise Exception("Must set entity_api_base_url field.")

    def __get_all(self):
        request = clients.ApiClientRequest(
            self.service_endpoint_base_url + 'GetAll', self.auth)
        response = self.http_get(request)
        return response

    def __get_by_filter(self, **kwargs):
        url = self.service_endpoint_base_url + 'GetByFilter'
        if 'filter' in kwargs and kwargs['filter'] is not None:
            url = "{}?Filter={filter}".format(url, **kwargs)

    def get_all(self):
        return self.process_request(self.__get_all)

    def get_by_filter(self, filter=None):
        """

        :rtype: ApiClientResponse
        """
        return self.process_request(self.__get_by_filter, **{
            'filter': filter
        })

    def __get_by_id(self, **kwargs):
        url = self.service_endpoint_base_url + 'GetById'
        if 'id' in kwargs and kwargs['id'] is not None:
            url = "{Id}?id={id}".format(url, **kwargs)

        request = clients.ApiClientRequest(url, self.auth)
        response = self.http_get(request)
        return response

    def __get_by_code(self, **kwargs):
        url = self.service_endpoint_base_url + 'GetByCode'
        if 'code' in kwargs and kwargs['code'] is not None:
            url = "{}?Code={code}".format(url, **kwargs)
        if 'full' in kwargs and kwargs['full'] is not None:
            url = "{}&Full={full}".format(url, **kwargs)

        request = clients.ApiClientRequest(url, self.auth)
        response = self.http_get(request)
        return response

    def get_by_id(self, id):
        """

        :rtype: ApiClientResponse
        """
        return self.process_request(self.__get_by_id, **{
            'id': id
        })

    def get_by_code(self, code, get_full=False):
        # type: (str) -> ApiClientResponse
        """

        :rtype: ApiClientResponse
        """
        return self.process_request(self.__get_by_code, **{
            'code': code,
            'full': get_full
        })

    # -----------------
    def get_list(self):
        self._validate()
        return self.http_get_json(self.entity_endpoint_base_url)

    def search(self, search_info):
        self._validate()
        return self.http_post_json(self.entity_endpoint_base_url + "_search", search_info)

    def search_with_scroll(self, search_info):
        if not self.scroll_id:
            search_info.update({'use_scroll': True})
        else:
            search_info.update({'use_scroll': True, 'scroll_id': self.scroll_id})

        _result = self.search(search_info)
        _content = _result.content

        if 'extended_info' in _content and 'scroll_id' in _content['extended_info']:
            self.scroll_id = _content['extended_info']['scroll_id']
        else:
            self.scroll_id = None

        return _result

    def create(self, entity):
        self._validate()
        return self.http_post_json(self.entity_endpoint_base_url, entity)

    def bulk_create(self, entity):
        self._validate()
        return self.http_post_json(self.entity_endpoint_base_url + '_bulk-create', entity)

    def update(self, entity, id):
        self._validate()
        return self.http_put_json(self.entity_endpoint_base_url + str(id), entity)

    def delete(self, id):
        self._validate()
        return self.http_delete(self.entity_endpoint_base_url + str(id))

    def bulk_delete(self, entities_id):
        self._validate()
        return self.http_post_json(self.entity_endpoint_base_url + '_bulk-delete', entities_id)
