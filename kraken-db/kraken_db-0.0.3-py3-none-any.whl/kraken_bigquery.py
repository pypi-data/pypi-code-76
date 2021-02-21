from google.cloud import bigquery
import datetime
import json


class Bigquery:

    def get(self):
    
        # Construct a BigQuery client object.
        client = bigquery.Client()

        query = """
            SELECT record_type, COUNT(record_type) as total_record, MAX(createdDate) as last_updated 
            FROM `kraken-v1.kraken.schema_records`
            GROUP BY record_type
            ORDER BY total_record DESC
            LIMIT 20
        """
        query_job = client.query(query)  # Make an API request.

        records = []

        for row in query_job:
            record = {}
            record['record_type'] = row['record_type']
            record['count'] = row['total_record']
            record['last_updated'] = row['last_updated']
            records.append(record)

        return json.dumps(records, default=str)




    def post(self, record_type, record_id, schema_name, schema_email, schema_url, created_date):

        # Construct a BigQuery client object.
        client = bigquery.Client()

        # TODO(developer): Set table_id to the ID of the model to fetch.
        table_id = "kraken-v1.kraken.kraken_record"

        table = client.get_table(table_id)  # Make an API request.

        rows_to_insert = [(record_type, record_id, schema_name, schema_email, schema_url, created_date)]


        errors = client.insert_rows(table, rows_to_insert)  # Make an API request.
        if errors == []:
            print("New rows have been added.")
        else:
            print("Error")
