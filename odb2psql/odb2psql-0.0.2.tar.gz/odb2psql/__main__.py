from odb2psql import to_psql
import sys
import click
import os


@click.command()
@click.option('--src',
              prompt="Full path (including filename) to source database OpenOffice .odb",
              help="Full path (including filename) to source database OpenOffice .odb")
@click.option('--out',
              help='If given, the file to write output of sql create statement. If not, the sql statement will be printed in console')
@click.option('--host', help='Host to postgresql server. If given, sql statement will be executed directly here')
@click.option('--username', help='Username to postgresql server. If given, sql statement will be executed directly here')
@click.option('--password', help='Password to postgresql server. If given, sql statement will be executed directly here')
@click.option('--db', help='Database to postgresql server. If given, sql statement will be executed directly here')
@click.option('--dump', help='Dump SQL statement to console', is_flag=True)
def run_convert_to_psql(src, out, host, username, password, db, dump):
    if not os.path.exists(src):
        click.echo(f'File is not existed: {src}')
        sys.exit(0)
    click.echo(f'Reading {src}')
    to_psql.convert(src, out, host, username, password, db, dump)


if __name__ == '__main__':
    run_convert_to_psql()