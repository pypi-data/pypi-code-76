import json
import uuid
import base64
import requests
import webbrowser
from requests.auth import HTTPDigestAuth


class payUnit:
    """
    Initiates and processes payments
    """

    def __init__(self, data):
        self.config_data = data
        data_keys = list(data.keys())
        if data_keys.count('api_key') == 0:
            raise Exception('api_key not present')
        if data_keys.count('apiUsername') == 0:
            raise Exception('apiUsername not present')
        if data_keys.count('return_url') == 0:
            raise Exception('return_url not present')
        if data_keys.count('apiPassword') == 0:
            raise Exception('apiPassword not present')
        if data_keys.count('currency') == 0:
            raise Exception('currency not present')
        if data_keys.count('mode') == 0:
            raise Exception('sdk mode not present')
        if(data['mode'].lower() != "test" and data['mode'].lower() != "live"):
            raise Exception('Invalid sdk mode')

    def makePayment(self, amount):
        if(int(amount) <= 0):
            raise Exception("Invalid transaction amount")

        apiUsername = self.config_data["apiUsername"]
        apiPassword = str(self.config_data["apiPassword"])
        api_key = str(self.config_data["api_key"])
        auth = apiUsername+":"+apiPassword
        environment = str(self.config_data['mode'])
        base64AuthData = base64.b64encode((auth).encode()).decode()
  

        test_url = 'https://app.payunit.net/api/gateway/initialize'

        headers = {
            "x-api-key": str(api_key),
            "content-type": "application/json",
            "Authorization": "Basic " + str(base64AuthData),
            "mode": str(environment.lower()),
        }

        test_body = {
            "notify_url": str(self.config_data['notify_url']),
            "transaction_id":  str(uuid.uuid1()),
            "total_amount": str(amount),
            "return_url": str(self.config_data['return_url']),
            "purchaseRef": str(self.config_data['purchaseRef']),
            "description": str(self.config_data['description']),
            "name": str(self.config_data['name']),
            "currency": str(self.config_data['currency'])
        }

        try:
            response = requests.post(
                test_url, data=json.dumps(test_body), headers=headers)
            response = response.json()
            
            if(response['body']['status'] == 200):
                webbrowser.open(response['body']['transaction_url'])
                return {"message": "Successfylly initated Transaction", "status": True}
        except:
            return {"err_message": "an error occured, payment gateway could not be found, check your connection", "status": False}
