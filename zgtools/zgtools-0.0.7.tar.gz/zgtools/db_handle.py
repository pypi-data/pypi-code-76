import pandas as pd
import sqlite3
import psycopg2
import re
import datetime
import tushare as ts
ts.set_token('46304a165e1a71a0ff4ffaaa9c3da977498c1d1c918c798322ffe6b1')
pro = ts.pro_api()


class DbHandle:
    def __init__(self, db_name, engine='sqlite3'):
        self.engine = engine
        self.db_name = db_name

    #每次访问数据库新建连接，访问数据库结束后关闭连接，防止一些BUG的发生
    def establish_connection(self):
        if self.engine == 'postgresql':
            return psycopg2.connect(host='localhost', user='postgres', password='lzg000', database=self.db_name)
        elif self.engine == 'sqlite3':
            return sqlite3.connect(self.db_name)

    #存进表的通用接口
    def to_db(self, df, table_name, start=None, end=None):
        #防止字符串日期无法识别报错
        try:
            if start:
                df = df[(df.date >= start)]
            elif end:
                df = df[(df.date <= end)]
        except:
            if start:
                df = df[(df.date >= datetime.datetime.strptime(start, '%Y-%m-%d'))]
            elif end:
                df = df[(df.date <= datetime.datetime.strptime(end, '%Y-%m-%d'))]
        db_conn = self.establish_connection()
        df.to_sql(table_name, con=db_conn, if_exists='append', index=False)
        db_conn.close()

    #判断表是否存在，防止把表顶掉
    def table_exists(self, table_name):
        db_conn = self.establish_connection()
        db_cursor = db_conn.cursor()
        # 这个函数用来判断表是否存在
        sql = "select name from sqlite_master where type='table' order by name"
        db_cursor.execute(sql)
        tables = [db_cursor.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        db_conn.close()
        if table_name in table_list:
            return True
        else:
            return False
        
    def create_table(self, table_config_dict):
        table_name_str = table_config_dict['table_name']
        drop_str = "DROP TABLE IF EXISTS "+table_name_str+";"
        create_str = " CREATE TABLE  IF NOT EXISTS "+table_name_str+" ("
        for col, attribute in table_config_dict['cols_attribute'].items():
            create_str += col + ' ' + attribute + ',\n'
        create_str = create_str[:-2] + ');'
        unique_index_str = "CREATE UNIQUE INDEX 'uq_" + table_name_str + "' ON  `" + table_name_str + "` ("
        for col in table_config_dict['unique_index']:
            unique_index_str += "'" + col + "'" + ' ASC,'
        unique_index_str = unique_index_str[:-1] + ");"       
            
        db_conn = self.establish_connection()
        db_cursor = db_conn.cursor()
        db_cursor.execute(drop_str)
        db_cursor.execute(create_str)
        db_cursor.execute(unique_index_str)
        db_conn.commit()
        db_conn.close()
        
    #得到建表的json
    def get_table_config(self, fpath):
        try:
            df = pd.read_excel(fpath)
        except:
            df = pd.read_csv(fpath)
        table_name_str = fpath.split('\\')[-1].split('.')[0]
        table_config_dict = {'table_name':str(), 'cols_attribute':{"ID": "INTEGER PRIMARY KEY AUTOINCREMENT"}, 'unique_index':[]}
        table_config_dict['table_name'] = table_name_str
        if 'datetime' in table_name_str:
            table_config_dict['unique_index'] = ['code', 'datetime']
        else:
            table_config_dict['unique_index'] = ['code', 'date']
        for col in df.columns:
            if col == 'code':  
                table_config_dict['cols_attribute'][col] = 'INTEGER NOT NULL'
            elif col == 'date':
                table_config_dict['cols_attribute'][col] = 'DATE NOT NULL'
            elif col == 'datetime':
                table_config_dict['cols_attribute'][col] = 'DATETIME NOT NULL'
            elif col == 'time':
                table_config_dict['cols_attribute'][col] = 'TIME NOT NULL'
            else:
                table_config_dict['cols_attribute'][col] = 'FLOAT'
        return table_config_dict

    def read_db(self, start, end, period = 'M', fields='*', code = None, table_name_str='fundamentals', datetime_index='date'):
        '''
        :param start: 开始日期，例如'2018-01-01'
        :param end: 结束日期
        :param fields: 列，例如['amoflow', 'code']
        :param code: 代码，三种方式，①'000001' ②['000001', '000002'] ③不传默认取所有
        :return: dataframe
        '''
        fields = ''.join([x + ',' for x in fields]).strip(',')
        table_name_str = table_name_str
        datetime_index = datetime_index

        #根据不同周期生成不同sql语句
        if period == 'D':
            datetime_sql = datetime_index+" >='"  + start + "' and "+datetime_index+" <= '" + end + "'"
        else:
            if period == 'W':
                cal_dates = self.cal_date(start, end, period='W', dtype='str')

            elif period == 'M':
                cal_dates = self.cal_date(start, end, period='M', dtype='str')

            cal_dates_sql = '(' + ','.join(map(lambda x: "'" + x + "'", cal_dates)) + ')'
            datetime_sql = datetime_index + " in " + cal_dates_sql

        #如果指定了股票代码，则取出指定的数据，默认取出所有数据
        if code:
            if isinstance(code, list):
                code = '(' + ','.join(map(lambda x: str(int(x)), code)) + ')'
                code_sql = 'in ' + code
            else:
                code_sql = '= ' + code

            str_sql = "select " + fields + " from " + table_name_str + " where code " + code_sql + " and " + datetime_sql
        else:
            str_sql = 'select ' + fields + ' from ' + table_name_str + " where " + datetime_sql
        conn = self.establish_connection()
        # if fields == '*':
        #     df = pd.read_sql(str_sql, con = conn, index_col='ID')
        # else:
        df = pd.read_sql(str_sql, con = conn)
        conn.close()
        print(str_sql)
        return df


    def cal_date(self, start, end, period, dtype='str'):
        #修正时间字符串格式
        start = start.replace('-', '')
        end = end.replace('-', '')
        #取交易日历
        df = pro.query('trade_cal', start_date=start, end_date=end)
        df_d = df[df.is_open == 1]
        df_d.set_index(pd.to_datetime(df_d['cal_date'], format='%Y%m%d'), inplace=True)
        #判断周期
        if period == 'D':
            cal_dates = df_d['cal_date']
        elif period == 'W':
            df_w = df_d.resample('W').agg({'cal_date':'last'})
            cal_dates = df_w['cal_date']
        elif period == 'M':
            df_m = df_d.resample('M').agg({'cal_date':'last'})
            cal_dates = df_m['cal_date']
        #删除空值
        cal_dates.dropna(inplace=True)
        #判断返回类型
        if dtype == 'str':
            cal_dates = cal_dates.astype(str).apply(lambda x: x[:4]+'-'+x[4:6]+'-'+x[6:]).tolist()#.index.to_series().dt.strftime('%Y-%m-%d').tolist()
        elif dtype == 'dt':
            cal_dates = pd.to_datetime(cal_dates, format='%Y%m%d').dt.date.tolist()
        return cal_dates


    def check_time(self, time):
        """
        :param time: 需要转换为YYYY-mm-dd格式str的日期，支持格式datetime.date, datetime.datetime, str, int

        :return: YYYY-mm-dd格式str的日期.
        """

        if isinstance(time, int):
            if 19000000 < time:
                time = str(time)
                str_time = time[0:4] + '-' + time[4:6] + '-' + time[6:]
            else:
                raise ValueError('数值型start,time必须为8位数int,如20180808,当前输入:{}'.format(time))
        elif isinstance(time, str):
            if len(time) == 10:
                time = datetime.datetime.strptime(time, '%Y-%m-%d')
            elif len(time) == 8:
                time = datetime.datetime.strptime(time, '%Y%m%d')
            elif len(time) == 19:
                time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
            else:
                raise ValueError('输入str类型时间仅支持"2010-08-08"或"20100808"')
            str_time = time.strftime('%Y-%m-%d')

        elif isinstance(time, (datetime.datetime, datetime.date)):
            try:
                str_time = time.strftime('%Y-%m-%d')
            except ValueError:
                raise ValueError('datetime型start,time必须符合YYYY-MM-DD hh:mm:ss,如2018-08-08 00:00:00')
        else:
            raise ValueError('时间格式错误:{}'.format(time))
        return str_time

class DbFactor(DbHandle):
    def __init__(self, engine, db_name='factor'):
        super().__init__(engine=engine, db_name=db_name)

    #把dateframe存入表factor_short_day
    def todb_factor_short(self, df, period, start=None, end=None):
        if period == 'D':
            self.to_db(df, 'factor_short_day', start=start, end=end)
        elif period == '30m':
            self.to_db(df, 'factor_short_30m', start=start, end=end)

    #读取短线因子表
    def read_factor_short(self, start, end, period, fields='*', code = None):
        '''
        :param start: 开始日期，例如'2018-01-01'
        :param end: 结束日期
        :param period: 周期，1m, 5m, 15m, 30m, D, W, M, Y
        :param fields: 列，例如['amoflow', 'code']
        :param code: 代码，三种方式，①'000001' ②['000001', '000002'] ③不传默认取所有
        :return: dataframe
        '''
        fields = ''.join([x + ',' for x in fields]).strip(',')
        table_basic_name = 'factor_short'
        if period == 'D':
            table_name_str = table_basic_name + '_' + 'day'
            datetime_index = 'date'
        elif period == '30m':
            table_name_str = table_basic_name + '_' + '30m'
            datetime_index = 'datetime'
        #如果指定了股票代码，则取出指定的数据，默认取出所有数据
        if code:
            if isinstance(code, list):
                code = '(' + ','.join(map(lambda x: str(int(x)), code)) + ')'
                str_sql = "select " + fields + " from " + table_name_str + " where code in " + code + " and "+datetime_index+" >='"  + start + "' and "+datetime_index+" <= '" + end + "'"

            else:
                str_sql = "select " + fields + " from " + table_name_str + " where code = '" + code + "' and "+datetime_index+" >='"  + start + "' and "+datetime_index+" <= '" + end + "'"
        else:
            str_sql = 'select ' + fields + ' from ' + table_name_str + " where "+datetime_index+" >='"  + start + "' and "+datetime_index+" <= '" + end + "'"
        conn = self.establish_connection()
        if fields == '*':
            df = pd.read_sql(str_sql, con = conn, index_col='ID')
        else:
            df = pd.read_sql(str_sql, con = conn)
        conn.close()
        print(str_sql)
        return df

class FundamentalsFactor(DbHandle):
    def __init__(self, engine='sqlite3', db_name=r'C:\数据库\Sqlite\database\L1_fundamentals.sqlite3'):
        super().__init__(engine=engine, db_name=db_name)

    #把dateframe存入表factor_short_day
    def todb_fundamentals(self, df, start=None, end=None):
            self.to_db(df, 'fundamentals', start=start, end=end)

    def read_factor(self, start, end, period = 'M', fields='*', code = None, table_name_str='fundamentals', datetime_index='date'):
        '''
        :param start: 开始日期，例如'2018-01-01'
        :param end: 结束日期
        :param fields: 列，例如['amoflow', 'code']
        :param code: 代码，三种方式，①'000001' ②['000001', '000002'] ③不传默认取所有
        :return: dataframe
        '''
        fields = ''.join([x + ',' for x in fields]).strip(',')
        table_name_str = table_name_str
        datetime_index = datetime_index

        #根据不同周期生成不同sql语句
        if period == 'D':
            datetime_sql = datetime_index+" >='"  + start + "' and "+datetime_index+" <= '" + end + "'"
        else:
            if period == 'W':
                cal_dates = self.cal_date(start, end, period='W', dtype='str')

            elif period == 'M':
                cal_dates = self.cal_date(start, end, period='M', dtype='str')

            cal_dates_sql = '(' + ','.join(map(lambda x: "'" + x + "'", cal_dates)) + ')'
            datetime_sql = datetime_index + " in " + cal_dates_sql

        #如果指定了股票代码，则取出指定的数据，默认取出所有数据
        if code:
            if isinstance(code, list):
                code = '(' + ','.join(map(lambda x: str(int(x)), code)) + ')'
                code_sql = 'in ' + code
            else:
                code_sql = '= ' + code

            str_sql = "select " + fields + " from " + table_name_str + " where code " + code_sql + " and " + datetime_sql
        else:
            str_sql = 'select ' + fields + ' from ' + table_name_str + " where " + datetime_sql
        conn = self.establish_connection()
        # if fields == '*':
        #     df = pd.read_sql(str_sql, con = conn, index_col='ID')
        # else:
        df = pd.read_sql(str_sql, con = conn)
        conn.close()
        print(str_sql)
        return df

class MktHandle(DbHandle):
    def __init__(self, engine='sqlite3', db_name=r'C:\数据库\Sqlite\database\L1_tushare_data.sqlite3'):
        super().__init__(engine=engine, db_name=db_name)

    def fq(self, df, target_cols=['open', 'high', 'low', 'close'], adj='qfq'):
        '''
        :param df: 行情数据df，带有复权因子列adj_factor
        :param target_cols: 要复权的列
        :return:
        '''
        now_adj = df['adj_factor'].iat[-1] if adj=='qfq' else df['adj_factor'].iat[0]
        df.loc[:, target_cols] = df[target_cols].mul(df['adj_factor'], axis=0) / now_adj
        return df

    def read_day(self, start, end, period='M', fields='*', code=None, table_name_str='ts_day_data',
                    datetime_index='date', adj='qfq'):

        start = self.check_time(start)
        end = self.check_time(end)

        if adj and 'adj_factor' not in fields: fields.append('adj_factor')

        df = self.read_db(start, end, period=period, fields=fields, code=code, table_name_str=table_name_str,
                    datetime_index=datetime_index)
        if adj:
            target_cols = [x for x in fields if x in ['open', 'high', 'low', 'close']]
            df = df.groupby('code').apply(lambda x: self.fq(x, target_cols=target_cols, adj=adj))  # 前复权
            df = df[df.columns.difference(['adj_factor'])]
        return df

if __name__ == '__main__':
    #初始化一个factor数据库管理对象
    #%%
    d = FundamentalsFactor(engine='sqlite3')
    #入库
    # df = pd.read_csv('fundamentals.csv')
    # df_val = df[['code', 'date', '']]
    # d.todb_fundamentals(df)
    # #从库里取数据
    df = d.read_factor(start = '2018-11-01', end = '2019-12-01', period='W')


    # #建表
    # table_config_dict = d.get_table_config('fundamentals.csv')
    # d.create_table(table_config_dict)
    # #入库
    # df = pd.read_csv('fundamentals.csv')
    # df.drop_duplicates(['code', 'date'], inplace=True)
    # d.todb_fundamentals(df)

