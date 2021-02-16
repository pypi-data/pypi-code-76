# beepbeep.bq: google bigquery functions
from typing import Optional, Dict, Union, Any
import os
import json
from datetime import datetime
from google.cloud import bigquery


def stream_json_into_bq_with_id(id_string: str, json_string: str, destination_ref: str) -> dict:
    """
    Streams a JSON string as text into a single row in a three column (all string) BigQuery table for subsequent decoding, with the following schema:
    
    
    Args:   
        id_string (string): row identifier
        json_string (string): data payload
        destination_ref (string): BigQuery table destination reference (project_id.dataset_id.table_name)
    
    Returns:
        A dict containing 
        status (string): "success" for successful stream, "error" for a failed stream or "fail" for other failure.
        message (string): Exception or error message if applicable
    """
    try:
        current_time = datetime.now()
        current_timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
        
        project_id = os.environ.get('GCP_PROJECT')
        BQ = bigquery.Client(project=project_id)

        table = BQ.get_table(destination_ref)

        rows_to_insert = [(id_string, json_string, current_timestamp)]

        errors = BQ.insert_rows(
            table, rows_to_insert, row_ids=[None] * len(rows_to_insert)
        )

        stream_log: dict # Union[str, dict] 
        if len(errors) == 0:
            stream_log = {"status": "success", "message": None}
        else:
            error_string = json.dumps(errors)
            stream_log = {"status": "error", "message": error_string}

    except Exception as e:
        stream_log = {"status": "fail", "message": e}
    
    return stream_log