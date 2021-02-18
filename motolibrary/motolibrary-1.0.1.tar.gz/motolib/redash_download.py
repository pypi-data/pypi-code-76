# down_redash.py
# Dependencies - requests, pandas

import os
import requests
import time
import pandas as pd
import datetime
from customsol_pkg.errors import RedashAPIError

def redash_download(query_id, api_key, region, file_name, params={}):
    """
    -------------------------------------------------------
    Download query response to local dir as file_name
    -------------------------------------------------------
    Parameters:
        query_id : string
            ID of Redash Query
        api_key : string
            User API key
        region : string
            Country for Redash (ie. CA or US)
        file_name : string
            File will be downloaded and saved locally as csv with this name
            !! NO EXTENSION !!
        params : Dictionary
            (Optional) Dictionary of query params -- Default = {} (empty)

    Raises:
        ValueError: Region code is Invalid
        RedashAPIError: Unable to connect to Redash API or requested query
    ------------------------------------------------------
    """

    # Create request header using provided API key
    header = {'Authorization': f'Key {api_key}'}

    # Use provided region to generate a job url and pass param
    job_url = ''
    pass_param = ''
    redash_csv = ''

    if region.lower() == 'ca':
        job_url = 'https://redash.motocommerce.ca/api/jobs/{}'
        pass_param = f'https://redash.motocommerce.ca/api/queries/{query_id}/refresh'
        redash_csv = f'https://redash.motocommerce.ca/api/queries/{query_id}/results.csv?api_key={api_key}'

    elif region.lower() == 'us' or region.lower() == 'usa':
        job_url = 'https://redash.motocommerce.com/api/jobs/{}'
        pass_param = f'https://redash.motocommerce.com/api/queries/{query_id}/refresh'
        redash_csv = f'https://redash.motocommerce.com/api/queries/{query_id}/results.csv?api_key={api_key}'

    else:
        raise ValueError('Invalid region code passed. Use CA for Canada and US for USA.')

    # Download data from Redash query


    print(f'Exporting Query - ID: {query_id}...')

    # Set Up Requests Object
    s = requests.Session()
    s.headers.update(header)
    print('Fetching report using Redash API...')
    # Post the Refresh with the New Parameters
    response = s.post(pass_param, params=params)
    print(f'Redash Response Status Code: {response.status_code}')

    if response.status_code == 404:
        raise RedashAPIError('Invalid API Key')

    if response.status_code == 400:
        raise RedashAPIError('Invalid Query ID')

    # Wait for Refresh Job to Complete
    job = response.json()['job']

    while job['status'] not in (3, 4):
        response = s.get(job_url.format(job['id']))
        job = response.json()['job']
        time.sleep(1)

    if job['status'] == 3:
        param_id = job['query_result_id']
    else:
        param_id = None

    # Return Updated Query
    response = s.get(redash_csv.format(param_id))

    # Export data to .csv file
    text_file = open(str(file_name + '.csv'), 'w', newline='', encoding='utf-8')
    n = text_file.write(response.text)
    text_file.close()

    print(f'Downloaded {file_name}\n')

    return
