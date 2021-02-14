import hmac

import requests


class BamboraPayformClient:
    API_VERSION = 'w3.1'
    BASE_URL = 'https://payform.bambora.com/pbwapi'

    def __init__(self, api_key, private_key):
        self.api_key = api_key
        self.private_key = private_key

    def get_token(self, order_number=None, amount=None, email=None, callback_url=None):
        authcode_input = '|'.join([self.api_key, order_number])
        payload = {
            'version': self.API_VERSION,
            'api_key': self.api_key,
            'order_number': order_number,
            'amount': amount,
            'currency': 'EUR',
            'email': email,
            'payment_method': {
                'type': 'e-payment',
                'return_url': callback_url,
                'notify_url': callback_url,
            },
            'authcode': self._authcode(authcode_input),
        }

        r = requests.post('{}/auth_payment'.format(self.BASE_URL), json=payload)
        data = r.json()

        if data.get('result') != 0:
            raise Exception('Token request failed with code {}: {}'.format(data.get('result'), data.get('errors')))

        return data.get('token')

    def get_payment_methods(self):
        payload = {
            'version': '2',
            'api_key': self.api_key,
            'currency': 'EUR',
            'authcode': self._authcode(self.api_key),
        }

        r = requests.post('{}/merchant_payment_methods'.format(self.BASE_URL), json=payload)
        # TODO: Check for errors and throw

        return r.json()

    def payment_url(self, token):
        return '{}/token/{}'.format(self.BASE_URL, token)

    def validate_callback_request(self, request):
        return_code = request.GET.get('RETURN_CODE')
        order_number = request.GET.get('ORDER_NUMBER')
        settled = request.GET.get('SETTLED')
        incident_id = request.GET.get('INCIDENT_ID')
        authcode = request.GET.get('AUTHCODE')

        authcode_parts = [return_code, order_number]
        if settled is not None:
            authcode_parts.append(settled)

        if incident_id is not None:
            authcode_parts.append(incident_id)

        authcode_input = '|'.join(authcode_parts)
        if authcode != self._authcode(authcode_input):
            return False

        return True

    def _authcode(self, input):
        return hmac.new(
            self.private_key.encode('utf8'),
            input.encode('utf8'),
            digestmod='sha256'
        ).hexdigest().upper()
