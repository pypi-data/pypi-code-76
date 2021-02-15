import sys

import pyodbc
path = r'D:\Code\acc2psql\fn.accdb'
conn = pyodbc.connect(f'Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={path};')
cursor = conn.cursor()

psql = ''
tables = []

for t in cursor.tables():
    tables.append(t.table_name)

table_column_count={}
drop_tables = ''
create_tables = {}
for t in tables:
    if not 'MSys' in t and not '~TMP' in t and not 'qry_' in t:# and t == 'transaksisaham':
        # print(t)

        count_stat = 0
        foreign_keys = ''
        foreign_keys_exist = {}
        for st in cursor.statistics(t):
            count_stat = count_stat + 1
            # print(st)
            # ke [2] pasti mulai informasi foreign key
            # jika st[5] ada karakter "_" makd dicek. jika yang pertama adalah id, maka itu berarti foreign key one to many, dimana tabelnya ada di bagian kedua. That's it!
            if count_stat >= 3:
                # print('x', st[8])
                c0 = str(st[2])
                c5 = st[8]
                # print('x', str(c5).split('_'))
                c1 = str(c5).split('_')[0]
                c2 = str(c5).split('_')[1]

                # it is foreign key!
                if c1 == 'id' and foreign_keys_exist.get(c5, None) is None:
                    foreign_keys_exist[c5] = True
                    foreign_keys = f'{foreign_keys}FOREIGN KEY ({c5}) REFERENCES {c2} ({c1}{c2}) ON DELETE CASCADE,\n'

        foreign_keys = foreign_keys[:-2]

        columns = ''
        column_count = 0
        for c in cursor.columns(table=t):
            column_count = column_count + 1
            type = c[5]
            if c[5] == 'COUNTER':
                type = 'SERIAL PRIMARY KEY'
            elif c[5] == 'VARCHAR':
                type = f'VARCHAR({c[6]})'
            elif c[5] == 'DATETIME':
                type = 'TIMESTAMP'
            elif c[5] == 'BIT':
                type = 'BOOLEAN'

            columns = f'{columns} {c.column_name} {type},\n'
        columns = columns[:-2]

        table_column_count[t] = column_count

        if foreign_keys is not '':
            foreign_keys = f'\n, {foreign_keys}'

        drop_tables = f'{drop_tables}DROP TABLE IF EXISTS {t};\n'
        create_sql = f'CREATE TABLE {t} (\n' \
               f'{columns}\n' \
               f'{foreign_keys}\n' \
               f');\n'
        create_tables[t] = create_sql

table_independent = {}
table_dependent = {}
drop_table_independent = {}
drop_table_dependent = {}

for k in create_tables:
    if '_' not in k:
        table_independent[k] = create_tables[k]
        drop_table_independent[k] = f'DROP TABLE IF EXISTS {k};\n'
    else:
        table_dependent[k] = create_tables[k]
        drop_table_dependent[k] = f'DROP TABLE IF EXISTS {k};\n'

drop_tables = ''
for t in drop_table_independent:
    drop_tables = f'{drop_tables}{drop_table_independent[t]}'

for t in drop_table_dependent:
    drop_tables = f'{drop_tables}{drop_table_dependent[t]}'

create_sql = ''
for t in table_independent:
    create_sql = f'{create_sql}{table_independent[t]}'

for t in table_dependent:
    create_sql = f'{create_sql}{table_dependent[t]}'


#SQL Generations
psql = f'{drop_tables}\n{create_sql}'
print(psql)