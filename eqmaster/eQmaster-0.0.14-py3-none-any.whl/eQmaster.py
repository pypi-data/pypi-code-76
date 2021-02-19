import pandas, datetime, json, boto3, os, pytz
import shioaji as sj

def is_market_open(market_name):

    # config_filename = 'market.json'
    # bucket = 'ephod-tech.trading-advisor.auto-trade.configuration'
    config_file = os.environ['config_path']
    # config_key = 'query-master/market.json'

    j = None
    local_config_file = config_file

    if config_file.startswith('s3://'):
        s3 = boto3.client('s3')
        s3.download_file(bucket, config_key, config_filename)

        f = open('market.json')
        j = json.load(f)

        local_config_file = 'market.json'
    else:
        f = open(os.environ['config_path'])
        j = json.load(f)


    if j is not None:
        timezone = j['timezone']
        curr_date = datetime.datetime.now().replace(tzinfo=pytz.timezone(timezone))
        curr_date_str = curr_date.strftime('%Y-%m-%d')
        weekday = curr_date.weekday()
        curr_time_stamp = curr_date.timestamp()
        start_timestamp = datetime.datetime.strptime(f'{curr_date_str} 09:00:00','%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.timezone(timezone)).timestamp()
        end_timestamp = datetime.datetime.strptime(f'{curr_date_str} 13:30:00','%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.timezone(timezone)).timestamp()

        if ( weekday < 5 and 
            curr_date_str not in j['market_close_dates'] and 
            curr_time_stamp >= start_timestamp and curr_time_stamp <= end_timestamp ):
            return True
    
    if local_config_file is not None:
        os.remove(local_config_file)
    
    return False

def get_current_quote(stock_symbol):

    api = sj.Shioaji()
    api.login(
        person_id=os.environ['person_id'],
        passwd=os.environ['password'], 
        contracts_cb=lambda security_type: print(f'{repr(security_type)} fetch done.')
    )
    contracts = [api.Contracts.Stocks[stock_symbol]]
    snapshots = api.snapshots(contracts)
    return pandas.DataFrame(snapshots)

def get(stock_list, from_date, to_date):

    df = None 
    stock_src = os.environ['stock_data_src']

    for stock_symbol in stock_list:

        filename = stock_src.replace('{stock_symbol}', stock_symbol)
        if df is None:
            df = pandas.read_parquet(filename)

        else:
            df = df.append(pandas.read_parquet(filename))
    
    df['Date'] = df['mdate'].apply(lambda x: x[:10])
    df.rename(
        columns = {
            'open_d':'Open', 
            'high_d':'High', 
            'low_d':'Low',
            'close_d':'Close', 
            'volume': 'Volume', 
            'close_adj': 'Adj Close', 
            'stockno': 'Outstanding Share',
            'pe_ratio': 'PER',
            'pb_ratio': 'PBR',
            'cdiv_ratio': 'CDIVR',
            'open_adj': 'Open Adj',
            'high_adj': 'High Adj',
            'low_adj': 'Low Adj',
            'open_adj': 'Open Adj'
        }, 
        inplace = True
    )

    mask = ((df['Date'] >= from_date) & (df['Date'] <= to_date))
    
    return df.loc[mask][['Date','Open','High','Low','Close','Volume','Adj Close','Outstanding Share','PER','PBR','CDIVR','Open Adj','High Adj','Low Adj','Open Adj']]

def setup(settings=None):
    if settings is not None: 
        for key in settings:
            os.environ[key] = settings[key]