import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
from clickhouse_driver import Client
from pyathenajdbc import connect as athena_connect
from elasticsearch import Elasticsearch
from sshtunnel import SSHTunnelForwarder
import pymysql

# import config of credentials from local file
import sys
sys.path.append('/Users/jinghanma/Helium10/utility_jma/util_config') # user needs to change the path to their own path
from oauth_config import *


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def conn_db(db_server, db_type='PostgreSQL', db_name=None):
    """

    :param db_server: {'h10_maindb',
                       'market_tracker',
                       'profit_s0',
                       'profit_s1',
                       'ppc',
                       'mws',
                       'cerebro',
                       'us_cluster',
                       'non_us_cluster',
                       'back_office'}, str
    :param db_type: {'PostgreSQL', 'MySQL'}, str, default='PostgreSQL'
    :param db_name: {'profits_shard_1','profits_shard_2',...,'profits_shard_16'}, str
                    specify database shard for profits_s1
    :return: database connector
    """
    server = oauth_db()[db_server]
    host = server['hostname']
    port = server['port']
    user = server['username']
    pwd = server['password']

    if not db_name:
        dbname = server['dbname']
    else:
        dbname = db_name

    if db_type == 'PostgreSQL':
        engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(user,
                                                                    pwd,
                                                                    host,
                                                                    port,
                                                                    dbname))
    elif db_type == 'MySQL':
        engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(user,
                                                                       pwd,
                                                                       host,
                                                                       port,
                                                                       dbname))
    else:
        print('Database type is not PostgreSQL nor MySQL')

    return engine.connect()


def conn_mysqlssh(server_name, query):
    """
    :param server_name: {'portals', 'followups'}, str
    :param query: str
    :return: query result in pandas DataFrame
    """
    server = oauth_mysql_ssh()[server_name]
    ssh_host = server['ssh_host']
    ssh_user = server['ssh_user']
    ssh_port = server['ssh_port']

    sql_hostname = server['sql_hostname']
    sql_username = server['sql_username']
    sql_password = server['sql_password']
    sql_database = server['sql_main_database']
    sql_port = server['sql_port']

    with SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_pkey="/Users/jinghanma/.ssh/id_rsa",
            remote_bind_address=(sql_hostname, sql_port)) as tunnel:

        conn = pymysql.connect(host='127.0.0.1',
                               user=sql_username,
                               passwd=sql_password,
                               db=sql_database,
                               port=tunnel.local_bind_port)
        data = pd.read_sql(query, conn)
    return data


def conn_clickhouse(cluster_name, settings=None):
    """
    :param cluster_name: {'kt', 'phrases', 'us_cluster', 'non_us_cluster'}, str
    :return: database connector
    """
    server = oauth_clickhouse()[cluster_name]
    host = server['hostname']
    port = server['port']
    user = server['username']
    pwd = server['password']
    db = server['dbname']

    if not settings:
        client = Client(host=host,
                        port=port,
                        user=user,
                        password=pwd,
                        database=db)
    else:
        client = Client(host=host,
                        port=port,
                        user=user,
                        password=pwd,
                        database=db,
                        settings=settings)
    return client


def conn_snowflake(cluster_name='om_sample'):
    """
    :param cluster_name: {'om_sample'}, str
    :return: database connector
    """
    server = oauth_snowflake()[cluster_name]
    account = server['accountname']
    user = server['username']
    pwd = server['password']
    warehouse = server['warehousename']
    db = server['dbname']
    schema = server['schemaname']
    curr_role = server['rolename']

    engine = create_engine(URL(
        account=account,
        user=user,
        password=pwd,
        database=db,
        schema=schema,
        warehouse=warehouse,
        role=curr_role
    ))

    return engine.connect()


def conn_athena():
    """
    :param db_name
    :return: athena connector
    """
    tool = oauth_aws()['athena']
    region = tool['region']
    user = tool['username']
    pwd = tool['password']
    output_location = tool['S3OutputLocation']
    driver = tool['driver_path']

    conn = athena_connect(User=user,
                          Password=pwd,
                          S3OutputLocation=output_location,
                          AwsRegion=region,
                          driver_path=driver)

    return conn


def conn_es():
    pass


if __name__ == "__main__":
    pass
    #################### test PostgreSQL  #########################

    # q_h10 = """
    #     select *
    #     from
    #         "StripeSubscription"
    #     limit 10
    #     """
    #
    # print('h10_maindb result:\n', pd.read_sql(q_h10, conn_db('h10_maindb')))
    #
    # q_mt = """
    #     select *
    #     from
    #         "Market"
    #     limit 10
    #     """
    #
    # print('market-tracker result:\n', pd.read_sql(q_mt, conn_db('market_tracker')))
    #
    # q_p0 = """
    #     select *
    #     from
    #         "MonthlySales"
    #     limit 10
    #     """
    #
    # print('profits0 result:\n', pd.read_sql(q_p0, conn_db('profit_s0')))
    #
    # q_p1 = """
    #     select *
    #     from
    #         "AmzOrderItem"
    #     limit 10
    #     """
    #
    # print('profits1 result:\n', pd.read_sql(q_p1, conn_db('profit_s1', db_name='profits_shard_9')))
    #
    # q_ppc = """
    #     select *
    #     from
    #         "campaign"
    #     limit 10
    #     """
    #
    # print('ADS ppc result:\n', pd.read_sql(q_ppc, conn_db('ppc')))
    # 
    # q_ads = """
    #     select *
    #     from
    #         "agency_subscription_metrics"
    #     limit 10
    #     """
    #
    # print('Prestozon ADS Internal-analytics result:\n', pd.read_sql(q_ads, conn_db('ads')))
    #
    # q_mws = """
    #     select *
    #     from
    #         "MwsListing"
    #     limit 10
    #     """
    #
    # print('MWS-listing result:\n', pd.read_sql(q_mws, conn_db('mws')))



    #################### test MySQL  #########################
    # q_bo = """
    #     select *
    #     from
    #         crushit
    #     limit 10
    #     """
    #
    # print('back-office result:\n', pd.read_sql(q_bo, conn_db('back_office', db_type='MySQL')))


    #################### test ClickHouse  #########################
    # q_ch = """
    #     show tables
    #     """
    # print('click house KT cluster tables:', conn_clickhouse('kt').execute(q_ch))
    # print('\n\nclick house Phrases cluster tables:', conn_clickhouse('kt').execute(q_ch))
    # print('\n\nclick house us cluster tables:', conn_clickhouse('us_cluster').execute(q_ch))
    # print('\n\nclick house non-us cluster tables:', conn_clickhouse('non_us_cluster').execute(q_ch))


    #################### test Snowflake  #########################
    # q_snow = """
    #     show tables
    #     """
    # print('snowflake ordermetrics tables:', pd.read_sql(q_snow, conn_snowflake()))
    # print('snowflake helium10 tables:', pd.read_sql(q_snow, conn_snowflake()))


    #################### test Snowflake  #########################
    # q_athena = """
    #     select * from "segment-logs"."mobile_output" limit 10
    #     """
    # print('athena data test:', pd.read_sql(q_athena, conn_athena()))


    #################### test Elasticsearch  #########################
    # q_es = """
    #     select * from "segment-logs"."mobile_output" limit 10
    #     """
    # print('athena data test:', pd.read_sql(q_athena, conn_athena()))

    #################### test ssh MySQL portals  #########################
    # q_portals = """
    #     select * from campaign.H10KP_ClickThroughRate limit 10
    #     """
    # print('ssh mysql Portals test:\n\n', conn_mysqlssh('portals', q_portals))

    #################### test ssh MySQL followups  #########################
    # q_followups = """
    #     select * from followup.H10KP_TotalDailyCustomer limit 10
    #     """
    # print('ssh mysql Portals test:\n', conn_mysqlssh('followups', q_followups))
