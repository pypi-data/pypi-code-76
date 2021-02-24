import pandas as pd
from db_connection import *
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


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
    # print('athena data test:', pd.read_sql(q_es, conn_es()))

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