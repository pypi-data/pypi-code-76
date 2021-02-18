import sys

from collections import OrderedDict
from datalake_scripts.common.base_script import BaseScripts
from datalake_scripts.common.logger import logger
from datalake_scripts.engines.get_engine import Threats
from datalake_scripts.helper_scripts.output_builder import CsvBuilder


def main(override_args=None):
    """Method to start the script"""
    starter = BaseScripts()

    # Load initial args
    parser = starter.start('Submit a new threat to Datalake from a file')
    required_named = parser.add_argument_group('required arguments')
    # required_named.add_argument(
    #     'query_hash',
    #     help='the query hash from which to retrieve the response hashkeys',
    #     required=True
    # )

    logger.debug(f'START: as_misp_threat.py')

    if override_args:
        args = parser.parse_args(override_args)
    else:
        args = parser.parse_args()

    # Load api_endpoints and tokens
    endpoint_config, main_url, tokens = starter.load_config(args)
    threats_engine = Threats(endpoint_config, args.env, tokens)
    response_dict = threats_engine.get_threats(
        '8671d099a2eabeb3e634732d204f0efa',
        limit=1,
        response_format='application/x-misp+json',
    )
    print(response_dict)


if __name__ == '__main__':
    sys.exit(main())
