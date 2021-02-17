import logging


def generate_response(response, to_return_key='value'):
    if response.ok:
        if to_return_key in response.json().keys():
            return (response.json()[to_return_key])
        elif 'message' in response.json().keys():
            return (response.json()['message'])
        else:
            return True
    else:
        if 'errors' in response.json().keys():
            logging.error("There was an error. Please, check the details below. \n {}".format(
                response.json()['errors']))
        else:
            logging.error("There was an error. Please, check the details below. \n {}".format(
                response.json()['message']))
        return None
