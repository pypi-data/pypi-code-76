from collections import namedtuple

from .util import serialize

ServiceResponse = namedtuple('ServiceResult', ['success', 'status', 'data', 'message',
                                               'trace', 'need_data'])


def success_response(message=''):
    return ServiceResponse(success=True, status='success', data=None, message=message,
                           trace='', need_data=False)


def success_response_with_data(data=None, message=''):
    return ServiceResponse(success=True, status='success', data=data, message=message,
                           trace='', need_data=True)


def error_response(status='fail', message='', trace=''):
    return ServiceResponse(success=False, status=status, data=None, message=message,
                           trace=trace, need_data=False)


def error_response_with_data(status='fail', data=None, message='', trace='', data_key='data'):
    assert data_key != 'status'
    assert data_key != 'message'
    assert data_key != 'trace'
    return ServiceResponse(success=False, status=status, data=data, message=message,
                           trace=trace, need_data=True)


def format_service_response(response):
    if response.status == 'success':
        return _respond_success(response)
    if response.status == 'fail':
        return _respond_fail(response)
    return _respond_other(response)


def _respond_fail(response):
    return {
        'status': response.status,
        'message': response.message,
        'trace': response.trace
    }


def _respond_other(response):
    resp = {
        'status': response.status
    }
    _append_data(resp, response)
    if response.message:
        resp['message'] = response.message
    return resp


def _respond_success(response):
    resp = {
        'status': response.status
    }
    _append_data(resp, response)
    return resp


def _append_data(resp, response):
    if response.need_data:
        resp['data'] = serialize(response.data)
