import sys
from google.cloud import bigquery

TB = 1099511627776      # 1 TB
PRICING_ON_DEMAND = 5   # $5.00 per TB

class Estimator():
    def __init__(self):
        self.__client = bigquery.Client()
        self.__job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)

    def check(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                query = f.read()

            query_job = self.__client.query(
                query,
                job_config=self.__job_config,
            )

            dollar = query_job.total_bytes_processed / TB * PRICING_ON_DEMAND

            return {
                "total_bytes_processed": query_job.total_bytes_processed,
                "doller": str(dollar),
            }

        except Exception as e:
            raise e

# if __name__ == '__main__':
#     if len(sys.argv) == 2:
#         estimation = Estimation()
#         response = estimation.calc(sys.argv[1])
#         print(response)
#     else:
#         print('Please set a argument: sql-file')
