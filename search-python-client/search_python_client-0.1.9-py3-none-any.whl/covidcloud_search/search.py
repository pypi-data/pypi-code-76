import os
import requests

from typing import List, Union


def ga4gh_get_drs(
    id: str = '',
) -> Union[List[dict], dict, int]:
    
    """
    Get DRS from DNAstack's covidcloud
    
    :param id: DRS ID. Leave '' to get all drs data.

    :return:
        If statuscode 200: Json response/s in dict format
        If statuscode 400: Returns statuscode

    Example:
        id = '0000bee7-6e47-4e0c-b3e4-9e574eac508b'
        drs_data  = ga4gh_get_drs(id)
    """
    drs_url = 'https://drs.covidcloud.ca/ga4gh/drs/v1/objects/'
    extended_url = os.path.join(drs_url, id)
    response = requests.get(extended_url)
    
    if response.status_code == 200:
        if id:
            return response.json()['object']
        else:
            return response.json()['objects']
    
    else:
        return response.status_code
    

def ga4gh_search_db(
    query: str,
) -> Union[List[dict], int]:

    """
    Returns list formatted ga4gh search response from a url and query

    :param query: SQL query
    
    :return: 
        If statuscode 200: Json response/s in dict format
        If statuscode 400: Returns statuscode

    Example:
        query = 'SELECT * FROM coronavirus_dnastack_curated.covid_cloud_production.sequences_view LIMIT 1000'
        meta_data  = ga4gh_search_db(query)

    """

    search_url = 'https://ga4gh-search-adapter-presto-covid19-public.prod.dnastack.com/search'
    response = requests.post(search_url, json={'query': query})
    
    if response.status_code == 200:
        response_url = response.json()['pagination']

        data = []
        while response_url:
            response = requests.get(response_url['next_page_url'])
            
            if response.status_code == 200:
                data += response.json()['data']
                response_url = response.json()['pagination']
            
            else:
                return response.status_code

        return data
    
    else:
        return response.status_code
