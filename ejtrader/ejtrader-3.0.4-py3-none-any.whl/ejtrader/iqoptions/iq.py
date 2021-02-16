import logging
import time
import os
from ejtrader_iq.stable_api import IQ_Option
import pandas as pd


def iq_login(verbose = False, iq = None, checkConnection = False,email=None, password=None,AccountType=None):
    
    if verbose:
        logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')

    if iq == None:
      print("Trying to connect to IqOption")
      
      iq=IQ_Option(email,password) # YOU HAVE TO ADD YOUR USERNAME AND PASSWORD
      iq.connect()

    if iq != None:
      while True:
        if iq.check_connect() == False:
          print('Error when trying to connect')
          print(iq)
          print("Retrying")
          iq.connect()
        else:
          if not checkConnection:
            print('Successfully Connected! Account type : ' + AccountType)
          break
        time.sleep(3)
    if AccountType == "DEMO":
        iq.change_balance("PRACTICE") # PRACTICE or REAL
        
    elif AccountType == "REAL":
        iq.change_balance("REAL") # PRACTICE or REAL
        

    return iq
def timeframe_to_sec(timeframe):
    # Timeframe dictionary
    TIMECANDLE = {
        "S30": 30,
        "M1": 60,
        "M2": 120,
        "M3": 180,
        "M4": 240,
        "M5": 300,
        "M15": 900,
        "M30": 1800,
        "H1": 3600,
            
    }
    return TIMECANDLE[timeframe]  

def time_trade(timeframe):
    # Timeframe dictionary
    TIMETTRADE = {
        "S30": 1,
        "M1": 1,
        "M2": 2,
        "M3": 3,
        "M4": 4,
        "M5": 5,
        "M15": 15,
        "M30": 30,
        "H1": 60,
            
    }
    return TIMETTRADE[timeframe]        

def iq_buy_binary(iq,contract,symbol,timeframe):
    timeframe = time_trade(timeframe)
    done,id = iq.buy(contract,symbol,"call",int(timeframe))
    
    if not done:
        print('Error call')
        print(done, id)
        exit(0)
    
    return id


def iq_sell_binary(iq,contract,symbol,timeframe):
    timeframe = time_trade(timeframe)
    done,id = iq.buy(contract,symbol,"put",int(timeframe))
    
    if not done:
        print('Error put')
        print(done, id)
        exit(0)
    
    return id
  
def iq_get_candles(iq,symbol,timeframe):
    iq_login(iq = iq, checkConnection = True)
    return  iq.get_candles(symbol, int(timeframe), 1000, time.time())

    
def iq_get_all_candles(iq,symbol,timeframe,start_candle):
     
    
    final_data = []
    
    for x in range(1):
        iq_login(iq = iq, checkConnection = True)
        data = iq.get_candles(symbol, int(timeframe), 1000, start_candle)
        start_candle = data[0]['to']-1
        final_data.extend(data)
    return final_data

def iq_get_data(iq,symbol,symbols,timeframe): 
    actives = symbols
    timeframe = timeframe_to_sec(timeframe)
    final_data = pd.DataFrame()
    for active in actives:
        current = iq_get_all_candles(iq,active,timeframe,time.time())
        main = pd.DataFrame()
        useful_frame = pd.DataFrame()
        for candle in current:
            useful_frame = pd.DataFrame(list(candle.values()),index = list(candle.keys())).T.drop(columns = ['at'])
            useful_frame = useful_frame.set_index(useful_frame['id']).drop(columns = ['id'])
            main = main.append(useful_frame)
            main.drop_duplicates()
        if active == symbol:
            final_data = main.drop(columns = {'to'})
        else:
            main = main.drop(columns = {'from','to','open','min','max'})
            main.columns = [f'close_{active}',f'volume_{active}']
            final_data = final_data.join(main)
    final_data = final_data.loc[~final_data.index.duplicated(keep = 'first')]
    return final_data.rename(columns = {'from':'date','min':'low', 'max':'high'})




def iq_predict_data(iq,symbol,symbols,timeframe):
    actives = symbols
    main = pd.DataFrame()
    current = pd.DataFrame()
    for active in actives:
        if active == symbol:
            main = iq_get_fastdata(iq,active,timeframe).drop(columns = {'to'})
        else:
            current = iq_get_fastdata(iq,active,timeframe)
            current = current.drop(columns = {'from','to','open','min','max'})
            current.columns = [f'close_{active}',f'volume_{active}']
            main = main.join(current)

    return main.rename(columns = {'from':'date','min':'low', 'max':'high'})

    
def iq_get_fastdata(iq,symbol,timeframe): 
    iq_login(iq = iq, checkConnection = True)
    timeframe = timeframe_to_sec(timeframe)
    candles = iq.get_candles(symbol,int(timeframe),50,time.time())
    useful_frame = pd.DataFrame()
    main = pd.DataFrame()
    for candle in candles:
        useful_frame = pd.DataFrame(list(candle.values()),index = list(candle.keys())).T.drop(columns = ['at'])
        useful_frame = useful_frame.set_index(useful_frame['id']).drop(columns = ['id'])
        main = main.append(useful_frame)
        
    return main
    
def iq_get_balance(iq):
    return iq.get_balance()

def iq_market_isOpen(iq):
    isOpen = []
    opened_market=iq.get_all_open_time()
    
    for type_name, data in opened_market.items():
        for Asset,value in data.items():
            if value['open'] == True:
                value = 'open'
            else:
                value = 'close'
            result = {
            "Asset": Asset,
            "Type" : type_name, 
            "Status" : value
             }
            isOpen.append(result)
        
    return isOpen



def iq_get_payout(iq,symbol=None,typed='turbo'):
    payout = iq.get_all_profit()   
    return payout[symbol][typed]

def iq_get_remaning(iq,timeframe):
    t = time_trade(timeframe)
    remaning_time=iq.get_remaning(t)
    purchase_time=remaning_time
    return purchase_time

def iq_checkwin(iq,id):
    return iq.check_win_v3(id)


def iq_book_live(iq,symbol):
    return iq.start_mood_stream(symbol)

def iq_book_history(iq,symbol):
    return iq.get_traders_mood(symbol)
    
    


    
