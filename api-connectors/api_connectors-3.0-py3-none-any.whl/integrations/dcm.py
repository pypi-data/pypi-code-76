import io
import random
import time
from datetime import datetime
from typing import List

from apiclient import http

from api_connectors.integrations.google_base import GoogleBase


class DFAReportingAPI(GoogleBase):
    """ Doubleclick Campaign Manager API
        :arg credentials:

        Documentation: https://developers.google.com/doubleclick-advertisers/rest/v3.4
    """
    resource_name = 'dfareporting'
    version = 'v3.4'

    def extract_profiles(self):
        return self.client.userProfiles().list().execute()['items']

    def get_ads(self, profile_id: str):
        """ Get all ads """
        request = self.client.ads().list(profileId=profile_id, active=True)

        while True:
            # Execute request and print response.
            response = request.execute()
            yield from response['ads']
            if response['ads'] and response['nextPageToken']:
                request = self.client.ads().list_next(request, response)
            else:
                break

    def construct_report(self,
                         profile_id: str,
                         start_date: datetime,
                         end_date: datetime,
                         metrics: List[str],
                         dimensions: List[dict]):
        # 1. Create a report resource.
        start_day = start_date.strftime('%Y-%m-%d')
        end_day = end_date.strftime('%Y-%m-%d')
        report = {
            # Set the required fields "name" and "type".
            'name': f'Get{profile_id}:{start_day}->{end_day}',
            'type': 'STANDARD',
            # Set optional fields.
            'format': 'CSV'
        }

        # 2. Define the report criteria.
        criteria = {
            'dateRange': {
                'startDate': start_day,
                'endDate': end_day
            },
            'dimensions': dimensions,
            'metricNames': metrics
        }

        # Add the criteria to the report resource.
        report['criteria'] = criteria

        # 3. (optional) Look up compatible fields.
        # self.find_compatible_fields(profile_id, report)

        # 4. Add dimension filters to the report criteria.
        self.add_dimension_filters(profile_id, report)

        # 5. Save the report resource.
        report = self.insert_report_resource(profile_id, report)

        # Run the report.
        report_file = self.client.reports().run(profileId=profile_id, reportId=report['id']).execute()

        # Wait for the report file to finish processing.
        # An exponential backoff strategy is used to conserve request quota.
        sleep = 0
        start_time = time.time()
        while True:
            report_file = self.client.files().get(reportId=report['id'],
                                                  fileId=report_file['id']).execute()

            status = report_file['status']
            if status == 'REPORT_AVAILABLE':
                print('File status is %s, ready to download.' % status)
                break
            elif status != 'PROCESSING':
                raise Exception('File status is %s, processing failed.' % status)
            elif time.time() - start_time > MAX_RETRY_ELAPSED_TIME:
                raise Exception('File processing deadline exceeded.')

            sleep = next_sleep_interval(sleep)
            print('File status is %s, sleeping for %d seconds.' % (status, sleep))
            time.sleep(sleep)

        request = self.client.files().get_media(reportId=report['id'], fileId=report_file['id'])
        out_file = io.BytesIO()

        # Chunk size to use when downloading report files. Defaults to 32MB.
        CHUNK_SIZE = 32 * 1024 * 1024
        downloader = http.MediaIoBaseDownload(out_file, request, chunksize=CHUNK_SIZE)

        # Execute the get request and download the file.
        download_finished = False
        while download_finished is False:
            _, download_finished = downloader.next_chunk()

        report_data = self.ReportFile(out_file.getvalue())
        return report_data

    class ReportFile:
        def __init__(self, initial_report: bytes):
            self.full = initial_report.decode('utf-8')
            self.head, body_csv = self.full.split('Report Fields', maxsplit=1)
            self.csv, self.overall = body_csv.strip().rsplit('\n', maxsplit=1)

    def find_compatible_fields(self, profile_id, report):
        """Finds and adds a compatible dimension/metric to the report."""
        fields = self.client.reports().compatibleFields().query(
            profileId=profile_id, body=report
        ).execute()

        report_fields = fields['reportCompatibleFields']

        if report_fields['dimensions']:
            # Add a compatible dimension to the report.
            report['criteria']['dimensions'].append({
                'name': report_fields['dimensions'][0]['name']
            })
        elif report_fields['metrics']:
            # Add a compatible metric to the report.
            report['criteria']['metricNames'].append(
                report_fields['metrics'][0]['name'])

        print('Updated report criteria (with compatible fields):\n%s' %
              report['criteria'])

    def add_dimension_filters(self, profile_id, report):
        """Finds and adds a valid dimension filter to the report."""
        # Query advertiser dimension values for report run dates.
        request = {
            'dimensionName': 'dfa:advertiser',
            'endDate': report['criteria']['dateRange']['endDate'],
            'startDate': report['criteria']['dateRange']['startDate']
        }

        values = self.client.dimensionValues().query(
            profileId=profile_id, body=request
        ).execute()

        if values['items']:
            # Add a value as a filter to the report criteria.
            report['criteria']['dimensionFilters'] = [values['items'][0]]

        print('\nUpdated report criteria (with valid dimension filters):\n%s' %
              report['criteria'])

    def insert_report_resource(self, profile_id, report):
        """Inserts the report."""
        inserted_report = self.client.reports().insert(
            profileId=profile_id, body=report).execute()

        print('\nSuccessfully inserted new report with ID %s.' %
              inserted_report['id'])

        return inserted_report


# The following values control retry behavior while the report is processing.
# Minimum amount of time between polling requests. Defaults to 10 seconds.
MIN_RETRY_INTERVAL = 10
# Maximum amount of time between polling requests. Defaults to 10 minutes.
MAX_RETRY_INTERVAL = 10 * 60
# Maximum amount of time to spend polling. Defaults to 1 hour.
MAX_RETRY_ELAPSED_TIME = 60 * 60


def next_sleep_interval(previous_sleep_interval):
    """Calculates the next sleep interval based on the previous."""
    min_interval = previous_sleep_interval or MIN_RETRY_INTERVAL
    max_interval = previous_sleep_interval * 3 or MIN_RETRY_INTERVAL
    return min(MAX_RETRY_INTERVAL, random.randint(min_interval, max_interval))
