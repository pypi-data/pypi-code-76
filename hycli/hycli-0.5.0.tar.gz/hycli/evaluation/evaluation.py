from datetime import datetime
import enum
import sqlite3
from sqlite3 import Error
import json
from pathlib import Path

import pandas as pd
import sqlalchemy

from hycli import ModelComparer


class Granularity(enum.Enum):
    """Model statistics on a specific aggregate level.

    MODEL: Model statistics on an aggregate level of model.
    ENTITY: Model statistics on an aggregate level of entity.
    VENDOR: Model statistics on an aggregate level of vendor.
    """
    MODEL = "model"
    ENTITY = "entity"
    VENDOR = "vendor"


def db_file_dir():
    return Path(__file__).parent.parent.parent


class Database:
    """Sqlite database object with specified schema for the model evaluation. """
    METADATA = sqlalchemy.MetaData()
    model = sqlalchemy.Table(
        "model",
        METADATA,
        sqlalchemy.Column("job_id", sqlalchemy.TEXT, nullable=False, index=True),
        sqlalchemy.Column("model_id", sqlalchemy.TEXT, nullable=False, index=True),
        sqlalchemy.Column("accuracy", sqlalchemy.NUMERIC, nullable=False),
        sqlalchemy.UniqueConstraint("job_id", "model_id", name="jm_uix"),
    )
    entity = sqlalchemy.Table(
        "entity",
        METADATA,
        sqlalchemy.Column("job_id", sqlalchemy.TEXT, nullable=False, index=True),
        sqlalchemy.Column("model_id", sqlalchemy.TEXT, nullable=False, index=True),
        sqlalchemy.Column("entity", sqlalchemy.TEXT, nullable=False, index=True),
        sqlalchemy.Column("accuracy", sqlalchemy.NUMERIC, nullable=False),
        sqlalchemy.UniqueConstraint("job_id", "model_id", "entity", name="jme_uix"),
    )
    vendor = sqlalchemy.Table(
        "vendor",
        METADATA,
        sqlalchemy.Column("job_id", sqlalchemy.TEXT, nullable=False, index=True),
        sqlalchemy.Column("model_id", sqlalchemy.TEXT, nullable=False, index=True),
        sqlalchemy.Column("entity", sqlalchemy.TEXT, nullable=False, index=True),
        sqlalchemy.Column("vendor", sqlalchemy.TEXT, nullable=False, index=True),
        sqlalchemy.Column("accuracy", sqlalchemy.NUMERIC, nullable=False),
        sqlalchemy.Column("number_of_documents", sqlalchemy.INTEGER, nullable=False),
        sqlalchemy.Column("number_of_errors", sqlalchemy.INTEGER, nullable=False),
        sqlalchemy.UniqueConstraint(
            "job_id", "model_id", "vendor", "entity", name="jmve_uix"
        ))

    def __init__(self, metadata=METADATA):
        self.db_file_path = str((db_file_dir() / "pythonsqlite.db").absolute())
        self.engine = sqlalchemy.create_engine(f"sqlite:///{self.db_file_path}")
        self.conn = self._create_connection()
        metadata.create_all(self.engine)

    def _create_connection(self):
        try:
            conn = sqlite3.connect(self.db_file_path, timeout=10)
            return conn
        except Error as e:
            raise e

    def execute_sql(self, sql: str):
        """Execute a single query in database. """
        try:
            c = self.conn.cursor()
            c.execute(sql)
            self.conn.commit()
        except Error as e:
            print(sql)
            raise e

    def table_exist(self, table: str) -> bool:
        """Check if a table already exists in database. """
        c = self.conn.cursor()
        c.execute(
            f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table}';"
        )
        if c.fetchone()[0] == 1:
            return True
        else:
            return False


def _col_entity_error(entity, model_suffix):
    """Generate a column name for error, e.g. foo_error_m1 for the entity foo. """
    return f"{entity}_error_{model_suffix}"


def _col_entity_improvement(entity):
    """Generate a column name for improvement, e.g. foo_improve for the entity foo. """
    return f"{entity}_improve"


def _col_entity(entity, model_suffix):
    """Generate a column name for improvement, e.g. foo_improve for the entity foo. """
    return f"{entity}_{model_suffix}"


def _check_columns_exist(cols_1: {}, cols_2: {}):
    """Ensure cols_1 is a subset of cols_2. """
    missing_cols = cols_1.difference(cols_2)
    if len(missing_cols) > 0:
        raise Exception(f'Entities {missing_cols} missing in {cols_2}')


class Evaluation:
    """A class to create model evaluation reporting and write the results in database.

        Args:
            job_id (str): Automatically generated ID for a new evaluation job. Use an existing job_id to get reporting
                from previous jobs.
            ground_truth_file (str): Excel file containing the truth for the evaluation purpose. First row muss contain
                file_name, entity_1_name, entity_2_name etc.
            model_1_file (str): Excel file containing the extraction result for the model 1. First row muss contain
                file_name, entity_1_name, entity_2_name etc.
            model_2_file (str): Excel file containing the extraction result for the model 2. First row muss contain
                file_name, entity_1_name, entity_2_name etc.
            entities (dict): The name of the entities to evaluate. Default: all entities in the ground_truth_file.
            vendor_field (str): The column in the ground_truth_file which contains the name of the vendor. This field is
                required if granularity is 'vendor' or 'all'.
        """

    def __init__(
            self,
            job_id=None,
            ground_truth_file=None,
            model_1_file=None,
            model_2_file=None,
            entities=None,
            vendor_field=None
    ):

        self.job_id = job_id or datetime.now().strftime("%Y%m%d_%H%M%S")

        self.ground_truth_file = ground_truth_file
        self.model_1_file = model_1_file
        self.model_2_file = model_2_file

        gt_cols = set(pd.read_excel(io=self.ground_truth_file, sheet_name="header", engine="openpyxl").columns)
        m1_cols = set(pd.read_excel(io=self.model_1_file, sheet_name="header", engine="openpyxl").columns)
        m2_cols = set(pd.read_excel(io=self.model_2_file, sheet_name="header", engine="openpyxl").columns)

        # if entities not specified,
        # set default: all entities from the ground_truth which exist both model_1_file and model_2_file
        if entities is None:
            self.entities = gt_cols.intersection(m1_cols).intersection(m2_cols)
            self.entities.remove('file_name')
        else:
            self.entities = entities
        _check_columns_exist(self.entities, gt_cols)
        _check_columns_exist(self.entities, m1_cols)
        _check_columns_exist(self.entities, m2_cols)

        self.vendor_field = vendor_field
        if self.vendor_field:
            _check_columns_exist({self.vendor_field}, gt_cols)

        self.db = Database()
        self._initialize_tables()

    def create_report(self, granularity: Granularity = Granularity.MODEL) -> dict:
        """Evaluate the performance by comparing the model_file with the ground_truth_file. """

        # A LIST OF QUERIES TO BE EXECUTED BASED ON THE REPORT GRANULARITY
        queries = []

        if granularity == Granularity.MODEL:
            queries.append(self._sql_model_report())
        elif granularity == Granularity.ENTITY:
            queries.extend(self._sql_entity_report())
        elif granularity == Granularity.VENDOR:
            queries.extend(self._sql_vendor_report())
        for query in queries:
            self.db.execute_sql(query)

        return self._get_data_from_table(table=granularity.name)

    def _get_data_from_table(self, table):
        df = pd.read_sql_query(
            f"""SELECT * FROM "{table}" WHERE job_id = '{self.job_id}'; """, self.db.conn)
        data = json.loads(df.to_json(orient='records'))
        return data

    # This function shall be moved to compare.py, since there is dependency on the compare.py
    def _create_header_comparison(self):

        self.model_1 = ModelComparer(self.ground_truth_file, self.model_1_file)
        self.model_2 = ModelComparer(self.ground_truth_file, self.model_2_file)
        self.model_1.load_files()
        self.model_2.load_files()
        self.comparison_1 = self.model_1.compare_differences()
        self.comparison_2 = self.model_2.compare_differences()
        exclude = [
            "Total difference",
            "Total difference in percent",
            "Number of documents",
            "Number of compared columns",
            "Compared data points",
            "Overall difference in percent",
            "Overall accuracy in percent",
        ]
        self.df_1_header = self.comparison_1["header"][
            ~self.comparison_1["header"].file_name.isin(exclude)
        ]
        self.df_2_header = self.comparison_2["header"][
            ~self.comparison_2["header"].file_name.isin(exclude)
        ]

        if self.vendor_field:
            df_vendor = pd.read_excel(
                io=self.ground_truth_file, sheet_name="header", engine="openpyxl"
            )[["file_name", self.vendor_field]]
            self.df_1_header = self.df_1_header.merge(df_vendor, on="file_name", how="left")
            self.df_2_header = self.df_2_header.merge(df_vendor, on="file_name", how="left")

        return self.df_1_header, self.df_2_header

    def _initialize_tables(self):
        if not self.db.table_exist(f"merged_comparison_{self.job_id}"):
            self.df_1_header, self.df_2_header = self._create_header_comparison()
            table_comparison_1 = f"comparison_1_{self.job_id}"
            table_comparison_2 = f"comparison_2_{self.job_id}"
            self.df_1_header.to_sql(
                name=table_comparison_1,
                con=self.db.conn,
                index=False,
                if_exists="replace",
            )
            self.df_2_header.to_sql(
                name=table_comparison_2,
                con=self.db.conn,
                index=False,
                if_exists="replace",
            )
            self.db.execute_sql(self._sql_merged_comparison())
            self.db.execute_sql(f"""DROP TABLE IF EXISTS "{table_comparison_1}"; """)
            self.db.execute_sql(f"""DROP TABLE IF EXISTS "{table_comparison_2}"; """)
            print(f"Created table merged_comparison_{self.job_id}.")
        else:
            print(f"Skip creating table merged_comparison_{self.job_id}.")

    def _sql_merged_comparison(self):
        columns = []
        for entity in self.entities:
            columns.append(f"""c1."{entity}_x" as "{entity}_gt",
c1."{entity}_y" as "{entity}_m1",
c2."{entity}_y" as "{entity}_m2",
CASE WHEN c1."diff_{entity}" != 0 THEN 1 ELSE 0 END AS "{_col_entity_error(entity, 'm1')}",
CASE WHEN c2."diff_{entity}" != 0 THEN 1 ELSE 0 END AS "{_col_entity_error(entity, 'm2')}",
(CASE WHEN c1."diff_{entity}" != 0 THEN 1 ELSE 0 END) - (CASE WHEN c2."diff_{entity}" != 0 THEN 1 ELSE 0 END) AS "{_col_entity_improvement(entity)}"
""")
        columns = ",\n    ".join(columns)
        vendor_col = f"""c1."{self.vendor_field}", """ if self.vendor_field else ""
        query = f"""CREATE TABLE merged_comparison_{self.job_id} AS
SELECT
    c1.file_name,
    {vendor_col}
    {columns}
FROM "comparison_1_{self.job_id}" AS c1
LEFT JOIN "comparison_2_{self.job_id}" AS c2 ON c1.file_name = c2.file_name;"""
        return query

    def _sql_model_report(self):
        number_of_errors_m1 = []
        number_of_errors_m2 = []
        for entity in self.entities:
            number_of_errors_m1.append(_col_entity_error(entity, "m1"))
            number_of_errors_m2.append(_col_entity_error(entity, "m2"))
        sum_errors_m1 = " +".join(number_of_errors_m1)
        sum_errors_m2 = " +".join(number_of_errors_m2)
        query = f"""INSERT OR IGNORE INTO model
SELECT '{self.job_id}',
       '{self.model_1_file}',
    ROUND(100 * CAST(SUM(CASE
                           WHEN {sum_errors_m1} = 0 THEN 1
                           ELSE 0 END) AS FLOAT) / CAST(SUM(1) AS FLOAT), 2) AS "accuracy"
FROM "merged_comparison_{self.job_id}"
UNION
SELECT '{self.job_id}',
       '{self.model_2_file}',
    ROUND(100 * CAST(SUM(CASE
                           WHEN {sum_errors_m2} = 0 THEN 1
                           ELSE 0 END) AS FLOAT) / CAST(SUM(1) AS FLOAT), 2) AS "accuracy"
FROM "merged_comparison_{self.job_id}";
"""
        return query

    def _sql_entity_report(self):
        queries = []
        for entity in self.entities:
            query = f"""
INSERT OR IGNORE INTO "entity"
SELECT '{self.job_id}' AS job_id,
       '{self.model_1_file}' AS model_id,
       '{entity}' AS entity,
        ROUND(CAST(SUM(CASE WHEN {_col_entity_error(entity, 'm1')} = 0 THEN 1 ELSE 0 END) AS FLOAT) / CAST(SUM(1) AS FLOAT), 4) AS accuracy
FROM "merged_comparison_{self.job_id}"
UNION
SELECT '{self.job_id}' AS job_id,
       '{self.model_2_file}' AS model_id,
       '{entity}' AS entity,
        ROUND(CAST(SUM(CASE WHEN {_col_entity_error(entity, 'm2')} = 0 THEN 1 ELSE 0 END) AS FLOAT) / CAST(SUM(1) AS FLOAT), 4) AS accuracy
FROM "merged_comparison_{self.job_id}";
"""
            queries.append(query)
        return queries

    def _sql_vendor_report(self):
        queries = []
        for entity in self.entities:
            query = f"""INSERT OR IGNORE INTO vendor
SELECT '{self.job_id}' AS job_id,
       '{self.model_1_file}' AS model_id,
       '{entity}' AS entity,
       "{self.vendor_field}" AS vendor,
       ROUND(CAST(SUM(CASE WHEN {_col_entity_error(entity, 'm1')} = 0 THEN 1 ELSE 0 END) AS FLOAT) / CAST(SUM(1) AS FLOAT), 4) AS accuracy,
       COUNT(*) AS number_of_documents,
       SUM({_col_entity_error(entity, 'm1')}) AS number_of_errors
FROM "merged_comparison_{self.job_id}"
GROUP BY 1,2,3,4
UNION
SELECT '{self.job_id}' AS job_id,
       '{self.model_2_file}' AS model_id,
       '{entity}' AS entity,
       "{self.vendor_field}" AS vendor,
       ROUND(CAST(SUM(CASE WHEN {_col_entity_error(entity, 'm2')} = 0 THEN 1 ELSE 0 END) AS FLOAT) / CAST(SUM(1) AS FLOAT), 4) AS accuracy,
       COUNT(*) AS number_of_documents,
       SUM({_col_entity_error(entity, 'm2')}) AS number_of_errors
FROM "merged_comparison_{self.job_id}"
GROUP BY 1,2,3,4;
"""
            queries.append(query)
        return queries
