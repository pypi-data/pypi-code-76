# beepbeep.fb: facebook graph api functions
from typing import Any, Dict, List, Union
import requests
from datetime import datetime


def debug_access_token(access_token: str) -> Union[dict, Any]:
    """
    Request API Endpoint: https://graph.facebook.com/debug_token?input_token={input-token}&access_token={valid-access-token}.
    
    Parameters:
        access_token (str): The Access Token that is being inspected. This parameter must be specified.

    Returns:
        A object containg:
        if data then return:
        data (dict) : Metadata about a given access token. This includes data such as the user for which the token was issued, 
        whether the token is still valid, when it expires, and what permissions the app has for the given user.

        otherwise it returns:
        error (dict) : Describing the type of error
    """

    debug_url = f"https://graph.facebook.com/debug_token?input_token={access_token}&access_token={access_token}"
    response = requests.get(debug_url)

    return response.json()


def get_token_expiry_dates(debug_response: dict) -> dict:
    """Get metadata that includes: 'issued_at', 'data_access_expires_at and expires_at.
    

    Parameters:
        debug_response (dict): An object containing metadata about a given access token.

    Returns:
        A object containg:
        if data then return:
        data (dict) : 'issued_at', 'data_access_expires_at and expires_at

        otherwise it returns:
        error (dict) : Describing the type of error
    """

    token_dates = {}
    try:
        if debug_response.get('error') is not None:
            print("Something went wrong:\n", debug_response['error']['message'])
            token_dates['Error'] = debug_response['error'].get('message')
        else:
            # Avoid KeyError by using get() function to access the key value. If the key is missing, None is returned
            if debug_response['data'].get('issued_at') is not None:
                token_dates['issued_at'] = datetime.fromtimestamp(debug_response['data'].get('issued_at')).strftime("%m/%d/%Y, %H:%M:%S")
            else:
                token_dates['issued_at'] = debug_response['data'].get('issued_at')

            if debug_response['data'].get('data_access_expires_at') is not None:
                token_dates['data_access_expires_at'] = datetime.fromtimestamp(debug_response['data'].get('data_access_expires_at')).strftime("%m/%d/%Y, %H:%M:%S")
            else:
                token_dates['data_access_expires_at'] = debug_response['data'].get('data_access_expires_at')
            
            if debug_response['data'].get('expires_at') is not None:
                token_dates['expires_at'] = datetime.fromtimestamp(debug_response['data'].get('expires_at')).strftime("%m/%d/%Y, %H:%M:%S")
            else:
                token_dates['expires_at'] = debug_response['data'].get('expires_at')
    except Exception as e:
        print(e)

    return token_dates


def exchange_token(api_version: str, client_id: str, client_secret: str, access_token: str) -> Union[dict, Any]:
    """
    Function to exchange short live token.


    Request API Endpoint =  https://graph.facebook.com/{graph-api-version}/oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={your-access-token}
    
    Parameters:
        api_version (str) : Graph API version e.g: v8.0, v9.0.
        client_id (str) : Unique App ID for your app.
        client_secret (str) : The App Secret.
        access_token (str) : The Access Token that is being inspected to exchange it for a long live token.
    
    Returns: 
        An object containing:
            # Here details of the object results...
    """
    exchange_url =  f"https://graph.facebook.com/{api_version}/oauth/access_token?grant_type=fb_exchange_token&client_id={client_id}&client_secret={client_secret}&fb_exchange_token={access_token}"
    response = requests.get(exchange_url)
    
    return response.json()


def get_valid_insights_metrics(media_type: str) -> list:
    """
    Get the total number of people who liked your Page or the number of people who shared stories about your Page.

    Parameters:
        media_type (str) : Media type attribute
    
    Returns: 
        A list of multiple metrics
    """

    all_field_parameters = {"IMAGE": ['engagement', 'impressions', 'reach', 'saved'],
                            "VIDEO": ['engagement', 'impressions', 'reach', 'saved', 'video_views'],
                            "CAROUSEL_ALBUM": ['carousel_album_engagement', 'carousel_album_impressions', 'carousel_album_reach', 'carousel_album_saved'],
                            "STORY": ['exits', 'impressions', 'reach', 'replies', 'taps_forward', 'taps_back']
                            }
    valid_metrics = all_field_parameters[media_type]
    
    return valid_metrics


def get_media_objects(api_version: str, ig_user_id: str, fields_list: list, access_token: str) -> Union[dict, Any]:
    """
    This function makes a request to the API Endpoint:
        https://graph.facebook.com/{graph-api-version}/{ig-user-id}/media?fields={fields}&access_token={access-token}


    Parameters:
        api_version (str) : Graph API version e.g: v8.0, v9.0.
        ig_user_id (str) : Instagram User ID Represents an Instagram Business Account or an Instagram Creator Account.
        fields_list (list) : {fields_list} A comma-separated list of Fields you want returned.
        access_token (str) : The app user's User Access Token. This parameter must be specified.
    
    Returns: 
        An object containing:
             "id", "media_type", "media_url" ...
        otherwise it returns:
        error (dict) : Describing the type of error
    """

    # Method join return a string.
    # So then fields_list argument would not be change of type list to str.
    if type(fields_list) == list:
        fields = ','.join(fields_list)  
    
    media_objects_url = f"https://graph.facebook.com/{api_version}/{ig_user_id}/media?fields={fields}&access_token={access_token}"
    #print('media_objects request:', media_objects_url)

    response = requests.get(media_objects_url)
    
    return response.json()


def get_media_insights (api_version: str, ig_media_id: str, metrics_list: list, access_token: str) -> Union[dict, Any]:
    """
    This function makes a request to the API Endpoint:
        https://graph.facebook.com/v9.0/{ig-media-id}/insights?metric={metrics}&access_token={access-token}


    Parameters:
        api_version (str) : Graph API version e.g: v8.0, v9.0.
        ig_media_id (str) : Instagram Media ID Represents and Instagram photo, video, story, or album.
        metrics_list (list) : {metrics} A comma-separated list of Metrics you want returned.
        access_token (str) : The app user's User Access Token. This parameter must be specified.
    
    Returns: 
        An object containing:
             'photo', 'video', 'story', 'album'
        otherwise it returns:
        error (dict) : Describing the type of error
    """
    
    # Method join return a string.
    # So then fields_list argument would not be change of type list to str.
    if type(metrics_list) == list:
        metrics = ','.join(metrics_list)

    media_insights_url = f"https://graph.facebook.com/{api_version}/{ig_media_id}/insights?metric={metrics}&access_token={access_token}"
    #print('media_insights request:', media_insights_url)
    response = requests.get(media_insights_url)
    
    return response.json()


def get_user_insights (
        api_version: str, 
        ig_user_id: str, 
        metrics_list: list, 
        period: str, 
        since: str, 
        until: str, 
        access_token: str) -> Union[dict, Any]:
    """
    This function makes a request to the API Endpoint:
        https://graph.facebook.com/v9.0/{ig-user-id}/insights?metric={metric}&period={period}&since={since}&until={until}&access_token={access-token}


    Parameters:
        api_version (str) : Graph API version e.g: v8.0, v9.0.
        ig_user_id (str) : Instagram User ID Represents an Instagram Business Account or an Instagram Creator Account.
        metrics_list (list) : {metric} A comma-separated list of Metrics you want returned. If requesting multiple metrics, 
            they must all have the same compatible Period.
        period (str) : {period} A Period that is compatible with the metrics you are requesting.
        since (str) : Unix timestamp - Used in conjunction with {until} to define a Range. If you omit since and until, 
            the API defaults to a 2 day range: yesterday through today.
        until (str) : Unix timestamp - Used in conjunction with {since} to define a Range. If you omit since and until, 
            the API defaults to a 2 day range: yesterday through today.
        access_token (str) : The app user's User Access Token. This parameter must be specified.
    
    Returns: 
        An object containing:
             'photo', 'video', 'story', 'album'
        otherwise it returns:
        error (dict) : Describing the type of error
    """

    if type(metrics_list) == list:
        metrics = ','.join(metrics_list)

    user_insights_url = f"https://graph.facebook.com/v9.0/{ig_user_id}/insights?metric={metrics}&period={period}&since={since}&until={until}&access_token={access_token}"
    #print('user_insights_url request:', user_insights_url)
    response = requests.get(user_insights_url)
    
    return response.json()


if __name__ == '__main__':
    #def type_hint_test():
    # *********************** TYPE HINT *************************
    result_debug_access_token = debug_access_token("EAAKBaHr9LcEBAGv2hKfqlc34Kpp3joWP7SnJgyRmU0F9gxifdJ9mmWeZCuQ1pwbmeAZBbSEF0yBCmcJK1MZAKBMzGSsTgCsv67rmCa3deKaVd4FBCqtGE5RrBP22GlKb6ZAPnTESqeZAofBEGZCvEIl6qZBrZBvDvFHlM5BIyaQUWTQF7VVq1dVZCnBjLwtBMD5JTgvyZBBOclxZAxcjfqjWnuE")
    print(type(result_debug_access_token))

    result_get_token_expiry_dates = get_token_expiry_dates(result_debug_access_token)
    print(type(result_get_token_expiry_dates))
    print(result_get_token_expiry_dates)

    result_exchange_token = exchange_token('api_version', 'client_id', 'client_secret', 'access_token')
    print(type(result_exchange_token))
    print(result_exchange_token)

    media_type_list = ['IMAGE', 'VIDEO', 'CAROUSEL_ALBUM', 'STORY']
    result_get_valid_insights_metrics = get_valid_insights_metrics(media_type_list[1])
    print(type(result_get_valid_insights_metrics))
    print(result_get_valid_insights_metrics)

    get_media_objects_list = ['IMAGE', 'VIDEO', 'CAROUSEL_ALBUM', 'STORY']
    result_get_media_objects = get_media_objects('api_version', 'ig_user_id', get_media_objects_list, 'access_token')
    print(type(result_get_media_objects))
    print(result_get_media_objects)
        
    get_media_insights_list = ['photo', 'video', 'story', 'album']
    result_get_media_insights = get_media_insights('api_version', 'ig_media_id', get_media_insights_list, 'access_token')
    print(type(result_get_media_insights))
    print(result_get_media_insights)

    metrics_list = ['photo', 'video', 'story', 'album']
    result_get_user_insights = get_user_insights('api_version', 'ig_user_id', metrics_list, 'period', 'since', 'until', 'access_token')
    print(type(result_get_user_insights))
    print(result_get_user_insights)

    # **************************** Docstrings **************************
    print(debug_access_token.__doc__)
    print(get_token_expiry_dates.__doc__)
    print(exchange_token.__doc__)
    print(get_media_objects.__doc__)
    print(get_media_insights.__doc__)
    print(get_user_insights.__doc__)

        # mypy fb.py
    #type_hint_test()
    pass