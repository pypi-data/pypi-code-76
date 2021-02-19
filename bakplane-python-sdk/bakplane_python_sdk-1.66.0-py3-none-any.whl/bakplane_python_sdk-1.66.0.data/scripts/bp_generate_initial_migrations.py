#!python

import json
import os
import pathlib
import typing
from abc import ABC, abstractmethod
from functools import lru_cache

import boto3
import click
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import (
    Table,
    Column,
    String,
    MetaData,
    TIMESTAMP,
    BigInteger,
    Index,
)
import sqlalchemy.types as types
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql.base import BYTEA
from sqlalchemy.schema import CreateTable
from sqlalchemy.sql.ddl import CreateIndex, DropTable
from sqlalchemy.sql.sqltypes import (
    BOOLEAN,
    DATE,
    DATETIME,
    DECIMAL,
    FLOAT,
    Integer,
    JSON,
    TIME,
    TEXT,
)
from sqlalchemy_redshift.dialect import RedshiftDialect

UP_TABLES_MIGRATION_NAME = "1_tables.up.sql"
DOWN_TABLES_MIGRATION_NAME = "1_tables.down.sql"


class VarcharMax(types.UserDefinedType):
    def get_col_spec(self):
        return "VARCHAR(MAX)"


class MigrationProvider(ABC):
    def create_table(
        self,
        name: str,
        schema: str,
        columns: typing.List[Column],
        primary_key_columns: typing.List[str],
        **kwargs,
    ) -> Table:
        return Table(
            name,
            self.get_metadata(),
            *columns,
            PrimaryKeyConstraint(*primary_key_columns),
            schema=schema,
            **kwargs,
        )

    def get_dating_columns(self):
        return [
            "effective_start_dt",
            "effective_end_dt",
            "valid_start_dt",
            "valid_end_dt",
            "knowledge_start_dt",
            "knowledge_end_dt",
        ]

    def get_hashing_columns(self):
        return ["knowledge_hash", "payload_hash"]

    def supports_partitioning(self):
        return False

    def supports_indices(self):
        return False

    def get_partition_ranges(self):
        return [1900] + list(range(1995, 2030)) + [3000]

    def get_metadata(self) -> MetaData:
        return MetaData()

    @abstractmethod
    def get_sqlalchemy_dialect(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

    def add_partitioning_constraint(self, tbl: Table):
        pass

    def get_auxiliary_columns(self):
        return [
            Column("ingestion_session_id", BigInteger, nullable=False),
            Column("resource_code", String(128), nullable=False),
        ]

    def create_partition_table(
        self, f, schema: str, parent_name: str, _from: str, to: str
    ):
        pass

    def drop_partition_table(
        self, f, schema: str, parent_name: str, _from: str, to: str
    ):
        pass

    def map_attribute_type(self, t: str, col):
        pass


class PostgresProvider(MigrationProvider):
    def supports_indices(self):
        return True

    def supports_partitioning(self):
        return True

    def get_sqlalchemy_dialect(self):
        return postgresql.dialect()

    def get_name(self):
        return "postgres"

    def drop_partition_table(
        self, f, schema: str, parent_name: str, _from: str, to: str
    ):
        stmt = f"DROP TABLE {schema}.{parent_name}_p{_from}_{to};\n"
        f.write(stmt)

    def create_partition_table(
        self, f, schema: str, parent_name: str, _from: str, to: str
    ):
        stmt = f"CREATE TABLE {schema}.{parent_name}_p{_from}_{to} PARTITION OF {schema}.{parent_name} FOR VALUES FROM ('{_from}-01-01') TO ('{to}-01-01');\n"
        f.write(stmt)

    def add_partitioning_constraint(
        self, tbl: Table, column: str = "effective_start_dt"
    ):
        tbl.dialect_options["postgresql"]["partition_by"] = f"RANGE({column})"

    def map_attribute_type(self, t: str, col):
        return map_attribute_type(t, col)


class RedshiftProvider(MigrationProvider):
    def create_table(
        self,
        name: str,
        schema: str,
        columns: typing.List[Column],
        primary_key_columns: typing.List[str],
        **kwargs,
    ) -> Table:
        dist_key_columns = ["knowledge_hash"]

        dist_columns = list(filter(lambda x: "identity" in x.name, columns))
        if len(dist_columns) > 0:
            dist_key_columns = dist_columns

        return super(RedshiftProvider, self).create_table(
            name,
            schema,
            columns,
            primary_key_columns,
            redshift_distkey=dist_key_columns[0],
            redshift_sortkey=[
                "effective_start_dt",
                "effective_end_dt",
                "knowledge_start_dt",
                "knowledge_end_dt",
                "valid_start_dt",
                "valid_end_dt",
            ],
        )

    def supports_indices(self):
        return False

    def supports_partitioning(self):
        return False

    def get_sqlalchemy_dialect(self):
        return RedshiftDialect()

    def get_name(self):
        return "redshift"

    def map_attribute_type(self, t: str, col):
        if t == "text":
            return VarcharMax
        else:
            return map_attribute_type(t, col)


class MigrationProviderFactory(object):
    @staticmethod
    @lru_cache()
    def get(warehouse):
        if warehouse == "postgres" or warehouse == "postgresql":
            return PostgresProvider()
        elif warehouse == "redshift":
            return RedshiftProvider()
        raise ValueError("Invalid warehouse provided.")


def create_schema_if_needed(
    f_up,
    f_down,
    provider: MigrationProvider,
    doc: typing.Dict[str, typing.Any],
):
    required_schemas = [doc["provider"]]

    for r in doc["resources"]:
        required_schemas.append(r["dataset"])

    for rs in set(required_schemas):
        f_up.write(f"CREATE SCHEMA {rs};\n")
        f_down.write(f"DROP SCHEMA {rs};\n")


def create_table_if_needed(
    f_up,
    f_down,
    provider: MigrationProvider,
    r: typing.Dict[str, typing.Any],
    schema: str,
):
    columns = []
    indices = [
        ["knowledge_hash", "payload_hash", "resource_code"],
    ]

    ix_count = 0

    found_context = False
    for ctx in r["context"]:
        if ctx["warehouse_kind"] == provider.get_name():
            found_context = True
            for p in ctx["pointers"]:
                columns.append(
                    Column(p["column_name"], BigInteger, nullable=False)
                )

                indices.append(
                    [
                        p["column_name"],
                        "effective_start_dt",
                        "effective_end_dt",
                    ]
                )

    if not found_context:
        if "pointers" in r and len(r["pointers"]) > 0:
            for p in r["pointers"]:
                columns.append(
                    Column(
                        f'{p["entity_type"]}_identity',
                        BigInteger,
                        nullable=False,
                    )
                )

    # add attributes
    for c in r["schema"]["attributes"]:
        columns.append(
            Column(
                c["name"],
                provider.map_attribute_type(c["data_type"], c),
                nullable="mode" in c and c["mode"] == "nullable",
            )
        )

    # add dating columns
    for dc in provider.get_dating_columns():
        columns.append(Column(dc, TIMESTAMP, nullable=False))

    # add hashing
    for hc in provider.get_hashing_columns():
        columns.append(Column(hc, BigInteger, nullable=False))

    columns.extend(provider.get_auxiliary_columns())

    tbl = provider.create_table(
        r["code"],
        schema,
        columns,
        [
            "knowledge_hash",
            "payload_hash",
            "knowledge_end_dt",
            "effective_start_dt",
            "valid_start_dt",
        ],
    )

    if provider.supports_partitioning():
        provider.add_partitioning_constraint(tbl)

    tbl_up_statement = str(
        CreateTable(tbl).compile(dialect=provider.get_sqlalchemy_dialect())
    ).rstrip()

    tbl_down_statement = str(
        DropTable(tbl).compile(dialect=provider.get_sqlalchemy_dialect())
    ).rstrip()

    f_up.write(f"{tbl_up_statement};\n")
    f_down.write(f"{tbl_down_statement};\n")

    if provider.supports_indices():
        for i in indices:
            ix = Index(
                f'{r["code"]}_ix_{ix_count}', *[tbl.c.get(x) for x in i]
            )
            ix_count += 1

            cx = str(
                CreateIndex(ix).compile(
                    dialect=provider.get_sqlalchemy_dialect()
                )
            )

            f_up.write(f"{cx};\n")

    if provider.supports_partitioning():
        ranges = provider.get_partition_ranges()
        for i in range(0, len(ranges) - 1):
            provider.create_partition_table(
                f_up, schema, r["code"], str(ranges[i]), str(ranges[i + 1])
            )

    return tbl


def map_attribute_type(t: str, col):
    t = t.lower()
    if t == "string":
        return String(col.get("length", 128))
    if t == "text":
        return TEXT
    elif t == "integer":
        return Integer
    elif t == "numeric":
        scale = col.get("scale", 4)
        precision = col.get("precision", 15)
        if scale and precision and scale > 0 and precision > 0:
            return DECIMAL(scale=scale, precision=precision)
        else:
            return DECIMAL()
    elif t == "timestamp":
        return TIMESTAMP
    elif t == "boolean":
        return BOOLEAN
    elif t == "floating":
        return FLOAT
    elif t == "bytes":
        return BYTEA
    elif t == "date":
        return DATE
    elif t == "datetime":
        return DATETIME
    elif t == "time":
        return TIME
    elif t == "json":
        return JSON
    elif t == "bigint":
        return BigInteger

    raise ValueError(f"Invalid field type `{t}`.")


def handle_adapter_migrations():
    return None, None


def handle_resource_migrations(
    provider: MigrationProvider,
    r: typing.Dict[str, typing.Any],
    doc: typing.Dict[str, typing.Any],
):
    up_file = os.path.join(
        "migrations", r["code"], provider.get_name(), UP_TABLES_MIGRATION_NAME
    )

    down_file = os.path.join(
        "migrations",
        r["code"],
        provider.get_name(),
        DOWN_TABLES_MIGRATION_NAME,
    )

    pathlib.Path(
        os.path.join("migrations", r["code"], provider.get_name())
    ).mkdir(parents=True, exist_ok=True)

    click.echo(f"Adding table migrations to `{up_file}` ...")

    with open(up_file, "w") as f_up:
        with open(down_file, "w") as f_down:
            create_table_if_needed(f_up, f_down, provider, r, doc["provider"])

    click.echo(f"Table up migrations successfully written to `{up_file}`.")
    click.echo(
        f"Table down  migrations successfully written to `{down_file}`."
    )

    return up_file, down_file


def generate_initial_migration_for_resource(
    provider: MigrationProvider,
    r: typing.Dict[str, typing.Any],
    doc: typing.Dict[str, typing.Any],
    bucket: str,
    upload: bool,
):
    client = boto3.client("s3")

    (
        tbl_migration_file_up,
        tbl_migration_file_down,
    ) = handle_resource_migrations(provider, r, doc)

    tbl_migration_dst_path = (
        doc["code"] + "/" + r["code"] + "/" + provider.get_name() + "/"
    )

    if upload:
        click.echo(f"Uploading table migration to `{tbl_migration_dst_path}.")

        client.upload_file(
            tbl_migration_file_up,
            bucket,
            tbl_migration_dst_path + os.path.basename(tbl_migration_file_up),
        )
        client.upload_file(
            tbl_migration_file_down,
            bucket,
            tbl_migration_dst_path + os.path.basename(tbl_migration_file_down),
        )


def generate_initial_migrations(
    provider: MigrationProvider,
    doc: typing.Dict[str, typing.Any],
    bucket: str,
    upload: bool,
):
    for r in doc["resources"]:
        generate_initial_migration_for_resource(
            provider, r, doc, bucket, upload
        )


@click.command()
@click.option(
    "--metadata", "-m", required=True, help="The metadata resource path."
)
@click.option(
    "--warehouse",
    "-w",
    multiple=True,
    required=True,
    help="You can provide multiple warehouse destinations.",
)
@click.option(
    "--bucket",
    "-b",
    default="bakplane-dev-migrations-internal",
    required=True,
    help="The bucket containing the migrations.",
)
@click.option(
    "--upload",
    "-u",
    default=True,
    required=True,
    help="The bucket containing the migrations.",
)
def main(metadata, warehouse, bucket, upload):
    with open(metadata, "r") as f:
        doc = json.load(f)
        for w in warehouse:
            generate_initial_migrations(
                MigrationProviderFactory.get(w), doc, bucket, upload
            )


if __name__ == "__main__":
    main()
