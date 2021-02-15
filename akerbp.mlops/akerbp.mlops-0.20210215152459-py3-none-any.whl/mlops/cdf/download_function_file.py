# download_function_file.py

import os

from akerbp.mlops.cdf.helpers import download_file, set_up_cdf_client 


if __name__ == "__main__":
    """
    Read env vars and call the download file function
    """
    
    id = int(os.environ['FUNCTION_FILE_ID'])
    
    set_up_cdf_client()
    download_file(dict(id=id), f'./{id}.zip')