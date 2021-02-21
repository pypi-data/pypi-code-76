import json
import os
import sqlite3
import pprint
import psycopg2
import psycopg2.extras
import traceback
import sys
import logging

import pytz
from fk.utils import *
from pprint import pformat

logger = logging.getLogger(__name__)


class DatabaseConnection:

    # Global connection
    connection_instance = None

    def __init__(self, config):
        self.config = config
        self.db_hostname = self.config.get("db-hostname", None)
        self.db_port = self.config.get("db-port", None)
        self.db_username = self.config.get("db-username", None)
        self.db_password = self.config.get("db-password", None)
        self.db_database = self.config.get("db-database", None)
        self.db = None
        self.connstr = f"postgres://{self.db_username}:{redact(self.db_password)}@{self.db_hostname}:{self.db_port}/{self.db_database}"
        logger.info(f"DATABASE: {self.connstr}")
        self.connection_error = None
        self._prepare_db()

    def __del____(self):
        self._unprepare_db()

    def is_ok(self):
        return self.db_hostname and self.db_port and self.db_username and self.db_password and self.db_database

    @staticmethod
    def get_connection(config):
        if not DatabaseConnection.connection_instance:
            DatabaseConnection.connection_instance = DatabaseConnection(config)
        return DatabaseConnection.connection_instance

    def _unprepare_db(self):
        if self.db:
            try:
                # Make sure data is stored
                self.db.commit()
                self.db.close()
            except Exception as e1:
                pass
            try:
                del self.db
            except Exception as e2:
                pass
            self.db = None
            logger.info("PostgreSQL connection is closed")

    # Internal helper to connect to database
    def _prepare_db(self):
        try:
            self.db = psycopg2.connect(host=self.db_hostname, port=self.db_port, user=self.db_username, password=self.db_password, database=self.db_database)

            # Create a cursor to let us work with the database
            with self.db:
                with self.db.cursor() as c:
                    # logger.info( self.db.get_dsn_parameters(),"\n")

                    c.execute("SELECT version();")
                    record = c.fetchone()
                    logger.info(f"Connected to: {record[0]}\n")
                    return True

        except (Exception, psycopg2.Error) as error:
            logger.warning("###   ###   ###   ###   ###   ###   ###   #")
            logger.warning("##   ###   ###   ###   ###   ###   ###   ##")
            logger.warning("")
            logger.warning(f"Error while connecting to PostgreSQL {error}")
            self.connection_error = error
            self._unprepare_db()
        return False

    def _query(self, query, data={}, mode="none"):
        cursor = None
        try:
            if not self.db:
                logger.warning("###   ###   ###   ###   ###   ###   ###   #")
                logger.warning("##   ###   ###   ###   ###   ###   ###   ##")
                logger.warning("")
                logger.warning("No database while making query")
                if self.connection_error:
                    logger.warning(f"Connection error was {self.connection_error}")
                else:
                    logger.warning("No connection error was set, did we even try to connect?")
            with self.db:
                with self.db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                    cursor.execute(query, data)
                    if mode == "many":
                        res = cursor.fetchall()
                        # Convert to real dictionaries
                        if res is None:
                            return None
                        out = []
                        for row in res:
                            out.append(dict(row))
                        return out
                    elif mode == "one":
                        res = cursor.fetchone()
                        if res is None:
                            return None
                        return dict(res)
                    elif mode == "exists":
                        res = cursor.fetchone()
                        return res is not None
                    else:
                        return
        except Exception as e:
            logger.error("")
            logger.error("")
            logger.error(f"###############################################")
            logger.error(f"#    Querying: {query}")
            if cursor and cursor.query:
                logger.error(f"#    Injected: {cursor.query.decode()}")
            logger.error(f"#         For: {mode}")
            logger.error(f"# Failed with:")
            if isinstance(e, psycopg2.InterfaceError):
                logger.error(f"# + Connection error({type(e).__name__}): e={e} ")
            elif isinstance(e, psycopg2.Error):
                logger.error(f"# + e={e} ({type(e).__name__})")
                logger.error(f"# + e.pgerror:{e.pgerror}")
                logger.error(f"# + e.pgcode: {e.pgcode}")
                logger.error(f"# + e.cursor: {e.cursor}")
                if e.diag:
                    logger.error(f"# + e.diag:")
                    logger.error(f"#   + column_name:             {e.diag.column_name}")
                    logger.error(f"#   + constraint_name:         {e.diag.constraint_name}")
                    logger.error(f"#   + context:                 {e.diag.context}")
                    logger.error(f"#   + datatype_name:           {e.diag.datatype_name}")
                    logger.error(f"#   + internal_position:       {e.diag.internal_position}")
                    logger.error(f"#   + internal_query:          {e.diag.internal_query}")
                    logger.error(f"#   + message_detail:          {e.diag.message_detail}")
                    logger.error(f"#   + message_hint:            {e.diag.message_hint}")
                    logger.error(f"#   + message_primary:         {e.diag.message_primary}")
                    logger.error(f"#   + schema_name:             {e.diag.schema_name}")
                    logger.error(f"#   + severity:                {e.diag.severity}")
                    logger.error(f"#   + source_file:             {e.diag.source_file}")
                    logger.error(f"#   + source_function:         {e.diag.source_function}")
                    logger.error(f"#   + source_line:             {e.diag.source_line}")
                    logger.error(f"#   + sqlstate:                {e.diag.sqlstate}")
                    logger.error(f"#   + statement_position:      {e.diag.statement_position}")
                    logger.error(f"#   + table_name:              {e.diag.table_name}")
                    logger.error(f"#   + severity_nonlocalized:   {e.diag.severity_nonlocalized}")
            else:
                logger.error(f"# + NON DB ERROR({type(e).__name__}): e={e} ")
            logger.error(f"#          At:")
            traceback.print_exception(type(e), e, e.__traceback__)
            logger.error(f"#       Stack:")
            traceback.print_stack()
            logger.error(f"#######################################")
            logger.error("")
            logger.error("")

    def query_many(self, query, data={}):
        return self._query(query, data, "many")

    def query_one(self, query, data={}):
        return self._query(query, data, "one")

    def query_none(self, query, data={}):
        return self._query(query, data, "none")

    def query_exists(self, query, data={}):
        return self._query(query, data, "exists")


class Database:
    def __init__(self, config):
        self.config = config
        self.dbc = DatabaseConnection.get_connection()
        self.create_tables()

    def create_tables(self):

        # Create a table to hold our parsed sales pop data
        # Note we have a composite primary key so that it is impossible to insert same combination of link + site_id + api_key more than once
        self.dbc.query_none(
            """
				create table if not exists "sales_pop" (
					link varchar(255) null,
					site_id bigint not null,
					api_key varchar(255) null,
					comment	text null,
					created_at	timestamptz not null default now(),
					spread	interval null,
					fetched_at	timestamptz null,
					fetched_count integer not null default 0,

					sale_date_first_ever timestamptz null,
					sale_date_first timestamptz null,
					sale_date_last timestamptz null,

					primary key (site_id)
				); """
        )

        # Create a table to keep product information
        self.dbc.query_none(
            """
				create table if not exists "product_sales" (
					p_sale_customerAddress varchar(255) not null,
					p_sale_customerCity varchar(255) not null,
					p_sale_customerCountry varchar(255) not null,
					p_sale_customerFirstName varchar(255) not null,
					p_sale_customerLastName varchar(255) not null,
					p_sale_customerName varchar(255) not null,
					p_sale_image varchar(1023) not null,
					p_sale_productLink varchar(1023) not null,
					p_sale_productName varchar(255) not null,
					p_sale_status varchar(255) not null,
					p_sale_type varchar(255) not null,
					p_sale_id bigint not null,
					link varchar(255) not null,
					site_id bigint not null,
					api_key varchar(255) null,
					created_at timestamptz not null default now(),
					primary key (p_sale_id)
				); """
        )

        # Create a table to keep shopify sites
        self.dbc.query_none(
            """
				create table if not exists "shopify_sites" (
					id bigint primary key,
					myshopify_name varchar(255),
					hostname varchar(255),
					last_page_source text,
					last_headers text,
					created_at timestamptz not null default now(),
					updated_at timestamptz not null default now()
				); """
        )

        # Create a table to keep track of snipes
        self.dbc.query_none(
            """
				create table if not exists "snipe_status" (
					id varchar(1023),
					type varchar(255),
					ok boolean not null,
					error varchar(255),
					created_at timestamptz not null default now(),
					primary key (type, id)
				); """
        )

        # Create a table to keep beeketing shop info
        self.dbc.query_none(
            """
				create table if not exists "beeketing_accounts" (
					id integer primary key,
					shop_api_key varchar(255),
					shop_domain varchar(255),
					shop_absolute_domain varchar(255),
					shop_email varchar(255),
					shop_platform varchar(255),
					shop_name varchar(255),
					full_json text not null,
					created_at timestamptz not null default now(),
					updated_at timestamptz not null default now()
				); """
        )

    # Insert a beeketing_account into database if it does not already exist
    def insert_beeketing_account(self, account):
        self.dbc.query_none(
            """
				insert into beeketing_accounts(
					id,
					shop_api_key,
					shop_domain,
					shop_absolute_domain,
					shop_email,
					shop_platform,
					shop_name,
					full_json,
					updated_at
					)
				values(
					%(id)s,
					%(shop_api_key)s,
					%(shop_domain)s,
					%(shop_absolute_domain)s,
					%(shop_email)s,
					%(shop_platform)s,
					%(shop_name)s,
					%(full_json)s,
					now()
				)
				on conflict
				do nothing
			;""",
            account,
        )

    # Get myshopify urls from websites nmetwork requests
    def get_myshopify_from_websites(self, offset=0, limit=1):
        return self.dbc.query_many(
            """
				select (regexp_match(page_source, '([a-z0-9]+\.myshopify\.com)'))[1] as link
				from "websites"
				where "created_at" >= '2019-08-27'::date
				and "page_dom"  ~ '[a-z0-9]+\.myshopify\.com'
					order by created_at asc
					limit %(limit)s
					offset %(offset)s;
			;""",
            {"offset": (offset,), "limit": (limit,)},
        )

    # Return true only if there has been registered a snipe
    def snipe_exists(self, type, id):
        return self.dbc.query_exists(
            """
				select id, type
				from snipe_status
				where type= %s
				and id= %s
				limit 1
			;""",
            (type, id),
        )

    # Insert a snipe status
    def upsert_snipe(self, type, id, ok, error):
        return self.dbc.query_none(
            """
				insert into snipe_status
					(type, id, ok, error)
				values
					(%s, %s, %s, %s)
				on conflict
				do nothing
				;
			""",
            (type, id, ok, error),
        )

    # Insert a product sale into database
    def insert_product_sale(self, data):
        return self.dbc.query_none(
            """
				insert into product_sales(
					p_sale_customerAddress,
					p_sale_customerCity,
					p_sale_customerCountry,
					p_sale_customerFirstName,
					p_sale_customerLastName,
					p_sale_customerName,
					p_sale_image,
					p_sale_productLink,
					p_sale_productName,
					p_sale_status,
					p_sale_type,
					p_sale_id, link, site_id, api_key
					)
				values
					(
					%(p_sale_customerAddress)s,
					%(p_sale_customerCity)s,
					%(p_sale_customerCountry)s,
					%(p_sale_customerFirstName)s,
					%(p_sale_customerLastName)s,
					%(p_sale_customerName)s,
					%(p_sale_image)s,
					%(p_sale_productLink)s,
					%(p_sale_productName)s,
					%(p_sale_status)s,
					%(p_sale_type)s,
					%(p_sale_id)s,
					%(link)s,
					%(site_id)s,
					%(api_key)s)
				on conflict
				do nothing
				;""",
            data,
        )

    def get_salespop_count(self):
        return self.dbc.query_one(
            """
				select count(*)
				from sales_pop
			;"""
        )

    def get_now(self):
        r = self.query_one(
            """
				select now()
			;"""
        )
        r = r.replace(tzinfo=pytz.UTC)
        return r

    # Get sales_pop_ids in need of update
    def get_ripe_salespops(self, limit=1):
        return self.dbc.query_many(
            """
				select
					link,
					site_id,
					api_key,
					created_at,
					spread,
					spread_int,
					sale_date_first_ever,
					sale_date_first,
					sale_date_last,
					fetched_at,
				fetched_count
				from sales_pop
				,lateral(select case when
									spread is null
									then
									interval '1 minute'
									else
									spread
									end
				 ) AS s1(spread_int)

				, lateral(select

				(
				 fetched_at is null
				  or
				 ( ( now() - fetched_at  + spread_int * 2 ) > ( 0 * interval '1 sec' ) )
				)::boolean

				 ) as s2(is_due)
				where is_due
				and (fetched_count is null or fetched_count >= 50)
				order by fetched_count desc, fetched_at asc
					limit %(limit)s;
			;""",
            {"limit": limit},
        )

    def get_salespop_by_offset(self, limit=1, offset=0):
        return self.dbc.query_many(
            """
				select
					link,
					site_id,
					api_key,
					created_at,
					spread,
					sale_date_first_ever,
					sale_date_first,
					sale_date_last,
					fetched_at,
					fetched_count
				from sales_pop
				order by site_id::integer
					limit %(limit)s
					offset %(offset)s;
					;
			""",
            {"limit": limit, "offset": offset},
        )

    def get_salespop_by_site_id(self, site_id):
        return self.dbc.query_one(
            """
				select
				 link,
				 site_id,
				 api_key,
				 created_at,
				 comment,
				 spread,
				 sale_date_first_ever,
				 sale_date_first,
				 sale_date_last,
				 fetched_at,
				 fetched_count

				from sales_pop
				where site_id= %(site_id)s
			;""",
            {"site_id": site_id},
        )

    # Insert a link + site + key into database if it does not already exist
    def upsert_spop_id(self, spop):
        return self.dbc.query_none(
            """
				insert into sales_pop
					(
					link,
					site_id ,
					api_key,
					comment,
					spread,
					fetched_at,
					fetched_count,
					sale_date_first_ever,
					sale_date_first,
					sale_date_last
					)
				values
					(
					%(link)s,
					%(site_id)s,
					%(api_key)s,
					%(comment)s,
					%(spread)s,
					%(fetched_at)s,
					%(fetched_count)s,
					%(sale_date_first_ever)s,
					%(sale_date_first)s,
					%(sale_date_last)s
					)
				on conflict (site_id)
				do update
					set
						link=%(link)s,
						api_key=%(api_key)s,
						comment=%(comment)s,
						spread=%(spread)s,
						fetched_at=now(),
						fetched_count = sales_pop.fetched_count + 1,
						sale_date_first_ever=%(sale_date_first_ever)s,
						sale_date_first=%(sale_date_first)s,
						sale_date_last=%(sale_date_last)s
					where sales_pop.site_id=%(site_id)s

				returning site_id
			;""",
            spop,
        )

    # Return all entries
    def get_entries(self):
        return self.dbc.query_many(
            """
				select
					link,
					site_id,
					api_key
				from sales_pop
				order by
					link,
					site_id,
					api_key
			;"""
        )

    def get_shop_by_id(self, id):
        return self.dbc.query_one(
            """
				select *
				from shopify_sites
				where id = %s
			;""",
            (id,),
        )

    # Return all uniquely distinct links
    def get_distinct_links(self):
        return self.dbc.query_many(
            """
				select distinct link
				from sales_pop
			;"""
        )

    def get_site_ids_for_link(self, link):
        return self.dbc.query_many(
            """
				select distinct site_id
				from sales_pop
				where link = %s
			;""",
            (link),
        )

    def get_api_keys_for_link_site_id(self, link, site_id):
        return self.dbc.query_many(
            """
				select distinct api_key
				from sales_pop
				where link = %s
				and  site_id = %s
			;""",
            (link, site_id),
        )

    def get_shops_by_score(self, limit=1):
        return self.dbc.query_many(
            """
				select * from shopify_sites
				order by
					( cast(myshopify_name is not null as integer)
					+ cast(hostname is not null as integer)
					+ cast(updated_at is not null as integer)
					+ cast(last_page_source is not null as integer)
					+ cast(last_headers is not null as integer) ) asc,
				( now() - updated_at ) desc
				limit %s;
			""",
            (limit,),
        )

    # Insert an empty shop with given id into database, updating it if it already exists
    def upsert_shop_id(self, id):
        return self.dbc.query_none(
            """
				insert into shopify_sites
				(id, created_at)
				values
				(%s, now() )
				on conflict (id)
				do nothing
			;""",
            (id,),
        )

    # Insert shop with given id into database, updating it if it already exists
    def upsert_shop(self, shop):
        return self.dbc.query_none(
            """
				insert into shopify_sites
					(id,
					myshopify_name,
					hostname,
					last_page_source,
					last_headers
					)
				values
					(
					%(id)s,
					%(myshopify_name)s,
					%(hostname)s,
					%(last_page_source)s,
					%(last_headers)s
					)
				on conflict (id)
				do update
					set
						myshopify_name=%(myshopify_name)s,
						hostname=%(hostname)s,
						last_page_source=%(last_page_source)s,
						last_headers=%(last_headers)s,
						updated_at=now()
			;""",
            shop,
        )


def entrypoint(context):
    db = Database(context.config)

    db.upsert_shop_id(8008135)
    db.upsert_shop_id(1337)
    db.upsert_shop_id(420)

    shop69 = {"id": 69, "myshopify_name": "arne", "hostname": "arne", "last_page_source": "arne", "last_headers": "arne"}

    shop420 = {"id": 420, "myshopify_name": "nils", "hostname": "nils", "last_page_source": "arne", "last_headers": "arne"}

    db.upsert_shop(shop69)
    db.upsert_shop(shop420)

    ret = db.get_shops_by_score(10)
    print(f"get_shops_by_score={ret}")

    db.upsert_spop_id("site_id", "api_key", "input_link")
    db.upsert_spop_id("site_id", "api_key", "input_link")
    db.upsert_spop_id("site_id", "api_key", "input_link2")

    ret = db.get_entries()
    print(f"get_entries={ret}")


# Main entrypoint of script
if __name__ == "__main__":
    entrypoint()
