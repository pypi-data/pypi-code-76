import requests
from dukeai.config import base_url


def get_token(username, password):
    url = "https://api.duke.ai/token/get_token"

    headers = {
              'username': username.upper(),
              'password': password
             }

    response = requests.request("GET", url, headers=headers)

    return response.json


def get_tax_info(cust_id, token, tax_info):
    url = base_url + f'/{cust_id}/tax_info/{tax_info}'

    headers = {
                'Authorization': token
              }
    response = requests.request("GET", url, headers=headers)

    return response.text


def update_tax_info(cust_id, token, tax_info, payload):
    """
            payload =   {
                          "Filling_Status": "string",
                          "Pre_tax_deduction": {
                            "status": true,
                            "amount": 0
                          },
                          "Tax_credit": {
                            "status": true,
                            "amount": 0
                          },
                          "Standard_Deduction": {
                            "status": true
                          },
                          "Itemize_Deduction": {
                            "status": true,
                            "amount": 0
                          },
                          "Other_Income": 0
                        }
    """

    url = base_url + f'/{cust_id}/tax_info/{tax_info}'

    headers = {
               'Authorization': token,
               'Content-Type': 'application/json'
              }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


def get_ifta_trip_id(cust_id, token):

    url = base_url + f'/{cust_id}/ifta'

    headers = {
                'Authorization': token
              }

    response = requests.request("GET", url, headers=headers)

    return response.text


def send_ifta_data(cust_id, token):
    """
    payload = {
                  "positionList": [
                    {
                      "timestamp": "string",
                      "state": "string",
                      "longitude": "string",
                      "latitude": "string"
                    }
                  ],
                  "tripId": "c9c3cf65-e8fd-42b1-b600-a09bf2bf8838",
                  "status": "new"
                }
    """
    url = base_url + f'/{cust_id}/ifta'

    headers = {
                'Authorization': token,
                'Content-Type': 'application/json'
              }

    response = requests.request("POST", url, headers=headers)

    return response.text
